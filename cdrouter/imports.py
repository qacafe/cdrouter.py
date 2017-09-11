#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Imports."""

import os.path
from marshmallow import Schema, fields, post_load
from .cdr_datetime import DateTime
from .cdr_dictfield import DictField

class Import(object):
    """Model for CDRouter Staged Imports.

    :param id: (optional) Staged import ID as an int.
    :param user_id: (optional) User ID as an int.
    :param created: (optional) Creation time as `DateTime`.
    :param updated: (optional) Last-updated time as `DateTime`.
    :param archive: (optional) Path to archive as string.
    :param path: (optional) Local filepath as string.
    :param url: (optional) URL to fetch as string.
    :param insecure: (optional) Allow insecure HTTPS connections if bool `True`.
    :param size: (optional) Size of import as int.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.user_id = kwargs.get('user_id', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)
        self.archive = kwargs.get('archive', None)
        self.path = kwargs.get('path', None)
        self.url = kwargs.get('url', None)
        self.insecure = kwargs.get('insecure', None)
        self.size = kwargs.get('size', None)

class ImportSchema(Schema):
    id = fields.Int(as_string=True)
    user_id = fields.Int(as_string=True)
    created = DateTime()
    updated = DateTime()
    archive = fields.Str()
    path = fields.Str()
    url = fields.Str()
    insecure = fields.Bool()
    size = fields.Int()

    @post_load
    def post_load(self, data):
        return Import(**data)

class Response(object):
    """Model for CDRouter Import Responses.

    :param imported: (optional) Bool `True` if resource imported successfully.
    :param id: (optional) Resource ID as an int.
    :param name: (optional) Resource name as string.
    :param message: (optional) Response message as string.
    """
    def __init__(self, **kwargs):
        self.imported = kwargs.get('imported', None)
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.message = kwargs.get('message', None)

class ResponseSchema(Schema):
    imported = fields.Bool()
    id = fields.Int(as_string=True, missing=None)
    name = fields.Str(missing=None)
    message = fields.Str(missing=None)

    @post_load
    def post_load(self, data):
        return Response(**data)

class Resource(object):
    """Model for CDRouter Import Resources.

    :param name: (optional) Set to string to rename resource, leave empty to keep original
    :param should_import: (optional) Bool `True` if resource should be imported.
    :param existing_id: (optional) Contains ID as an int of existing resource which will be overwritten if `should_import` is `True`.
    :param response: (optional) :class:`imports.Response <imports.Response>` object
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.should_import = kwargs.get('should_import', None)
        self.existing_id = kwargs.get('existing_id', None)
        self.response = kwargs.get('response', None)

class ResourceSchema(Schema):
    name = fields.Str(missing=None)
    should_import = fields.Bool(attribute='should_import', load_from='import', dump_to='import')
    existing_id = fields.Int(as_string=True, missing=None)
    response = fields.Nested(ResponseSchema, missing=None)

    @post_load
    def post_load(self, data):
        return Resource(**data)

class Request(object):
    """Model for CDRouter Import Requests.

    :param replace_existing: (optional) Bool `True` if existing resources should be overwritten.
    :param configs: (optional) Dict of strings to :class:`imports.Resource <imports.Resource>` objects.
    :param devices: (optional) Dict of strings to :class:`imports.Resource <imports.Resource>` objects.
    :param packages: (optional) Dict of strings to :class:`imports.Resource <imports.Resource>` objects.
    :param results: (optional) Dict of strings to :class:`imports.Resource <imports.Resource>` objects.
    :param tags: (optional) Tags to add to imported resources as string list.
    """
    def __init__(self, **kwargs):
        self.replace_existing = kwargs.get('replace_existing', None)

        self.configs = kwargs.get('configs', None)
        self.devices = kwargs.get('devices', None)
        self.packages = kwargs.get('packages', None)
        self.results = kwargs.get('results', None)

        self.tags = kwargs.get('tags', None)

class RequestSchema(Schema):
    replace_existing = fields.Bool()

    configs = DictField(fields.Str(), ResourceSchema())
    devices = DictField(fields.Str(), ResourceSchema())
    packages = DictField(fields.Str(), ResourceSchema())
    results = DictField(fields.Str(), ResourceSchema())

    tags = fields.List(fields.Str(), missing=None)

    @post_load
    def post_load(self, data):
        return Request(**data)

class ImportsService(object):
    """Service for accessing CDRouter Imports."""

    RESOURCE = 'imports'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self):
        """Get a list of staged (in-progress) imports.

        :return: :class:`imports.Import <imports.Import>` list
        """
        schema = ImportSchema()
        resp = self.service.list(self.base)
        return self.service.decode(schema, resp, many=True)

    def stage_import_from_file(self, fd, filename='upload.gz'):
        """Stage an import from a file upload.

        :param fd: File-like object to upload.
        :param filename: (optional) Filename to use for import as string.
        :return: :class:`imports.Import <imports.Import>` object
        """
        schema = ImportSchema()
        resp = self.service.post(self.base,
                                 files={'file': (filename, fd)})
        return self.service.decode(schema, resp)

    def stage_import_from_filesystem(self, filepath):
        """Stage an import from a filesystem path.

        :param filepath: Local filesystem path as string.
        :return: :class:`imports.Import <imports.Import>` object
        """
        schema = ImportSchema()
        resp = self.service.post(self.base,
                                 params={'path': filepath})
        return self.service.decode(schema, resp)

    def stage_import_from_url(self, url, token=None, username=None, password=None, insecure=False):
        """Stage an import from a URL to another CDRouter system.

        :param url: URL to import as string.
        :param token: (optional) API token to use as string (may be required if importing from a CDRouter 10+ system).
        :param username: (optional) API username to use as string (may be required if importing from a CDRouter 10+ system).
        :param password: (optional) API password to use as string (may be required if importing from a CDRouter 10+ system).
        :param insecure: (optional) Allow insecure HTTPS connections if bool `True`.
        :return: :class:`imports.Import <imports.Import>` object
        """
        schema = ImportSchema()
        resp = self.service.post(self.base,
                                 params={'url': url, 'token': token, 'username': username, 'password': password, 'insecure': insecure})
        return self.service.decode(schema, resp)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a staged import.

        :param id: Staged import ID as an int.
        :return: :class:`imports.Import <imports.Import>` object
        :rtype: imports.Import
        """
        schema = ImportSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def get_commit_request(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a commit request for a staged import.

        :param id: Staged import ID as an int.
        :return: :class:`imports.Request <imports.Request>` object
        :rtype: imports.Request
        """
        schema = RequestSchema()
        resp = self.service.get(self.base+str(id)+'/request/')
        return self.service.decode(schema, resp)

    def commit(self, id, impreq): # pylint: disable=invalid-name,redefined-builtin
        """Commit a staged import.

        :param id: Staged import ID as an int.
        :param impreq: :class:`imports.Request <imports.Request>` object
        :return: :class:`imports.Request <imports.Request>` object
        :rtype: imports.Request
        """
        schema = RequestSchema()
        json = self.service.encode(schema, impreq)

        schema = RequestSchema()
        resp = self.service.post(self.base+str(id)+'/', json=json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a staged import.

        :param id: Staged import ID as an int.
        """
        return self.service.delete_id(self.base, id)
