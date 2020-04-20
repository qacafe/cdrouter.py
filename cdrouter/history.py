#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter History."""

import collections

from marshmallow import Schema, fields, post_load
from .cdr_datetime import DateTime

class History(object):
    """Model for CDRouter History entries.

    :param user_id: (optional) User ID as an int.
    :param created: (optional) Entry creation time as `DateTime`.
    :param resource: (optional) Resource type as string.
    :param id: (optional) Resource ID as an int.
    :param name: (optional) Resource name as string.
    :param action: (optional) Action name as string.
    :param description: (optional) Resource description as string.
    """
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id', None)
        self.created = kwargs.get('created', None)
        self.resource = kwargs.get('resource', None)
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.action = kwargs.get('action', None)
        self.description = kwargs.get('description', None)

class HistorySchema(Schema):
    user_id = fields.Int(as_string=True)
    created = DateTime()
    resource = fields.Str()
    id = fields.Int(as_string=True)
    name = fields.Str()
    action = fields.Str()
    description = fields.Str()

    @post_load
    def post_load(self, data):
        return History(**data)

class Page(collections.namedtuple('Page', ['data', 'links'])):
    """Named tuple for a page of list response data.

    :param data: :class:`history.History <history.History>` list
    :param links: :class:`cdrouter.Links <cdrouter.Links>` object
    """

class HistoryService(object):
    """Service for accessing CDRouter History."""

    RESOURCE = 'history'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, type=None, sort=None, limit=None, page=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of history entries.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`history.Page <history.Page>` object
        """
        schema = HistorySchema()
        resp = self.service.list(self.base, filter, type, sort, limit, page, detailed=detailed)
        hs, l = self.service.decode(schema, resp, many=True, links=True)
        return Page(hs, l)

    def iter_list(self, *args, **kwargs):
        """Get a list of history entries.  Whereas ``list`` fetches a single
        page of history entries according to its ``limit`` and
        ``page`` arguments, ``iter_list`` returns all history entries
        by internally making successive calls to ``list``.

        :param args: Arguments that ``list`` takes.
        :param kwargs: Optional arguments that ``list`` takes.
        :return: :class:`historys.History <historys.History>` list

        """
        return self.service.iter_list(self.list, *args, **kwargs)
