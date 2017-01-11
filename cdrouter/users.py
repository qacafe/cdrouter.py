#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Users."""

from marshmallow import Schema, fields, post_load

class User(object):
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
    id = fields.Str()
    admin = fields.Bool()
    disabled = fields.Bool()
    name = fields.Str()
    description = fields.Str()
    created = fields.DateTime()
    updated = fields.DateTime()
    token = fields.Str()

    password = fields.Str()
    password_confirm = fields.Str()

    @post_load
    def post_load(self, data):
        return User(**data)

class UsersService(object):
    """Service for accessing CDRouter Users."""

    RESOURCE = 'users'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of users."""
        schema = UserSchema(exclude=('created', 'updated', 'token', 'password', 'password_confirm'))
        resp = self.service.list(self.base, filter, sort, limit, page)
        return self.service.decode(schema, resp, many=True)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a user."""
        schema = UserSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def create(self, resource):
        """Create a new user."""
        schema = UserSchema(exclude=('id', 'created', 'updated', 'token'))
        json = self.service.encode(schema, resource)

        schema = UserSchema(exclude=('password', 'password_confirm'))
        resp = self.service.create(self.base, json)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a user."""
        schema = UserSchema(exclude=('id', 'created', 'updated', 'token', 'password', 'password_confirm'))
        json = self.service.encode(schema, resource)

        schema = UserSchema(exclude=('password', 'password_confirm'))
        resp = self.service.edit(self.base, resource.id, json)
        return self.service.decode(schema, resp)

    def change_password(self, id, new, old=None, change_token=True): # pylint: disable=invalid-name,redefined-builtin
        """Change a user's password."""
        schema = UserSchema(exclude=('password', 'password_confirm'))
        resp = self.service.post(self.base+str(id)+'/password/',
                                  params={'change_token', change_token},
                                  json={'old': old, 'new': new, 'new_confirm': new})
        return self.service.decode(schema, resp)

    def change_token(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Change a user's token."""
        schema = UserSchema(exclude=('password', 'password_confirm'))
        resp = self.service.post(self.base+str(id)+'/token/')
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a user."""
        return self.service.delete_id(self.base, id)

    def bulk_copy(self, ids):
        """Bulk copy a set of users."""
        schema = UserSchema()
        return self.service.bulk_copy(self.base, self.RESOURCE, ids, schema)

    def bulk_edit(self, _fields, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of users."""
        return self.service.bulk_edit(self.base, self.RESOURCE, _fields, ids=ids, filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of users."""
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)
