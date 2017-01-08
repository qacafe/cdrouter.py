#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

class TagsService(object):
    RESOURCE = 'tags'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, resource=None, sort=None):
        return self.service.get(self.base, params={'resource': resource, 'sort': sort})

    def get(self, name):
        return self.service.get_id(self.base, name)

    def edit(self, resource):
        return self.service.edit(self.base, resource['name'], resource)

    def delete(self, name):
        return self.service.delete_id(self.base, name)
