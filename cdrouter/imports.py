#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Imports."""

import os.path
from marshmallow import Schema, fields, post_load
from .cdr_datetime import DateTime

class Import(object):
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
    id = fields.Str()
    user_id = fields.Str()
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
    def __init__(self, **kwargs):
        self.imported = kwargs.get('imported', None)
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.message = kwargs.get('message', None)

class ResponseSchema(Schema):
    imported = fields.Bool()
    id = fields.Str(missing=None)
    name = fields.Str(missing=None)
    message = fields.Str(missing=None)

    @post_load
    def post_load(self, data):
        return Response(**data)

class Request(object):
    def __init__(self, **kwargs):
        self.replace_existing = kwargs.get('replace_existing', None)

        self.configs = kwargs.get('configs', None)
        self.devices = kwargs.get('devices', None)
        self.packages = kwargs.get('packages', None)
        self.results = kwargs.get('results', None)

        self.tags = kwargs.get('tags', None)

class RequestSchema(Schema):
    replace_existing = fields.Bool()

    configs = fields.Dict()
    devices = fields.Dict()
    packages = fields.Dict()
    results = fields.Dict()

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
        """Get a list of staged (in-progress) imports."""
        schema = ImportSchema()
        resp = self.service.list(self.base)
        return self.service.decode(schema, resp, many=True)

    def stage_import_from_file(self, filepath):
        """Stage an import from a file upload."""
        schema = ImportSchema()
        resp = self.service.post(self.base,
                                 files={'file': (os.path.basename(filepath), open(filepath, 'rb'))})
        return self.service.decode(schema, resp)

    def stage_import_from_filesystem(self, filepath):
        """Stage an import from a filesystem path."""
        schema = ImportSchema()
        resp = self.service.post(self.base,
                                 params={'path': filepath})
        return self.service.decode(schema, resp)

    def stage_import_from_url(self, url, token=None, insecure=False):
        """Stage an import from a URL to another CDRouter system."""
        schema = ImportSchema()
        resp = self.service.post(self.base,
                                 params={'url': url, 'token': token, 'insecure': insecure})
        return self.service.decode(schema, resp)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a staged import."""
        schema = ImportSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def get_commit_request(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a commit request for a staged import."""
        schema = RequestSchema()
        resp = self.service.get(self.base+str(id)+'/request/')
        return self.service.decode(schema, resp)

    def commit(self, id, impreq): # pylint: disable=invalid-name,redefined-builtin
        """Commit a staged import."""
        schema = RequestSchema()
        json = self.service.encode(schema, impreq)

        schema = RequestSchema()
        resp = self.service.post(self.base+str(id)+'/', json=json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a staged import."""
        return self.service.delete_id(self.base, id)
