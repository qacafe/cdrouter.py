#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

import os.path
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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

class Configs:
    RESOURCE = 'configs'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base, filter, sort, limit, page)

    def get_new(self):
        return self.service._get(self.base, params={'template': 'default'})

    def get(self, id, format=None):
        return self.service.get(self.base, id, params={'format': format})

    def get_plaintext(self, id):
        return self.get(id, format='text')

    def create(self, resource):
        return self.service.create(self.base, resource)

    def edit(self, resource):
        return self.service.edit(self.base, resource['id'], resource)

    def delete(self, id):
        return self.service.delete(self.base, id)

    def get_shares(self, id):
        return self.service.shares(self.base, id)

    def edit_shares(self, id, user_ids):
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id):
        return self.service.export(self.base, id)

    def check_config(self, contents):
        return self.service._post(self.base, params={'process': 'check'}, json={'contents': contents})

    def upgrade_config(self, contents):
        return self.service._post(self.base, params={'process': 'upgrade'}, json={'contents': contents})

    def get_networks(self, contents):
        return self.service._post(self.base, params={'process': 'networks'}, json={'contents': contents})

    def bulk_export(self, ids):
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        return self.service.bulk_copy(self.base, self.RESOURCE, ids)

    def bulk_edit(self, fields, ids=None, filter=None, all=False, testvars=None):
        return self.service.bulk_edit(self.base, self.RESOURCE, fields, ids=ids, filter=filter, all=all, testvars=testvars)

    def bulk_delete(self, ids=None, filter=None, all=False):
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)

    def list_testvars(self, id):
        return self.service._get(self.base+str(id)+'/testvars/')

    def get_testvar(self, id, name, group=None):
        return self.service._get(self.base+str(id)+'/testvars/'+name+'/', params={'group': group})

    def edit_testvar(self, id, name, value, group=None):
        return self.service._patch(self.base+str(id)+'/testvars/'+name+'/', params={'group': group}, json={'value': value})

    def delete_testvar(self, id, name, group=None):
        return self.service._delete(self.base+str(id)+'/testvars/'+name+'/', params={'group': group})

    def bulk_edit_testvars(self, id, testvars):
        return self.service._post(self.base+str(id)+'/testvars/', params={'bulk': 'edit'}, json=testvars)

class Devices:
    RESOURCE = 'devices'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base, filter, sort, limit, page)

    def get(self, id):
        return self.service.get(self.base, id)

    def create(self, resource):
        return self.service.create(self.base, resource)

    def edit(self, resource):
        return self.service.edit(self.base, resource['id'], resource)

    def delete(self, id):
        return self.service.delete(self.base, id)

    def get_shares(self, id):
        return self.service.shares(self.base, id)

    def edit_shares(self, id, user_ids):
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id):
        return self.service.export(self.base, id)

    def bulk_export(self, ids):
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        return self.service.bulk_copy(self.base, self.RESOURCE, ids)

    def bulk_edit(self, fields, ids=None, filter=None, all=False):
        return self.service.bulk_edit(self.base, self.RESOURCE, fields, ids=ids, filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False):
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)

    def list_attachments(self, id, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base+str(id)+'/attachments/', filter, sort, limit, page)

    def get_attachment(self, id, attid):
        return self.service._get(self.base+str(id)+'/attachments/'+str(attid)+'/')

    def create_attachment(self, id, filepath):
        return self.service._post(self.base+str(id)+'/attachments/'+str(attid)+'/', files={'file': (os.path.basename(filepath), open(filepath, 'rb'))})

    def download_attachment(self, id, attid):
        return self.service._get(self.base+str(id)+'/attachments/'+str(attid)+'/', params={'format': 'download'})

    def download_thumbnail(self, id, attid, size=None):
        return self.service._get(self.base+str(id)+'/attachments/'+str(attid)+'/', params={'format': 'thumbnail', 'size': size})

    def edit_attachment(self, id, attid, resource):
        return self.service._patch(self.base+str(id)+'/attachments/'+str(attid)+'/', json=resource)

    def delete_attachment(self, id, attid):
        return self.service._delete(self.base+str(id)+'/attachments/'+str(attid)+'/')

