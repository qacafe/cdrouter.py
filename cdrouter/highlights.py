#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

class Highlights(object):
    RESOURCE = 'highlights'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service, id, seq):
        self.service = service
        self.base = '/results/'+str(id)+'/tests/'+str(seq)+self.BASE

    def list(self):
        return self.service.list(self.base, filter)

    def get(self, line):
        return self.service.get(self.base, line)

    def create_or_edit(self, resource):
        return self.service.edit(self.base, resource['line'], resource)

    def delete(self, line):
        return self.service.delete(self.base, line)
