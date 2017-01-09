#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Packages."""

class PackagesService(object):
    """Service for accessing CDRouter Packages."""

    RESOURCE = 'packages'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of packages."""
        return self.service.list(self.base, filter, sort, limit, page)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a package."""
        return self.service.get_id(self.base, id)

    def create(self, resource):
        """Create a new package."""
        return self.service.create(self.base, resource)

    def edit(self, resource):
        """Edit a package."""
        return self.service.edit(self.base, resource['id'], resource)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a package."""
        return self.service.delete_id(self.base, id)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get shares for a package."""
        return self.service.shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Edit shares for a package."""
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Export a package."""
        return self.service.export(self.base, id)

    def analyze(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of tests that will be skipped for a package."""
        return self.service.post(self.base+str(id)+'/', params={'process': 'analyze'})

    def bulk_export(self, ids):
        """Bulk export a set of packages."""
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        """Bulk copy a set of packages."""
        return self.service.bulk_copy(self.base, self.RESOURCE, ids)

    def bulk_edit(self, fields, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of packages."""
        return self.service.bulk_edit(self.base, self.RESOURCE,
                                      fields, ids=ids, filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of packages."""
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)
