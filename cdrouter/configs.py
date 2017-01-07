#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

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
