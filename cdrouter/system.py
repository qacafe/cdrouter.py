#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter System."""

import os.path

from marshmallow import Schema, fields, post_load

class Version(object):
    """Model for CDRouter Release Versions.

    :param raw: (optional) Raw version as string.
    :param major: (optional) Major version as int.
    :param minor: (optional) Minor version as int.
    :param build: (optional) Build version as int.
    """
    def __init__(self, **kwargs):
        self.raw = kwargs.get('raw', None)
        self.major = kwargs.get('major', None)
        self.minor = kwargs.get('minor', None)
        self.build = kwargs.get('build', None)

class VersionSchema(Schema):
    raw = fields.Str()
    major = fields.Int()
    minor = fields.Int()
    build = fields.Int()

    @post_load
    def post_load(self, data):
        return Version(**data)

class ReleaseLatest(object):
    """Model for CDRouter Latest Releases.

    :param latest: (optional) :class:`system.Version <system.Version>` object.
    :param current: (optional) :class:`system.Version <system.Version>` object.
    :param newer: (optional) Bool `True` if newer release available.
    """
    def __init__(self, **kwargs):
        self.latest = kwargs.get('latest', None)
        self.current = kwargs.get('current', None)
        self.newer = kwargs.get('newer', None)

class ReleaseLatestSchema(Schema):
    latest = fields.Nested(VersionSchema)
    current = fields.Nested(VersionSchema)
    newer = fields.Bool()

    @post_load
    def post_load(self, data):
        return ReleaseLatest(**data)

class Testsuite(object):
    """Model for CDRouter Testsuite names.

    :param shortname: (optional) Brief testsuite name as string.
    :param name: (optional) Full testsuite name as string.
    """
    def __init__(self, **kwargs):
        self.shortname = kwargs.get('shortname', None)
        self.name = kwargs.get('name', None)

class TestsuiteSchema(Schema):
    shortname = fields.Str()
    name = fields.Str()

    @post_load
    def post_load(self, data):
        return Testsuite(**data)

class Release(object):
    """Model for CDRouter Releases.

    :param build_date: (optional) Build date as string.
    :param filename: (optional) Installer filename as string.
    :param version: (optional) :class:`system.Version <system.Version>` object
    :param testsuite: (optional) :class:`system.Testsuite <system.Testsuite>` object
    :param nonce: (optional) Upgrade nonce as string.
    """
    def __init__(self, **kwargs):
        self.build_date = kwargs.get('build_date', None)
        self.filename = kwargs.get('filename', None)
        self.version = kwargs.get('version', None)
        self.testsuite = kwargs.get('testsuite', None)
        self.nonce = kwargs.get('nonce', None)

class ReleaseSchema(Schema):
    build_date = fields.Str()
    filename = fields.Str()
    version = fields.Nested(VersionSchema)
    testsuite = fields.Nested(TestsuiteSchema)
    nonce = fields.Str(missing=None)

    @post_load
    def post_load(self, data):
        return Release(**data)

class Upgrade(object):
    """Model for CDRouter Upgrades.

    :param success: (optional) Bool `True` if successful.
    :param installer: (optional) Installer filename as string.
    :param output: (optional) Output as string.
    :param error: (optional) Error output as string.
    """
    def __init__(self, **kwargs):
        self.success = kwargs.get('success', None)
        self.installer_path = kwargs.get('installer_path', None)
        self.output = kwargs.get('output', None)
        self.error = kwargs.get('error', None)

class UpgradeSchema(Schema):
    success = fields.Bool()
    installer_path = fields.Str(missing=None)
    output = fields.Str(missing=None)
    error = fields.Str(missing=None)

    @post_load
    def post_load(self, data):
        return Upgrade(**data)

class InterfaceFlags(object):
    """Model for CDRouter Interface Flags.

    :param up: (optional) Bool `True` if interface is up.
    :param broadcast: (optional) Bool `True` if interface is broadcasting.
    :param loopback: (optional) Bool `True` if interface is a loopback interface.
    :param point_to_point: (optional) Bool `True` if interface is a point-to-point interface.
    :param multicast: (optional) Bool `True` if interface is multicast.
    """
    def __init__(self, **kwargs):
        self.up = kwargs.get('up', None)
        self.broadcast = kwargs.get('broadcast', None)
        self.loopback = kwargs.get('loopback', None)
        self.point_to_point = kwargs.get('point_to_point', None)
        self.multicast = kwargs.get('multicast', None)

