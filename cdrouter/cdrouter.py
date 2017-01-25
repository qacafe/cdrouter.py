#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

import io
import os
import re
import requests
from requests_toolbelt.downloadutils import stream
from requests_toolbelt import sessions
from requests_toolbelt.utils.user_agent import user_agent
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from marshmallow import Schema, fields, post_load

from . import __version__
from .cdr_datetime import DateTime
from .configs import ConfigsService
from .devices import DevicesService
from .attachments import AttachmentsService
from .jobs import JobsService
from .packages import PackagesService
from .results import ResultsService
from .testresults import TestResultsService
from .annotations import AnnotationsService
from .captures import CapturesService
from .highlights import HighlightsService
from .imports import ImportsService
from .exports import ExportsService
from .history import HistoryService
from .system import SystemService
from .tags import TagsService
from .testsuites import TestsuitesService
from .users import UsersService

class Links(object):
    def __init__(self, **kwargs):
        self.first = kwargs.get('first', None)
        self.last = kwargs.get('last', None)
        self.current = kwargs.get('current', None)
        self.total = kwargs.get('total', None)
        self.limit = kwargs.get('limit', None)
        self.next = kwargs.get('next', None)
        self.prev = kwargs.get('prev', None)

class LinksSchema(Schema):
    first = fields.Int()
    last = fields.Int()
    current = fields.Int()
    total = fields.Int()
    limit = fields.Int()
    next = fields.Int(missing=None)
    prev = fields.Int(missing=None)

    @post_load
    def post_load(self, data):
        return Links(**data)

class Response(object):
    def __init__(self, **kwargs):
        self.timestamp = kwargs.get('timestamp', None)
        self.error = kwargs.get('error', None)
        self.data = kwargs.get('data', None)
        self.links = kwargs.get('links', None)

class ResponseSchema(Schema):
    timestamp = DateTime()
    error = fields.Str(missing=None)
    data = fields.Dict(missing=None)

    @post_load
    def post_load(self, data):
        return Response(**data)

class ListResponseSchema(ResponseSchema):
    data = fields.List(fields.Dict(), missing=None)
    links = fields.Nested(LinksSchema, missing=None)

    @post_load
    def post_load(self, data):
        return Response(**data)

class Share(object):
    """Model for CDRouter Shares.

    :param user_id: (optional) User ID as string.
    :param read: (optional) Bool `True` if reading is allowed.
    :param write: (optional) Bool `True` if writing is allowed.
    :param execute: (optional) Bool `True` if executing is allowed.
    """
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id', None)
        self.read = kwargs.get('read', None)
        self.write = kwargs.get('write', None)
        self.execute = kwargs.get('execute', None)

class ShareSchema(Schema):
    user_id = fields.Str()
    read = fields.Bool()
    write = fields.Bool()
    execute = fields.Bool()

    @post_load
    def post_load(self, data):
        return Share(**data)

class CDRouterError(BaseException):
    def __init__(self, message, response):
        self.message = message
        self.response = response

    def __str__(self):
        return self.message

class Auth(requests.auth.AuthBase): # pylint: disable=too-few-public-methods
    """Class for authorizing CDRouter Web API requests."""

    def __init__(self, token=None):
        self.token = token

    def __call__(self, r):
        if self.token != None:
            r.headers['authorization'] = 'Bearer ' + self.token
        return r

