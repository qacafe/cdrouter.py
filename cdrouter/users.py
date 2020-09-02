#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Users."""

import collections

from marshmallow import Schema, fields, post_load
from .cdr_error import CDRouterError
from .cdr_datetime import DateTime
from .filters import Field as field

class User(object):
    """Model for CDRouter Users.

    :param id: (optional) User ID as an int.
    :param admin: (optional) Bool `True` if user is an administrator.
    :param disabled: (optional) Bool `True` if user is disabled.
    :param name: (optional) User name as string.
    :param description: (optional) User description as string.
    :param created: (optional) User creation time as `DateTime`.
    :param updated: (optional) User last-updated time as `DateTime`.
    :param token: (optional) User's API token as string.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.admin = kwargs.get('admin', None)
        self.disabled = kwargs.get('disabled', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)
        self.token = kwargs.get('token', None)

        # only needed for change_password
        self.password = kwargs.get('password', None)
        self.password_confirm = kwargs.get('password_confirm', None)

class UserSchema(Schema):
    id = fields.Int(as_string=True)
    admin = fields.Bool()
    disabled = fields.Bool()
    name = fields.Str()
    description = fields.Str()
    created = DateTime()
    updated = DateTime()
    token = fields.Str()

    password = fields.Str()
    password_confirm = fields.Str()

    @post_load
    def post_load(self, data):
        return User(**data)

class Page(collections.namedtuple('Page', ['data', 'links'])):
    """Named tuple for a page of list response data.

    :param data: :class:`users.User <users.User>` list
    :param links: :class:`cdrouter.Links <cdrouter.Links>` object
    """

class UsersService(object):
    """Service for accessing CDRouter Users."""

    RESOURCE = 'users'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, type=None, sort=None, limit=None, page=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of users.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`users.Page <users.Page>` object
        """
        schema = UserSchema()
        if not detailed:
            schema = UserSchema(exclude=('created', 'updated', 'token', 'password', 'password_confirm'))
        resp = self.service.list(self.base, filter, type, sort, limit, page, detailed=detailed)
        us, l = self.service.decode(schema, resp, many=True, links=True)
        return Page(us, l)

    def iter_list(self, *args, **kwargs):
        """Get a list of users.  Whereas ``list`` fetches a single page of
        users according to its ``limit`` and ``page`` arguments,
        ``iter_list`` returns all users by internally making
        successive calls to ``list``.

        :param args: Arguments that ``list`` takes.
        :param kwargs: Optional arguments that ``list`` takes.
        :return: :class:`users.User <users.User>` list

        """
        return self.service.iter_list(self.list, *args, **kwargs)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a user.

        :param id: User ID as an int.
        :return: :class:`users.User <users.User>` object
        :rtype: users.User
        """
        schema = UserSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def get_by_name(self, name): # pylint: disable=invalid-name,redefined-builtin
        """Get a user by name.

        :param name: User name as string.
        :return: :class:`users.User <users.User>` object
        :rtype: users.User
        """
        rs, _ = self.list(filter=field('name').eq(name), limit=1)
        if len(rs) == 0:
            raise CDRouterError('no such user')
        return rs[0]

    def create(self, resource):
        """Create a new user.

        :param resource: :class:`users.User <users.User>` object
        :return: :class:`users.User <users.User>` object
        :rtype: users.User
        """
        schema = UserSchema(exclude=('id', 'created', 'updated', 'token'))
        json = self.service.encode(schema, resource)

        schema = UserSchema(exclude=('password', 'password_confirm'))
        resp = self.service.create(self.base, json)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a user.

        :param resource: :class:`users.User <users.User>` object
        :return: :class:`users.User <users.User>` object
        :rtype: users.User
        """
        schema = UserSchema(exclude=('id', 'created', 'updated', 'token', 'password', 'password_confirm'))
        json = self.service.encode(schema, resource)

        schema = UserSchema(exclude=('password', 'password_confirm'))
        resp = self.service.edit(self.base, resource.id, json)
        return self.service.decode(schema, resp)

    def change_password(self, id, new, old=None, change_token=True): # pylint: disable=invalid-name,redefined-builtin
        """Change a user's password.

        :param id: User ID as an int.
        :param new: New password as string.
        :param old: (optional) Old password as string (required if performing action as non-admin).
        :param change_token: (optional) If bool `True`, also generate a new API token for user.
        :return: :class:`users.User <users.User>` object
        :rtype: users.User
        """
        schema = UserSchema(exclude=('password', 'password_confirm'))
        resp = self.service.post(self.base+str(id)+'/password/',
                                  params={'change_token': change_token},
                                  json={'old': old, 'new': new, 'new_confirm': new})
        return self.service.decode(schema, resp)

    def change_token(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Change a user's token.

        :param id: User ID as an int.
        :return: :class:`users.User <users.User>` object
        :rtype: users.User
        """
        schema = UserSchema(exclude=('password', 'password_confirm'))
        resp = self.service.post(self.base+str(id)+'/token/')
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a user.

        :param id: User ID as an int.
        """
        return self.service.delete_id(self.base, id)

    def bulk_copy(self, ids):
        """Bulk copy a set of users.

        :param ids: Int list of user IDs.
        :return: :class:`users.User <users.User>` list
        """
        schema = UserSchema()
        return self.service.bulk_copy(self.base, self.RESOURCE, ids, schema)

    def bulk_edit(self, _fields, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of users.

        :param _fields: :class:`users.User <users.User>` object
        :param ids: (optional) Int list of user IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        schema = UserSchema(exclude=('id', 'created', 'updated', 'token', 'password', 'password_confirm'))
        _fields = self.service.encode(schema, _fields, skip_none=True)
        return self.service.bulk_edit(self.base, self.RESOURCE, _fields, ids=ids, filter=filter, type=type, all=all)

    def bulk_delete(self, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of users.

        :param ids: (optional) Int list of user IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, type=type, all=all)
