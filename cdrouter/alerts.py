#
# Copyright (c) 2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Alerts."""

import collections
from functools import partial

from marshmallow import Schema, fields, post_load
from .cdr_datetime import DateTime
from .cdr_dictfield import DictField

class Alert(object):
    """Model for CDRouter Alerts.

    :param id: (optional) Result ID as an int.
    :param idx: (optional) Alert index as an int.
    :param created: (optional) Creation time as `DateTime`.
    :param updated: (optional) Last-updated time as `DateTime`.
    :param seq: (optional) TestResult sequence ID as an int.
    :param loop: (optional) Loop number as an int.
    :param test_name: (optional) Test name as string.
    :param test_description: (optional) Test description as string.
    :param category: (optional) Alert category as a string.
    :param description: (optional) Alert description as a string.
    :param dest_ip: (optional) Alert destination IP as a string.
    :param dest_port: (optional) Alert destination port as an int.
    :param interface: (optional) Alert incoming interface as a string.
    :param payload: (optional) Alert payload as a base64 string.
    :param payload_ascii: (optional) Alert payload as an ASCII string.
    :param payload_hex: (optional) Alert payload as a hex string.
    :param proto: (optional) Alert protocol as a string.
    :param references: (optional) Alert references as a string list.
    :param rev: (optional) Alert rule revision as an int.
    :param rule: (optional) Alert rule as a string.
    :param rule_set: (optional) Alert rule set as a string.
    :param severity: (optional) Alert severity as an int.
    :param sid: (optional) Alert rule SID as an int.
    :param signature: (optional) Alert signature as a string.
    :param src_ip: (optional) Alert source IP as a string.
    :param src_port: (optional) Alert source port as an int.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.idx = kwargs.get('idx', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)

        self.seq = kwargs.get('seq', None)
        self.loop = kwargs.get('loop', None)
        self.test_name = kwargs.get('test_name', None)
        self.test_description = kwargs.get('test_description', None)

        self.category = kwargs.get('category', None)
        self.description = kwargs.get('description', None)
        self.dest_ip = kwargs.get('dest_ip', None)
        self.dest_port = kwargs.get('dest_port', None)
        self.interface = kwargs.get('interface', None)
        self.payload = kwargs.get('payload', None)
        self.payload_ascii = kwargs.get('payload_ascii', None)
        self.payload_hex = kwargs.get('payload_hex', None)
        self.proto = kwargs.get('proto', None)
        self.references = kwargs.get('references', None)
        self.rev = kwargs.get('rev', None)
        self.rule = kwargs.get('rule', None)
        self.rule_set = kwargs.get('rule_set', None)
        self.severity = kwargs.get('severity', None)
        self.sid = kwargs.get('sid', None)
        self.signature = kwargs.get('signature', None)
        self.src_ip = kwargs.get('src_ip', None)
        self.src_port = kwargs.get('src_port', None)

class AlertSchema(Schema):
    id = fields.Int(as_string=True)
    idx = fields.Int(as_string=True)
    created = DateTime()
    updated = DateTime()

    seq = fields.Int(as_string=True)
    loop = fields.Int(as_string=True)
    test_name = fields.Str()
    test_description = fields.Str()

    category = fields.Str()
    description = fields.Str(missing=None)
    dest_ip = fields.Str()
    dest_port = fields.Int(as_string=True, missing=None)
    interface = fields.Str()
    payload = fields.Str(missing=None)
    payload_ascii = fields.Str(missing=None)
    payload_hex = fields.Str(missing=None)
    proto = fields.Str()
    references = fields.List(fields.Str(), missing=None)
    rev = fields.Int(as_string=True)
    rule = fields.Str()
    rule_set = fields.Str()
    severity = fields.Int(as_string=True)
    sid = fields.Int(as_string=True)
    signature = fields.Str()
    src_ip = fields.Str()
    src_port = fields.Int(as_string=True, missing=None)

    @post_load
    def post_load(self, data):
        return Alert(**data)

class SeverityCount(object):
    """Model for CDRouter Severity Counts.

    :param name: (optional) Severity name as a string.
    :param severity: (optional) Severity as an int.
    :param count: (optional) Count as an int.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.severity = kwargs.get('severity', None)
        self.count = kwargs.get('count', None)

class SeverityCountSchema(Schema):
    name = fields.Str()
    severity = fields.Int(as_string=True)
    count = fields.Int(as_string=True)

    @post_load
    def post_load(self, data):
        return SeverityCount(**data)

class CategoryCount(object):
    """Model for CDRouter Category Counts.

    :param category: (optional) Category name as a string.
    :param severity: (optional) Severity as an int.
    :param count: (optional) Count as an int.
    """
    def __init__(self, **kwargs):
        self.category = kwargs.get('category', None)
        self.severity = kwargs.get('severity', None)
        self.count = kwargs.get('count', None)

class CategoryCountSchema(Schema):
    category = fields.Str()
    severity = fields.Int(as_string=True)
    count = fields.Int(as_string=True)

    @post_load
    def post_load(self, data):
        return CategoryCount(**data)

