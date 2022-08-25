#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import pytest

from cdrouter.cdrouter import CDRouterError
from cdrouter.filters import Field as field
from cdrouter.jobs import Job

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestJobs:
    def test_list(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        (jobs, links) = c.jobs.list()
        assert len(jobs) == 0
        assert links.total == 0

        package = c.packages.get_by_name('example')
        c.jobs.launch(Job(package_id=package.id))

        (jobs, links) = c.jobs.list()
        assert len(jobs) == 1
        assert links.total == 1

    def test_iter_list(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        assert len(list(c.jobs.iter_list())) == 0

        package = c.packages.get_by_name('example')
        c.jobs.launch(Job(package_id=package.id))

        assert len(list(c.jobs.iter_list())) == 1

    def test_get(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        assert len(list(c.jobs.iter_list())) == 0

        package = c.packages.get_by_name('example')
        c.jobs.launch(Job(package_id=package.id))

        assert len(list(c.jobs.iter_list())) == 1

        u = c.users.get_by_name('admin')

        jobs = list(c.jobs.iter_list())
        assert len(jobs) == 1
        j = jobs[0]
        assert j.id > 0
        assert j.package_id == package.id
        assert j.config_id == 0
        assert j.device_id == 0
        assert j.user_id == u.id
        assert j.automatic is False
        assert j.interface_names == ['eth0']
        assert j.uses_wireless is False
        assert j.uses_ics is False

        with pytest.raises(CDRouterError, match='no such Job'):
            c.jobs.get(9999)

    def test_edit(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')
        import_all_from_file(c, 'tests/testdata/example2.gz')

        new_config = c.configs.get_by_name('Cisco E4200')
        new_device = c.devices.get_by_name('Cisco E4200')
        new_package = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')

        package = c.packages.get_by_name('example')

        c.jobs.launch(Job(package_id=package.id))
        c.jobs.launch(Job(package_id=package.id))
        c.jobs.launch(Job(package_id=package.id))
        c.jobs.launch(Job(package_id=package.id))
        c.jobs.launch(Job(package_id=package.id))

        jobs = list(c.jobs.iter_list(filter=[field('active').eq(False)]))

        for j in jobs:
            j.package_id = new_package.id
            j.config_id = new_config.id
            j.device_id = new_device.id
            j = c.jobs.edit(j)
            assert j.package_id == new_package.id
            assert j.config_id == new_config.id
            assert j.device_id == new_device.id

            j = c.jobs.get(j.id)
            assert j.package_id == new_package.id
            assert j.config_id == new_config.id
            assert j.device_id == new_device.id

    def test_launch(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')
        config = c.configs.get_by_name('example.conf')

        assert len(list(c.jobs.iter_list())) == 0

        j = c.jobs.launch(Job(package_id=package.id))
        assert j.id > 0
        assert j.package_id == package.id
        assert j.package_name == package.name
        assert j.config_id == 0
        assert j.config_name == config.name
        assert j.device_id == 0
        assert j.device_name == ''
        assert j.interface_names == ['eth0']
        assert j.uses_wireless is False
        assert j.uses_ics is False

        assert len(list(c.jobs.iter_list())) == 1

    def test_delete(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')

        assert len(list(c.jobs.iter_list())) == 0

        c.jobs.launch(Job(package_id=package.id))
        c.jobs.launch(Job(package_id=package.id))
        c.jobs.launch(Job(package_id=package.id))
        c.jobs.launch(Job(package_id=package.id))
        c.jobs.launch(Job(package_id=package.id))

        assert len(list(c.jobs.iter_list())) == 5

        jobs = list(c.jobs.iter_list(filter=[field('active').eq(False)]))

        for j in jobs:
            c.jobs.delete(j.id)

        assert len(list(c.jobs.iter_list())) == (5 - len(jobs))

    def test_get_interfaces(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')

        j = c.jobs.launch(Job(package_id=package.id))

        intfs = c.jobs.get_interfaces(j)
        assert len(intfs) == 1
        assert intfs[0].name == 'wan'
        assert intfs[0].value == 'eth0'
        assert intfs[0].is_wireless is False
        assert intfs[0].is_ics is False

    def test_bulk_launch(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')

        c.jobs.bulk_launch(jobs=[
            Job(package_id=package.id),
            Job(package_id=package.id),
            Job(package_id=package.id)
        ])

        assert len(list(c.jobs.iter_list())) == 3

        # TODO(niels): cdrouterd panics if bulk_launch is called with
        # jobs=None, uncomment this once this has been fixed, see
        # sc-19680
        # c.jobs.bulk_launch(filter=[field('name').eq('example')])

        # assert len(list(c.jobs.iter_list())) == 4

    def test_bulk_delete(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')

        c.jobs.launch(Job(package_id=package.id))
        j2 = c.jobs.launch(Job(package_id=package.id))
        j3 = c.jobs.launch(Job(package_id=package.id))
        j4 = c.jobs.launch(Job(package_id=package.id))
        j5 = c.jobs.launch(Job(package_id=package.id))
        assert len(list(c.jobs.iter_list())) == 5

        c.jobs.bulk_delete(ids=[j2.id, j3.id])
        assert len(list(c.jobs.iter_list())) == 3
        with pytest.raises(CDRouterError, match='no such Job'):
            c.jobs.get(j2.id)
        with pytest.raises(CDRouterError, match='no such Job'):
            c.jobs.get(j3.id)

        c.jobs.bulk_delete(ids=[j4.id, j5.id])
        assert len(list(c.jobs.iter_list())) == 1
        with pytest.raises(CDRouterError, match='no such Job'):
            c.jobs.get(j4.id)
        with pytest.raises(CDRouterError, match='no such Job'):
            c.jobs.get(j5.id)
