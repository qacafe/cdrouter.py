#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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

class Auth(requests.auth.AuthBase): # pylint: disable=too-few-public-methods
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['authorization'] = 'Bearer ' + self.token
        return r

class Service(object):
    BASE = '/api/v1'

    def __init__(self, base, token, insecure=False):
        self.base = base.rstrip('/')+self.BASE
        self.token = token
        self.insecure = insecure

        if insecure:
            # disable annoying InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # base request methods
    def _req(self, path, method='GET', json=None, data=None, params=None, headers=None, files=None):
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        if files is None:
            files = {}
        headers.update({'user-agent': 'cdrouter.py https://github.com/qacafe/cdrouter.py'})
        return requests.request(method, self.base+path, params=params, headers=headers, files=files,
                                json=json, data=data, verify=(not self.insecure), auth=Auth(self.token))

    def _get(self, path, params=None):
        return self._req(path, method='GET', params=params)

    def _post(self, path, json=None, data=None, params=None, files=None):
        return self._req(path, method='POST', json=json, data=data, params=params, files=files)

    def _patch(self, path, json):
        return self._req(path, method='PATCH', json=json)

    def _delete(self, path, params=None):
        return self._req(path, method='DELETE', params=params)

    # cdrouter-specific request methods
    def list(self, base, filter=None, sort=None, limit=None, page=None, format=None): # pylint: disable=redefined-builtin
        return self._get(base, params={'filter': filter, 'sort': sort, 'limit':
                                       limit, 'page': page, 'format': format})

    def get(self, base, id, params=None): # pylint: disable=invalid-name,redefined-builtin
        return self._get(base+str(id)+'/', params=params)

    def create(self, base, resource):
        return self._post(base, json=resource)

    def edit(self, base, id, resource): # pylint: disable=invalid-name,redefined-builtin
        return self._patch(base+str(id)+'/', json=resource)

    def delete(self, base, id): # pylint: disable=invalid-name,redefined-builtin
        return self._delete(base+str(id)+'/')

    def get_shares(self, base, id): # pylint: disable=invalid-name,redefined-builtin
        return self._get(base+str(id)+'/shares/')

    def edit_shares(self, base, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        return self._patch(base+str(id)+'/shares/', json={'user_ids': map(int, user_ids)})

    def export(self, base, id, format='gz', params=None): # pylint: disable=invalid-name,redefined-builtin
        params.update({'format': format})
        return self._get(base+str(id)+'/', params=params)

    def bulk_export(self, base, ids, params=None):
        if params is None:
            params = {}
        params.update({'bulk': 'export', 'ids': map(str, ids)})
        return self._get(base, params=params)

    def bulk_copy(self, base, resource, ids):
        return self._post(base, params={'bulk': 'copy'},
                          json={resource: [{'id': str(x)} for x in ids]})

    def bulk_edit(self, base, resource, fields, ids=None, filter=None, all=False, testvars=None): # pylint: disable=redefined-builtin
        json = {'fields': fields}
        if ids != None or testvars != None:
            if ids != None:
                json[resource] = [{'id': str(x)} for x in ids]
            if testvars != None:
                json['testvars'] = testvars

        return self._post(base, params={'bulk': 'edit', 'filter': filter, 'all': all}, json=json)

    def bulk_delete(self, base, resource, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        json = None
        if ids != None:
            json = {resource: [{'id': str(x)} for x in ids]}
        return self._post(base, params={'bulk': 'delete', 'filter': filter, 'all': all}, json=json)

    # resource service methods
    def configs(self):
        return ConfigsService(self)

    def devices(self):
        return DevicesService(self)

    def jobs(self):
        return JobsService(self)

    def packages(self):
        return PackagesService(self)

    def results(self):
        return ResultsService(self)

    def tests(self):
        return TestResultsService(self)

    def annotations(self):
        return AnnotationsService(self)

    def captures(self):
        return CapturesService(self)

    def highlights(self):
        return HighlightsService(self)

    def imports(self):
        return ImportsService(self)

    def exports(self):
        return ExportsService(self)

    def history(self):
        return HistoryService(self)

    def system(self):
        return SystemService(self)

    def tags(self):
        return TagsService(self)

    def testsuites(self):
        return TestsuitesService(self)

    def users(self):
        return UsersService(self)
