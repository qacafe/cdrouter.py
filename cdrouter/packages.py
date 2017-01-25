#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Packages."""

from marshmallow import Schema, fields, post_load
from .testsuites import TestSchema
from .cdr_datetime import DateTime

class Analysis(object):
    """Model for CDRouter Package Analysis.

    :param total_count: (optional) Total count as an int.
    :param run_count: (optional) Run count as an int.
    :param skipped_count: (optional) Skipped test count as an int.
    :param skipped_tests: (optional) Skipped tests as a string list.
    """
    def __init__(self, **kwargs):
        self.total_count = kwargs.get('total_count', None)
        self.run_count = kwargs.get('run_count', None)
        self.skipped_count = kwargs.get('skipped_count', None)
        self.skipped_tests = kwargs.get('skipped_tests', None)

class AnalysisSchema(Schema):
    total_count = fields.Int()
    run_count = fields.Int()
    skipped_count = fields.Int()
    skipped_tests = fields.Nested(TestSchema, many=True)

    @post_load
    def post_load(self, data):
        return Analysis(**data)

class Options(object):
    """Model for CDRouter Package Options.

    :param forever: (optional) Bool `True` if package looped forver.
    :param loop: (optional) Loop count as a string.
    :param repeat: (optional) Repeat count as a string.
    :param maxfail: (optional) Max fail count as a string.
    :param duration: (optional) Max testing time duration as a string.
    :param wait: (optional) Wait between tests duration as a string.
    :param pause: (optional) Bool `True` is pausing between tests.
    :param shuffle: (optional) Bool `True` if testlist is shuffled.
    :param seed: (optional) Shuffle seed as a string.
    :param retry: (optional) Retry count as a string.
    :param rdelay: (optional) Retry delay as a string.
    """
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

    @post_load
    def post_load(self, data):
        return Options(**data)

class Package(object):
    """Model for CDRouter Packages.

    :param id: (optional) Package ID as a string.
    :param name: (optional) Name as a string.
    :param description: (optional) Description as a string.
    :param created: (optional) Creation time as `DateTime`.
    :param updated: (optional) Last-updated time as `DateTime`.
    :param test_count: (optional) Test count as a string.
    :param testlist: (optional) Testlist as a string list.
    :param extra_cli_args: (optional) Extra CLI args as a string.
    :param user_id: (optional) User ID as a string.
    :param agent_id: (optional) Agent ID as a string.
    :param config_id: (optional) Config ID as a string.
    :param result_id: (optional) Result ID as a string (if a package snapshot).
    :param device_id: (optional) Device ID as a string.
    :param options: (optional) :class:`packages.Options <packages.Options>` object
    :param tags: (optional) Tags as a string list.
    :param use_as_testlist: (optional) Bool `True` if package is used as a testlist.
    :param note: (optional) Note as a string.
    """
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
    created = DateTime()
    updated = DateTime()
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
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, type=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of packages.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :return: :class:`packages.Package <packages.Package>` list
        """
        schema = PackageSchema(exclude=('testlist', 'extra_cli_args', 'agent_id', 'options', 'note'))
        resp = self.service.list(self.base, filter, type, sort, limit, page)
        return self.service.decode(schema, resp, many=True)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a package.

        :param id: Package ID as string.
        :return: :class:`packages.Package <packages.Package>` object
        :rtype: packages.Package
        """
        schema = PackageSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def create(self, resource):
        """Create a new package.

        :param resource: :class:`packages.Package <packages.Package>` object
        :return: :class:`packages.Package <packages.Package>` object
        :rtype: packages.Package
        """
        schema = PackageSchema(exclude=('id', 'created', 'updated', 'test_count', 'agent_id', 'result_id'))
        json = self.service.encode(schema, resource)

        schema = PackageSchema()
        resp = self.service.create(self.base, json)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a package.

        :param resource: :class:`packages.Package <packages.Package>` object
        :return: :class:`packages.Package <packages.Package>` object
        :rtype: packages.Package
        """
        schema = PackageSchema(exclude=('id', 'created', 'updated', 'test_count', 'agent_id', 'result_id'))
        json = self.service.encode(schema, resource)

        schema = PackageSchema()
        resp = self.service.edit(self.base, resource.id, json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a package.

        :param id: Package ID as string.
        """
        return self.service.delete_id(self.base, id)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get shares for a package.

        :param id: Package ID as string.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.get_shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Edit shares for a package.

        :param id: Package ID as string.
        :param user_ids: User IDs as int list.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Export a package.

        :param id: Package ID as string.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.export(self.base, id)

    def analyze(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of tests that will be skipped for a package.

        :param id: Package ID as string.
        :return: :class:`packages.Analysis <packages.Analysis>` object
        :rtype: packages.Analysis
        """
        schema = AnalysisSchema()
        resp = self.service.post(self.base+str(id)+'/', params={'process': 'analyze'})
        return self.service.decode(schema, resp)

    def bulk_export(self, ids):
        """Bulk export a set of packages.

        :param ids: String list of package IDs.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        """Bulk copy a set of packages.

        :param ids: String list of package IDs.
        :return: :class:`packages.Package <packages.Package>` list
        """
        schema = PackageSchema()
        return self.service.bulk_copy(self.base, self.RESOURCE, ids, schema)

    def bulk_edit(self, _fields, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of packages.

        :param _fields: :class:`packages.Package <packages.Package>` object
        :param ids: (optional) String list of package IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_edit(self.base, self.RESOURCE,
                                      _fields, ids=ids, filter=filter, type=type, all=all)

    def bulk_delete(self, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of packages.

        :param ids: (optional) String list of package IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, type=type, all=all)
