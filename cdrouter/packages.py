#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Packages."""

import collections

from marshmallow import Schema, fields, post_load
from .cdr_error import CDRouterError
from .results import OptionsSchema as ResultOptionsSchema
from .testsuites import TestSchema
from .cdr_datetime import DateTime
from .filters import Field as field

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
    :param loop: (optional) Loop count as an int.
    :param repeat: (optional) Repeat count as an int.
    :param maxfail: (optional) Max fail count as an int.
    :param duration: (optional) Max testing time duration as an int.
    :param wait: (optional) Wait between tests duration as an int.
    :param pause: (optional) Bool `True` is pausing between tests.
    :param shuffle: (optional) Bool `True` if testlist is shuffled.
    :param seed: (optional) Shuffle seed as an int.
    :param retry: (optional) Retry count as an int.
    :param rdelay: (optional) Retry delay as an int.
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
    loop = fields.Int(as_string=True)
    repeat = fields.Int(as_string=True)
    maxfail = fields.Int(as_string=True)
    duration = fields.Int(as_string=True)
    wait = fields.Int(as_string=True)
    pause = fields.Bool()
    shuffle = fields.Bool()
    seed = fields.Int(as_string=True)
    retry = fields.Int(as_string=True)
    rdelay = fields.Int(as_string=True)

    @post_load
    def post_load(self, data):
        return Options(**data)

class Schedule(object):
    """Model for CDRouter Package Schedule.

    :param enabled: (optional) Bool `True` if schedule is enabled.
    :param spec: (optional) Cron spec schedule as a string.
    :param options: (optional) :class:`results.Options <results.Options>` object
    """
    def __init__(self, **kwargs):
        self.enabled = kwargs.get('enabled', None)
        self.spec = kwargs.get('spec', None)
        self.options = kwargs.get('options', None)

class ScheduleSchema(Schema):
    enabled = fields.Bool()
    spec = fields.Str()
    options = fields.Nested(ResultOptionsSchema)

    @post_load
    def post_load(self, data):
        return Schedule(**data)

