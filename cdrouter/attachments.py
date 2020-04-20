#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

import collections
from functools import partial
import io
import os.path

from requests_toolbelt.downloadutils import stream
from marshmallow import Schema, fields, post_load
from .cdr_datetime import DateTime

class Attachment(object):
    """Model for CDRouter Attachments.

    :param id: (optional) Attachment ID as an int.
    :param name: (optional) Name as string.
    :param description: (optional) Description as string.
    :param created: (optional) Creation time as `DateTime`.
    :param updated: (optional) Last-updated time as `DateTime`.
    :param size: (optional) Attachment size as an int.
    :param path: (optional) Filepath to attachment as string.
    :param device_id: (optional) Device ID as an int.
    """
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
    id = fields.Int(as_string=True)
    name = fields.Str()
    description = fields.Str()
    created = DateTime()
    updated = DateTime()
    size = fields.Int()
    path = fields.Str()
    device_id = fields.Int(as_string=True)

    @post_load
    def post_load(self, data):
        return Attachment(**data)

class Page(collections.namedtuple('Page', ['data', 'links'])):
    """Named tuple for a page of list response data.

    :param data: :class:`attachments.Attachment <attachments.Attachment>` list
    :param links: :class:`cdrouter.Links <cdrouter.Links>` object
    """

class AttachmentsService(object):
    RESOURCE = 'attachments'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id): # pylint: disable=invalid-name,redefined-builtin
        return 'devices/'+str(id)+'/'+self.BASE

    def list(self, id, filter=None, type=None, sort=None, limit=None, page=None, detailed=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of a device's attachments.

        :param id: Device ID as an int.
        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`attachments.Page <attachments.Page>` object
        """
        schema = AttachmentSchema()
        if not detailed:
            schema = AttachmentSchema(exclude=('path'))
        resp = self.service.list(self._base(id), filter, type, sort, limit, page, detailed=detailed)
        at, l = self.service.decode(schema, resp, many=True, links=True)
        return Page(at, l)

    def iter_list(self, id, *args, **kwargs):
        """Get a list of attachments.  Whereas ``list`` fetches a single page
        of attachments according to its ``limit`` and ``page``
        arguments, ``iter_list`` returns all attachments by internally
        making successive calls to ``list``.

        :param id: Device ID as an int.
        :param args: Arguments that ``list`` takes.
        :param kwargs: Optional arguments that ``list`` takes.
        :return: :class:`attachments.Attachment <attachments.Attachment>` list

        """
        l = partial(self.list, id)
        return self.service.iter_list(l, *args, **kwargs)

    def get(self, id, attid): # pylint: disable=invalid-name,redefined-builtin
        """Get a device's attachment.

        :param id: Device ID as an int.
        :param attid: Attachment ID as an int.
        :return: :class:`attachments.Attachment <attachments.Attachment>` object
        :rtype: attachments.Attachment
        """
        schema = AttachmentSchema()
        resp = self.service.get_id(self._base(id), attid)
        return self.service.decode(schema, resp)

    def create(self, id, fd, filename='attachment-name'): # pylint: disable=invalid-name,redefined-builtin
        """Add an attachment to a device.

        :param id: Device ID as an int.
        :param fd: File-like object to upload.
        :param filename: (optional) Name to use for new attachment as a string.
        :return: :class:`attachments.Attachment <attachments.Attachment>` object
        :rtype: attachments.Attachment
        """
        schema = AttachmentSchema(exclude=('id', 'created', 'updated', 'size', 'path', 'device_id'))
        resp = self.service.post(self._base(id),
                                 files={'file': (filename, fd)})
        return self.service.decode(schema, resp)

    def download(self, id, attid): # pylint: disable=invalid-name,redefined-builtin
        """Download a device's attachment.

        :param id: Device ID as an int.
        :param attid: Attachment ID as an int.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        resp = self.service.get_id(self._base(id), attid, params={'format': 'download'}, stream=True)
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        resp.close()
        b.seek(0)
        return (b, self.service.filename(resp))

    def thumbnail(self, id, attid, size=None): # pylint: disable=invalid-name,redefined-builtin
        """Download thumbnail of a device's attachment.  Attachment must be a
        GIF, JPEG or PNG image.

        :param id: Device ID as an int.
        :param attid: Attachment ID as an int.
        :param size: (optional) Height in pixels of generated thumbnail.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """

        resp = self.service.get_id(self._base(id), attid, params={'format': 'thumbnail', 'size': size}, stream=True)
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        resp.close()
        b.seek(0)
        return (b, self.service.filename(resp))

    def edit(self, resource): # pylint: disable=invalid-name,redefined-builtin
        """Edit a device's attachment.

        :param resource: :class:`attachments.Attachment <attachments.Attachment>` object
        :return: :class:`attachments.Attachment <attachments.Attachment>` object
        :rtype: attachments.Attachment
        """
        schema = AttachmentSchema(exclude=('id', 'created', 'updated', 'size', 'path', 'device_id'))
        json = self.service.encode(schema, resource)

        schema = AttachmentSchema()
        resp = self.service.edit(self._base(resource.device_id), resource.id, json)
        return self.service.decode(schema, resp)

    def delete(self, id, attid): # pylint: disable=invalid-name,redefined-builtin
        """Delete a device's attachment.

        :param id: Device ID as an int.
        :param attid: Attachment ID as an int.
        """
        return self.service.edit(self._base(id), attid)
