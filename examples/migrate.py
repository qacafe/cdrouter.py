#!/usr/bin/env python

import argparse
from datetime import datetime
import os
import re
import sys

from cdrouter import CDRouter
from cdrouter.cdrouter import CDRouterError
from cdrouter.filters import Field as field

parser = argparse.ArgumentParser(description="""
Migrate resources between CDRouter systems.

Base URLs for source and destination CDRouter systems should be in the
form 'http[s]://host:port', for example 'http://localhost:8015' or
'https://cdrouter.lan'.  The --insecure flag may be required if
specifying an HTTPS URL to a CDRouter system using a self-signed
certificate.

Authentication via an API token or a user/password is required for
CDRouter systems that do not have Automatic Login enabled.  An API
token can be provided with the --src-token and --dst-token flags.  A
user/password can be provided with the --src-user/--src-password and
--dst-user/--dst-password flags.  If a user flag is provided but the
corresponding password flag is omitted, %(prog)s will prompt for it at
runtime.

By default, all supported resource types are migrated.  This can be
customized by providing a comma-separated list of resource types to
the --resources flag.  For example, to only migrate configs and
packages, use '--resources configs,packages'.  To further restrict the
resources to migrate based on their creation time, pass a date in
YYYY-MM-DD format to the --after or --before flags.

Resources that already exist on the destination system are not
migrated.  To change this behavior, use the --overwrite flag.

""", formatter_class=argparse.RawDescriptionHelpFormatter)

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

parser.add_argument('src_base', help='Base URL of CDRouter source system')
parser.add_argument('dst_base', help='Base URL of CDRouter destination system')

parser.add_argument('--src-token', metavar='STR', help='API token to use with source CDRouter system', default=None)
parser.add_argument('--dst-token', metavar='STR', help='API token to use with destination CDRouter system', default=None)

parser.add_argument('--src-user', metavar='STR', help='Username to use with source CDRouter system', default=None)
parser.add_argument('--src-password', metavar='STR', help='Password to use with source CDRouter system', default=None)

parser.add_argument('--dst-user', metavar='STR', help='Username to use with destination CDRouter system', default=None)
parser.add_argument('--dst-password', metavar='STR', help='Password to use with destination CDRouter system', default=None)

parser.add_argument('--insecure', help='Allow insecure HTTPS connections', action='store_true', default=False)
parser.add_argument('--overwrite', help='Overwrite existing resources on destination CDRouter system', action='store_true', default=False)
parser.add_argument('--resources', metavar='LIST', help='Comma-separated list of resource types to migrate (default: %(default)s)', type=str, default='configs,devices,packages,results')

parser.add_argument('--after', metavar='DATE', help='Migrate only resources created after this date (format: YYYY-MM-DD)', type=valid_date, default=None)
parser.add_argument('--before', metavar='DATE', help='Migrate only resources created before this date (format: YYYY-MM-DD)', type=valid_date, default=None)

parser.add_argument('--verbose', help='Enable verbose output', action='store_true', default=False)

args = parser.parse_args()

def print_verbose(msg):
    if args.verbose:
        print(msg)

def migrate(src, dst, resource, name_or_id, filter, should_import_rtypes):
    plural = '{}s'.format(resource)
    src_service = getattr(src, plural)
    dst_service = getattr(dst, plural)

    for r in src_service.iter_list(filter=filter):
        try:
            si = None

            if not args.overwrite:
                dst_r = None
                dst_name = r.id

                try:
                    if name_or_id is 'id':
                        dst_r = dst_service.get(r.id)
                    elif name_or_id is 'name':
                        dst_name = r.name
                        dst_r = dst_service.get_by_name(r.name)
                except CDRouterError as cde:
                    if cde.response is None or cde.response.status_code != 404:
                        raise cde

                if dst_r is not None:
                    print_verbose('Skipping {} {}, already exists'.format(resource, dst_name))
                    continue

            url = '{}/{}/{}/'.format(args.src_base.rstrip('/'), plural, r.id)
            si = dst.imports.stage_import_from_url(url, token=src.token, insecure=args.insecure)
            impreq = dst.imports.get_commit_request(si.id)

            should_import = False

            for rtype in should_import_rtypes:
                rs = getattr(impreq, rtype)
                for name in rs:
                    if args.overwrite or rs[name].existing_id is None:
                        rs[name].should_import = should_import = True

            if not should_import:
                print_verbose('Skipping {} {}'.format(resource, r.id))
                dst.imports.delete(si.id)
                continue

            impreq = dst.imports.commit(si.id, impreq)

            rs = getattr(impreq, plural)
            for name in rs:
                if not rs[name].should_import:
                    continue
                if rs[name].response.imported:
                    print('Imported {} {}'.format(resource, name))
                else:
                    print_verbose('Error importing {} {}: {}'.format(resource, name, rs[name].response.message))
        except CDRouterError as cde:
            print('Error migrating {} {}: {}'.format(resource, r.id, cde))
            if si is not None:
                dst.imports.delete(si.id)

try:
    # don't allow API token to be set from environment variable since
    # behavior is potentially confusing with two CDRouter systems
    if 'CDROUTER_API_TOKEN' in os.environ:
        del os.environ['CDROUTER_API_TOKEN']

    src = CDRouter(args.src_base, token=args.src_token, insecure=args.insecure)
    if args.src_token is None and args.src_user is not None:
        src.authenticate(args.src_user, args.src_password)

    dst = CDRouter(args.dst_base, token=args.dst_token, insecure=args.insecure)
    if args.dst_token is None and args.dst_user is not None:
        dst.authenticate(args.dst_user, args.dst_password)

    resources = args.resources.split(',')

    # devices were added in CDRouter 10.1
    src_devices = re.match('^10\.0\.', src.testsuites.info().release) is None
    dst_devices = re.match('^10\.0\.', dst.testsuites.info().release) is None

    filter = []
    if args.after is not None:
        filter.append(field('created').gt(args.after))
    if args.before is not None:
        filter.append(field('created').lt(args.before))

    if 'packages' in resources:
        migrate(src, dst, 'package', 'name', filter, ['configs', 'devices', 'packages'])
    if 'configs' in resources:
        migrate(src, dst, 'config', 'name', filter, ['configs'])
    if src_devices and dst_devices and 'devices' in resources:
        migrate(src, dst, 'device', 'name', filter, ['devices'])
    if 'results' in resources:
        migrate(src, dst, 'result', 'id', filter, ['results'])
except KeyboardInterrupt:
    print('Caught interrupt, terminating...')
    sys.exit(1)
