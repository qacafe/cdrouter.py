#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Tags."""

class TagsService(object):
    """Service for accessing CDRouter Tags."""

    RESOURCE = 'tags'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, resource=None, sort=None):
        """Get a list of tags."""
        return self.service.get(self.base, params={'resource': resource, 'sort': sort})

    def get(self, name):
        """Get a tag."""
        return self.service.get_id(self.base, name)

    def edit(self, resource):
        """Edit a tag."""
        return self.service.edit(self.base, resource['name'], resource)

    def delete(self, name):
        """Delete a tag."""
        return self.service.delete_id(self.base, name)
