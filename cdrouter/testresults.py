#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter TestResults."""

from marshmallow import Schema, fields, post_load
from .cdr_datetime import DateTime

class Summary(object):
    def __init__(self, **kwargs):
        self.errors = kwargs.get('errors', None)
        self.fails = kwargs.get('fails', None)
        self.passes = kwargs.get('passes', None)
        self.warnings = kwargs.get('warnings', None)

class SummarySchema(Schema):
    errors = fields.Int()
    fails = fields.Int()
    passes = fields.Int()
    warnings = fields.Int()

    @post_load
    def post_load(self, data):
        return Summary(**data)

class Line(object):
    def __init__(self, **kwargs):
        self.raw = kwargs.get('raw', None)

        self.line = kwargs.get('line', None)
        self.header = kwargs.get('header', None)
        self.section = kwargs.get('section', None)
        self.prefix = kwargs.get('prefix', None)
        self.name = kwargs.get('name', None)
        self.timestamp = kwargs.get('timestamp', None)
        self.message = kwargs.get('message', None)

        self.interface = kwargs.get('interface', None)
        self.packet = kwargs.get('packet', None)

        self.src = kwargs.get('src', None)
        self.dst = kwargs.get('dst', None)
        self.proto = kwargs.get('proto', None)
        self.info = kwargs.get('info', None)

        self.summary = kwargs.get('summary', None)

class LineSchema(Schema):
    raw = fields.Str()

    line = fields.Int()
    header = fields.Bool(missing=None)
    section = fields.Bool(missing=None)
    prefix = fields.Str(missing=None)
    name = fields.Str(missing=None)
    timestamp = fields.Str(missing=None)
    message = fields.Str()

    interface = fields.Str(missing=None)
    packet = fields.Str(missing=None)

    src = fields.Str(missing=None)
    dst = fields.Str(missing=None)
    proto = fields.Str(missing=None)
    info = fields.Str(missing=None)

    summary = fields.Nested(SummarySchema)

    @post_load
    def post_load(self, data):
        return Line(**data)

class Log(object):
    def __init__(self, **kwargs):
        self.offset = kwargs.get('offset', None)
        self.limit = kwargs.get('limit', None)
        self.lines = kwargs.get('lines', None)
        self.total = kwargs.get('total', None)

class LogSchema(Schema):
    offset = fields.Int()
    limit = fields.Int()
    lines = fields.Nested(LineSchema, many=True)
    total = fields.Int()

    @post_load
    def post_load(self, data):
        return Log(**data)

class TestResult(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.seq = kwargs.get('seq', None)
        self.loop = kwargs.get('loop', None)
        self.result = kwargs.get('result', None)
        self.retries = kwargs.get('retries', None)
        self.started = kwargs.get('started', None)
        self.duration = kwargs.get('duration', None)
        self.flagged = kwargs.get('flagged', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.skip_name = kwargs.get('skip_name', None)
        self.skip_reason = kwargs.get('skip_reason', None)
        self.log = kwargs.get('log', None)
        self.note = kwargs.get('note', None)

class TestResultSchema(Schema):
    id = fields.Str()
    seq = fields.Str()
    loop = fields.Str()
    result = fields.Str()
    retries = fields.Int()
    started = DateTime()
    duration = fields.Int()
    flagged = fields.Bool()
    name = fields.Str()
    description = fields.Str()
    skip_name = fields.Str()
    skip_reason = fields.Str()
    log = fields.Str()
    note = fields.Str()

    @post_load
    def post_load(self, data):
        return TestResult(**data)

class TestResultsService(object):
    """Service for accessing CDRouter TestResults."""

    RESOURCE = 'tests'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id): # pylint: disable=invalid-name,redefined-builtin
        return 'results/'+str(id)+self.BASE

    def list(self, id, filter=None, sort=None, limit=None, page=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of test results."""
        schema = TestResultSchema()
        resp = self.service.list(self._base(id), filter, sort, limit, page)
        return self.service.decode(schema, resp, many=True)

    def list_csv(self, id, filter=None, sort=None, limit=None, page=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of test results as CSV."""
        return self.service.list(self._base(id), filter, sort, limit, page, format='csv')

    def get(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        """Get a test result."""
        schema = TestResultSchema()
        resp = self.service.get_id(self._base(id), seq)
        return self.service.decode(schema, resp)

    def edit(self, id, resource): # pylint: disable=invalid-name,redefined-builtin
        """Edit a test result."""
        schema = TestResultSchema(exclude=('id', 'seq', 'loop', 'result', 'retries', 'started', 'duration', 'name', 'description', 'skip_name', 'skip_reason', 'log'))
        json = self.service.encode(schema, resource)

        schema = TestResultSchema()
        resp = self.service.edit(self._base(id), resource.seq, json)
        return self.service.decode(schema, resp)

    def get_log(self, id, seq, offset=None, limit=None, filter=None, packets=None, timestamp_format=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a test result's log."""
        schema = LogSchema()
        resp = self.service.get(self._base(id)+str(seq)+'/log/',
                                params={'offset': offset, 'limit': limit, 'filter': filter,
                                        'packets': packets, 'timestamp_format': timestamp_format, 'format': 'json'})
        return self.service.decode(schema, resp)

    def get_log_plaintext(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        """Get a test result's log as plaintext."""
        return self.service.get(self._base(id)+str(seq)+'/log/',
                                params={'format': 'text'})
