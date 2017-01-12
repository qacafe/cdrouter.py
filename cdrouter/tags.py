#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Tags."""

from marshmallow import Schema, fields, post_load

class ResourceTags(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.tags = kwargs.get('tags', None)

class Tag(object):
    def __init__(self, **kwargs):
        self.resource = kwargs.get('resource', None)
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.count = kwargs.get('count', None)
        self.tags = kwargs.get('tags', None)

        self.configs = kwargs.get('configs', None)
        self.devices = kwargs.get('devices', None)
        self.packages = kwargs.get('packages', None)
        self.results = kwargs.get('results', None)

class ResourceTagsSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    tags = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return ResourceTags(**data)

class TagSchema(Schema):
    resource = fields.Str()
    id = fields.Str()
    name = fields.Str()
    count = fields.Int()
    tags = fields.List(fields.Str())

    configs = fields.Nested(ResourceTagsSchema, many=True)
    devices = fields.Nested(ResourceTagsSchema, many=True)
    packages = fields.Nested(ResourceTagsSchema, many=True)
    results = fields.Nested(ResourceTagsSchema, many=True)

    @post_load
    def post_load(self, data):
        return Tag(**data)

class TagsService(object):
    """Service for accessing CDRouter Tags."""

    RESOURCE = 'tags'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, resource=None, sort=None):
        """Get a list of tags."""
        schema = TagSchema()
        resp = self.service.get(self.base, params={'resource': resource, 'sort': sort})
        return self.service.decode(schema, resp, many=True)

    def get(self, name):
        """Get a tag."""
        schema = TagSchema()
        resp = self.service.get_id(self.base, name)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a tag."""
        schema = TagSchema(only=('name', 'configs', 'devices', 'packages', 'results'))
        json = self.service.encode(schema, resource)

        schema = TagSchema()
        resp = self.service.edit(self.base, resource.name, json)
        return self.service.decode(schema, resp)

    def delete(self, name):
        """Delete a tag."""
        return self.service.delete_id(self.base, name)
