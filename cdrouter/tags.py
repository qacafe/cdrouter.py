#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Tags."""

from marshmallow import Schema, fields, post_load

class ResourceTags(object):
    """Model for CDRouter Resource Tags.

    :param id: (optional) Resource ID as an int.
    :param name: (optional) Resource name as string.
    :param tags: (optional) Resource tags as a string list.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.tags = kwargs.get('tags', None)

class ResourceTagsSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    tags = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return ResourceTags(**data)

class Tag(object):
    """Model for CDRouter Tags.

    :param resource: (optional) Resource type as string.
    :param id: (optional) Resource ID as an int.
    :param name: (optional) Resource name as string.
    :param count: (optional) Resource tag count as an int.
    :param tags: (optional) Resource tags as a string list.
    :param configs: (optional) :class:`tags.ResourceTags <tags.ResourceTags>` list
    :param devices: (optional) :class:`tags.ResourceTags <tags.ResourceTags>` list
    :param packages: (optional) :class:`tags.ResourceTags <tags.ResourceTags>` list
    :param results: (optional) :class:`tags.ResourceTags <tags.ResourceTags>` list
    """
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

class TagSchema(Schema):
    resource = fields.Str()
    id = fields.Int(as_string=True)
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
        """Get a list of tags.

        :param resource: (optional) Restrict to given resource type as string.
        :param sort: (optional) Sort fields to apply as string list.
        :return: :class:`tags.Tag <tags.Tag>` list
        """
        schema = TagSchema()
        resp = self.service.get(self.base, params={'resource': resource, 'sort': sort})
        return self.service.decode(schema, resp, many=True)

    def get(self, name):
        """Get a tag.

        :param name: Tag name as string.
        :return: :class:`tags.Tag <tags.Tag>` object
        :rtype: tags.Tag
        """
        schema = TagSchema()
        resp = self.service.get_id(self.base, name)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a tag.

        :param resource: :class:`tags.Tag <tags.Tag>` object
        :return: :class:`tags.Tag <tags.Tag>` object
        :rtype: tags.Tag
        """
        schema = TagSchema(only=('name', 'configs', 'devices', 'packages', 'results'))
        json = self.service.encode(schema, resource)

        schema = TagSchema()
        resp = self.service.edit(self.base, resource.name, json)
        return self.service.decode(schema, resp)

    def delete(self, name):
        """Delete a tag.

        :param name: Tag name as string.
        """
        return self.service.delete_id(self.base, name)
