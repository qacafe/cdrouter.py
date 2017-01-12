#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Jobs."""

from marshmallow import Schema, fields, post_load
from .cdr_datetime import DateTime

class Job(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.status = kwargs.get('status', None)
        self.options = kwargs.get('options', None)
        self.package_id = kwargs.get('package_id', None)
        self.package_name = kwargs.get('package_name', None)
        self.device_id = kwargs.get('device_id', None)
        self.device_name = kwargs.get('device_name', None)
        self.result_id = kwargs.get('result_id', None)
        self.user_id = kwargs.get('user_id', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)

class Options(object):
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

class JobSchema(Schema):
    id = fields.Str()
    status = fields.Str()
    options = fields.Nested(OptionsSchema)
    package_id = fields.Str()
    package_name = fields.Str()
    device_id = fields.Str()
    device_name = fields.Str()
    result_id = fields.Str(missing=None)
    user_id = fields.Str()
    created = DateTime()
    updated = DateTime()

    @post_load
    def post_load(self, data):
        return Job(**data)

class JobsService(object):
    """Service for accessing CDRouter Jobs."""

    RESOURCE = 'jobs'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of jobs."""
        schema = JobSchema()
        resp = self.service.list(self.base, filter, sort, limit, page)
        return self.service.decode(schema, resp, many=True)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a job."""
        schema = JobSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a tag."""
        schema = JobSchema(exclude=('id', 'status', 'options', 'package_name', 'device_name', 'result_id', 'user_id', 'created', 'updated'))
        json = self.service.encode(schema, resource)

        schema = JobSchema()
        resp = self.service.edit(self.base, resource.name, json)
        return self.service.decode(schema, resp)

    def launch(self, resource):
        """Launch a new job."""
        schema = JobSchema(exclude=('id', 'status', 'package_name', 'device_name', 'result_id', 'user_id', 'created', 'updated'))
        json = self.service.encode(schema, resource)

        schema = JobSchema()
        resp = self.service.create(self.base, json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a job."""
        return self.service.delete_id(self.base, id)

    @staticmethod
    def _package_id(id): # pylint: disable=invalid-name,redefined-builtin
        if isinstance(id, (str, int)):
            return {'package_id': str(id)}
        return id

    def bulk_launch(self, jobs=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk launch a set of jobs."""
        json = None
        if jobs is not None:
            schema = JobSchema(exclude=('id', 'status', 'package_name', 'device_name', 'result_id', 'user_id', 'created', 'updated'))
            jobs_json = self.service.encode(schema, jobs, many=True)
            json = {self.RESOURCE: jobs_json}

        schema = JobSchema()
        resp = self.service.post(self.base,
                                 params={'bulk': 'launch', 'filter': filter, 'all': all}, json=json)
        return self.service.decode(schema, resp, many=True)

    def bulk_delete(self, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of jobs."""
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)
