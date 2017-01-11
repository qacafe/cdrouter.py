#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Packages."""

from marshmallow import Schema, fields, post_load
from testsuites import TestSchema

class Analyze(object):
    def __init__(self, **kwargs):
        self.total_count = kwargs.get('total_count', None)
        self.run_count = kwargs.get('run_count', None)
        self.skipped_count = kwargs.get('skipped_count', None)
        self.skipped_tests = kwargs.get('skipped_tests', None)

class AnalyzeSchema(Schema):
    total_count = fields.Int()
    run_count = fields.Int()
    skipped_count = fields.Int()
    skipped_tests = fields.Nested(TestSchema, many=True)

    @post_load
    def post_load(self, data):
        return Analyze(**data)

class Options(object):
    def __init__(self, **kwargs):
        self.forever = kwargs.get('forever', None)
        self.loop = kwargs.get('loop', None)
        self.repeat = kwargs.get('repeat', None)
        self.maxfail = kwargs.get('maxfail', None)
        self.duration = kwargs.get('duration', None)
        self.wait = kwargs.get('wait', None)
        self.pause = kwargs.get('pause', None)
        self.shuffle = kwargs.get('shuffle', None)
        self.seed = kwargs.get('seed', None)
        self.retry = kwargs.get('retry', None)
        self.rdelay = kwargs.get('rdelay', None)
        self.sync = kwargs.get('sync', None)

class OptionsSchema(Schema):
    forever = fields.Bool()
    loop = fields.Str()
    repeat = fields.Str()
    maxfail = fields.Str()
    duration = fields.Str()
    wait = fields.Str()
    pause = fields.Bool()
    shuffle = fields.Bool()
    seed = fields.Str()
    retry = fields.Str()
    rdelay = fields.Str()
    sync = fields.Bool()

    @post_load
    def post_load(self, data):
        return Options(**data)

class Package(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)
        self.test_count = kwargs.get('test_count', None)
        self.testlist = kwargs.get('testlist', None)
        self.extra_cli_args = kwargs.get('extra_cli_args', None)
        self.user_id = kwargs.get('user_id', None)
        self.agent_id = kwargs.get('agent_id', None)
        self.config_id = kwargs.get('config_id', None)
        self.result_id = kwargs.get('result_id', None)
        self.device_id = kwargs.get('device_id', None)
        self.options = kwargs.get('options', None)
        self.tags = kwargs.get('tags', None)
        self.use_as_testlist = kwargs.get('use_as_testlist', None)
        self.note = kwargs.get('note', None)

class PackageSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    created = fields.DateTime()
    updated = fields.DateTime()
    test_count = fields.Str()
    testlist = fields.List(fields.Str())
    extra_cli_args = fields.Str()
    user_id = fields.Str()
    agent_id = fields.Str()
    config_id = fields.Str()
    result_id = fields.Str(missing=None)
    device_id = fields.Str()
    options = fields.Nested(OptionsSchema)
    tags = fields.List(fields.Str())
    use_as_testlist = fields.Bool()
    note = fields.Str(missing=None)

    @post_load
    def post_load(self, data):
        return Package(**data)

class PackagesService(object):
    """Service for accessing CDRouter Packages."""

    RESOURCE = 'packages'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of packages."""
        schema = PackageSchema(exclude=('testlist', 'extra_cli_args', 'agent_id', 'options', 'note'))
        resp = self.service.list(self.base, filter, sort, limit, page)
        return self.service.decode(schema, resp, many=True)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a package."""
        schema = PackageSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def create(self, resource):
        """Create a new package."""
        schema = PackageSchema(exclude=('id', 'created', 'updated', 'test_count', 'agent_id', 'result_id'))
        json = self.service.encode(schema, resource)

        schema = PackageSchema()
        resp = self.service.create(self.base, json)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a package."""
        schema = PackageSchema(exclude=('id', 'created', 'updated', 'test_count', 'agent_id', 'result_id'))
        json = self.service.encode(schema, resource)

        schema = PackageSchema()
        resp = self.service.edit(self.base, resource.id, json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a package."""
        return self.service.delete_id(self.base, id)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get shares for a package."""
        return self.service.get_shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Edit shares for a package."""
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Export a package."""
        return self.service.export(self.base, id)

    def analyze(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of tests that will be skipped for a package."""
        schema = AnalyzeSchema()
        resp = self.service.post(self.base+str(id)+'/', params={'process': 'analyze'})
        return self.service.decode(schema, resp)

    def bulk_export(self, ids):
        """Bulk export a set of packages."""
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        """Bulk copy a set of packages."""
        schema = PackageSchema()
        return self.service.bulk_copy(self.base, self.RESOURCE, ids, schema)

    def bulk_edit(self, _fields, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of packages."""
        return self.service.bulk_edit(self.base, self.RESOURCE,
                                      _fields, ids=ids, filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of packages."""
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)
