#
# Copyright (c) 2017-2023 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Results."""

from collections import namedtuple
import io

from requests_toolbelt.downloadutils import stream
from marshmallow import Schema, fields, post_load, EXCLUDE
from .cdr_datetime import DateTime
from .testresults import TestResultSchema
from .alerts import AlertSchema
from .configs import InterfacesSchema, TestvarSchema
from .metrics import GraphMetric, GraphMetricSchema, Page as MetricPage, MetricSchema as MetricsDotMetricSchema

class TestCount(object):
    """Model for CDRouter Test Counts.

    :param name: (optional) Name as a string.
    :param count: (optional) Count as an int.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.count = kwargs.get('count', None)

class TestCountSchema(Schema):
    name = fields.Str()
    count = fields.Int(as_string=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return TestCount(**data)

class TestDuration(object):
    """Model for CDRouter Test Durations.

    :param name: (optional) Name as a string.
    :param duration: (optional) Duration as an int.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.duration = kwargs.get('duration', None)

class TestDurationSchema(Schema):
    name = fields.Str()
    duration = fields.Int(as_string=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return TestDuration(**data)

class ResultBreakdown(object):
    """Model for CDRouter Result Breakdowns.

    :param passed: (optional) Pass count as an int.
    :param failed: (optional) Fail count as an int.
    :param skipped: (optional) Skipped count as an int.
    :param alerted: (optional) Alerted count as an int.
    """
    def __init__(self, **kwargs):
        self.passed = kwargs.get('passed', None)
        self.failed = kwargs.get('failed', None)
        self.skipped = kwargs.get('skipped', None)
        self.alerted = kwargs.get('alerted', None)

class ResultBreakdownSchema(Schema):
    passed = fields.Int(as_string=True)
    failed = fields.Int(as_string=True)
    skipped = fields.Int(as_string=True)
    alerted = fields.Int(as_string=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return ResultBreakdown(**data)

class TimeBreakdown(object):
    """Model for CDRouter Time Breakdowns.

    :param passed: (optional) Pass duration as an int.
    :param failed: (optional) Fail duration as an int.
    """
    def __init__(self, **kwargs):
        self.passed = kwargs.get('passed', None)
        self.failed = kwargs.get('failed', None)

class TimeBreakdownSchema(Schema):
    passed = fields.Int(as_string=True)
    failed = fields.Int(as_string=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return TimeBreakdown(**data)

class SetStats(object):
    """Model for CDRouter Result Set Stats.

    :param frequent_failures: (optional) :class:`results.TestCount <results.TestCount>` list
    :param longest_tests: (optional) :class:`results.TestDuration <results.TestDuration>` list
    :param result_breakdown: (optional) :class:`results.ResultBreakdown <results.ResultBreakdown>` object
    :param time_breakdown: (optional) :class:`results.TimeBreakdown <results.TimeBreakdown>` object
    """
    def __init__(self, **kwargs):
        self.frequent_failures = kwargs.get('frequent_failures', None)
        self.longest_tests = kwargs.get('longest_tests', None)
        self.result_breakdown = kwargs.get('result_breakdown', None)
        self.time_breakdown = kwargs.get('time_breakdown', None)

class SetStatsSchema(Schema):
    frequent_failures = fields.Nested(lambda: TestCountSchema(many=True), unknown=EXCLUDE)
    longest_tests = fields.Nested(lambda: TestDurationSchema(many=True), unknown=EXCLUDE)
    result_breakdown = fields.Nested(ResultBreakdownSchema, unknown=EXCLUDE)
    time_breakdown = fields.Nested(TimeBreakdownSchema, unknown=EXCLUDE)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return SetStats(**data)

class TestResultSummary(object):
    """Model for CDRouter TestResult summaries.

    :param id: (optional) Result ID as an int.
    :param seq: (optional) TestResult sequence ID as an int.
    :param result: (optional) Test result as string.
    :param alerts: (optional) Alert count as an int.
    :param duration: (optional) Test duration as int.
    :param flagged: (optional) `True` if test is flagged.
    :param name: (optional) Test name as string.
    :param description: (optional) Test description as string.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.seq = kwargs.get('seq', None)
        self.result = kwargs.get('result', None)
        self.alerts = kwargs.get('alerts', None)
        self.duration = kwargs.get('duration', None)
        self.flagged = kwargs.get('flagged', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)

class TestResultSummarySchema(Schema):
    id = fields.Int(as_string=True)
    seq = fields.Int(as_string=True)
    result = fields.Str()
    alerts = fields.Int()
    duration = fields.Int()
    flagged = fields.Bool()
    name = fields.Str()
    description = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return TestResultSummary(**data)

class TestResultDiff(object):
    """Model for CDRouter TestResult diffs.

    :param name: (optional) Test name as a string.
    :param summaries: (optional) :class:`results.TestResultSummary <results.TestResultSummary>` list
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.summaries = kwargs.get('summaries', None)

class TestResultDiffSchema(Schema):
    name = fields.Str()
    summaries = fields.Nested(lambda: TestResultSummarySchema(many=True), unknown=EXCLUDE)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return TestResultDiff(**data)

class DiffStats(object):
    """Model for CDRouter Result Diff Stats.

    :param tests: (optional) :class:`results.TestResultDiff <results.TestResultDiff>` list
    """
    def __init__(self, **kwargs):
        self.tests = kwargs.get('tests', None)

class DiffStatsSchema(Schema):
    tests = fields.Nested(lambda: TestResultDiffSchema(many=True), unknown=EXCLUDE)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return DiffStats(**data)

class TestResultBreakdown(object):
    """Model for CDRouter TestResult Breakdowns.

    :param failed_at_least_once: (optional) :class:`results.TestCount <results.TestCount>` list
    :param passed_every_time: (optional) :class:`results.TestCount <results.TestCount>` list
    """
    def __init__(self, **kwargs):
        self.failed_at_least_once = kwargs.get('failed_at_least_once', None)
        self.passed_every_time = kwargs.get('passed_every_time', None)

class TestResultBreakdownSchema(Schema):
    failed_at_least_once = fields.Nested(lambda: TestCountSchema(many=True), unknown=EXCLUDE)
    passed_every_time = fields.Nested(lambda: TestCountSchema(many=True), unknown=EXCLUDE)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return TestResultBreakdown(**data)

class Progress(object):
    """Model for CDRouter Result Progress.

    :param finished: (optional) Finished count as an int.
    :param total: (optional) Total count as an int.
    :param progress: (optional) Progress as an int.
    :param unit: (optional) Unit as a string.
    """
    def __init__(self, **kwargs):
        self.finished = kwargs.get('finished', None)
        self.total = kwargs.get('total', None)
        self.progress = kwargs.get('progress', None)
        self.unit = kwargs.get('unit', None)

class ProgressSchema(Schema):
    finished = fields.Int()
    total = fields.Int()
    progress = fields.Int()
    unit = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return Progress(**data)

class SingleStats(object):
    """Model for CDRouter Single Results Stats.

    :param result_breakdown: (optional) :class:`results.ResultBreakdown <results.ResultBreakdown>` object
    :param progress: (optional) :class:`results.Progress <results.Progress>` object
    """
    def __init__(self, **kwargs):
        self.result_breakdown = kwargs.get('result_breakdown', None)
        self.progress = kwargs.get('progress', None)

class SingleStatsSchema(Schema):
    result_breakdown = fields.Nested(TestResultBreakdownSchema, unknown=EXCLUDE)
    progress = fields.Nested(ProgressSchema, unknown=EXCLUDE)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return SingleStats(**data)

class SummaryStats(object):
    """Model for CDRouter Summary Results Stats.

    :param result_breakdown: (optional) :class:`results.ResultBreakdown <results.ResultBreakdown>` object
    :param test_summaries: (optional) :class:`testresults.TestResult <testresults.TestResult>` list
    """
    def __init__(self, **kwargs):
        self.result_breakdown = kwargs.get('result_breakdown', None)
        self.test_summaries = kwargs.get('test_summaries', None)

class SummaryStatsSchema(Schema):
    result_breakdown = fields.Nested(ResultBreakdownSchema, unknown=EXCLUDE)
    test_summaries = fields.Nested(lambda: TestResultSchema(many=True), load_default=None, unknown=EXCLUDE)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return SummaryStats(**data)

class PackageCount(object):
    """Model for CDRouter Package Counts.

    :param package_name: (optional) Package name as a string.
    :param count: (optional) Count as an int.
    """
    def __init__(self, **kwargs):
        self.package_name = kwargs.get('package_name', None)
        self.count = kwargs.get('count', None)

class PackageCountSchema(Schema):
    package_name = fields.Str()
    count = fields.Int(as_string=True, load_default=None)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return PackageCount(**data)

class DeviceCount(object):
    """Model for CDRouter Device Counts.

    :param device_name: (optional) Device name as a string.
    :param count: (optional) Count as an int.
    """
    def __init__(self, **kwargs):
        self.device_name = kwargs.get('device_name', None)
        self.count = kwargs.get('count', None)

class DeviceCountSchema(Schema):
    device_name = fields.Str()
    count = fields.Int(as_string=True, load_default=None)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return DeviceCount(**data)

class AllStats(object):
    """Model for CDRouter All Results Stats.

    :param frequent_packages: (optional) :class:`results.PackageCount <results.PackageCount>` list
    :param package_names: (optional) :class:`results.PackageCount <results.PackageCount>` list
    :param frequent_devices: (optional) :class:`results.DeviceCount <results.DeviceCount>` list
    :param device_names: (optional) :class:`results.DeviceCount <results.DeviceCount>` list
    """
    def __init__(self, **kwargs):
        self.frequent_packages = kwargs.get('frequent_packages', None)
        self.package_names = kwargs.get('package_names', None)
        self.frequent_devices = kwargs.get('frequent_devices', None)
        self.device_names = kwargs.get('device_names', None)

class AllStatsSchema(Schema):
    frequent_packages = fields.Nested(lambda: PackageCountSchema(many=True), unknown=EXCLUDE)
    package_names = fields.Nested(lambda: PackageCountSchema(many=True), unknown=EXCLUDE)
    frequent_devices = fields.Nested(lambda: DeviceCountSchema(many=True), unknown=EXCLUDE)
    device_names = fields.Nested(lambda: DeviceCountSchema(many=True), unknown=EXCLUDE)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return AllStats(**data)

# type aliases for Metric and MetricSchema types which were moved to
# metrics.GraphMetric and metrics.GraphMetricSchema in cdrouter.py
# v0.9.0.  See https://docs.python.org/3/library/typing.html for more
# info on type aliases which were added in Python 3.5.
Metric = GraphMetric
MetricSchema = GraphMetricSchema

class LogDirFile(object):
    """Model for CDRouter Logdir Files.

    :param name: (optional) Name as a string.
    :param size: (optional) Filesize as an int.
    :param modified: (optional) Last-updated time as a `DateTime`.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.size = kwargs.get('size', None)
        self.modified = kwargs.get('modified', None)

class LogDirFileSchema(Schema):
    name = fields.Str()
    size = fields.Int()
    modified = DateTime()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return LogDirFile(**data)

class Options(object):
    """Model for CDRouter Result Options.

    :param tags: (optional) Tags as string list.
    :param skip_tests: (optional) Tests to skip as string list.
    :param begin_at: (optional) Test name to begin testing at as string.
    :param end_at: (optional) Test name to end testing at as string.
    :param testvars: (optional) Extra testvars to set as a :class:`configs.Testvar <configs.Testvar>` list.
    :param extra_cli_args: (optional) Extra `cdrouter-cli` arguments as string.
    """
    def __init__(self, **kwargs):
        self.tags = kwargs.get('tags', None)
        self.skip_tests = kwargs.get('skip_tests', None)
        self.begin_at = kwargs.get('begin_at', None)
        self.end_at = kwargs.get('end_at', None)
        self.testvars = kwargs.get('testvars', None)
        self.extra_cli_args = kwargs.get('extra_cli_args', None)

class OptionsSchema(Schema):
    tags = fields.List(fields.Str(), load_default=None)
    skip_tests = fields.List(fields.Str(), load_default=None)
    begin_at = fields.Str()
    end_at = fields.Str()
    testvars = fields.Nested(TestvarSchema, many=True, load_default=None, unknown=EXCLUDE)
    extra_cli_args = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return Options(**data)

class Feature(object):
    """Model for CDRouter Result Feature.

    :param feature: (optional) Feature as a string.
    :param enabled: (optional) `True` if feature is enabled.
    :param reason: (optional) Reason as a string
    """
    def __init__(self, **kwargs):
        self.feature = kwargs.get('feature', None)
        self.enabled = kwargs.get('enabled', None)
        self.reason = kwargs.get('reason', None)

class FeatureSchema(Schema):
    feature = fields.Str()
    enabled = fields.Bool()
    reason = fields.Str(load_default=None)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return Feature(**data)

class UpdateField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if 'result' in value and 'status' in value:
            return ResultSchema().load(value, unknown=EXCLUDE)
        if 'result' in value and 'status' not in value:
            return TestResultSchema().load(value, unknown=EXCLUDE)
        if 'sid' in value and 'rev' in value:
            return AlertSchema().load(value, unknown=EXCLUDE)
        self.fail('invalid')
        return None

class Update(object):
    """Model for CDRouter Result Update.

    :param id: (optional) Update ID as an int.
    :param timestamp: (optional) System time as `DateTime`.
    :param progress: (optional) :class:`results.Progress <results.Progress>` object
    :param running: (optional) :class:`testresults.TestResult <testresults.TestResult>` object
    :param updates: (optional) :class:`results.Result <results.Result>`, :class:`testresults.TestResult <testresults.TestResult>` and :class:`alerts.Alert <alerts.Alert>` list
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.timestamp = kwargs.get('timestamp', None)
        self.progress = kwargs.get('progress', None)
        self.running = kwargs.get('running', None)
        self.updates = kwargs.get('updates', None)

class UpdateSchema(Schema):
    id = fields.Int(as_string=True)
    timestamp = DateTime()
    progress = fields.Nested(ProgressSchema(), load_default=None, unknown=EXCLUDE)
    running = fields.Nested(TestResultSchema(), load_default=None, unknown=EXCLUDE)
    updates = fields.List(UpdateField, load_default=None)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return Update(**data)

class Result(object):
    """Model for CDRouter Results.

    :param id: (optional) Result ID as an int.
    :param created: (optional) Creation time as `DateTime`.
    :param updated: (optional) Last-updated time as `DateTime`.
    :param locked: (optional) Bool `True` if result is locked.
    :param result: (optional) Result as a string.
    :param active: (optional) Bool `True` if status is 'running' or 'paused'.
    :param status: (optional) Status as a string.
    :param loops: (optional) Loop count as an int.
    :param tests: (optional) Test count as an int.
    :param passed: (optional) Passed count as an int.
    :param fail: (optional) Failed count as an int.
    :param alerts: (optional) Alert count as an int.
    :param duration: (optional) Duration in seconds as an int.
    :param size_on_disk: (optional) Size on disk in bytes as an int.
    :param starred: (optional) Bool `True` if result is starred.
    :param archived: (optional) Bool `True` if result is archived.
    :param result_dir: (optional) Filepath to result directory as a string.
    :param agent_name: (optional) Agent name as a string.
    :param package_name: (optional) Package name as a string.
    :param device_name: (optional) Device name as a string.
    :param config_name: (optional) Config name as a string.
    :param package_id: (optional) Package ID as an int.
    :param device_id: (optional) Device ID as an int.
    :param config_id: (optional) Config ID as an int.
    :param user_id: (optional) User ID as an int.
    :param note: (optional) Note as a string.
    :param pause_message: (optional) Pause message as a string (if currently paused).
    :param build_info: (optional) Build info as a string.
    :param tags: (optional) Tags as a string list.
    :param testcases: (optional) Testcases as a string list.
    :param options: (optional) :class:`results.Options <results.Options>` object
    :param features: (optional) Dict of feature name strings to :class:`results.Feature <results.Feature>` objects.
    :param interfaces: (optional) :class:`configs.Interfaces <configs.Interfaces>` list.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)
        self.locked = kwargs.get('locked', None)
        self.result = kwargs.get('result', None)
        self.active = kwargs.get('active', None)
        self.status = kwargs.get('status', None)
        self.loops = kwargs.get('loops', None)
        self.tests = kwargs.get('tests', None)
        self.passed = kwargs.get('pass', None)
        self.fail = kwargs.get('fail', None)
        self.alerts = kwargs.get('alerts', None)
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
        self.features = kwargs.get('features', None)
        self.interfaces = kwargs.get('interfaces', None)

class ResultSchema(Schema):
    id = fields.Int(as_string=True)
    created = DateTime()
    updated = DateTime()
    locked = fields.Bool(load_default=False)
    result = fields.Str()
    active = fields.Bool()
    status = fields.Str()
    loops = fields.Int()
    tests = fields.Int()
    passed = fields.Int(attribute='pass', data_key='pass')
    fail = fields.Int()
    alerts = fields.Int()
    duration = fields.Int()
    size_on_disk = fields.Int()
    starred = fields.Bool()
    archived = fields.Bool()
    result_dir = fields.Str()
    agent_name = fields.Str()
    package_name = fields.Str()
    device_name = fields.Str()
    config_name = fields.Str()
    package_id = fields.Int(as_string=True)
    device_id = fields.Int(as_string=True)
    config_id = fields.Int(as_string=True)
    user_id = fields.Int(as_string=True)
    note = fields.Str()
    pause_message = fields.Str(load_default=None)
    build_info = fields.Str(load_default=None)
    tags = fields.List(fields.Str())
    testcases = fields.List(fields.Str(), load_default=None)
    options = fields.Nested(OptionsSchema, unknown=EXCLUDE)
    features = fields.Dict(keys=fields.Str(), values=fields.Nested(FeatureSchema()), unknown=EXCLUDE)
    interfaces = fields.Nested(InterfacesSchema, many=True, unknown=EXCLUDE)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return Result(**data)

class Page(namedtuple('Page', ['data', 'links'])):
    """Named tuple for a page of list response data.

    :param data: :class:`results.Result <results.Result>` list
    :param links: :class:`cdrouter.Links <cdrouter.Links>` object
    """

class ResultsService(object):
    """Service for accessing CDRouter Results."""

    RESOURCE = 'results'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, type=None, sort=None, limit=None, page=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of results, using summary representation by default (see
        ``detailed`` parameter).

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`results.Page <results.Page>` object
        """
        schema = ResultSchema()
        if not detailed:
            schema = ResultSchema(exclude=('result', 'loops', 'tests', 'result_dir', 'agent_name', 'config_name', 'note', 'pause_message', 'testcases', 'options', 'build_info', 'interfaces'))
        resp = self.service.list(self.base, filter, type, sort, limit, page, detailed=detailed)
        rs, l = self.service.decode(schema, resp, many=True, links=True)
        return Page(rs, l)

    def iter_list(self, *args, **kwargs):
        """Get a list of results.  Whereas ``list`` fetches a single page of
        results according to its ``limit`` and ``page`` arguments,
        ``iter_list`` returns all results by internally making
        successive calls to ``list``.

        :param args: Arguments that ``list`` takes.
        :param kwargs: Optional arguments that ``list`` takes.
        :return: :class:`results.Result <results.Result>` list

        """
        return self.service.iter_list(self.list, *args, **kwargs)

    def list_csv(self, filter=None, type=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of results as CSV.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :rtype: string
        """
        return self.service.list(self.base, filter, type, sort, limit, page, format='csv').text

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a result.

        :param id: Result ID as an int.
        :return: :class:`results.Result <results.Result>` object
        :rtype: results.Result
        """
        schema = ResultSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def updates(self, id, update_id=None): # pylint: disable=invalid-name,redefined-builtin
        """Get updates of a running result via long-polling.  If no updates are available, CDRouter waits up to 10 seconds before sending an empty response.

        :param id: Result ID as an int.
        :param update_id: (optional) Update ID as an int.
        :return: :class:`results.Update <results.Update>` object
        :rtype: results.Update

        """
        if update_id is None:
            update_id = -1
        schema = UpdateSchema()
        resp = self.service.get_id(self.base, id, params={'updates': update_id})
        return self.service.decode(schema, resp)

    def stop(self, id, when=None): # pylint: disable=invalid-name,redefined-builtin
        """Stop a running result.

        :param id: Result ID as an int.
        :param when: Must be string `end-of-test` or `end-of-loop`.
        """
        return self.service.post(self.base+str(id)+'/stop/', params={'when': when})

    def stop_end_of_test(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Stop a running result at the end of the current test.

        :param id: Result ID as an int.
        """
        return self.stop(id, 'end-of-test')

    def stop_end_of_loop(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Stop a running result at the end of the current loop.

        :param id: Result ID as an int.
        """
        return self.stop(id, 'end-of-loop')

    def pause(self, id, when=None): # pylint: disable=invalid-name,redefined-builtin
        """Pause a running result.

        :param id: Result ID as an int.
        :param when: Must be string `end-of-test` or `end-of-loop`.
        """
        return self.service.post(self.base+str(id)+'/pause/', params={'when': when})

    def pause_end_of_test(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Pause a running result at the end of the current test.

        :param id: Result ID as an int.
        """
        return self.pause(id, 'end-of-test')

    def pause_end_of_loop(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Pause a running result at the end of the current loop.

        :param id: Result ID as an int.
        """
        return self.pause(id, 'end-of-loop')

    def unpause(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Unpause a running result.

        :param id: Result ID as an int.
        """
        return self.service.post(self.base+str(id)+'/unpause/')

    def edit(self, resource):
        """Edit a result.

        :param resource: :class:`results.Result <results.Result>` object
        :return: :class:`results.Result <results.Result>` object
        :rtype: results.Result
        """
        schema = ResultSchema(exclude=('id', 'created', 'updated', 'result', 'active', 'status', 'loops', 'tests', 'passed', 'fail', 'alerts', 'duration', 'size_on_disk', 'result_dir', 'agent_name', 'package_name', 'config_name', 'package_id', 'config_id', 'pause_message', 'build_info', 'options', 'features', 'interfaces'))
        json = self.service.encode(schema, resource)

        schema = ResultSchema()
        resp = self.service.edit(self.base, resource.id, json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a result.

        :param id: Result ID as an int.
        """
        return self.service.delete_id(self.base, id)

    def lock(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Lock a result.  Locking prevents the result from being modified or deleted until it is unlocked.

        :param id: Result ID as an int.
        :return: :class:`results.Result <results.Result>` object
        :rtype: results.Result
        """
        schema = ResultSchema()
        resp = self.service.post(self.base+str(id)+'/lock/')
        return self.service.decode(schema, resp)

    def unlock(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Unlock a result.  Unlocking a locked result allows it to be modified or deleted once again.

        :param id: Result ID as an int.
        :return: :class:`results.Result <results.Result>` object
        :rtype: results.Result
        """
        schema = ResultSchema()
        resp = self.service.post(self.base+str(id)+'/unlock/')
        return self.service.decode(schema, resp)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get shares for a result.

        :param id: Result ID as an int.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.get_shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Edit shares for a result.

        :param id: Result ID as an int.
        :param user_ids: User IDs as int list.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id, exclude_captures=False): # pylint: disable=invalid-name,redefined-builtin
        """Export a result.

        :param id: Result ID as an int.
        :param exclude_captures: If bool `True`, don't export capture files
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.export(self.base, id, params={'exclude_captures': exclude_captures})

    def bulk_export(self, ids, exclude_captures=False):
        """Bulk export a set of results.

        :param ids: Int list of result IDs.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.bulk_export(self.base, ids, params={'exclude_captures': exclude_captures})

    def bulk_edit(self, _fields, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of results.

        :param _fields: :class:`results.Result <results.Result>` object
        :param ids: (optional) Int list of result IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        schema = ResultSchema(exclude=('id', 'created', 'updated', 'result', 'active', 'status', 'loops', 'tests', 'passed', 'fail', 'duration', 'size_on_disk', 'result_dir', 'agent_name', 'package_name', 'config_name', 'package_id', 'config_id', 'pause_message', 'build_info', 'options', 'features', 'interfaces'))
        _fields = self.service.encode(schema, _fields, skip_none=True)
        return self.service.bulk_edit(self.base, self.RESOURCE, _fields, ids=ids, filter=filter, type=type, all=all)

    def bulk_delete(self, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of results.

        :param ids: (optional) Int list of result IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, type=type, all=all)

    def all_stats(self):
        """Compute stats for all results.

        :return: :class:`results.AllStats <results.AllStats>` object
        :rtype: results.AllStats
        """
        schema = AllStatsSchema()
        resp = self.service.post(self.base, params={'stats': 'all'})
        return self.service.decode(schema, resp)

    def set_stats(self, ids):
        """Compute stats for a set of results.

        :param id: Result IDs as int list.
        :return: :class:`results.SetStats <results.SetStats>` object
        :rtype: results.SetStats
        """
        schema = SetStatsSchema()
        resp = self.service.post(self.base, params={'stats': 'set'}, json=[{'id': str(x)} for x in ids])
        return self.service.decode(schema, resp)

    def diff_stats(self, ids):
        """Compute diff stats for a set of results.

        :param id: Result IDs as int list.
        :return: :class:`results.DiffStats <results.DiffStats>` object
        :rtype: results.DiffStats
        """
        schema = DiffStatsSchema()
        resp = self.service.post(self.base, params={'stats': 'diff'}, json=[{'id': str(x)} for x in ids])
        return self.service.decode(schema, resp)

    def single_stats(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Compute stats for a result.

        :param id: Result ID as an int.
        :return: :class:`results.SingleStats <results.SingleStats>` object
        :rtype: results.SingleStats
        """
        schema = SingleStatsSchema()
        resp = self.service.get(self.base+str(id)+'/', params={'stats': 'all'})
        return self.service.decode(schema, resp)

    def progress_stats(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Compute progress stats for a result.

        :param id: Result ID as an int.
        :return: :class:`results.Progress <results.Progress>` object
        :rtype: results.Progress
        """
        schema = ProgressSchema()
        resp = self.service.get(self.base+str(id)+'/', params={'stats': 'progress'})
        return self.service.decode(schema, resp)

    def summary_stats(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Compute summary stats for a result.

        :param id: Result ID as an int.
        :return: :class:`results.SummaryStats <results.SummaryStats>` object
        :rtype: results.SummaryStats
        """
        schema = SummaryStatsSchema()
        resp = self.service.get(self.base+str(id)+'/', params={'stats': 'summary'})
        return self.service.decode(schema, resp)

    def list_logdir(self, id, filter=None, sort=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of logdir files.

        :param id: Result ID as an int.
        :param filter: Filter to apply as string.
        :param sort: Sort field to apply as string.
        :return: :class:`results.LogDirFile <results.LogDirFile>` list
        """
        schema = LogDirFileSchema()
        resp = self.service.list(self.base+str(id)+'/logdir/', filter, sort)
        return self.service.decode(schema, resp, many=True)

    def get_logdir_file(self, id, filename): # pylint: disable=invalid-name,redefined-builtin
        """Download a logdir file.

        :param id: Result ID as an int.
        :param filename: Logdir filename as string.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        resp = self.service.get(self.base+str(id)+'/logdir/'+filename+'/', stream=True)
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        resp.close()
        b.seek(0)
        return (b, self.service.filename(resp))

    def download_logdir_archive(self, id, format='zip', exclude_captures=False): # pylint: disable=invalid-name,redefined-builtin
        """Download logdir archive in tgz or zip format.

        :param id: Result ID as an int.
        :param format: (optional) Format to download, must be string `zip` or `tgz`.
        :param exclude_captures: If bool `True`, don't include capture files
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        resp = self.service.get(self.base+str(id)+'/logdir/', params={'format': format, 'exclude_captures': exclude_captures}, stream=True)
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        resp.close()
        b.seek(0)
        return (b, self.service.filename(resp))

    def list_metrics(self, id, filter=None, type=None, sort=None, limit=None, page=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of metrics, using summary representation by default (see
        ``detailed`` parameter).

        :param id: Result ID as an int.
        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`metrics.Page <metrics.Page>` object
        :rtype: metrics.Page
        """
        # metrics.MetricSchema imported as MetricsDotMetricSchema due to
        # MetricSchema type alias declared above for
        # backwards-compatibility
        schema = MetricsDotMetricSchema()
        resp = self.service.list(self.base+str(id)+'/metrics/', filter, type, sort, limit, page, detailed=detailed)
        rs, l = self.service.decode(schema, resp, many=True, links=True)
        return MetricPage(rs, l)

    def get_test_metric(self, id, tname, metric): # pylint: disable=invalid-name,redefined-builtin
        """Get a test graph metric.  This method is only for getting "bandwidth" or "latency" test metrics.

        This method is DEPRECATED since cdrouter.py v0.9.0, new code
        should use TestResultsService.get_test_metric instead.

        :param id: Result ID as an int.
        :param tname: Test name as string.
        :param metric: Metric name as string.
        :return: :class:`metrics.GraphMetric <metrics.GraphMetric>` list
        :rtype: metrics.GraphMetric
        """
        schema = GraphMetricSchema()
        resp = self.service.get(self.base+str(id)+'/metrics/'+tname+'/'+metric+'/')
        return self.service.decode(schema, resp, many=True)

    def get_test_metric_csv(self, id, tname, metric): # pylint: disable=invalid-name,redefined-builtin
        """Get a test metric as CSV.  This method is only for getting "bandwidth" or "latency" test metrics.

        :param id: Result ID as an int.
        :param tname: Test name as string.
        :param metric: Metric name as string.
        :rtype: string
        """
        return self.service.get(self.base+str(id)+'/metrics/'+tname+'/'+metric+'/',
                                params={'format': 'csv'}).text
