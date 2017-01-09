#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter TestResults."""

class TestResultsService(object):
    """Service for accessing CDRouter TestResults."""

    RESOURCE = 'tests'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id): # pylint: disable=invalid-name,redefined-builtin
        return '/results/'+str(id)+self.BASE

    def list(self, id, filter=None, sort=None, limit=None, page=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of test results."""
        return self.service.list(self._base(id), filter, sort, limit, page)

    def list_csv(self, id, filter=None, sort=None, limit=None, page=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of test results as CSV."""
        return self.service.list(self._base(id), filter, sort, limit, page, format='csv')

    def get(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        """Get a test result."""
        return self.service.get_id(self._base(id), seq)

    def edit(self, id, resource): # pylint: disable=invalid-name,redefined-builtin
        """Edit a test result."""
        return self.service.edit(self._base(id), resource['seq'], resource)

    def get_log(self, id, seq, offset=None, limit=None, filter=None, packets=None, timestamp_format=None, format=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a test result's log."""
        return self.service.get(self._base(id)+str(seq)+'/log/',
                                params={'offset': int(offset), 'limit': int(limit), 'filter': filter,
                                        'packets': bool(packets), 'timestamp_format': timestamp_format, 'format': format})

    def get_log_plaintext(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        """Get a test result's log as plaintext."""
        return self.get_log(id, seq, format='text')
