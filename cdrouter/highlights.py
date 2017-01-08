#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

class HighlightsService(object):
    RESOURCE = 'highlights'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        return '/results/'+str(id)+'/tests/'+str(seq)+self.BASE

    def list(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        return self.service.list(self._base(id, seq), filter)

    def get(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        return self.service.get_id(self._base(id, seq), line)

    def create_or_edit(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        return self.service.edit(self._base(id, seq), resource['line'], resource)

    def delete(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        return self.service.delete_id(self._base(id, seq), line)
