#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Users."""

class UsersService(object):
    """Service for accessing CDRouter Users."""

    RESOURCE = 'users'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of users."""
        return self.service.list(self.base, filter, sort, limit, page)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a user."""
        return self.service.get_id(self.base, id)

    def create(self, resource):
        """Create a new user."""
        return self.service.create(self.base, resource)

    def edit(self, resource):
        """Edit a user."""
        return self.service.edit(self.base, resource['id'], resource)

    def change_password(self, id, new, old=None, change_token=True): # pylint: disable=invalid-name,redefined-builtin
        """Change a user's password."""
        return self.service.post(self.base+str(id)+'/password/',
                                  params={'change_token', change_token},
                                  json={'old': old, 'new': new, 'new_confirm': new})

    def change_token(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Change a user's token."""
        return self.service.post(self.base+str(id)+'/token/')

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a user."""
        return self.service.delete_id(self.base, id)

    def bulk_copy(self, ids):
        """Bulk copy a set of users."""
        return self.service.bulk_copy(self.base, self.RESOURCE, ids)

    def bulk_edit(self, fields, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of users."""
        return self.service.bulk_edit(self.base, self.RESOURCE, fields, ids=ids, filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of users."""
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)
