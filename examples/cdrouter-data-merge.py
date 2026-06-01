#!/usr/bin/env python3
"""
cdrouter-data-merge.py

A streamlined tool for merging assets from a remote CDRouter system into
the local CDRouter system. Always imports all assets in this order:
users, packages, configs, devices, results.

Package import has snapshot-based skip semantics: a package is skipped if
the package itself, or its associated config, or its associated device
already existed on the local system *before this run started*. Configs
and devices created during this run (as a side-effect of an earlier
package import) do not block subsequent packages.

With --force, packages are imported and existing configs/devices are
overwritten in place, unless any of the three (package, config, device)
is locked. Add --force-locked to also overwrite locked items.

Remote resources are iterated lazily — list metadata is fetched on demand
in pages rather than materialised up front — so the tool's memory
footprint stays bounded even when the remote system holds many thousands
of results.
"""

import argparse
import os
import re
import sys
import shutil
import uuid

try:
    from cdrouter import CDRouter
    from cdrouter.cdrouter import CDRouterError
except ImportError:
    print("Error: cdrouter.py module not found. Install it with: "
          "pip install cdrouter", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LOCAL_URL = "http://localhost"
NEW_USER_PASSWORD = "cdrouter"
DISK_HEADROOM_BYTES = 5 * 1024 ** 3  # 5 GB fixed headroom
TEMP_BASE_DIR = "/tmp"

IMPORT_ORDER = ["users", "packages", "configs", "devices", "results"]


# ---------------------------------------------------------------------------
# Argument Parsing
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge CDRouter assets from a remote system into the "
                    "local system.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Merge all assets from a remote system (add -r and -l to skip login prompts).
  By default, original resource ownership is preserved from the remote system:
    cdrouter-data-merge.py https://remote.example.com

  Proceed without user confirmation
    cdrouter-data-merge.py https://remote.example.com --yes

  Assign all imported resources to a specific local user:
    cdrouter-data-merge.py https://remote.example.com --owner alice

  Allow connections to systems with self-signed/invalid TLS certificates:
    cdrouter-data-merge.py https://remote.example.com --insecure

  Overwrite existing assets (but skip locked ones):
    cdrouter-data-merge.py https://remote.example.com --force

  Overwrite everything including locked assets:
    cdrouter-data-merge.py https://remote.example.com --force --force-locked
        """,
    )

    parser.add_argument(
        "remote_url",
        metavar="URL",
        help="URL of the remote CDRouter system (e.g. http://remote.example.com)"
    )

    parser.add_argument(
        "-r", "--remote-token",
        default=None,
        metavar="TOKEN",
        help=("API token for the remote CDRouter system. If omitted, the "
              "cdrouter library will prompt for credentials")
    )

    parser.add_argument(
        "-l", "--local-token",
        default=None,
        metavar="TOKEN",
        help=("API token for the local CDRouter system. If omitted, the "
              "cdrouter library will prompt for credentials")
    )

    parser.add_argument(
        "--owner",
        default=None,
        metavar="USERNAME",
        help=("Assign all imported resources to the given local user. The "
              "username must already exist on the local system. When omitted, "
              "original ownership from the remote system is preserved")
    )

    parser.add_argument(
        "--insecure",
        action="store_true",
        help=("Allow connections to CDRouter systems with self-signed or "
              "otherwise invalid TLS certificates")
    )

    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Proceed without user confirmation"
    )

    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help=("Overwrite existing assets on the local system. Locked assets "
              "are still skipped")
    )

    parser.add_argument(
        "--force-locked",
        action="store_true",
        help="With --force, also overwrite locked assets. Requires --force."
    )

    args = parser.parse_args()
    if args.force_locked and not args.force:
        parser.error("--force-locked requires --force")
    return args


# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------

def connect(url, token, label, insecure=False):
    """Connect to a CDRouter system. The cdrouter library will prompt for
    credentials interactively if no token is supplied.

    `insecure` disables TLS certificate verification — only set it when
    the user has explicitly opted in via --insecure.

    Returns (client, hostname). hostname is the value reported by the
    remote system itself via system.hostname() — used for display.
    """
    print(f"Connecting to {label} system: {url}")
    try:
        c = CDRouter(url, token=token, insecure=insecure)
        hostname = c.system.hostname()
        print(f"  Connected to {label} system: {url} ('{hostname}')")
        return c, hostname
    except CDRouterError as e:
        print(f"Error: Could not connect to {label} system: {e}",
              file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Remote resource counts and sizes (lazy)
# ---------------------------------------------------------------------------

def _resource_services(client):
    """Map of asset_type -> service for the five asset types we handle."""
    return {
        "users":    client.users,
        "packages": client.packages,
        "configs":  client.configs,
        "devices":  client.devices,
        "results":  client.results,
    }


def fetch_remote_counts(remote, remote_hostname):
    """Fetch the per-asset-type counts from the remote system using a
    single one-element page request per type. Returns a dict keyed by
    asset_type. Items themselves are not materialised — the import
    functions iterate lazily later.
    """
    print(f"\nFetching resource counts from remote system "
          f"'{remote_hostname}'...")
    counts = {}
    for asset_type, service in _resource_services(remote).items():
        print(f"  Counting {asset_type:9}...", end="", flush=True)
        try:
            page = service.list(limit=1, page=1)
            if page.links is not None and page.links.total is not None:
                count = page.links.total
            else:
                count = len(page.data)
            counts[asset_type] = count
            print(f" {count:4} found")
        except CDRouterError as e:
            print(f"\n  Error counting {asset_type}: {e}", file=sys.stderr)
            sys.exit(1)
    return counts


def compute_total_result_size(remote):
    """Sum size_on_disk across all remote results. Iterates result metadata
    lazily (non-detailed list) without materialising the full set; only a
    running total is kept.
    """
    total = 0
    try:
        for r in remote.results.iter_list():
            total += getattr(r, "size_on_disk", 0) or 0
    except CDRouterError as e:
        print(f"Warning: Could not compute total result size: {e}",
              file=sys.stderr)
        return None
    return total


# ---------------------------------------------------------------------------
# Local lookup helpers
# ---------------------------------------------------------------------------

def _is_not_found(e):
    """True if a CDRouterError represents a missing resource rather than a
    real API failure.

    The cdrouter library reports "not found" in two distinct ways:
      * via HTTP 404 on get-by-id paths (the CDRouterError carries the
        underlying response), and
      * via the literal message "no such <type>" raised by get_by_name
        when the filtered list comes back empty.
    """
    resp = getattr(e, "response", None)
    if resp is not None and getattr(resp, "status_code", None) == 404:
        return True
    return str(e).startswith("no such ")


def get_local_resource_by_name(local, asset_type, name):
    """Look up a resource on the local system by name. Returns None if
    the resource does not exist. Re-raises CDRouterError on real API
    failures so they don't get silently swallowed.
    """
    if not name:
        return None
    try:
        return getattr(local, asset_type).get_by_name(name)
    except CDRouterError as e:
        if _is_not_found(e):
            return None
        raise


def get_local_user_by_name(local, username):
    """Look up a user on the local system by name. None if not found."""
    try:
        return local.users.get_by_name(username)
    except CDRouterError as e:
        if _is_not_found(e):
            return None
        raise


def get_local_result_by_id(local, result_id):
    """Look up a result on the local system by ID. None if not found."""
    try:
        return local.results.get(result_id)
    except CDRouterError as e:
        if _is_not_found(e):
            return None
        raise


def is_locked(resource):
    """Return True if the given resource is locked."""
    return bool(getattr(resource, "locked", False))


# ---------------------------------------------------------------------------
# Disk space check
# ---------------------------------------------------------------------------

def check_disk_space(local, total_result_size):
    """Check whether the local system has enough disk space for all results,
    plus the fixed DISK_HEADROOM_BYTES of headroom.

    Returns (ok, available_space). available_space is None if the
    disk-space query fails (proceed with a warning).
    """
    size = total_result_size or 0
    try:
        available = local.system.space().avail
    except CDRouterError as e:
        print(f"Warning: Could not determine local disk space: {e}",
              file=sys.stderr)
        return True, None
    required = size + DISK_HEADROOM_BYTES
    return available >= required, available


# ---------------------------------------------------------------------------
# Formatting / pre-flight summary
# ---------------------------------------------------------------------------

def format_bytes(n):
    """Format a byte count as a human-readable string."""
    if n is None:
        return "unknown"
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} PB"


def print_preflight_summary(args, counts, total_result_size, available_space,
                            remote_hostname, local_hostname):
    """Print a summary of what is about to be imported."""
    print("\n" + "=" * 60)
    print("MERGE SUMMARY")
    print("=" * 60)
    print(f"  Remote system : {args.remote_url} ('{remote_hostname}')")
    print(f"  Local system  : {LOCAL_URL} ('{local_hostname}')")
    print(f"  Insecure TLS  : {'Yes' if args.insecure else 'No'}")
    print(f"  Force         : {'Yes' if args.force else 'No'}")
    print(f"  Force locked  : {'Yes' if args.force_locked else 'No'}")
    print(f"  Owner         : "
          f"{args.owner if args.owner else '(preserve original)'}")
    print()
    print("  Resources to import:")
    for asset_type in IMPORT_ORDER:
        count = counts.get(asset_type, 0)
        print(f"    {asset_type.capitalize():<9}: {count}")
    print()
    if args.owner:
        print(f"  Ownership: all imported resources will be owned by "
              f"'{args.owner}'.")
    else:
        print("  Ownership: all imported resources will be owned by their "
              "original users.")
    print()
    print(f"  New users will be created with default password: "
          f"'{NEW_USER_PASSWORD}'")
    print()
    print("  Package import behavior:")
    print("    * Each imported package will automatically import its")
    print("      associated config and device.")
    print("    * If any of these already exist on the local system, the")
    print("      package import will be skipped.")
    print("    * The --force and --force-locked options overwrite any")
    print("      existing config or device imported with a package.")
    print()
    if counts.get("results"):
        print(f"  Total result size to transfer : "
              f"{format_bytes(total_result_size)}")
        if available_space is not None:
            print(f"  Available disk space (local)  : "
                  f"{format_bytes(available_space)}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Import primitives
# ---------------------------------------------------------------------------

def make_temp_dir():
    """Create a single per-run temp subdirectory under TEMP_BASE_DIR. The
    caller is responsible for removing it at the end of the run (typically
    via shutil.rmtree in a finally block in main()).
    """
    temp_dir = os.path.join(TEMP_BASE_DIR, str(uuid.uuid4()))
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir


def export_and_stage(remote_service, resource_id, local, temp_dir):
    """Export a resource from the remote, save into temp_dir, and stage on
    the local system. The same temp_dir is reused across the whole run;
    each export is written under a unique filename so they don't collide.
    Returns the staged import Response.
    """
    data, filename = remote_service.export(resource_id)
    safe_filename = re.sub(r"[^\w.\-]", "_", filename)
    # Prefix with a uuid to guarantee uniqueness within the shared temp_dir.
    unique_filename = f"{uuid.uuid4().hex}_{safe_filename}"
    filepath = os.path.join(temp_dir, unique_filename)
    try:
        with open(filepath, "wb") as f:
            f.write(data.read())
        return local.imports.stage_import_from_filesystem(filepath)
    finally:
        # Drop the staged file as soon as it's been handed to the local
        # imports service — keeps the shared temp_dir from accumulating
        # gigabytes of result archives across the run.
        try:
            os.remove(filepath)
        except OSError:
            pass


def commit(local, staged, mode):
    """Commit a staged import.

    `mode` controls how each section of the commit request is handled:
      - "package"    : the package and its bundled config + device should
                       all be imported (Solution 1: always overwrite the
                       bundled config/device, even if a same-named one
                       already exists locally — this keeps the freshly
                       imported package linked to the right resource).
      - "config"     : import a standalone config.
      - "device"     : import a standalone device.
      - "result"     : import a result; suppress any bundled
                       configs/devices/packages.

    NOTE on `request.replace_existing`: the CDRouter API has a bug where
    setting it to False does not actually prevent existing resources from
    being overwritten. This script never sets it. All import/skip decisions
    are made per-Resource via `should_import`, which the API does honor.
    """
    request = local.imports.get_commit_request(staged.id)

    # Do NOT touch request.replace_existing — see docstring.

    if mode == "package":
        # Always import the package itself and its bundled config + device.
        # The caller has already done all the necessary skip/overwrite
        # checks against the original local snapshot; by the time we get
        # here, we have decided to proceed for this package.
        for section in (request.configs, request.devices, request.packages):
            for resource in (section or {}).values():
                resource.should_import = True

    elif mode == "result":
        for section in (request.configs, request.devices, request.packages):
            for resource in (section or {}).values():
                resource.should_import = False
        for resource in (request.results or {}).values():
            resource.should_import = True

    else:  # "config" or "device"
        for section in (request.configs, request.devices):
            for resource in (section or {}).values():
                resource.should_import = True

    response = local.imports.commit(staged.id, request)

    # Inspect for failures — only check sections we asked to import.
    if mode == "package":
        sections = [
            ("configs",  response.configs),
            ("devices",  response.devices),
            ("packages", response.packages),
        ]
    elif mode == "result":
        sections = [("results", response.results)]
    else:
        sections = [(mode + "s", getattr(response, mode + "s", {}))]

    for section_name, section in sections:
        for key, item in (section or {}).items():
            r = item.response
            if r is None:
                continue
            if not r.imported:
                # Items we explicitly suppressed via should_import=False
                # will report imported=False with no real error.
                if item.should_import is False:
                    continue
                msg = r.message or "unknown error"
                raise CDRouterError(
                    f"{section_name} '{key}': import failed: {msg}"
                )
    return response


def unlock(service, resource):
    """Unlock a local resource if it is currently locked."""
    if resource and is_locked(resource):
        service.unlock(resource.id)


# ---------------------------------------------------------------------------
# Snapshot of local configs/devices before package imports begin
# ---------------------------------------------------------------------------

def snapshot_originals(local):
    """Snapshot all current local configs and devices into name-keyed dicts.

    Resources that exist on the local system at this moment are 'originals'
    for the purposes of the package skip logic. Anything created later in
    this run (as a side-effect of a package import) is implicitly *not*
    in this snapshot and therefore does not block subsequent packages.
    """
    originals = {"configs": {}, "devices": {}}
    try:
        for c in local.configs.iter_list(detailed=True):
            originals["configs"][c.name] = c
        for d in local.devices.iter_list(detailed=True):
            originals["devices"][d.name] = d
    except CDRouterError as e:
        print(f"Error: Could not snapshot local resources: {e}", file=sys.stderr)
        sys.exit(1)
    print("\nPreserving original local configs and devices:")
    print(f"  {len(originals['configs'])} config(s)")
    print(f"  {len(originals['devices'])} device(s)")
    return originals


# ---------------------------------------------------------------------------
# Skip-line formatting
# ---------------------------------------------------------------------------

def _format_skip_line(prefix, name):
    """Pad `prefix` with two spaces of breathing room before `name`. The
    resulting line layout is "  <prefix><gap><name>" where <gap> grows
    with the prefix so all names are visually offset, but we no longer
    rely on a hard-coded column number tied to specific message wording.
    """
    return f"{prefix}  {name}"


# ---------------------------------------------------------------------------
# Import: Users
# ---------------------------------------------------------------------------

def import_users(remote, local, total, args, stats):
    """Import users from remote to local. New users get a fixed default
    password ('cdrouter'). Existing local users are never modified.
    The 'admin' user is always skipped.

    Users are iterated lazily from the remote — at most one page of user
    metadata is held in memory at a time.
    """
    if not total:
        return
    print(f"\n[Users] Importing {total} user(s)...")

    for user in remote.users.iter_list():
        if user.name == "admin":
            stats["users"]["skipped"] += 1
            continue
        try:
            existing = get_local_user_by_name(local, user.name)
            if existing:
                print(f"  Skipping user '{user.name}' (already exists)")
                stats["users"]["skipped"] += 1
                continue
            user.id = None
            user.token = None
            user.password = NEW_USER_PASSWORD
            user.password_confirm = NEW_USER_PASSWORD
            local.users.create(user)
            print(f"  Created user '{user.name}' (password: '{NEW_USER_PASSWORD}')")
            stats["users"]["imported"] += 1
        except CDRouterError as e:
            print(f"  Error importing user '{user.name}': {e}", file=sys.stderr)
            stats["users"]["errors"] += 1


# ---------------------------------------------------------------------------
# Import: Packages (with snapshot-based skip rule)
# ---------------------------------------------------------------------------

def _resolve_remote_name(service, resource_id):
    """Look up a remote resource's name by ID. None if not found."""
    if not resource_id:
        return None
    try:
        return service.get(resource_id).name
    except CDRouterError as e:
        if _is_not_found(e):
            return None
        raise


def _build_skip_reasons(package, config_name, device_name, local_package,
                       originals, args):
    """Determine why (if at all) this package should be skipped.

    Returns a list of (subject, reason) tuples where subject is one of
    'package', 'config', 'device' and reason is one of
    'already exists', 'is locked'. An empty list means the package should
    be imported.

    The package itself is checked normally (does it exist locally? is it
    locked?). Configs and devices are only "blocking" if they appear in
    the original-snapshot dicts — items created mid-run are not.

    All applicable reasons are returned; we don't short-circuit on the
    first one found. With both --force and --force-locked, this always
    returns an empty list.
    """
    reasons = []

    # The package itself
    if local_package:
        if is_locked(local_package) and not args.force_locked:
            reasons.append(("package", "is locked"))
        elif not args.force:
            reasons.append(("package", "already exists"))

    # The associated config (only originals block)
    if config_name and config_name in originals["configs"]:
        orig = originals["configs"][config_name]
        if is_locked(orig) and not args.force_locked:
            reasons.append(("config", "is locked"))
        elif not args.force:
            reasons.append(("config", "already exists"))

    # The associated device (only originals block)
    if device_name and device_name in originals["devices"]:
        orig = originals["devices"][device_name]
        if is_locked(orig) and not args.force_locked:
            reasons.append(("device", "is locked"))
        elif not args.force:
            reasons.append(("device", "already exists"))

    return reasons


def import_packages(remote, local, total, originals, args, stats, temp_dir):
    """Import packages from remote to local with snapshot-based skip logic.

    For each remote package, decide whether to skip based on whether the
    package, its config, or its device existed on the local system at
    snapshot time (subject to --force / --force-locked). If we proceed,
    delegate to commit() in 'package' mode, which always imports the
    bundled config and device (Solution 1).

    Packages are iterated lazily from the remote.
    """
    if not total:
        return
    print(f"\n[Packages] Importing {total} package(s)...")

    for package in remote.packages.iter_list(detailed=True):
        try:
            config_name = _resolve_remote_name(remote.configs, package.config_id)
            device_name = _resolve_remote_name(remote.devices, package.device_id)
            local_package = get_local_resource_by_name(local, "packages",
                                                      package.name)

            reasons = _build_skip_reasons(package, config_name, device_name,
                                          local_package, originals, args)

            if reasons:
                # Pull out the package-level reason (if any). Sub-bullets
                # are everything else, plus the package-level reason if it
                # was the only one.
                pkg_reasons = [r for r in reasons if r[0] == "package"]
                sub_reasons = [r for r in reasons if r[0] != "package"]

                if pkg_reasons:
                    _, pkg_reason = pkg_reasons[0]
                    main = f"Skipping package, {pkg_reason}:"
                else:
                    main = "Skipping package:"
                print("  " + _format_skip_line(main, package.name))
                for subject, reason in sub_reasons:
                    sub = f"    - {subject} {reason}:"
                    sub_name = config_name if subject == "config" else device_name
                    print("  " + _format_skip_line(sub, sub_name))

                stats["packages"]["skipped"] += 1
                continue

            # ---- Real import -----
            # Unlock anything locked that we're about to overwrite.
            if local_package:
                unlock(local.packages, local_package)
            if config_name and config_name in originals["configs"]:
                unlock(local.configs, originals["configs"][config_name])
            if device_name and device_name in originals["devices"]:
                unlock(local.devices, originals["devices"][device_name])

            try:
                staged = export_and_stage(remote.packages, package.id,
                                          local, temp_dir)
                commit(local, staged, mode="package")
                action = "Updated" if local_package else "Created"
                print(f"  {action} package '{package.name}' "
                      f"(config: '{config_name}', device: '{device_name}')")
                stats["packages"]["imported"] += 1
                stats["packages"]["imported_keys"].add(package.name)
                # The bundled config and device were also (re)written as
                # part of this package import — record them so that
                # apply_ownership treats them as imported, not skipped.
                if config_name:
                    stats["configs"]["imported_keys"].add(config_name)
                if device_name:
                    stats["devices"]["imported_keys"].add(device_name)
            except CDRouterError as e:
                print(f"  Error importing package '{package.name}': {e}",
                      file=sys.stderr)
                stats["packages"]["errors"] += 1

        except CDRouterError as e:
            print(f"  Error processing package '{package.name}': {e}",
                  file=sys.stderr)
            stats["packages"]["errors"] += 1


# ---------------------------------------------------------------------------
# Import: Configs / Devices (standalone)
# ---------------------------------------------------------------------------

def import_simple(asset_type, remote, local, total, args, stats, temp_dir):
    """Import standalone configs or devices.

    For each remote resource, skip if it exists locally; with --force,
    overwrite (still skipping locked items unless --force-locked is also
    set).

    Note: by the time this runs, many of the configs/devices referenced by
    packages will already be on the local system, having been brought in
    by import_packages(). Those will simply be skipped here (or
    overwritten with --force).

    Only the first applicable skip reason is reported. When both "exists"
    and "locked" are true, "is locked" wins because it requires a different
    flag to override.
    """
    if not total:
        return
    singular = asset_type[:-1]
    label = asset_type.capitalize()
    print(f"\n[{label}] Importing {total} {singular}(s)...")

    remote_service = getattr(remote, asset_type)
    local_service  = getattr(local,  asset_type)

    for resource in remote_service.iter_list(detailed=True):
        try:
            existing = get_local_resource_by_name(local, asset_type, resource.name)

            if existing:
                if is_locked(existing) and not args.force_locked:
                    main = f"Skipping {singular}, locked:"
                    print("  " + _format_skip_line(main, resource.name))
                    stats[asset_type]["skipped"] += 1
                    continue
                if not args.force:
                    main = f"Skipping {singular}, already exists:"
                    print("  " + _format_skip_line(main, resource.name))
                    stats[asset_type]["skipped"] += 1
                    continue

            try:
                if existing:
                    unlock(local_service, existing)
                staged = export_and_stage(remote_service, resource.id,
                                          local, temp_dir)
                commit(local, staged, mode=singular)
                action = "Updated" if existing else "Created"
                print(f"  {action} {singular} '{resource.name}'")
                stats[asset_type]["imported"] += 1
                stats[asset_type]["imported_keys"].add(resource.name)
            except CDRouterError as e:
                print(f"  Error importing {singular} '{resource.name}': {e}",
                      file=sys.stderr)
                stats[asset_type]["errors"] += 1

        except CDRouterError as e:
            print(f"  Error processing {singular} '{resource.name}': {e}",
                  file=sys.stderr)
            stats[asset_type]["errors"] += 1


# ---------------------------------------------------------------------------
# Import: Results
# ---------------------------------------------------------------------------

def _results_look_identical(remote_result, local_result):
    """Best-effort check that two results sharing an ID actually refer to
    the same test run. Compares package_name and duration — if either
    differs, treat them as unrelated and let the caller decide.
    """
    rpkg = getattr(remote_result, "package_name", None)
    lpkg = getattr(local_result,  "package_name", None)
    rdur = getattr(remote_result, "duration", None)
    ldur = getattr(local_result,  "duration", None)
    return rpkg == lpkg and rdur == ldur


def import_results(remote, local, total, args, stats, temp_dir):
    """Import results from remote to local. The bundled config, device,
    and package in each result archive are suppressed (they were already
    handled in earlier steps).

    Results are iterated lazily from the remote.

    Result IDs are preserved on import — so the same numeric ID can
    coincidentally exist on both systems for completely unrelated test
    runs. With --force, we therefore compare package_name and duration
    before overwriting; a mismatch is flagged and the import is skipped
    so the user can resolve the collision manually. (CDRouter does not
    allow importing a result under a different ID.)

    If the remote result has archived=True, the flag is restored on the
    local result after import (the CDRouter import process resets it).
    """
    if not total:
        return
    print(f"\n[Results] Importing {total} result(s)...")
    print(f"  [A] = archived result")

    for result in remote.results.iter_list(detailed=True):
        archived = getattr(result, "archived", False)
        tag = " [A]" if archived else "    "
        existing = get_local_result_by_id(local, result.id)

        if existing:
            if is_locked(existing) and not args.force_locked:
                main = "Skipping result, locked:"
                print("  " + _format_skip_line(main, f"id={result.id}"))
                stats["results"]["skipped"] += 1
                continue
            if not args.force:
                main = "Skipping result, already exists:"
                print("  " + _format_skip_line(main, f"id={result.id}"))
                stats["results"]["skipped"] += 1
                continue
            # --force is set: refuse to overwrite if the local result
            # looks like a different test run (ID collision).
            if not _results_look_identical(result, existing):
                main = "Skipping result, id collision (different run):"
                print("  " + _format_skip_line(main, f"id={result.id}"))
                print(f"    remote: package='{getattr(result, 'package_name', None)}', "
                      f"duration={getattr(result, 'duration', None)}")
                print(f"    local : package='{getattr(existing, 'package_name', None)}', "
                      f"duration={getattr(existing, 'duration', None)}")
                stats["results"]["skipped"] += 1
                continue

        size_str = format_bytes(getattr(result, "size_on_disk", 0) or 0)
        pkg = result.package_name

        print(f"  Importing result id={result.id}{tag} "
              f"(package: '{pkg}', size: {size_str})...")

        if existing:
            unlock(local.results, existing)
        try:
            staged = export_and_stage(remote.results, result.id, local, temp_dir)
        except Exception as e:
            print(f"  Error importing result id={result.id}{tag}: "
                  f"failed to save export to local temp file: {e}",
                  file=sys.stderr)
            stats["results"]["errors"] += 1
            continue

        try:
            commit(local, staged, mode="result")
        except Exception as e:
            print(f"  Error importing result id={result.id}{tag}: "
                  f"failed to commit import on local system: {e}",
                  file=sys.stderr)
            stats["results"]["errors"] += 1
            continue

        if archived:
            try:
                imported = local.results.get(result.id)
                imported.archived = True
                local.results.edit(imported)
            except CDRouterError as e:
                print(f"  Warning: Could not restore archived flag on "
                      f"result id={result.id}: {e}", file=sys.stderr)

        stats["results"]["imported"] += 1
        stats["results"]["bytes"] += getattr(result, "size_on_disk", 0) or 0
        stats["results"]["imported_keys"].add(result.id)


# ---------------------------------------------------------------------------
# Ownership
# ---------------------------------------------------------------------------

def apply_ownership(remote, local, args, stats, override_user=None):
    """Set ownership on imported local resources.

    Two modes:

      * `override_user is None` (default behavior, no --owner flag):
        preserve original ownership from the remote. For each non-user
        asset, look up the remote owner's username, find that user on
        the local system, and set the local resource's owner accordingly.

      * `override_user is a local User`: assign every imported resource
        to that single user. No remote owner lookup is performed.

    Only resources that were actually imported by this run are touched.
    Pre-existing local resources that were skipped during import keep
    their existing ownership — `stats[type]["imported_keys"]` is the
    authoritative record of what got written.

    Non-result resources are matched to the local system by name, since
    their IDs change on import. Results keep their remote ID, so they are
    matched by ID.
    """
    if override_user is not None:
        print(f"\n[Ownership] Assigning all imported resources to "
              f"'{override_user.name}'...")
    else:
        print("\n[Ownership] Applying original resource ownership...")

    plans = [
        ("configs",  remote.configs,  local.configs,  "name"),
        ("devices",  remote.devices,  local.devices,  "name"),
        ("packages", remote.packages, local.packages, "name"),
        ("results",  remote.results,  local.results,  "id"),
    ]

    for asset_type, remote_service, local_service, key in plans:
        imported_keys = stats[asset_type]["imported_keys"]
        if not imported_keys:
            continue
        for resource in remote_service.iter_list(detailed=True):
            resource_key = resource.name if key == "name" else resource.id
            if resource_key not in imported_keys:
                # This resource was skipped (already existed locally) or
                # errored during import — don't touch its ownership.
                continue

            label = getattr(resource, "name", None) or f"id={resource.id}"

            if override_user is not None:
                target_user_id = override_user.id
                owner_display  = override_user.name
            else:
                owner_id = getattr(resource, "user_id", None)
                if not owner_id:
                    continue
                try:
                    owner_name = remote.users.get(owner_id).name
                except CDRouterError:
                    print(f"  Warning: Could not resolve owner id={owner_id} "
                          f"for {asset_type} '{label}'", file=sys.stderr)
                    continue
                local_user = get_local_user_by_name(local, owner_name)
                if not local_user:
                    print(f"  Warning: Owner '{owner_name}' not found on local "
                          f"system; skipping ownership for {asset_type} "
                          f"'{label}'", file=sys.stderr)
                    continue
                target_user_id = local_user.id
                owner_display  = owner_name

            try:
                if key == "name":
                    local_resource = get_local_resource_by_name(
                        local, asset_type, resource.name)
                else:  # "id"
                    local_resource = get_local_result_by_id(local, resource.id)

                if local_resource is None:
                    # Resource wasn't imported (skipped, errored, or never
                    # made it to the local system) — nothing to update.
                    continue

                local_resource.user_id = target_user_id
                local_service.edit(local_resource)
                print(f"  Set owner of {asset_type} '{label}' "
                      f"to '{owner_display}'")
            except CDRouterError as e:
                print(f"  Warning: Could not set ownership for {asset_type} "
                      f"'{label}': {e}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Stats / final report
# ---------------------------------------------------------------------------

def make_stats():
    """Initialize the stats dict.

    Each per-type entry includes an `imported_keys` set listing the keys
    of resources that were actually written by this run (created or
    overwritten). `apply_ownership` consults this set so that resources
    skipped because they already existed locally are NOT re-owned.

    Key convention:
      * configs / devices / packages : the resource name (string)
      * results                      : the resource id (int)
    """
    s = {a: {"imported": 0, "skipped": 0, "errors": 0, "imported_keys": set()}
         for a in ("users", "packages", "configs", "devices")}
    s["results"] = {"imported": 0, "skipped": 0, "errors": 0, "bytes": 0,
                    "imported_keys": set()}
    return s


def print_summary_report(stats, local, total_result_size_before):
    """Print the final summary report."""
    print("\n" + "=" * 60)
    print("MERGE COMPLETE - SUMMARY REPORT")
    print("=" * 60)
    for asset_type in IMPORT_ORDER:
        s = stats[asset_type]
        print(f"  {asset_type.capitalize():<9}: "
              f"{s['imported']} imported, "
              f"{s['skipped']} skipped, "
              f"{s['errors']} errors")
    print()
    print(f"  Total result data transferred : "
          f"{format_bytes(stats['results']['bytes'])}")
    print(f"  Result size on remote system  : "
          f"{format_bytes(total_result_size_before)}")
    try:
        print(f"  Available disk space (local)  : "
              f"{format_bytes(local.system.space().avail)}")
    except CDRouterError:
        pass
    print("=" * 60)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    print()
    remote, remote_hostname = connect(args.remote_url, args.remote_token,
                                      "remote", insecure=args.insecure)
    print()
    local,  local_hostname  = connect(LOCAL_URL, args.local_token,
                                      "local",  insecure=args.insecure)

    # If --owner was given, the user must already exist on the local system.
    # Resolve it now so we fail fast (before any pre-flight or import work).
    override_user = None
    if args.owner is not None:
        override_user = get_local_user_by_name(local, args.owner)
        if override_user is None:
            print(f"Error: --owner user '{args.owner}' does not exist on the "
                  f"local system.", file=sys.stderr)
            sys.exit(1)

    counts = fetch_remote_counts(remote, remote_hostname)

    if counts.get("results"):
        print(f"\nComputing total size of {counts['results']} remote result(s)...")
        total_result_size = compute_total_result_size(remote)
    else:
        total_result_size = 0

    disk_ok, available_space = check_disk_space(local, total_result_size)

    print(f"\n\nMerging resources into local system '{local_hostname}'...")
    print_preflight_summary(args, counts, total_result_size, available_space,
                            remote_hostname, local_hostname)

    if not disk_ok:
        print("\nError: Insufficient disk space on local system.",
              file=sys.stderr)
        print(f"  Required : {format_bytes(total_result_size)} (plus "
              f"{format_bytes(DISK_HEADROOM_BYTES)} headroom)",
              file=sys.stderr)
        print(f"  Available: {format_bytes(available_space)}", file=sys.stderr)
        print("Aborting. No changes were made.", file=sys.stderr)
        sys.exit(1)

    # Confirmation prompt (skipped with --yes)
    if not args.yes:
        try:
            answer = input("\nProceed? [y/N] ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(0)
        if answer != "y":
            print("Aborted. No changes were made.")
            sys.exit(0)

    stats = make_stats()
    temp_dir = make_temp_dir()
    try:
        # 1. Users (must come first so apply_ownership can find them later)
        import_users(remote, local, counts["users"], args, stats)

        # 2. Snapshot local configs/devices BEFORE any package imports.
        originals = snapshot_originals(local)

        # 3. Packages (with snapshot-based skip logic; bundled configs/devices
        #    are imported as part of each package via Solution 1).
        import_packages(remote, local, counts["packages"], originals,
                        args, stats, temp_dir)

        # 4. Standalone configs and devices (most will be skipped because they
        #    were already brought in by package imports).
        import_simple("configs", remote, local, counts["configs"],
                      args, stats, temp_dir)
        import_simple("devices", remote, local, counts["devices"],
                      args, stats, temp_dir)

        # 5. Results
        import_results(remote, local, counts["results"], args, stats, temp_dir)

        # 6. Ownership — always applied. With --owner, all imported resources
        #    are assigned to the named user; otherwise original ownership
        #    from the remote system is preserved.
        apply_ownership(remote, local, args, stats, override_user=override_user)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    print_summary_report(stats, local, total_result_size)


if __name__ == "__main__":
    main()