class Jobs:
    RESOURCE = 'jobs'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base, filter, sort, limit, page)

    def get(self, id):
        return self.service.get(self.base, id)

    def launch(self, resource):
        return self.service.create(self.base, resource)

    def delete(self, id):
        return self.service.delete(self.base, id)

    def package_id(id):
        if isinstance(id, (str, int)):
            return {'package_id': str(id)}
        return id

    def bulk_launch(self, package_ids=None, filter=None, all=False):
        json = None
        if package_ids != None:
            json = {self.RESOURCE: map(self.package_id, package_ids)}
        return self.service._post(self.base, params={'bulk': 'launch', 'filter': filter, 'all': all}, json=json)

    def bulk_delete(self, ids=None, filter=None, all=False):
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)

class Packages:
    RESOURCE = 'packages'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base, filter, sort, limit, page)

    def get(self, id):
        return self.service.get(self.base, id)

    def create(self, resource):
        return self.service.create(self.base, resource)

    def edit(self, resource):
        return self.service.edit(self.base, resource['id'], resource)

    def delete(self, id):
        return self.service.delete(self.base, id)

    def get_shares(self, id):
        return self.service.shares(self.base, id)

    def edit_shares(self, id, user_ids):
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id):
        return self.service.export(self.base, id)

    def bulk_export(self, ids):
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        return self.service.bulk_copy(self.base, self.RESOURCE, ids)

    def bulk_edit(self, fields, ids=None, filter=None, all=False):
        return self.service.bulk_edit(self.base, self.RESOURCE, fields, ids=ids, filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False):
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)

class Results:
    RESOURCE = 'results'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base, filter, sort, limit, page)

    def list_csv(self, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base, filter, sort, limit, page, format='csv')

    def get(self, id):
        return self.service.get(self.base, id)

    def stop(self, id, when=None):
        return self.service._post(self.base+str(id)+'/stop/', params={'when': when})

    def stop_end_of_test(self, id):
        return self.stop(id, 'end-of-test')

    def stop_end_of_loop(self, id):
        return self.stop(id, 'end-of-loop')

    def pause(self, id, when=None):
        return self.service._post(self.base+str(id)+'/pause/', params={'when': when})

    def pause_end_of_test(self, id):
        return self.pause(id, 'end-of-test')

    def pause_end_of_loop(self, id):
        return self.pause(id, 'end-of-loop')

    def unpause(self, id):
        return self.service._post(self.base+str(id)+'/unpause/')

    def edit(self, resource):
        return self.service.edit(self.base, resource['id'], resource)

    def delete(self, id):
        return self.service.delete(self.base, id)

    def get_shares(self, id):
        return self.service.shares(self.base, id)

    def edit_shares(self, id, user_ids):
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id, exclude_captures=False):
        return self.service.export(self.base, id, params={'exclude_captures': exclude_captures})

    def bulk_export(self, ids, exclude_captures=False):
        return self.service.bulk_export(self.base, ids, params={'exclude_captures': exclude_captures})

    def bulk_copy(self, ids):
        return self.service.bulk_copy(self.base, self.RESOURCE, ids)

    def bulk_edit(self, fields, ids=None, filter=None, all=False):
        return self.service.bulk_edit(self.base, self.RESOURCE, fields, ids=ids, filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False):
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)

    def all_stats(self):
        return self.service._post(self.base, params={'stats': 'all'})

    def set_stats(self, ids):
        return self.service._post(self.base, params={'stats': 'set'}, json=map(lambda x: {'id': str(x)}, ids))

    def single_stats(self, id):
        return self.service._get(self.base+str(id)+'/', params={'stats': 'all'})

    def list_logdir(self, id, filter=None, sort=None):
        return self.service.list(self.base+str(id)+'/logdir/', filter, sort)

    def get_logdir_file(self, id, filename):
        return self.service._get(self.base+str(id)+'/logdir/'+filename+'/')

    def download_logdir_archive(self, id, format='zip', exclude_captures=False):
        return self.service._get(self.base+str(id)+'/logdir/'+filename+'/', params={'format': format, 'exclude_captures': exclude_captures})

    def get_test_metric(self, id, name, metric, format=None):
        return self.service._get(self.base+str(id)+'/metrics/'+name+'/'+metric+'/', params={'format': format})

    def get_test_metric_csv(self, id, name, metric):
        return self.get_test_metric_csv(id, name, metric, format='csv')