class Package(object):
    """Model for CDRouter Packages.

    :param id: (optional) Package ID as an int.
    :param name: (optional) Name as a string.
    :param description: (optional) Description as a string.
    :param created: (optional) Creation time as `DateTime`.
    :param updated: (optional) Last-updated time as `DateTime`.
    :param test_count: (optional) Test count as an int.
    :param testlist: (optional) Testlist as a string list.
    :param extra_cli_args: (optional) Extra CLI args as a string.
    :param user_id: (optional) User ID as an int.
    :param agent_id: (optional) Agent ID as an int.
    :param config_id: (optional) Config ID as an int.
    :param result_id: (optional) Result ID as an int (if a package snapshot).
    :param device_id: (optional) Device ID as an int.
    :param options: (optional) :class:`packages.Options <packages.Options>` object
    :param tags: (optional) Tags as a string list.
    :param use_as_testlist: (optional) Bool `True` if package is used as a testlist.
    :param note: (optional) Note as a string.
    :param schedule: (optional) :class:`packages.Schedule <packages.Schedule>` object
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
        self.schedule = kwargs.get('schedule', None)

class PackageSchema(Schema):
    id = fields.Int(as_string=True)
    name = fields.Str()
    description = fields.Str()
    created = DateTime()
    updated = DateTime()
    test_count = fields.Int(as_string=True)
    testlist = fields.List(fields.Str())
    extra_cli_args = fields.Str()
    user_id = fields.Int(as_string=True)
    agent_id = fields.Int(as_string=True)
    config_id = fields.Int(as_string=True)
    result_id = fields.Int(as_string=True, missing=None)
    device_id = fields.Int(as_string=True)
    options = fields.Nested(OptionsSchema)
    tags = fields.List(fields.Str())
    use_as_testlist = fields.Bool()
    note = fields.Str(missing=None)
    schedule = fields.Nested(ScheduleSchema)

    @post_load
    def post_load(self, data):
        return Package(**data)

class Page(collections.namedtuple('Page', ['data', 'links'])):
    """Named tuple for a page of list response data.

    :param data: :class:`packages.Package <packages.Package>` list
    :param links: :class:`cdrouter.Links <cdrouter.Links>` object
    """

class PackagesService(object):
    """Service for accessing CDRouter Packages."""

    RESOURCE = 'packages'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, type=None, sort=None, limit=None, page=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of packages.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`packages.Page <packages.Page>` object
        """
        schema = PackageSchema()
        if not detailed:
            schema = PackageSchema(exclude=('testlist', 'extra_cli_args', 'agent_id', 'options', 'note'))
        resp = self.service.list(self.base, filter, type, sort, limit, page, detailed=detailed)
        ps, l = self.service.decode(schema, resp, many=True, links=True)
        return Page(ps, l)

    def iter_list(self, *args, **kwargs):
        """Get a list of packages.  Whereas ``list`` fetches a single page of
        packages according to its ``limit`` and ``page`` arguments,
        ``iter_list`` returns all packages by internally making
        successive calls to ``list``.

        :param args: Arguments that ``list`` takes.
        :param kwargs: Optional arguments that ``list`` takes.
        :return: :class:`packages.Package <packages.Package>` list

        """
        return self.service.iter_list(self.list, *args, **kwargs)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a package.

        :param id: Package ID as an int.
        :return: :class:`packages.Package <packages.Package>` object
        :rtype: packages.Package
        """
        schema = PackageSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def get_by_name(self, name): # pylint: disable=invalid-name,redefined-builtin
        """Get a package by name.

        :param name: Package name as string.
        :return: :class:`packages.Package <packages.Package>` object
        :rtype: packages.Package
        """
        rs, _ = self.list(filter=field('name').eq(name), limit=1)
        if len(rs) == 0:
            raise CDRouterError('no such package')
        return rs[0]

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

        :param id: Package ID as an int.
        """
        return self.service.delete_id(self.base, id)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get shares for a package.

        :param id: Package ID as an int.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.get_shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Edit shares for a package.

        :param id: Package ID as an int.
        :param user_ids: User IDs as int list.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Export a package.

        :param id: Package ID as an int.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.export(self.base, id)

    def analyze(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of tests that will be skipped for a package.

        :param id: Package ID as an int.
        :return: :class:`packages.Analysis <packages.Analysis>` object
        :rtype: packages.Analysis
        """
        schema = AnalysisSchema()
        resp = self.service.post(self.base+str(id)+'/', params={'process': 'analyze'})
        return self.service.decode(schema, resp)

    def testlist_expanded(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of all tests in a package, with any addons, modules or testlists expanded.

        :param id: Package ID as an int.
        :rtype: string list
        """
        return self.service.post(self.base+str(id)+'/', params={'process': 'testlist-expanded'}).json()['data']

    def bulk_export(self, ids):
        """Bulk export a set of packages.

        :param ids: Int list of package IDs.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        """Bulk copy a set of packages.

        :param ids: Int list of package IDs.
        :return: :class:`packages.Package <packages.Package>` list
        """
        schema = PackageSchema()
        return self.service.bulk_copy(self.base, self.RESOURCE, ids, schema)

    def bulk_edit(self, _fields, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of packages.

        :param _fields: :class:`packages.Package <packages.Package>` object
        :param ids: (optional) Int list of package IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        schema = PackageSchema(exclude=('id', 'created', 'updated', 'test_count', 'agent_id', 'result_id'))
        _fields = self.service.encode(schema, _fields, skip_none=True)
        return self.service.bulk_edit(self.base, self.RESOURCE,
                                      _fields, ids=ids, filter=filter, type=type, all=all)

    def bulk_delete(self, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of packages.

        :param ids: (optional) Int list of package IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, type=type, all=all)
