#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Jobs."""

import collections

from marshmallow import Schema, fields, post_load
from .cdr_datetime import DateTime

class Options(object):
    """Model for CDRouter Job Options.

    :param tags: (optional) Tags as string list.
    :param skip_tests: (optional) Tests to skip as string list.
    :param begin_at: (optional) Test name to begin testing at as string.
    :param end_at: (optional) Test name to end testing at as string.
    :param extra_cli_args: (optional) Extra `cdrouter-cli` arguments as string.
    """
    def __init__(self, **kwargs):
        self.tags = kwargs.get('tags', None)
        self.skip_tests = kwargs.get('skip_tests', None)
        self.begin_at = kwargs.get('begin_at', None)
        self.end_at = kwargs.get('end_at', None)
        self.extra_cli_args = kwargs.get('extra_cli_args', None)

class OptionsSchema(Schema):
    tags = fields.List(fields.Str(), missing=None)
    skip_tests = fields.List(fields.Str(), missing=None)
    begin_at = fields.Str()
    end_at = fields.Str()
    extra_cli_args = fields.Str()

    @post_load
    def post_load(self, data):
        return Options(**data)

class Job(object):
    """Model for CDRouter Jobs.

    :param id: (optional) Job ID as an int.
    :param status: (optional) Bool `True` if user is an administrator.
    :param options: (optional) :class:`jobs.Options <jobs.Options>` object
    :param package_id: (optional) Package ID as an int.
    :param package_name: (optional) Package name as string.
    :param config_id: (optional) Config ID as an int.
    :param config_name: (optional) Config name as string.
    :param device_id: (optional) Device ID as an int.
    :param device_name: (optional) Device name as string.
    :param result_id: (optional) Result ID as an int.
    :param user_id: (optional) User ID as an int.
    :param created: (optional) Job creation time as `DateTime`.
    :param updated: (optional) Job last-updated time as `DateTime`.
    :param automatic: (optional) Bool `True` if job scheduled automatically `DateTime`.
    :param run_at: (optional) Job scheduled run-time `DateTime`.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.status = kwargs.get('status', None)
        self.options = kwargs.get('options', None)
        self.package_id = kwargs.get('package_id', None)
        self.package_name = kwargs.get('package_name', None)
        self.config_id = kwargs.get('config_id', None)
        self.config_name = kwargs.get('config_name', None)
        self.device_id = kwargs.get('device_id', None)
        self.device_name = kwargs.get('device_name', None)
        self.result_id = kwargs.get('result_id', None)
        self.user_id = kwargs.get('user_id', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)
        self.automatic = kwargs.get('automatic', None)
        self.run_at = kwargs.get('run_at', None)

class JobSchema(Schema):
    id = fields.Int(as_string=True)
    status = fields.Str()
    options = fields.Nested(OptionsSchema)
    package_id = fields.Int(as_string=True)
    package_name = fields.Str()
    config_id = fields.Int(as_string=True)
    config_name = fields.Str()
    device_id = fields.Int(as_string=True)
    device_name = fields.Str()
    result_id = fields.Int(as_string=True, missing=None)
    user_id = fields.Int(as_string=True)
    created = DateTime()
    updated = DateTime()
    automatic = fields.Bool()
    run_at = DateTime()

    @post_load
    def post_load(self, data):
        return Job(**data)

class Page(collections.namedtuple('Page', ['data', 'links'])):
    """Named tuple for a page of list response data.

    :param data: :class:`jobs.Job <jobs.Job>` list
    :param links: :class:`cdrouter.Links <cdrouter.Links>` object
    """

class JobsService(object):
    """Service for accessing CDRouter Jobs."""

    RESOURCE = 'jobs'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, type=None, sort=None, limit=None, page=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of jobs.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`jobs.Page <jobs.Page>` object
        """
        schema = JobSchema()
        resp = self.service.list(self.base, filter, type, sort, limit, page, detailed=detailed)
        js, l = self.service.decode(schema, resp, many=True, links=True)
        return Page(js, l)

    def iter_list(self, *args, **kwargs):
        """Get a list of jobs.  Whereas ``list`` fetches a single page of jobs
        according to its ``limit`` and ``page`` arguments,
        ``iter_list`` returns all jobs by internally making successive
        calls to ``list``.

        :param args: Arguments that ``list`` takes.
        :param kwargs: Optional arguments that ``list`` takes.
        :return: :class:`jobs.Job <jobs.Job>` list

        """
        return self.service.iter_list(self.list, *args, **kwargs)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a job.

        :param id: Job ID as an int.
        :return: :class:`jobs.Job <jobs.Job>` object
        :rtype: jobs.Job
        """
        schema = JobSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a job.

        :param resource: :class:`jobs.Job <jobs.Job>` object
        :return: :class:`jobs.Job <jobs.Job>` object
        :rtype: jobs.Job
        """
        schema = JobSchema(exclude=('id', 'status', 'options', 'package_name', 'config_name', 'device_name', 'result_id', 'user_id', 'created', 'updated', 'automatic', 'run_at'))
        json = self.service.encode(schema, resource)

        schema = JobSchema()
        resp = self.service.edit(self.base, resource.name, json)
        return self.service.decode(schema, resp)

    def launch(self, resource):
        """Launch a new job.

        :param resource: :class:`jobs.Job <jobs.Job>` object
        :return: :class:`jobs.Job <jobs.Job>` object
        :rtype: jobs.Job
        """
        schema = JobSchema(exclude=('id', 'status', 'package_name', 'config_name', 'device_name', 'result_id', 'user_id', 'created', 'updated', 'automatic'))
        json = self.service.encode(schema, resource)

        schema = JobSchema()
        resp = self.service.create(self.base, json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a job.

        :param id: Job ID as an int.
        """
        return self.service.delete_id(self.base, id)

    def bulk_launch(self, jobs=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk launch a set of jobs.

        :param jobs: :class:`jobs.Job <jobs.Job>` list
        :param filter: (optional) Filters to apply as a string list.
        :param all: (optional) Apply to all if bool `True`.
        """
        json = None
        if jobs is not None:
            schema = JobSchema(exclude=('id', 'status', 'package_name', 'config_name', 'device_name', 'result_id', 'user_id', 'created', 'updated', 'automatic'))
            jobs_json = self.service.encode(schema, jobs, many=True)
            json = {self.RESOURCE: jobs_json}

        schema = JobSchema()
        resp = self.service.post(self.base,
                                 params={'bulk': 'launch', 'filter': filter, 'all': all}, json=json)
        return self.service.decode(schema, resp, many=True)

    def bulk_delete(self, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of jobs.

        :param ids: (optional) Int list of job IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, type=type, all=all)
