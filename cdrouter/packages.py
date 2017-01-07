#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

class Packages(object):
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
        return self.service.bulk_edit(self.base, self.RESOURCE,
                                      fields, ids=ids, filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False):
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)
