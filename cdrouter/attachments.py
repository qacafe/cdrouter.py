#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

import os.path

class AttachmentsService(object):
    RESOURCE = 'attachments'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id): # pylint: disable=invalid-name,redefined-builtin
        return '/devices/'+str(id)+self.BASE

    def list(self, id, filter=None, sort=None, limit=None, page=None): # pylint: disable=invalid-name,redefined-builtin
        return self.service.list(self._base(id), filter, sort, limit, page)

    def get(self, id, attid): # pylint: disable=invalid-name,redefined-builtin
        return self.service.get_id(self._base(id), attid)

    def create(self, id, filepath): # pylint: disable=invalid-name,redefined-builtin
        return self.service.post(self._base(id),
                                 files={'file': (os.path.basename(filepath), open(filepath, 'rb'))})

    def download(self, id, attid): # pylint: disable=invalid-name,redefined-builtin
        return self.service.get_id(self._base(id), attid, params={'format': 'download'})

    def thumbnail(self, id, attid, size=None): # pylint: disable=invalid-name,redefined-builtin
        return self.service.get_id(self._base(id), attid, params={'format': 'thumbnail', 'size': size})

    def edit(self, id, resource): # pylint: disable=invalid-name,redefined-builtin
        return self.service.edit(self._base(id), resource['id'], resource)

    def delete(self, id, attid): # pylint: disable=invalid-name,redefined-builtin
        return self.service.edit(self._base(id), attid)
