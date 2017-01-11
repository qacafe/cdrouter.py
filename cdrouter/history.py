#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter History."""

from marshmallow import Schema, fields, post_load

class History(object):
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id', None)
        self.created = kwargs.get('created', None)
        self.resource = kwargs.get('resource', None)
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.action = kwargs.get('action', None)
        self.description = kwargs.get('description', None)

class HistorySchema(Schema):
    user_id = fields.Str()
    created = fields.DateTime()
    resource = fields.Str()
    id = fields.Str()
    name = fields.Str()
    action = fields.Str()
    description = fields.Str()

    @post_load
    def post_load(self, data):
        return History(**data)

class HistoryService(object):
    """Service for accessing CDRouter History."""

    RESOURCE = 'history'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of history entries."""
        schema = HistorySchema()
        resp = self.service.list(self.base, filter, sort, limit, page)
        return self.service.decode(schema, resp, many=True)