class TestResults:
    RESOURCE = 'tests'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service, id):
        self.service = service
        self.base = '/results/'+str(id)+self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base, filter, sort, limit, page)

    def list_csv(self, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base, filter, sort, limit, page, format='csv')

    def get(self, seq):
        return self.service.get(self.base, seq)

    def edit(self, resource):
        return self.service.edit(self.base, resource['seq'], resource)

    def get_log(self, seq, offset=None, limit=None, filter=None, packets=None, timestamp_offset=None, format=None):
        return self.service._get(self.base+str(seq)+'/log/', params={'offset': offset, 'limit': limit, 'filter': filter, 'packets':
                                                                     packets, 'timestamp_offset': timestamp_offset, 'format': format})

    def get_log_plaintext(self, seq):
        return self.get_log(seq, format='text')

class Annotations:
    RESOURCE = 'annotations'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service, id, seq):
        self.service = service
        self.base = '/results/'+str(id)+'/tests/'+str(seq)+self.BASE

    def list(self):
        return self.service.list(self.base, filter, sort, limit, page)

    def get(self, line):
        return self.service.get(self.base, line)

    def create_or_edit(self, resource):
        return self.service.edit(self.base, resource['line'], resource)

    def delete(self, line):
        return self.service.delete(self.base, line)

class Captures:
    RESOURCE = 'captures'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service, id, seq):
        self.service = service
        self.base = '/results/'+str(id)+'/tests/'+str(seq)+self.BASE

    def list(self):
        return self.service.list(self.base, filter, sort, limit, page)

    def get(self, intf):
        return self.service.get(self.base, intf)

    def download(self, intf, inline=False):
        return self.service.get(self.base, intf, params={'format': format, 'inline': inline})

    def summary(self, intf, filter=None, inline=False):
        return self.service._get(self.base+str(intf)+'/summary/', params={'filter': filter, 'inline': inline})

    def decode(self, intf, filter=None, frame=None, inline=False):
        return self.service._get(self.base+str(intf)+'/decode/', params={'filter': filter, 'frame': frame, 'inline': inline})

    def ascii(self, intf, filter=None, frame=None, inline=False):
        return self.service._get(self.base+str(intf)+'/ascii/', params={'filter': filter, 'frame': frame, 'inline': inline})

    def send_to_cloudshark(self, intf, inline=False):
        return self.service._post(self.base+str(intf)+'/cloudshark/', params={'inline': inline})

class Highlights:
    RESOURCE = 'highlights'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service, id, seq):
        self.service = service
        self.base = '/results/'+str(id)+'/tests/'+str(seq)+self.BASE

    def list(self):
        return self.service.list(self.base, filter, sort, limit, page)

    def get(self, line):
        return self.service.get(self.base, line)

    def create_or_edit(self, resource):
        return self.service.edit(self.base, resource['line'], resource)

    def delete(self, line):
        return self.service.delete(self.base, line)

class Imports:
    RESOURCE = 'imports'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self):
        return self.service.list(self.base)

    def stage_import_from_file(self, filepath):
        return self.service._post(self.base, files={'file': (os.path.basename(filepath), open(filepath, 'rb'))})

    def stage_import_from_filesystem(self, filepath):
        return self.service._post(self.base, params={'path': filepath})

    def stage_import_from_url(self, url, token=None, insecure=False):
        return self.service._post(self.base, params={'url': url, 'token': token, 'insecure': insecure})

    def get(self, id):
        return self.service.get(self.base, id)

    def get_commit_request(self, id):
        return self.service._get(self.base+str(id)+'/request/')

    def commit(self, id, commit_request):
        return self.service._post(self.base+str(id)+'/commit/', json=commit_request)

    def delete(self, id):
        return self.service.delete(self.base, id)

class Exports:
    RESOURCE = 'exports'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def bulk_export(self, config_ids=[], device_ids=[], package_ids=[], result_ids=[], exclude_captures=False):
        json={
            'configs': map(int, config_ids),
            'devices': map(int, device_ids),
            'packages': map(int, package_ids),
            'results': map(int, result_ids),
            'options': { 'exclude_captures': exclude_captures }
        }
        return self.service._post(self.base, json=json)

