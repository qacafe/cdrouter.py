#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Exports."""

class ExportsService(object):
    """Service for accessing CDRouter Exports."""

    RESOURCE = 'exports'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def bulk_export(self, config_ids=None, device_ids=None, package_ids=None, result_ids=None, exclude_captures=False):
        """Bulk export a set of configs, devices, packages and results."""
        if config_ids is None:
            config_ids = []
        if device_ids is None:
            device_ids = []
        if package_ids is None:
            package_ids = []
        if result_ids is None:
            result_ids = []
        json = {
            'configs': map(int, config_ids),
            'devices': map(int, device_ids),
            'packages': map(int, package_ids),
            'results': map(int, result_ids),
            'options': {'exclude_captures': exclude_captures}
        }
        return self.service.post(self.base, json=json)
