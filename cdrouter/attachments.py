#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

import os.path

from marshmallow import Schema, fields, post_load

class Attachment(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)
        self.size = kwargs.get('size', None)
        self.path = kwargs.get('path', None)
        self.device_id = kwargs.get('device_id', None)

class AttachmentSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    created = fields.DateTime()
    updated = fields.DateTime()
    size = fields.Int()
    path = fields.Str()
    device_id = fields.Str()

    @post_load
    def post_load(self, data):
        return Attachment(**data)

class AttachmentsService(object):
    RESOURCE = 'attachments'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id): # pylint: disable=invalid-name,redefined-builtin
        return '/devices/'+str(id)+self.BASE

    def list(self, id, filter=None, sort=None, limit=None, page=None): # pylint: disable=invalid-name,redefined-builtin
        schema = AttachmentSchema(exclude=('path'))
        resp = self.service.list(self._base(id), filter, sort, limit, page)
        return self.service.decode(schema, resp, many=True)

    def get(self, id, attid): # pylint: disable=invalid-name,redefined-builtin
        schema = AttachmentSchema()
        resp = self.service.get_id(self._base(id), attid)
        return self.service.decode(schema, resp)

    def create(self, id, filepath): # pylint: disable=invalid-name,redefined-builtin
        schema = AttachmentSchema()
        resp = self.service.post(self._base(id),
                                 files={'file': (os.path.basename(filepath), open(filepath, 'rb'))})
        return self.service.decode(schema, resp)

    def download(self, id, attid): # pylint: disable=invalid-name,redefined-builtin
        return self.service.get_id(self._base(id), attid, params={'format': 'download'})

    def thumbnail(self, id, attid, size=None): # pylint: disable=invalid-name,redefined-builtin
        return self.service.get_id(self._base(id), attid, params={'format': 'thumbnail', 'size': size})

    def edit(self, id, resource): # pylint: disable=invalid-name,redefined-builtin
        schema = AttachmentSchema(exclude=('id', 'created', 'updated', 'size', 'path', 'device_id'))
        json = self.service.encode(schema, resource)

        schema = AttachmentSchema()
        resp = self.service.edit(self._base(id), resource.id, json)
        return self.service.decode(schema, resp)

    def delete(self, id, attid): # pylint: disable=invalid-name,redefined-builtin
        return self.service.edit(self._base(id), attid)
