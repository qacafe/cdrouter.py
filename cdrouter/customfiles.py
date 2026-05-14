#
# Copyright (c) 2026 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Custom Files."""

import io

from marshmallow import Schema, fields, post_load, EXCLUDE
from requests_toolbelt.downloadutils import stream

from .cdr_datetime import DateTime

class FileInfo(object):
    """Model for CDRouter Custom Directory entries.

    :param name: (optional) File or directory name as string.
    :param path: (optional) Path relative to custom directory as string.
    :param size: (optional) Size in bytes as int.
    :param modified: (optional) Last modified time as `DateTime`.
    :param is_dir: (optional) Bool `True` if entry is a directory.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.path = kwargs.get('path', None)
        self.size = kwargs.get('size', None)
        self.modified = kwargs.get('modified', None)
        self.is_dir = kwargs.get('is_dir', None)

class FileInfoSchema(Schema):
    name = fields.Str()
    path = fields.Str()
    size = fields.Int()
    modified = DateTime()
    is_dir = fields.Bool()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return FileInfo(**data)

class CustomFilesService(object):
    """Service for accessing CDRouter Custom Files."""

    RESOURCE = 'system'
    BASE = RESOURCE + '/custom/files/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def get(self, path):
        """Get info for a file under /usr/cdrouter-data/custom/.

        :param path: Path to file relative to custom directory as string.
        :return: :class:`customfiles.FileInfo <customfiles.FileInfo>` object
        :rtype: customfiles.FileInfo
        """
        schema = FileInfoSchema()
        resp = self.service.get(self.base, params={'path': path})
        return self.service.decode(schema, resp)

    def list(self, path):
        """Get a directory listing under /usr/cdrouter-data/custom/.

        :param path: Path to directory relative to custom directory as string.
        :return: :class:`customfiles.FileInfo <customfiles.FileInfo>` list
        """
        schema = FileInfoSchema()
        resp = self.service.get(self.base, params={'path': path})
        return self.service.decode(schema, resp, many=True)

    def download(self, path):
        """Download a file from /usr/cdrouter-data/custom/.

        :param path: Path to file relative to custom directory as string.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        resp = self.service.get(self.base+'download', params={'path': path}, stream=True)
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        resp.close()
        b.seek(0)
        return (b, self.service.filename(resp))

    def upload(self, path, fd, filename='upload'):
        """Upload a file to a directory under /usr/cdrouter-data/custom/.

        :param path: Path to destination directory relative to custom directory as string.
        :param fd: File-like object to upload.
        :param filename: (optional) Filename to use for uploaded file as string.
        :return: :class:`customfiles.FileInfo <customfiles.FileInfo>` object
        :rtype: customfiles.FileInfo
        """
        schema = FileInfoSchema()
        resp = self.service.post(self.base+'upload', params={'path': path}, files={'file': (filename, fd)})
        return self.service.decode(schema, resp)

    def mkdir(self, path):
        """Create a directory under /usr/cdrouter-data/custom/.

        :param path: Path for new directory relative to custom directory as string.
        :return: :class:`customfiles.FileInfo <customfiles.FileInfo>` object
        :rtype: customfiles.FileInfo
        """
        schema = FileInfoSchema()
        resp = self.service.post(self.base+'mkdir', params={'path': path})
        return self.service.decode(schema, resp)

    def rename(self, path, name):
        """Rename a file or directory under /usr/cdrouter-data/custom/.

        :param path: Path to file or directory relative to custom directory as string.
        :param name: New filename as string (no path separators allowed).
        :return: :class:`customfiles.FileInfo <customfiles.FileInfo>` object
        :rtype: customfiles.FileInfo
        """
        schema = FileInfoSchema()
        resp = self.service.post(self.base+'rename', params={'path': path, 'name': name})
        return self.service.decode(schema, resp)

    def delete(self, path, recursive=False):
        """Delete a file or directory from /usr/cdrouter-data/custom/.

        :param path: Path to file or directory relative to custom directory as string.
        :param recursive: (optional) If bool `True`, delete non-empty directories recursively.
        """
        return self.service.post(self.base+'delete', params={'path': path, 'recursive': recursive})