class InterfaceFlagsSchema(Schema):
    up = fields.Bool()
    broadcast = fields.Bool()
    loopback = fields.Bool()
    point_to_point = fields.Bool()
    multicast = fields.Bool()

    @post_load
    def post_load(self, data):
        return InterfaceFlags(**data)

class InterfaceAddr(object):
    """Model for CDRouter Interface Addresses.

    :param network: (optional) Interface network as a string.
    :param address: (optional) Interface address as a string.
    """
    def __init__(self, **kwargs):
        self.network = kwargs.get('network', None)
        self.address = kwargs.get('address', None)

class InterfaceAddrSchema(Schema):
    network = fields.Str()
    address = fields.Str()

    @post_load
    def post_load(self, data):
        return InterfaceAddr(**data)

class Interface(object):
    """Model for CDRouter Interfaces.

    :param index: (optional) Interface index as an int.
    :param mtu: (optional) Interface MTU as an int.
    :param name: (optional) Interface name as a string.
    :param hardware_addr: (optional) Interface hardware address as a string.
    :param flags: (optional) :class:`system.InterfaceFlags <system.InterfaceFlags>` object
    :param addresses: (optional) :class:`system.InterfaceAddr <system.InterfaceAddr>` list
    :param multicast_addresses: (optional) :class:`system.InterfaceAddr <system.InterfaceAddr>` list
    """
    def __init__(self, **kwargs):
        self.index = kwargs.get('index', None)
        self.mtu = kwargs.get('mtu', None)
        self.name = kwargs.get('name', None)
        self.hardware_addr = kwargs.get('hardware_addr', None)
        self.flags = kwargs.get('flags', None)
        self.addresses = kwargs.get('addresses', None)
        self.multicast_addresses = kwargs.get('multicast_addresses', None)

class InterfaceSchema(Schema):
    index = fields.Int(as_string=True)
    mtu = fields.Int(as_string=True)
    name = fields.Str()
    hardware_addr = fields.Str()
    flags = fields.Nested(InterfaceFlagsSchema)
    addresses = fields.Nested(InterfaceAddrSchema, many=True, missing=None)
    multicast_addresses = fields.Nested(InterfaceAddrSchema, many=True, missing=None)

    @post_load
    def post_load(self, data):
        return Interface(**data)

class Preferences(object):
    """Model for CDRouter Preferences.

    :param automatic_logic: (optional) Bool `True` if Automatic Login is enabled.
    :param cloudshark_appliance_autotags: (optional) CloudShark Appliance autotags as a string.
    :param cloudshark_appliance_insecure: (optional) String `yes` if insecure CloudShark Appliance URLs are allowed.
    :param cloudshark_appliance_password: (optional) CloudShark Appliance password as a string.
    :param cloudshark_appliance_tags: (optional) CloudShark Appliance tags as a string.
    :param cloudshark_appliance_token: (optional) CloudShark Appliance API token as a string.
    :param cloudshark_appliance_url: (optional) CloudShark Appliance URL as a string.
    :param cloudshark_appliance_username: (optional) CloudShark Appliance username as a string.
    :param hostname: (optional) CDRouter system's hostname as a string.
    :param migrated: (optional) Migrated resources as a string list.
    :param port: (optional) CDRouter's HTTP port as an int.
    :param https: (optional) CDRouter's HTTPS port as an int.
    :param force_https: (optional) If string `yes`, redirect HTTP connections to CDRouter to HTTPS.
    :param use_cloudshark: (optional) If string `yes`, use CloudShark Appliance for capture viewing.
    :param log_timestamp_format: (optional) Log timestamp format, must be string `short` or `long`.
    :param editor_keymap: (optional) Config editor keymap, must be string `default`, `emacs` or `vim`.
    :param lounge_url: (optional) CDRouter Support Lounge URL as a string.
    :param lounge_insecure: (optional) If bool `True`, allow insecure HTTPS connections to the CDRouter Support Lounge.
    """
    def __init__(self, **kwargs):
        self.automatic_login = kwargs.get('automatic_login', None)
        self.cloudshark_appliance_autotags = kwargs.get('cloudshark_appliance_autotags', None)
        self.cloudshark_appliance_insecure = kwargs.get('cloudshark_appliance_insecure', None)
        self.cloudshark_appliance_password = kwargs.get('cloudshark_appliance_password', None)
        self.cloudshark_appliance_tags = kwargs.get('cloudshark_appliance_tags', None)
        self.cloudshark_appliance_token = kwargs.get('cloudshark_appliance_token', None)
        self.cloudshark_appliance_url = kwargs.get('cloudshark_appliance_url', None)
        self.cloudshark_appliance_username = kwargs.get('cloudshark_appliance_username', None)
        self.hostname = kwargs.get('hostname', None)
        self.migrated = kwargs.get('migrated', None)
        self.port = kwargs.get('port', None)
        self.https = kwargs.get('https', None)
        self.force_https = kwargs.get('force_https', None)
        self.use_cloudshark = kwargs.get('use_cloudshark', None)
        self.log_timestamp_format = kwargs.get('log_timestamp_format', None)
        self.editor_keymap = kwargs.get('editor_keymap', None)
        self.lounge_url = kwargs.get('lounge_url', None)
        self.lounge_insecure = kwargs.get('lounge_insecure', None)

