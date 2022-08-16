#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import shutil

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestExports:
    def test_bulk_export(self, c, tmp_path):
        tmp_path = str(tmp_path)

        import_all_from_file(c, 'tests/testdata/example.gz')

        config = c.configs.get_by_name('Cisco E4200')
        device = c.devices.get_by_name('Cisco E4200')
        package = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')
        result = c.results.get(20220821222306)

        (b, filename) = c.exports.bulk_export(
            config_ids=[config.id],
            device_ids=[device.id],
            package_ids=[package.id],
            result_ids=[result.id]
        )

        filename = '{}/{}'.format(tmp_path, 'example.gz')
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

        c.configs.delete(config.id)
        c.devices.delete(device.id)
        c.packages.delete(package.id)
        c.results.delete(result.id)

        import_all_from_file(c, filename)

        config = c.configs.get_by_name('Cisco E4200')
        device = c.devices.get_by_name('Cisco E4200')
        package = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')
        result = c.results.get(20220821222306)
