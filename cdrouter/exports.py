#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

class Exports:
    RESOURCE = 'exports'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def bulk_export(self, config_ids=[], device_ids=[], package_ids=[], result_ids=[], exclude_captures=False):
        json={
            'configs': map(int, config_ids),
            'devices': map(int, device_ids),
            'packages': map(int, package_ids),
            'results': map(int, result_ids),
            'options': { 'exclude_captures': exclude_captures }
        }
        return self.service._post(self.base, json=json)
