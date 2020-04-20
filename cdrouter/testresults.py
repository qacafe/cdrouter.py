#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter TestResults."""

import collections
from functools import partial

from marshmallow import Schema, fields, post_load
from .cdr_datetime import DateTime

class Summary(object):
    """Model for CDRouter Log Section Summaries.

    :param errors: (optional) Error log count as int.
    :param fails: (optional) Fail log count as int.
    :param passes: (optional) Pass log count as int.
    :param warnings: (optional) Warning log count as int.
    :param alerts: (optional) Alert log count as int.
    """
    def __init__(self, **kwargs):
        self.errors = kwargs.get('errors', None)
        self.fails = kwargs.get('fails', None)
        self.passes = kwargs.get('passes', None)
        self.warnings = kwargs.get('warnings', None)
        self.alerts = kwargs.get('alerts', None)

class SummarySchema(Schema):
    errors = fields.Int()
    fails = fields.Int()
    passes = fields.Int()
    warnings = fields.Int()
    alerts = fields.Int()

    @post_load
    def post_load(self, data):
        return Summary(**data)

class Line(object):
    """Model for CDRouter Log Lines.

    :param raw: (optional) Raw log text as string.
    :param line: (optional) Line number as int.
    :param header: (optional) `True` if line is a header.
    :param section: (optional) `True` if line is a section.
    :param prefix: (optional) Log prefix as string.
    :param name: (optional) Log stack name as string.
    :param timestamp: (optional) Log timestamp as string.
    :param timestamp_display: (optional) Log display timestamp as string.
    :param message: (optional) Log message as string.
    :param interface: (optional) Log interface as string (if packet log).
    :param packet: (optional) Log frame number as an int (if packet log).
    :param src: (optional) Log source address as string (if packet log).
    :param dst: (optional) Log destination address as string (if packet log).
    :param proto: (optional) Log protocol name as string (if packet log).
    :param info: (optional) Log protocol summary as string (if packet log).
    :param alert_interface: (optional) Log alert interface as string (if alert log).
    :param alert_index: (optional) Log alert index as an int (if alert log).
    :param alert_src: (optional) Log alert source address as string (if alert log).
    :param alert_dst: (optional) Log alert destination address as string (if alert log).
    :param alert_proto: (optional) Log alert protocol name as string (if alert log).
    :param alert_src_port: (optional) Log alert source port as int (if alert log).
    :param alert_dst_port: (optional) Log alert destination port as int (if alert log).
    :param alert_signature: (optional) Log alert signature as string (if alert log).
    :param alert_severity: (optional) Log alert severity as int (if alert log).
    :param alert_severity_display: (optional) Log alert display severity as string (if alert log).
    :param alert_sid: (optional) Log alert SID as int (if alert log).
    :param alert_rev: (optional) Log alert revision as int (if alert log).

    :param summary: (optional) :class:`testresults.Summary <testresults.Summary>` object (if section log)
    """
    def __init__(self, **kwargs):
        self.raw = kwargs.get('raw', None)

        self.line = kwargs.get('line', None)
        self.header = kwargs.get('header', None)
        self.section = kwargs.get('section', None)
        self.prefix = kwargs.get('prefix', None)
        self.name = kwargs.get('name', None)
        self.timestamp = kwargs.get('timestamp', None)
        self.timestamp_display = kwargs.get('timestamp_display', None)
        self.message = kwargs.get('message', None)

        self.interface = kwargs.get('interface', None)
        self.packet = kwargs.get('packet', None)

        self.src = kwargs.get('src', None)
        self.dst = kwargs.get('dst', None)
        self.proto = kwargs.get('proto', None)
        self.info = kwargs.get('info', None)

        self.alert_interface = kwargs.get('alert_interface', None)
        self.alert_index = kwargs.get('alert_index', None)

        self.alert_src = kwargs.get('alert_src', None)
        self.alert_dst = kwargs.get('alert_dst', None)
        self.alert_proto = kwargs.get('alert_proto', None)
        self.alert_src_port = kwargs.get('alert_src_port', None)
        self.alert_dst_port = kwargs.get('alert_dst_port', None)
        self.alert_signature = kwargs.get('alert_signature', None)
        self.alert_severity = kwargs.get('alert_severity', None)
        self.alert_severity_display = kwargs.get('alert_severity_display', None)
        self.alert_sid = kwargs.get('alert_sid', None)
        self.alert_rev = kwargs.get('alert_rev', None)

        self.summary = kwargs.get('summary', None)