class PreferencesSchema(Schema):
    automatic_login = fields.Bool()
    cloudshark_appliance_autotags = fields.Str()
    cloudshark_appliance_insecure = fields.Str()
    cloudshark_appliance_password = fields.Str()
    cloudshark_appliance_tags = fields.Str()
    cloudshark_appliance_token = fields.Str()
    cloudshark_appliance_url = fields.Str()
    cloudshark_appliance_username = fields.Str()
    hostname = fields.Str()
    migrated = fields.List(fields.Str())
    port = fields.Int()
    https = fields.Int()
    force_https = fields.Str()
    use_cloudshark = fields.Str()
    log_timestamp_format = fields.Str()
    editor_keymap = fields.Str()
    lounge_url = fields.Str()
    lounge_insecure = fields.Bool()

    @post_load
    def post_load(self, data):
        return Preferences(**data)

class Space(object):
    """Model for CDRouter Disk Space Usage.

    :param avail: (optional) Available disk space as an int.
    :param path: (optional) Path to CDRouter's data directory as a string.
    :param pcent: (optional) Percentage of disk space used as an int.
    :param size: (optional) Total disk space as an int.
    :param unit: (optional) Disk space units as a string, default is 'bytes'.
    :param used: (optional) Used disk space as an int.
    """
    def __init__(self, **kwargs):
        self.avail = kwargs.get('avail', None)
        self.path = kwargs.get('path', None)
        self.pcent = kwargs.get('pcent', None)
        self.size = kwargs.get('size', None)
        self.unit = kwargs.get('unit', None)
        self.used = kwargs.get('used', None)

class SpaceSchema(Schema):
    avail = fields.Int()
    path = fields.Str()
    pcent = fields.Int()
    size = fields.Int()
    unit = fields.Str()
    used = fields.Int()

    @post_load
    def post_load(self, data):
        return Space(**data)

