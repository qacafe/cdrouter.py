#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter System."""

import os.path

class SystemService(object):
    """Service for accessing CDRouter System."""

    RESOURCE = 'system'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def latest_lounge_release(self):
        """Get the latest release of CDRouter from the CDRouter Support Lounge."""
        return self.service.get(self.base+'lounge/latest/')

    def check_for_lounge_upgrade(self, email, password):
        """Check the CDRouter Support Lounge for eligible upgrades using your
        Support Lounge email & password."""
        return self.service.post(self.base+'lounge/check/',
                                 json={'email': email, 'password': password})

    def lounge_upgrade(self, email, password, release_id):
        """Download & install an upgrade from the CDRouter Support Lounge
        using your Support Lounge email & password. Please note that any
        running tests will be stopped."""
        return self.service.post(self.base+'lounge/upgrade/',
                                 json={'email': email, 'password': password, 'release': {'id': int(release_id)}})

    def manual_upgrade(self, filepath):
        """Upgrade CDRouter manually by uploading a .bin installer from the
        CDRouter Support Lounge. Please note that any running tests will be
        stopped."""
        return self.service.post(self.base+'upgrade/',
                                 files={'file': (os.path.basename(filepath), open(filepath, 'rb'))})

    def restart(self):
        """Restart CDRouter web interface. Please note that any running tests will be stopped."""
        return self.service.post(self.base+'restart/')

    def time(self):
        """Get system time."""
        return self.service.post(self.base+'time/')

    def hostname(self):
        """Get system hostname."""
        return self.service.post(self.base+'hostname/')

    def interfaces(self, addresses=False):
        """Get system interfaces."""
        return self.service.post(self.base+'interfaces/', params={'addresses': addresses})

    def get_preferences(self):
        """Get preferences from /usr/cdrouter-data/etc/config.yml."""
        return self.service.get(self.base+'preferences/')

    def edit_preferences(self, resource):
        """Edit preferences in /usr/cdrouter-data/etc/config.yml."""
        return self.service.patch(self.base+'preferences/', json=resource)
