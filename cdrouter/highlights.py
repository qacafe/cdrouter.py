#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Highlights."""

class HighlightsService(object):
    """Service for accessing CDRouter Highlights."""

    RESOURCE = 'highlights'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        return '/results/'+str(id)+'/tests/'+str(seq)+self.BASE

    def list(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of highlights."""
        return self.service.list(self._base(id, seq), filter)

    def get(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        """Get a highlight."""
        return self.service.get_id(self._base(id, seq), line)

    def create_or_edit(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        """Create or edit a highlight."""
        return self.service.edit(self._base(id, seq), resource['line'], resource)

    def delete(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        """Get a highlight."""
        return self.service.delete_id(self._base(id, seq), line)