class LineSchema(Schema):
    raw = fields.Str()

    line = fields.Int()
    header = fields.Bool(missing=None)
    section = fields.Bool(missing=None)
    prefix = fields.Str(missing=None)
    name = fields.Str(missing=None)
    timestamp = fields.Str(missing=None)
    timestamp_display = fields.Str(missing=None)
    message = fields.Str()

    interface = fields.Str(missing=None)
    packet = fields.Int(as_string=True, missing=None)

    src = fields.Str(missing=None)
    dst = fields.Str(missing=None)
    proto = fields.Str(missing=None)
    info = fields.Str(missing=None)

    alert_interface = fields.Str(missing=None)
    alert_index = fields.Int(as_string=True, missing=None)

    alert_src = fields.Str(missing=None)
    alert_dst = fields.Str(missing=None)
    alert_proto = fields.Str(missing=None)
    alert_src_port = fields.Int(as_string=True, missing=None)
    alert_dst_port = fields.Int(as_string=True, missing=None)
    alert_signature = fields.Str(missing=None)
    alert_severity = fields.Int(as_string=True, missing=None)
    alert_severity_display = fields.Str(missing=None)
    alert_sid = fields.Int(as_string=True, missing=None)
    alert_rev = fields.Int(as_string=True, missing=None)

    summary = fields.Nested(SummarySchema)

    @post_load
    def post_load(self, data):
        return Line(**data)

