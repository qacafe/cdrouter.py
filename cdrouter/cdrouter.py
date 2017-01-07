#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .configs import Configs
from .devices import Devices
from .jobs import Jobs
from .packages import Packages
from .results import Results
from .testresults import TestResults
from .annotations import Annotations
from .captures import Captures
from .highlights import Highlights
from .imports import Imports
from .exports import Exports
from .history import History
from .system import System
from .tags import Tags
from .testsuites import Testsuites
from .users import Users

class Auth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['authorization'] = 'Bearer ' + self.token
        return r

class Service:
    BASE = '/api/v1'

    def __init__(self, base, token, insecure=False):
        self.base = base.rstrip('/')+self.BASE
        self.token = token
        self.insecure = insecure

        if insecure:
            # disable annoying InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # base request methods
    def _req(self, path, method='GET', json=None, data=None, params={}, headers={}, files={}):
        headers.update({'user-agent': 'cdrouter.py https://github.com/qacafe/cdrouter.py'})
        return requests.request(method, self.base+path, params=params, headers=headers, files=files,
                                json=json, data=data, verify=(not self.insecure), auth=Auth(self.token))

    def _get(self, path, params={}):
        return self._req(path, method='GET', params=params)

    def _post(self, path, json=None, data=None, params={}, files={}):
        return self._req(path, method='POST', json=json, data=data, params=params, files=files)

    def _patch(self, path, json):
        return self._req(path, method='PATCH', json=json)

    def _delete(self, path, params={}):
        return self._req(path, method='DELETE', params=params)

    # cdrouter-specific request methods
    def list(self, base, filter=None, sort=None, limit=None, page=None, format=None):
        return self._get(base, params={'filter': filter, 'sort': sort, 'limit': limit, 'page': page, 'format': format})

    def get(self, base, id, params={}):
        return self._get(base+str(id)+'/', params=params)

    def create(self, base, resource):
        return self._post(base, json=resource)

    def edit(self, base, id, resource):
        return self._patch(base+str(id)+'/', json=resource)

    def delete(self, base, id):
        return self._delete(base+str(id)+'/')

    def get_shares(self, base, id):
        return self._get(base+str(id)+'/shares/')

    def edit_shares(self, base, id, user_ids):
        return self._patch(base+str(id)+'/shares/', json={'user_ids': map(int, user_ids)})

    def export(self, base, id, format='gz', params={}):
        params.update({'format': format})
        return self._get(base+str(id)+'/', params=params)

    def bulk_export(self, base, ids, params={}):
        params.update({'bulk': 'export', 'ids': map(str, ids)})
        return self._get(base, params=params)

    def bulk_copy(self, base, resource, ids):
        return self._post(base, params={'bulk': 'copy'}, json={resource: map(lambda x: {'id': str(x)}, ids)})

    def bulk_edit(self, base, resource, fields, ids=None, filter=None, all=False, testvars=None):
        json = None
        if ids != None or testvars != None:
            json = {}
            if ids != None:
                json['resource'] = map(lambda x: {'id': str(x)}, ids)
            if testvars != None:
                json['testvars'] = testvars

        return self._post(base, params={'bulk': 'edit', 'filter': filter, 'all': all}, json=json)

    def bulk_delete(self, base, resource, ids=None, filter=None, all=False):
        json=None
        if ids != None: json={resource: map(lambda x: {'id': str(x)}, ids)}
        return self._post(base, params={'bulk': 'delete', 'filter': filter, 'all': all}, json=json)

    # resource service methods
    def configs(self):
        return Configs(self)

    def devices(self):
        return Devices(self)

    def jobs(self):
        return Jobs(self)

    def packages(self):
        return Packages(self)

    def results(self):
        return Results(self)

    def tests(self, id):
        return TestResults(self, id)

    def annotations(self, id, seq):
        return Annotations(self, id, seq)

    def captures(self, id, seq):
        return Captures(self, id, seq)

    def highlights(self, id, seq):
        return Highlights(self, id, seq)

    def imports(self):
        return Imports(self)

    def exports(self):
        return Exports(self)

    def history(self):
        return History(self)

    def system(self):
        return System(self)

    def tags(self):
        return Tags(self)

    def testsuites(self):
        return Testsuites(self)

    def users(self):
        return Users(self)