class History:
    RESOURCE = 'history'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base, filter, sort, limit, page)

class System:
    RESOURCE = 'system'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def latest_lounge_release(self):
        return self.service._get(self.base+'lounge/latest/')

    def check_for_lounge_upgrade(self, email, password):
        return self.service._post(self.base+'lounge/check/', json={'email': email, 'password': password})

    def lounge_upgrade(self, email, password, release_id):
        return self.service._post(self.base+'lounge/upgrade/', json={'email': email, 'password': password, 'release': { 'id': int(release_id) } })

    def manual_upgrade(self, filepath):
        return self.service._post(self.base+'upgrade/', files={'file': (os.path.basename(filepath), open(filepath, 'rb'))})

    def restart(self):
        return self.service._post(self.base+'restart/')

    def time(self):
        return self.service._post(self.base+'time/')

    def hostname(self):
        return self.service._post(self.base+'hostname/')

    def interfaces(self, addresses=False):
        return self.service._post(self.base+'interfaces/', params={'addresses': addresses})

    def get_preferences(self):
        return self.service._get(self.base+'preferences/')

    def edit_preferences(self, resource):
        return self.service._patch(self.base+'preferences/', json=resource)

class Tags:
    RESOURCE = 'tags'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, resource=None, sort=None):
        return self.service._get(self.base, params={'resource': resource, 'sort': sort})

    def get(self, name):
        return self.service.get(self.base, name)

    def edit(self, resource):
        return self.service.edit(self.base, resource['name'], resource)

    def delete(self, name):
        return self.service.delete(self.base, name)

class Testsuites:
    RESOURCE = 'testsuites'
    BASE = '/' + RESOURCE + '/1/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def info(self):
        return self.service._get(self.base)

    def search(self, query):
        return self.service._get(self.base+'search/', params={'q': query})

    def list_groups(self, filter=None, sort=None):
        return self.service.list(self.base+'groups/', filter, sort)

    def get_group(self, name):
        return self.service._get(self.base+'groups/'+name+'/')

    def list_modules(self, filter=None, sort=None):
        return self.service.list(self.base+'modules/', filter, sort)

    def get_module(self, name):
        return self.service._get(self.base+'modules/'+name+'/')

    def list_tests(self, filter=None, sort=None):
        return self.service.list(self.base+'tests/', filter, sort)

    def get_test(self, name):
        return self.service._get(self.base+'tests/'+name+'/')

    def list_labels(self, filter=None, sort=None):
        return self.service.list(self.base+'labels/', filter, sort)

    def get_label(self, name):
        return self.service._get(self.base+'labels/'+name+'/')

    def list_errors(self, filter=None, sort=None):
        return self.service.list(self.base+'errors/', filter, sort)

    def get_error(self, name):
        return self.service._get(self.base+'errors/'+name+'/')

    def list_testvars(self, filter=None, sort=None):
        return self.service.list(self.base+'testvars/', filter, sort)

    def get_testvar(self, name):
        return self.service._get(self.base+'testvars/'+name+'/')

class Users:
    RESOURCE = 'users'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base, filter, sort, limit, page)

    def get(self, id):
        return self.service.get(self.base, id)

    def create(self, resource):
        return self.service.create(self.base, resource)

    def edit(self, resource):
        return self.service.edit(self.base, resource['id'], resource)

    def change_password(self, id, new, old=None, change_token=True):
        return self.service._post(self.base+str(id)+'/password/', params={'change_token', change_token},
                                  json={'old': old, 'new': new, 'new_confirm': new})

    def change_token(self, id):
        return self.service._post(self.base+str(id)+'/token/')

    def delete(self, id):
        return self.service.delete(self.base, id)

    def bulk_copy(self, ids):
        return self.service.bulk_copy(self.base, self.RESOURCE, ids)

    def bulk_edit(self, fields, ids=None, filter=None, all=False):
        return self.service.bulk_edit(self.base, self.RESOURCE, fields, ids=ids, filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False):
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)
