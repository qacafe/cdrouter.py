#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter System."""

import os.path

from marshmallow import Schema, fields, post_load

class Version(object):
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
    def __init__(self, **kwargs):
        self.build_date = kwargs.get('build_date', None)
        self.filename = kwargs.get('filename', None)
        self.version = kwargs.get('version', None)
        self.id = kwargs.get('id', None)
        self.article_id = kwargs.get('article_id', None)
        self.testsuite = kwargs.get('testsuite', None)

class ReleaseSchema(Schema):
    build_date = fields.Str()
    filename = fields.Str()
    version = fields.Nested(VersionSchema)
    id = fields.Int()
    article_id = fields.Int()
    testsuite = fields.Nested(TestsuiteSchema)

    @post_load
    def post_load(self, data):
        return Release(**data)

class Upgrade(object):
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
    def __init__(self, **kwargs):
        self.index = kwargs.get('index', None)
        self.mtu = kwargs.get('mtu', None)
        self.name = kwargs.get('name', None)
        self.hardware_addr = kwargs.get('hardware_addr', None)
        self.flags = kwargs.get('flags', None)
        self.addresses = kwargs.get('addresses', None)
        self.multicast_addresses = kwargs.get('multicast_addresses', None)

class InterfaceSchema(Schema):
    index = fields.Str()
    mtu = fields.Str()
    name = fields.Str()
    hardware_addr = fields.Str()
    flags = fields.Nested(InterfaceFlagsSchema)
    addresses = fields.Nested(InterfaceAddrSchema, many=True, missing=None)
    multicast_addresses = fields.Nested(InterfaceAddrSchema, many=True, missing=None)

    @post_load
    def post_load(self, data):
        return Interface(**data)

class Preferences(object):
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

class SystemService(object):
    """Service for accessing CDRouter System."""

    RESOURCE = 'system'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def latest_lounge_release(self):
        """Get the latest release of CDRouter from the CDRouter Support Lounge."""
        schema = ReleaseLatestSchema()
        resp = self.service.get(self.base+'lounge/latest/')
        return self.service.decode(schema, resp)

    def check_for_lounge_upgrade(self, email, password):
        """Check the CDRouter Support Lounge for eligible upgrades using your
        Support Lounge email & password."""
        schema = ReleaseSchema()
        resp = self.service.post(self.base+'lounge/check/',
                                 json={'email': email, 'password': password})
        return self.service.decode(schema, resp)

    def lounge_upgrade(self, email, password, release_id):
        """Download & install an upgrade from the CDRouter Support Lounge
        using your Support Lounge email & password. Please note that any
        running tests will be stopped."""
        schema = UpgradeSchema()
        resp = self.service.post(self.base+'lounge/upgrade/',
                                 json={'email': email, 'password': password, 'release': {'id': int(release_id)}})
        return self.service.decode(schema, resp)

    def manual_upgrade(self, filepath):
        """Upgrade CDRouter manually by uploading a .bin installer from the
        CDRouter Support Lounge. Please note that any running tests will be
        stopped."""
        schema = UpgradeSchema()
        resp = self.service.post(self.base+'upgrade/',
                                 files={'file': (os.path.basename(filepath), open(filepath, 'rb'))})
        return self.service.decode(schema, resp)

    def restart(self):
        """Restart CDRouter web interface. Please note that any running tests will be stopped."""
        return self.service.post(self.base+'restart/')

    def time(self):
        """Get system time."""
        return self.service.post(self.base+'time/').json()['data']['time']

    def hostname(self):
        """Get system hostname."""
        return self.service.post(self.base+'hostname/').json()['data']

    def interfaces(self, addresses=False):
        """Get system interfaces."""
        schema = InterfaceSchema()
        resp = self.service.get(self.base+'interfaces/', params={'addresses': addresses})
        return self.service.decode(schema, resp, many=True)

    def get_preferences(self):
        """Get preferences from /usr/cdrouter-data/etc/config.yml."""
        schema = PreferencesSchema()
        resp = self.service.get(self.base+'preferences/')
        return self.service.decode(schema, resp)

    def edit_preferences(self, resource):
        """Edit preferences in /usr/cdrouter-data/etc/config.yml."""
        schema = PreferencesSchema()
        json = self.service.encode(schema, resource)

        schema = PreferencesSchema()
        resp = self.service.patch(self.base+'preferences/', json=json)
        return self.service.decode(schema, resp)
