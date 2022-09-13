#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

from datetime import datetime

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestDateTime:
    def test_datetime(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        config = c.configs.get_by_name('Cisco E4200')
        assert config.created == datetime(2016, 12, 14, 16, 18, 14, 515626)
        device = c.devices.get_by_name('Cisco E4200')
        assert device.created == datetime(2016, 12, 15, 11, 3, 3, 235051)
        package = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')
        assert package.created == datetime(2019, 4, 30, 11, 58, 11, 530826)
        result = c.results.get(20220821222306)
        assert result.created == datetime(2022, 8, 21, 22, 23, 6, 458665)
