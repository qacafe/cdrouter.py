#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Imports."""

import os.path

class ImportsService(object):
    """Service for accessing CDRouter Imports."""

    RESOURCE = 'imports'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self):
        """Get a list of staged (in-progress) imports."""
        return self.service.list(self.base)

    def stage_import_from_file(self, filepath):
        """Stage an import from a file upload."""
        return self.service.post(self.base,
                                 files={'file': (os.path.basename(filepath), open(filepath, 'rb'))})

    def stage_import_from_filesystem(self, filepath):
        """Stage an import from a filesystem path."""
        return self.service.post(self.base,
                                 params={'path': filepath})

    def stage_import_from_url(self, url, token=None, insecure=False):
        """Stage an import from a URL to another CDRouter system."""
        return self.service.post(self.base,
                                 params={'url': url, 'token': token, 'insecure': insecure})

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a staged import."""
        return self.service.get_id(self.base, id)

    def get_commit_request(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a commit request for a staged import."""
        return self.service.get(self.base+str(id)+'/request/')

    def commit(self, id, commit_request): # pylint: disable=invalid-name,redefined-builtin
        """Commit a staged import."""
        return self.service.post(self.base+str(id)+'/commit/', json=commit_request)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a staged import."""
        return self.service.delete_id(self.base, id)
