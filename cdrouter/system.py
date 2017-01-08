#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

import os.path

class SystemService(object):
    RESOURCE = 'system'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def latest_lounge_release(self):
        return self.service.get(self.base+'lounge/latest/')

    def check_for_lounge_upgrade(self, email, password):
        return self.service.post(self.base+'lounge/check/',
                                 json={'email': email, 'password': password})

    def lounge_upgrade(self, email, password, release_id):
        return self.service.post(self.base+'lounge/upgrade/',
                                 json={'email': email, 'password': password, 'release': {'id': int(release_id)}})

    def manual_upgrade(self, filepath):
        return self.service.post(self.base+'upgrade/',
                                 files={'file': (os.path.basename(filepath), open(filepath, 'rb'))})

    def restart(self):
        return self.service.post(self.base+'restart/')

    def time(self):
        return self.service.post(self.base+'time/')

    def hostname(self):
        return self.service.post(self.base+'hostname/')

    def interfaces(self, addresses=False):
        return self.service.post(self.base+'interfaces/', params={'addresses': addresses})

    def get_preferences(self):
        return self.service.get(self.base+'preferences/')

    def edit_preferences(self, resource):
        return self.service.patch(self.base+'preferences/', json=resource)