class RuleSetCount(object):
    """Model for CDRouter RuleSet Counts.

    :param name: (optional) RuleSet name as a string.
    :param count: (optional) Count as an int.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.count = kwargs.get('count', None)

class RuleSetCountSchema(Schema):
    name = fields.Str()
    count = fields.Int(as_string=True)

    @post_load
    def post_load(self, data):
        return RuleSetCount(**data)

class SignatureCount(object):
    """Model for CDRouter Signature Counts.

    :param signature: (optional) Signature name as a string.
    :param severity: (optional) Severity as an int.
    :param count: (optional) Count as an int.
    """
    def __init__(self, **kwargs):
        self.signature = kwargs.get('signature', None)
        self.severity = kwargs.get('severity', None)
        self.count = kwargs.get('count', None)

class SignatureCountSchema(Schema):
    signature = fields.Str()
    severity = fields.Int(as_string=True)
    count = fields.Int(as_string=True)

    @post_load
    def post_load(self, data):
        return SignatureCount(**data)

class TestCount(object):
    """Model for CDRouter Test Counts.

    :param name: (optional) Test name as a string.
    :param count: (optional) Count as an int.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.count = kwargs.get('count', None)

class TestCountSchema(Schema):
    name = fields.Str()
    count = fields.Int(as_string=True)

    @post_load
    def post_load(self, data):
        return TestCount(**data)

class AddrCount(object):
    """Model for CDRouter Addr Counts.

    :param addr: (optional) Address as a string.
    :param count: (optional) Count as an int.
    """
    def __init__(self, **kwargs):
        self.addr = kwargs.get('addr', None)
        self.count = kwargs.get('count', None)

class AddrCountSchema(Schema):
    addr = fields.Str()
    count = fields.Int(as_string=True)

    @post_load
    def post_load(self, data):
        return AddrCount(**data)

class AllStats(object):
    """Model for CDRouter All Alerts Stats.

    :param severities: (optional) Dict of ints to :class:`alerts.SeverityCount <alerts.SeverityCount>`
    :param categories: (optional) :class:`alerts.CategoryCount <alerts.CategoryCount>` list
    :param rule_sets: (optional) :class:`alerts.RuleSetCount <alerts.RuleSetCount>` list
    :param signatures: (optional) :class:`alerts.SignatureCount <alerts.SignatureCount>` list
    :param tests: (optional) :class:`alerts.TestCount <alerts.TestCount>` list
    :param frequent_sources: (optional) :class:`alerts.AddrCount <alerts.AddrCount>` list
    :param frequent_destinations: (optional) :class:`alerts.AddrCount <alerts.AddrCount>` list
    """
    def __init__(self, **kwargs):
        self.severities = kwargs.get('severities', None)
        self.categories = kwargs.get('categories', None)
        self.rule_sets = kwargs.get('rule_sets', None)
        self.signatures = kwargs.get('signatures', None)
        self.tests = kwargs.get('tests', None)
        self.frequent_sources = kwargs.get('frequent_sources', None)
        self.frequent_destinations = kwargs.get('frequent_destinations', None)

class AllStatsSchema(Schema):
    severities = DictField(fields.Int(), SeverityCountSchema())
    categories = fields.Nested(CategoryCountSchema, many=True)
    rule_sets = fields.Nested(RuleSetCountSchema, many=True)
    signatures = fields.Nested(SignatureCountSchema, many=True)
    tests = fields.Nested(TestCountSchema, many=True)
    frequent_sources = fields.Nested(AddrCountSchema, many=True)
    frequent_destinations = fields.Nested(AddrCountSchema, many=True)

    @post_load
    def post_load(self, data):
        return AllStats(**data)

class Page(collections.namedtuple('Page', ['data', 'links'])):
    """Named tuple for a page of list response data.

    :param data: :class:`alerts.Alert <alerts.Alert>` list
    :param links: :class:`cdrouter.Links <cdrouter.Links>` object
    """

class AlertsService(object):
    """Service for accessing CDRouter Alerts."""

    RESOURCE = 'alerts'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id): # pylint: disable=invalid-name,redefined-builtin
        return 'results/'+str(id)+self.BASE

    def list(self, id, filter=None, type=None, sort=None, limit=None, page=None, detailed=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of alerts.

        :param id: Result ID as an int.
        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`alerts.Page <alerts.Page>` object
        """
        schema = AlertSchema()
        if not detailed:
            schema = AlertSchema(exclude=('id', 'payload', 'payload_ascii', 'payload_hex', 'references'))
        resp = self.service.list(self._base(id), filter, type, sort, limit, page, detailed=detailed)
        trs, l =self.service.decode(schema, resp, many=True, links=True)
        return Page(trs, l)

    def iter_list(self, id, *args, **kwargs):
        """Get a list of alerts.  Whereas ``list`` fetches a single
        page of alerts according to its ``limit`` and ``page``
        arguments, ``iter_list`` returns all alerts by internally
        making successive calls to ``list``.

        :param id: Result ID as an int.
        :param args: Arguments that ``list`` takes.
        :param kwargs: Optional arguments that ``list`` takes.
        :return: :class:`alerts.Alert <alerts.Alert>` list

        """
        l = partial(self.list, id)
        return self.service.iter_list(l, *args, **kwargs)

    def get(self, id, idx): # pylint: disable=invalid-name,redefined-builtin
        """Get an alert.

        :param id: Result ID as an int.
        :param idx: Alert index as an int.
        :return: :class:`alerts.Alert <alerts.Alert>` object
        :rtype: alerts.Alert
        """
        schema = AlertSchema()
        resp = self.service.get_id(self._base(id), idx)
        return self.service.decode(schema, resp)

    def all_stats(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Compute alert stats for a single result.

        :param id: Result ID as an int.
        :return: :class:`alerts.AllStats <alerts.AllStats>` object
        :rtype: alerts.AllStats
        """
        schema = AllStatsSchema()
        resp = self.service.post(self._base(id), params={'stats': 'all'})
        return self.service.decode(schema, resp)
