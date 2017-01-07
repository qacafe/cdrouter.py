#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

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