class CDRouter(object):
    """Service for accessing the CDRouter Web API."""
    BASE = '/api/v1/'

    def __init__(self, base, token=None, insecure=False):
        self.base = base.rstrip('/')+self.BASE
        self.token = token
        if self.token is None:
            self.token = os.environ.get('CDROUTER_API_TOKEN')
        self.insecure = insecure

        if insecure:
            # disable annoying InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self.session = sessions.BaseUrlSession(base_url=base+self.BASE)

        #: :class:`configs.ConfigsService <configs.ConfigsService>` object
        self.configs = ConfigsService(self)
        #: :class:`devices.DevicesService <devices.DevicesService>` object
        self.devices = DevicesService(self)
        #: :class:`attachments.AttachmentsService <attachments.AttachmentsService>` object
        self.attachments = AttachmentsService(self)
        #: :class:`jobs.JobsService <jobs.JobsService>` object
        self.jobs = JobsService(self)
        #: :class:`packages.PackagesService <packages.PackagesService>` object
        self.packages = PackagesService(self)
        #: :class:`results.ResultsService <results.ResultsService>` object
        self.results = ResultsService(self)
        #: :class:`testresults.TestResultsService <testresults.TestResultsService>` object
        self.tests = TestResultsService(self)
        #: :class:`annotations.AnnotationsService <annotations.AnnotationsService>` object
        self.annotations = AnnotationsService(self)
        #: :class:`captures.CapturesService <captures.CapturesService>` object
        self.captures = CapturesService(self)
        #: :class:`highlights.HighlightsService <highlights.HighlightsService>` object
        self.highlights = HighlightsService(self)
        #: :class:`imports.ImportsService <imports.ImportsService>` object
        self.imports = ImportsService(self)
        #: :class:`exports.ExportsService <exports.ExportsService>` object
        self.exports = ExportsService(self)
        #: :class:`history.HistoryService <history.HistoryService>` object
        self.history = HistoryService(self)
        #: :class:`system.SystemService <system.SystemService>` object
        self.system = SystemService(self)
        #: :class:`tags.TagsService <tags.TagsService>` object
        self.tags = TagsService(self)
        #: :class:`testsuites.TestsuitesService <testsuites.TestsuitesService>` object
        self.testsuites = TestsuitesService(self)
        #: :class:`users.UsersService <users.UsersService>` object
        self.users = UsersService(self)

    # base request methods
    def _req(self, path, method='GET', json=None, data=None, params=None, headers=None, files=None, stream=None):
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        if files is None:
            files = {}
            headers.update({'user-agent': user_agent('cdrouter.py', __version__)})
        return self.session.request(method, path, params=params, headers=headers, files=files, stream=stream,
                                    json=json, data=data, verify=(not self.insecure), auth=Auth(token=self.token))

    def get(self, path, params=None, stream=None):
        return self._req(path, method='GET', params=params, stream=stream)

    def post(self, path, json=None, data=None, params=None, files=None, stream=None):
        return self._req(path, method='POST', json=json, data=data, params=params, stream=stream, files=files)

    def patch(self, path, json, params=None):
        return self._req(path, method='PATCH', json=json, params=params)

    def delete(self, path, params=None):
        return self._req(path, method='DELETE', params=params)

    # cdrouter-specific request methods
    def list(self, base, filter=None, type=None, sort=None, limit=None, page=None, format=None): # pylint: disable=redefined-builtin
        if sort != None:
            if not isinstance(sort, list):
                sort = [sort]
            sort = ','.join(sort)
        return self.get(base, params={'filter': filter, 'type': type, 'sort': sort, 'limit': limit,
                                      'page': page, 'format': format})

    def get_id(self, base, id, params=None): # pylint: disable=invalid-name,redefined-builtin
        return self.get(base+str(id)+'/', params=params)

    def create(self, base, resource):
        return self.post(base, json=resource)

    def edit(self, base, id, resource): # pylint: disable=invalid-name,redefined-builtin
        return self.patch(base+str(id)+'/', json=resource)

    def delete_id(self, base, id): # pylint: disable=invalid-name,redefined-builtin
        return self.delete(base+str(id)+'/')

    def get_shares(self, base, id): # pylint: disable=invalid-name,redefined-builtin
        schema = ShareSchema()
        resp = self.get(base+str(id)+'/shares/')
        return self.decode(schema, resp, many=True)

    def edit_shares(self, base, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        schema = ShareSchema()
        resp = self.patch(base+str(id)+'/shares/', json={'user_ids': map(int, user_ids)})
        return self.decode(schema, resp, many=True)

    def filename(self, resp, filename=None):
        if 'content-disposition' in resp.headers:
            m = re.search('filename="([^"]+)"', resp.headers['content-disposition'])
            if m is not None:
                filename = m.group(1)
        return filename

    def export(self, base, id, format='gz', params=None): # pylint: disable=invalid-name,redefined-builtin
        if params is None:
            params = {}
        params.update({'format': format})
        resp = self.get(base+str(id)+'/', params=params, stream=True)
        resp.raise_for_status()
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        b.seek(0)
        return (b, self.filename(resp))

    def bulk_export(self, base, ids, params=None):
        if params is None:
            params = {}
        params.update({'bulk': 'export', 'ids': map(str, ids)})
        resp = self.get(base, params=params, stream=True)
        resp.raise_for_status()
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        b.seek(0)
        return (b, self.filename(resp))

    def bulk_copy(self, base, resource, ids, schema):
        resp = self.post(base, params={'bulk': 'copy'},
                         json={resource: [{'id': str(x)} for x in ids]})
        return self.decode(schema, resp, many=True)

    def bulk_edit(self, base, resource, fields, ids=None, filter=None, type=None, all=False, testvars=None): # pylint: disable=redefined-builtin
        json = {'fields': fields}
        if ids != None or testvars != None:
            if ids != None:
                json[resource] = [{'id': str(x)} for x in ids]
            if testvars != None:
                json['testvars'] = testvars

        return self.post(base, params={'bulk': 'edit', 'filter': filter, 'type': type, 'all': all}, json=json)

    def bulk_delete(self, base, resource, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        json = None
        if ids != None:
            json = {resource: [{'id': str(x)} for x in ids]}
        return self.post(base, params={'bulk': 'delete', 'filter': filter, 'type': type, 'all': all}, json=json)

    def decode(self, schema, resp, many=None, links=False):
        json = resp.json()
        resp_schema = ResponseSchema()
        if many is True:
            resp_schema = ListResponseSchema()

        result = resp_schema.load(json).data

        if 400 <= resp.status_code < 600 and result.error is not None:
                raise CDRouterError(result.error, resp)

        resp.raise_for_status()

        if result.data is None:
            raise CDRouterError('no data field in JSON response!', resp)

        data = schema.load(result.data, many=many).data

        if many is True and links is True and result.links is not None:
            return (data, result.links)

        return data

    def encode(self, schema, resource, many=None):
        result = schema.dump(resource, many=many)
        return result.data