class Log(object):
    """Model for CDRouter Log.

    :param offset: (optional) Zero-based offset in logfile as int.
    :param limit: (optional) Limit as int.
    :param lines: (optional) :class:`testresults.Line <testresults.Line>` list
    :param total: (optional) Total line count as int.
    """
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
    """Model for CDRouter TestResults.

    :param id: (optional) Result ID as an int.
    :param seq: (optional) TestResult sequence ID as an int.
    :param loop: (optional) Loop number as an int.
    :param result: (optional) Test result as string.
    :param alerts: (optional) Alerts count as int.
    :param retries: (optional) Retry count as int.
    :param started: (optional) Test start time as `DateTime`.
    :param duration: (optional) Test duration as int.
    :param flagged: (optional) `True` if test is flagged.
    :param name: (optional) Test name as string.
    :param description: (optional) Test description as string.
    :param skip_name: (optional) Skip name for TestResult as string.
    :param skip_reason: (optional) Skip reason for TestResult as string.
    :param log: (optional) Logfile path for TestResult as string.
    :param note: (optional) Note for TestResult as string.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.seq = kwargs.get('seq', None)
        self.loop = kwargs.get('loop', None)
        self.result = kwargs.get('result', None)
        self.alerts = kwargs.get('alerts', None)
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
    id = fields.Int(as_string=True)
    seq = fields.Int(as_string=True)
    loop = fields.Int(as_string=True)
    result = fields.Str()
    alerts = fields.Int()
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

class Page(collections.namedtuple('Page', ['data', 'links'])):
    """Named tuple for a page of list response data.

    :param data: :class:`testresults.TestResult <testresults.TestResult>` list
    :param links: :class:`cdrouter.Links <cdrouter.Links>` object
    """

class TestResultsService(object):
    """Service for accessing CDRouter TestResults."""

    RESOURCE = 'tests'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id): # pylint: disable=invalid-name,redefined-builtin
        return 'results/'+str(id)+self.BASE

    def list(self, id, filter=None, type=None, sort=None, limit=None, page=None, detailed=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of test results.

        :param id: Result ID as an int.
        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`testresults.Page <testresults.Page>` object
        """
        schema = TestResultSchema()
        resp = self.service.list(self._base(id), filter, type, sort, limit, page, detailed=detailed)
        trs, l =self.service.decode(schema, resp, many=True, links=True)
        return Page(trs, l)

    def iter_list(self, id, *args, **kwargs):
        """Get a list of test results.  Whereas ``list`` fetches a single page
        of test results according to its ``limit`` and ``page``
        arguments, ``iter_list`` returns all test results by
        internally making successive calls to ``list``.

        :param id: Result ID as an int.
        :param args: Arguments that ``list`` takes.
        :param kwargs: Optional arguments that ``list`` takes.
        :return: :class:`testresults.TestResult <testresults.TestResult>` list

        """
        l = partial(self.list, id)
        return self.service.iter_list(l, *args, **kwargs)

    def list_csv(self, id, filter=None, type=None, sort=None, limit=None, page=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of test results as CSV.

        :param id: Result ID as an int.
        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :rtype: string
        """
        return self.service.list(self._base(id), filter, type, sort, limit, page, format='csv').text

    def get(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        """Get a test result.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :return: :class:`testresults.TestResult <testresults.TestResult>` object
        :rtype: testresults.TestResult
        """
        schema = TestResultSchema()
        resp = self.service.get_id(self._base(id), seq)
        return self.service.decode(schema, resp)

    def edit(self, resource): # pylint: disable=invalid-name,redefined-builtin
        """Edit a test result.

        :param resource: :class:`testresults.TestResult <testresults.TestResult>` object
        :return: :class:`testresults.TestResult <testresults.TestResult>` object
        :rtype: testresults.TestResult
        """
        schema = TestResultSchema(exclude=('id', 'seq', 'loop', 'result', 'alerts', 'retries', 'started', 'duration', 'name', 'description', 'skip_name', 'skip_reason', 'log'))
        json = self.service.encode(schema, resource)

        schema = TestResultSchema()
        resp = self.service.edit(self._base(resource.id), resource.seq, json)
        return self.service.decode(schema, resp)

    def list_log(self, id, seq, offset=None, limit=None, filter=None, packets=None, timestamp_format=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a test result's log.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param offset: (optional) Offset within logfile to get.
        :param limit: (optional) Limit returned list length.
        :param filter: (optional) Filters to apply as a string list.
        :param packets: (optional) Set to bool `False` to omit packet logs.
        :param timestamp_format: (optional) Timestamp format to use, must be string `long` or `short`.
        :return: :class:`testresults.Log <testresults.Log>` object
        :rtype: testresults.Log
        """
        schema = LogSchema()
        resp = self.service.get(self._base(id)+str(seq)+'/log/',
                                params={'offset': offset, 'limit': limit, 'filter': filter,
                                        'packets': packets, 'timestamp_format': timestamp_format, 'format': 'json'})
        return self.service.decode(schema, resp)

    def iter_list_log(self, id, seq, *args, **kwargs): # pylint: disable=invalid-name,redefined-builtin
        """Get a test result's log.  Whereas ``list_log`` fetches a single
        range of log lines according to its ``limit`` and ``offset``
        arguments, ``iter_list_log`` returns all log lines by
        internally making successive calls to ``list_log``.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param args: Arguments that ``list_log`` takes.
        :param kwargs: Optional arguments that ``list_log`` takes.
        :return: :class:`testresults.Line <testresults.Line>` list

        """

        def generate():
            offset = int(kwargs.get('offset', 0))
            if 'limit' not in kwargs:
                kwargs['limit'] = 250

            while True:
                logs = self.list_log(id, seq, *args, **kwargs)
                nlines = len(logs.lines)
                if nlines == 0:
                    break
                for l in logs.lines:
                    yield l
                offset = logs.lines[nlines-1].line
                kwargs.update({'offset': offset})

        return generate()

    def get_log_plaintext(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        """Get a test result's log as plaintext.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :rtype: string
        """
        return self.service.get(self._base(id)+str(seq)+'/log/',
                                params={'format': 'text'}).text