class SystemService(object):
    """Service for accessing CDRouter System."""

    RESOURCE = 'system'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def latest_lounge_release(self):
        """Get the latest release of CDRouter from the CDRouter Support Lounge.

        :return: :class:`system.ReleaseLatest <system.ReleaseLatest>` object
        :rtype: system.ReleaseLatest
        """
        schema = ReleaseLatestSchema()
        resp = self.service.get(self.base+'lounge/latest/')
        return self.service.decode(schema, resp)

    def check_for_lounge_upgrade(self, email):
        """Check the CDRouter Support Lounge for eligible upgrades using your
        Support Lounge email.

        :param email: CDRouter Support Lounge email as a string.
        :return: :class:`system.Release <system.Release>` object
        :rtype: system.Release
        """
        schema = ReleaseSchema()
        resp = self.service.post(self.base+'lounge/check/',
                                 json={'email': email})
        return self.service.decode(schema, resp)

    def lounge_upgrade(self, email, nonce, filename='cdrouter.bin'):
        """Download & install an upgrade from the CDRouter Support Lounge
        using your Support Lounge email and upgrade nonce. Please note
        that any running tests will be stopped.

        :param email: CDRouter Support Lounge email as a string.
        :param nonce: Upgrade nonce from :class:`system.Release <system.Release>`.
        :param filename: Upgrade filename from :class:`system.Release <system.Release>`.
        :return: :class:`system.Upgrade <system.Upgrade>` object
        :rtype: system.Upgrade
        """
        schema = UpgradeSchema()
        resp = self.service.post(self.base+'lounge/upgrade/',
                                 json={'email': email, 'release': {'nonce': nonce, 'filename': filename}})
        return self.service.decode(schema, resp)

    def manual_upgrade(self, fd, filename='cdrouter.bin'):
        """Upgrade CDRouter manually by uploading a .bin installer from the
        CDRouter Support Lounge. Please note that any running tests will be
        stopped.

        :param fd: File-like object to upload.
        :param filename: (optional) Filename to use for installer as string.
        :return: :class:`system.Upgrade <system.Upgrade>` object
        :rtype: system.Upgrade
        """
        schema = UpgradeSchema()
        resp = self.service.post(self.base+'upgrade/',
                                 files={'file': (filename, fd)})
        return self.service.decode(schema, resp)

    def lounge_update_license(self):
        """Download & install a license for your CDRouter system from the
        CDRouter Support Lounge.

        :return: :class:`system.Upgrade <system.Upgrade>` object
        :rtype: system.Upgrade
        """
        schema = UpgradeSchema()
        resp = self.service.post(self.base+'license/')
        return self.service.decode(schema, resp)

    def manual_update_license(self, fd, filename='cdrouter.lic'):
        """Update the license on your CDRouter system manually by uploading a
        .lic license from the CDRouter Support Lounge.

        :param fd: File-like object to upload.
        :param filename: (optional) Filename to use for license as string.
        :return: :class:`system.Upgrade <system.Upgrade>` object
        :rtype: system.Upgrade
        """
        schema = UpgradeSchema()
        resp = self.service.post(self.base+'license/',
                                 files={'file': (filename, fd)})
        return self.service.decode(schema, resp)

    def restart(self):
        """Restart CDRouter web interface. Please note that any running tests will be stopped."""
        return self.service.post(self.base+'restart/')

    def live(self):
        """Get CDRouter Live info from cdrouter-cli -live output.

        :rtype: string
        """
        return self.service.get(self.base+'live/').text

    def info(self):
        """Get system info from cdrouter-cli -info output.

        :rtype: string
        """
        return self.service.get(self.base+'info/').text

    def diagnostics(self):
        """Get system diagnostics from cdrouter-diag output.

        :rtype: string
        """
        return self.service.get(self.base+'diag/').text

    def time(self):
        """Get system time.

        :rtype: string
        """
        return self.service.get(self.base+'time/').json()['data']['time']

    def space(self):
        """Get system disk space usage.

        :return: :class:`system.Space <system.Space>` object
        :rtype: system.Space
        """
        schema = SpaceSchema()
        resp = self.service.get(self.base+'space/')
        return self.service.decode(schema, resp)

    def hostname(self):
        """Get system hostname.

        :rtype: string
        """
        return self.service.get(self.base+'hostname/').json()['data']

    def interfaces(self, addresses=False):
        """Get system interfaces.

        :param addresses: (optional) If bool `True`, include interface addresses.
        :return: :class:`system.Interface <system.Interface>` list
        """
        schema = InterfaceSchema()
        resp = self.service.get(self.base+'interfaces/', params={'addresses': addresses})
        return self.service.decode(schema, resp, many=True)

    def get_preferences(self):
        """Get preferences from /usr/cdrouter-data/etc/config.yml.

        :return: :class:`system.Preferences <system.Preferences>` object
        :rtype: system.Preferences
        """
        schema = PreferencesSchema()
        resp = self.service.get(self.base+'preferences/')
        return self.service.decode(schema, resp)

    def edit_preferences(self, resource):
        """Edit preferences in /usr/cdrouter-data/etc/config.yml.

        :param resource: :class:`system.Preferences <system.Preferences>` object
        :return: :class:`system.Preferences <system.Preferences>` object
        :rtype: system.Preferences
        """
        schema = PreferencesSchema()
        json = self.service.encode(schema, resource)

        schema = PreferencesSchema()
        resp = self.service.patch(self.base+'preferences/', json=json)
        return self.service.decode(schema, resp)
