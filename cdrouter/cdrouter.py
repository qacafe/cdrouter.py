#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

import io
import re
import requests
from requests_toolbelt.downloadutils import stream
from requests_toolbelt import sessions
from requests_toolbelt.utils.user_agent import user_agent
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from marshmallow import Schema, fields, post_load

from . import __version__
from .configs import ConfigsService
from .devices import DevicesService
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

class Share(object):
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
        self.insecure = insecure

        if insecure:
            # disable annoying InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self.session = sessions.BaseUrlSession(base_url=base+self.BASE)

        # resource-specific services
        self.configs = ConfigsService(self)
        self.devices = DevicesService(self)
        self.jobs = JobsService(self)
        self.packages = PackagesService(self)
        self.results = ResultsService(self)
        self.tests = TestResultsService(self)
        self.annotations = AnnotationsService(self)
        self.captures = CapturesService(self)
        self.highlights = HighlightsService(self)
        self.imports = ImportsService(self)
        self.exports = ExportsService(self)
        self.history = HistoryService(self)
        self.system = SystemService(self)
        self.tags = TagsService(self)
        self.testsuites = TestsuitesService(self)
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
        """Send an authorized GET request."""
        return self._req(path, method='GET', params=params, stream=None)

    def post(self, path, json=None, data=None, params=None, files=None):
        """Send an authorized POST request."""
        return self._req(path, method='POST', json=json, data=data, params=params, files=files)

    def patch(self, path, json, params=None):
        """Send an authorized PATCH request."""
        return self._req(path, method='PATCH', json=json, params=params)

    def delete(self, path, params=None):
        """Send an authorized DELETE request."""
        return self._req(path, method='DELETE', params=params)

    # cdrouter-specific request methods
    def list(self, base, filter=None, sort=None, limit=None, page=None, format=None): # pylint: disable=redefined-builtin
        """Send an authorized GET request for a collection."""
        if sort != None:
            sort = ','.join(sort)
        return self.get(base, params={'filter': filter, 'sort': sort, 'limit': limit,
                                      'page': page, 'format': format})

    def get_id(self, base, id, params=None): # pylint: disable=invalid-name,redefined-builtin
        """Send an authorized GET request to get a resource by ID."""
        return self.get(base+str(id)+'/', params=params)

    def create(self, base, resource):
        """Send an authorized POST request to create a new resource."""
        return self.post(base, json=resource)

    def edit(self, base, id, resource): # pylint: disable=invalid-name,redefined-builtin
        """Send an authorized PATCH request to edit a resource."""
        return self.patch(base+str(id)+'/', json=resource)

    def delete_id(self, base, id): # pylint: disable=invalid-name,redefined-builtin
        """Send an authorized DELETE request to delete a resource by ID."""
        return self.delete(base+str(id)+'/')

    def get_shares(self, base, id): # pylint: disable=invalid-name,redefined-builtin
        """Send an authorized GET request to get a resource's shares."""
        schema = ShareSchema()
        resp = self.get(base+str(id)+'/shares/')
        return self.decode(schema, resp, many=True)

    def edit_shares(self, base, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Send an authorized PATCH request to edit a resource's shares."""
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
        """Send an authorized GET request to export a resource."""
        if params is None:
            params = {}
        params.update({'format': format})
        resp = self.get(base+str(id)+'/', params=params, stream=True)
        resp.raise_for_status()
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        return (b, self.filename(resp))

    def bulk_export(self, base, ids, params=None):
        """Send an authorized GET request to bulk export a set of resources."""
        if params is None:
            params = {}
        params.update({'bulk': 'export', 'ids': map(str, ids)})
        resp = self.get(base, params=params, stream=True)
        resp.raise_for_status()
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        return (b, self.filename(resp))

    def bulk_copy(self, base, resource, ids, schema):
        """Send an authorized POST request to bulk copy a set of resources."""
        resp = self.post(base, params={'bulk': 'copy'},
                         json={resource: [{'id': str(x)} for x in ids]})
        return self.decode(schema, resp, many=True)

    def bulk_edit(self, base, resource, fields, ids=None, filter=None, all=False, testvars=None): # pylint: disable=redefined-builtin
        """Send an authorized POST request to bulk edit a set of resources."""
        json = {'fields': fields}
        if ids != None or testvars != None:
            if ids != None:
                json[resource] = [{'id': str(x)} for x in ids]
            if testvars != None:
                json['testvars'] = testvars

        return self.post(base, params={'bulk': 'edit', 'filter': filter, 'all': all}, json=json)

    def bulk_delete(self, base, resource, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Send an authorized POST request to bulk delete a set of resources."""
        json = None
        if ids != None:
            json = {resource: [{'id': str(x)} for x in ids]}
        return self.post(base, params={'bulk': 'delete', 'filter': filter, 'all': all}, json=json)

    def decode(self, schema, resp, many=None):
        resp.raise_for_status()
        json = resp.json()
        if 'error' in json:
            raise BaseException(json['error'])
        if 'data' not in json:
            raise BaseException('no data field in JSON response!')
        result = schema.load(json['data'], many=many)
        return result.data

    def encode(self, schema, resource, many=None):
        result = schema.dump(resource, many=many)
        return result.data
