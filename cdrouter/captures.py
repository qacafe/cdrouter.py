#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

class Captures(object):
    RESOURCE = 'captures'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service, id, seq):
        self.service = service
        self.base = '/results/'+str(id)+'/tests/'+str(seq)+self.BASE

    def list(self):
        return self.service.list(self.base, filter)

    def get(self, intf):
        return self.service.get(self.base, intf)

    def download(self, intf, inline=False):
        return self.service.get(self.base, intf, params={'format': format, 'inline': inline})

    def summary(self, intf, filter=None, inline=False):
        return self.service._get(self.base+str(intf)+'/summary/',
                                 params={'filter': filter, 'inline': inline})

    def decode(self, intf, filter=None, frame=None, inline=False):
        return self.service._get(self.base+str(intf)+'/decode/',
                                 params={'filter': filter, 'frame': frame, 'inline': inline})

    def ascii(self, intf, filter=None, frame=None, inline=False):
        return self.service._get(self.base+str(intf)+'/ascii/',
                                 params={'filter': filter, 'frame': frame, 'inline': inline})

    def send_to_cloudshark(self, intf, inline=False):
        return self.service._post(self.base+str(intf)+'/cloudshark/', params={'inline': inline})
