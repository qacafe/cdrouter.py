#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Jobs."""

class JobsService(object):
    """Service for accessing CDRouter Jobs."""

    RESOURCE = 'jobs'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of jobs."""
        return self.service.list(self.base, filter, sort, limit, page)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a job."""
        return self.service.get_id(self.base, id)

    def launch(self, resource):
        """Launch a new job."""
        return self.service.create(self.base, resource)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a job."""
        return self.service.delete_id(self.base, id)

    @staticmethod
    def _package_id(id): # pylint: disable=invalid-name,redefined-builtin
        if isinstance(id, (str, int)):
            return {'package_id': str(id)}
        return id

    def bulk_launch(self, package_ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk launch a set of jobs."""
        json = None
        if package_ids != None:
            json = {self.RESOURCE: map(self._package_id, package_ids)}
        return self.service.post(self.base,
                                 params={'bulk': 'launch', 'filter': filter, 'all': all}, json=json)

    def bulk_delete(self, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of jobs."""
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, all=all)
