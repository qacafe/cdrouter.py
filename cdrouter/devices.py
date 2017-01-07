#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

import os.path

class Devices(object):
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
        return self.service.bulk_edit(self.base, self.RESOURCE, fields, ids=ids,
                                      filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False):
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids,
                                        filter=filter, all=all)

    def list_attachments(self, id, filter=None, sort=None, limit=None, page=None):
        return self.service.list(self.base+str(id)+'/attachments/', filter, sort, limit, page)

    def get_attachment(self, id, attid):
        return self.service._get(self.base+str(id)+'/attachments/'+str(attid)+'/')

    def create_attachment(self, id, filepath):
        return self.service._post(self.base+str(id)+'/attachments/',
                                  files={'file': (os.path.basename(filepath), open(filepath, 'rb'))})

    def download_attachment(self, id, attid):
        return self.service._get(self.base+str(id)+'/attachments/'+str(attid)+'/',
                                 params={'format': 'download'})

    def download_thumbnail(self, id, attid, size=None):
        return self.service._get(self.base+str(id)+'/attachments/'+str(attid)+'/',
                                 params={'format': 'thumbnail', 'size': size})

    def edit_attachment(self, id, attid, resource):
        return self.service._patch(self.base+str(id)+'/attachments/'+str(attid)+'/', json=resource)

    def delete_attachment(self, id, attid):
        return self.service._delete(self.base+str(id)+'/attachments/'+str(attid)+'/')
