#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter History."""

class HistoryService(object):
    """Service for accessing CDRouter History."""

    RESOURCE = 'history'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of history entries."""
        return self.service.list(self.base, filter, sort, limit, page)
