#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

class TestResults(object):
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
        return self.service._get(self.base+str(seq)+'/log/',
                                 params={'offset': offset, 'limit': limit, 'filter': filter, 'packets':
                                         packets, 'timestamp_offset': timestamp_offset, 'format': format})

    def get_log_plaintext(self, seq):
        return self.get_log(seq, format='text')
