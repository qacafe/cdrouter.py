#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Results."""

from marshmallow import Schema, fields, post_load

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

class Result(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)
        self.result = kwargs.get('result', None)
        self.status = kwargs.get('status', None)
        self.loops = kwargs.get('loops', None)
        self.tests = kwargs.get('tests', None)
        self.passed = kwargs.get('pass', None)
        self.fail = kwargs.get('fail', None)
        self.duration = kwargs.get('duration', None)
        self.size_on_disk = kwargs.get('size_on_disk', None)
        self.starred = kwargs.get('starred', None)
        self.archived = kwargs.get('archived', None)
        self.result_dir = kwargs.get('result_dir', None)
        self.agent_name = kwargs.get('agent_name', None)
        self.package_name = kwargs.get('package_name', None)
        self.device_name = kwargs.get('device_name', None)
        self.config_name = kwargs.get('config_name', None)
        self.package_id = kwargs.get('package_id', None)
        self.device_id = kwargs.get('device_id', None)
        self.config_id = kwargs.get('config_id', None)
        self.user_id = kwargs.get('user_id', None)
        self.note = kwargs.get('note', None)
        self.pause_message = kwargs.get('pause_message', None)
        self.build_info = kwargs.get('build_info', None)
        self.tags = kwargs.get('tags', None)
        self.testcases = kwargs.get('testcases', None)
        self.options = kwargs.get('options', None)

class ResultSchema(Schema):
    id = fields.Str()
    created = fields.DateTime()
    updated = fields.DateTime()
    result = fields.Str()
    status = fields.Str()
    loops = fields.Int()
    tests = fields.Int()
    passed = fields.Int(attribute='pass', load_from='pass', dump_to='pass')
    fail = fields.Int()
    duration = fields.Int()
    size_on_disk = fields.Int()
    starred = fields.Bool()
    archived = fields.Bool()
    result_dir = fields.Str()
    agent_name = fields.Str()
    package_name = fields.Str()
    device_name = fields.Str()
    config_name = fields.Str()
    package_id = fields.Str()
    device_id = fields.Str()
    config_id = fields.Str()
    user_id = fields.Str()
    note = fields.Str()
    pause_message = fields.Str(missing=None)
    build_info = fields.Str()
    tags = fields.List(fields.Str())
    testcases = fields.List(fields.Str())
    options = fields.Nested(OptionsSchema)

    @post_load
    def post_load(self, data):
        return Result(**data)

class ResultsService(object):
    """Service for accessing CDRouter Results."""

    RESOURCE = 'results'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of results."""
        schema = ResultSchema(exclude=('result', 'loops', 'tests', 'result_dir', 'agent_name', 'config_name', 'note', 'pause_message', 'testcases', 'options', 'build_info'))
        resp = self.service.list(self.base, filter, sort, limit, page)
        return self.service.decode(schema, resp, many=True)

    def list_csv(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of results as CSV."""
        return self.service.list(self.base, filter, sort, limit, page, format='csv')

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a result."""
        schema = ResultSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def stop(self, id, when=None): # pylint: disable=invalid-name,redefined-builtin
        """Stop a running result."""
        return self.service.post(self.base+str(id)+'/stop/', params={'when': when})

    def stop_end_of_test(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Stop a running result at the end of the current test."""
        return self.stop(id, 'end-of-test')

    def stop_end_of_loop(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Stop a running result at the end of the current loop."""
        return self.stop(id, 'end-of-loop')

    def pause(self, id, when=None): # pylint: disable=invalid-name,redefined-builtin
        """Pause a running result."""
        return self.service.post(self.base+str(id)+'/pause/', params={'when': when})

    def pause_end_of_test(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Pause a running result at the end of the current test."""
        return self.pause(id, 'end-of-test')

    def pause_end_of_loop(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Pause a running result at the end of the current loop."""
        return self.pause(id, 'end-of-loop')

    def unpause(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Unpause a running result."""
        return self.service.post(self.base+str(id)+'/unpause/')

    def edit(self, resource):
        """Edit a result."""
        schema = ResultSchema()
        resp = self.service.edit(self.base, resource['id'], resource)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a result."""
        return self.service.delete_id(self.base, id)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get shares for a result."""
        return self.service.get_shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Edit shares for a result."""
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id, exclude_captures=False): # pylint: disable=invalid-name,redefined-builtin
        """Export a result."""
        return self.service.export(self.base, id, params={'exclude_captures': exclude_captures})

    def bulk_export(self, ids, exclude_captures=False):
        """Bulk export a set of results."""
        return self.service.bulk_export(self.base, ids, params={'exclude_captures': exclude_captures})

    def bulk_copy(self, ids):
        """Bulk copy a set of results."""
        schema = ResultSchema()
        return self.service.bulk_copy(self.base, self.RESOURCE, ids, schema)

    def bulk_edit(self, _fields, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of results."""
        return self.service.bulk_edit(self.base, self.RESOURCE, _fields, ids=ids, filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of results."""
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)

    def all_stats(self):
        """Compute stats for all results."""
        return self.service.post(self.base, params={'stats': 'all'})

    def set_stats(self, ids):
        """Compute stats for a set of results."""
        return self.service.post(self.base, params={'stats': 'set'}, json=[{'id': str(x)} for x in ids])

    def single_stats(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Compute stats for a result."""
        return self.service.get(self.base+str(id)+'/', params={'stats': 'all'})

    def list_logdir(self, id, filter=None, sort=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of logdir files."""
        return self.service.list(self.base+str(id)+'/logdir/', filter, sort)

    def get_logdir_file(self, id, filename): # pylint: disable=invalid-name,redefined-builtin
        """Download a logdir file."""
        return self.service.get(self.base+str(id)+'/logdir/'+filename+'/')

    def download_logdir_archive(self, id, filename, format='zip', exclude_captures=False): # pylint: disable=invalid-name,redefined-builtin
        """Download logdir archive in tgz or zip format."""
        return self.service.get(self.base+str(id)+'/logdir/'+filename+'/', params={'format': format, 'exclude_captures': exclude_captures})

    def get_test_metric(self, id, name, metric, format=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a test metric."""
        return self.service.get(self.base+str(id)+'/metrics/'+name+'/'+metric+'/',
                                params={'format': format})

    def get_test_metric_csv(self, id, name, metric): # pylint: disable=invalid-name,redefined-builtin
        """Get a test metric as CSV."""
        return self.get_test_metric(id, name, metric, format='csv')
