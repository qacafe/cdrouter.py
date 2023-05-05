#
# Copyright (c) 2022-2023 by QA Cafe.
# All Rights Reserved.
#

import shutil
import pytest

from cdrouter.cdrouter import CDRouterError
from cdrouter.packages import Package, Options, Schedule
from cdrouter.filters import Field as field
from cdrouter.users import User

from .utils import cdrouter_version, my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestPackages:
    def test_list(self, c):
        (packages, links) = c.packages.list()
        assert links.total == 8
        assert len(packages) == 8

        for ii in range(1, 6):
            p = Package(
                name='My package {}'.format(ii)
            )
            c.packages.create(p)

        (packages, links) = c.packages.list(limit=1)
        assert links.total == 13
        assert links.last == 13

    def test_iter_list(self, c):
        assert len(list(c.packages.iter_list(limit=1))) == 8

        for ii in range(1, 6):
            p = Package(
                name='My package {}'.format(ii)
            )
            c.packages.create(p)

        assert len(list(c.packages.iter_list(limit=1))) == 13

    def test_get(self, c):
        u = c.users.get_by_name('admin')

        import_all_from_file(c, 'tests/testdata/example.gz')

        config = c.configs.get_by_name('Cisco E4200')
        device = c.devices.get_by_name('Cisco E4200')

        p = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')
        p = c.packages.get(p.id)

        assert p.name == 'Cisco E4200 DHCPv4 relay-nofatal'
        assert p.description == 'DHCPv4 relay and different subnet masks on the ER-X'
        assert p.test_count == 2
        assert p.testlist == ['cdrouter_app_14', 'dns_45']
        assert p.extra_cli_args == ''
        assert p.user_id == u.id
        assert p.config_id == config.id
        assert p.result_id is None
        assert p.device_id == device.id
        assert p.options.forever is False
        assert p.options.loop == 0
        assert p.options.repeat == 0
        assert p.options.maxfail == 0
        assert p.options.duration == 0
        assert p.options.wait == 0
        assert p.options.pause is False
        assert p.options.shuffle is False
        assert p.options.seed == 0
        assert p.options.retry == 0
        assert p.options.rdelay == 0
        assert p.tags == ['nofatal']
        assert p.use_as_testlist is False
        assert 'Moving the unstable' in p.note
        assert p.schedule.enabled is False
        assert p.schedule.spec == '0 0 * * *'
        assert p.schedule.options.tags is None
        assert p.schedule.options.skip_tests is None
        assert p.schedule.options.begin_at == ''
        assert p.schedule.options.end_at == ''
        assert p.schedule.options.extra_cli_args == ''

        with pytest.raises(CDRouterError, match='no such package'):
            c.packages.get(99999)

    def test_get_by_name(self, c):
        u = c.users.get_by_name('admin')

        import_all_from_file(c, 'tests/testdata/example.gz')

        config = c.configs.get_by_name('Cisco E4200')
        device = c.devices.get_by_name('Cisco E4200')

        p = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')

        assert p.name == 'Cisco E4200 DHCPv4 relay-nofatal'
        assert p.description == 'DHCPv4 relay and different subnet masks on the ER-X'
        assert p.test_count == 2
        assert p.testlist == ['cdrouter_app_14', 'dns_45']
        assert p.extra_cli_args == ''
        assert p.user_id == u.id
        assert p.config_id == config.id
        assert p.result_id is None
        assert p.device_id == device.id
        assert p.options.forever is False
        assert p.tags == ['nofatal']
        assert p.use_as_testlist is False
        assert 'Moving the unstable' in p.note
        assert p.schedule.enabled is False
        assert p.schedule.spec == '0 0 * * *'

    def test_create(self, c):

        import_all_from_file(c, 'tests/testdata/example.gz')

        config = c.configs.get_by_name('Cisco E4200')
        device = c.devices.get_by_name('Cisco E4200')

        p = Package(
            name='My package',
            description='my cool package',
            testlist=['cdrouter_basic_1', 'cdrouter_basic_2'],
            extra_cli_args='-testvar lanMode=DHCP',
            config_id=config.id,
            device_id=device.id,
            options=Options(forever=True),
            tags=['bar', 'buz', 'foo'],
            note='i am a note',
            schedule=Schedule(enabled=True, spec='1 1 * * *')
        )
        p2 = c.packages.create(p)
        assert p2.id > 0
        assert p2.name == p.name
        assert p2.description == p.description
        assert p2.testlist == p.testlist
        assert p2.extra_cli_args == p.extra_cli_args
        assert p2.config_id == p.config_id
        assert p2.device_id == p.device_id
        assert p2.options.forever == p.options.forever
        assert p2.tags == p.tags
        assert p2.note == p.note
        assert p2.schedule.enabled == p.schedule.enabled
        assert p2.schedule.spec == p.schedule.spec

    def test_edit(self, c):
        p = Package(
            name='My package',
            testlist=['cdrouter_basic_1', 'cdrouter_basic_2'],
        )
        p = c.packages.create(p)

        new_testlist = ['cdrouter_basic_2', 'cdrouter_basic_100']
        p.testlist = new_testlist
        p = c.packages.edit(p)
        assert p.testlist == new_testlist

        p = c.packages.get(p.id)
        assert p.testlist == new_testlist

    def test_delete(self, c):
        assert len(list(c.packages.iter_list())) == 8

        p = Package(
            name='My package',
        )
        p2 = c.packages.create(p)

        assert len(list(c.packages.iter_list())) == 9

        c.packages.delete(p2.id)

        assert len(list(c.packages.iter_list())) == 8

        with pytest.raises(CDRouterError, match='no such package'):
            c.packages.get(p2.id)

    @pytest.mark.skipif(cdrouter_version() < (13, 14, 1), reason="lock endpoint added in 13.14.1")
    def test_lock(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        p = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')
        assert p.locked is False

        p = c.packages.lock(p.id)
        assert p.locked is True

        # locking a locked resource is a no-op, not an error
        c.packages.lock(p.id)
        c.packages.lock(p.id)
        c.packages.lock(p.id)

        p = c.packages.get(p.id)
        assert p.locked is True

        with pytest.raises(CDRouterError, match='cannot delete locked package'):
            c.packages.delete(p.id)

    @pytest.mark.skipif(cdrouter_version() < (13, 14, 1), reason="unlock endpoint added in 13.14.1")
    def test_unlock(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        p = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')
        assert p.locked is False

        p = c.packages.lock(p.id)
        assert p.locked is True

        with pytest.raises(CDRouterError, match='cannot delete locked package'):
            c.packages.delete(p.id)

        p = c.packages.unlock(p.id)
        assert p.locked is False

        # unlocking an unlocked resource is a no-op, not an error
        c.packages.unlock(p.id)
        c.packages.unlock(p.id)
        c.packages.unlock(p.id)

        p = c.packages.get(p.id)
        assert p.locked is False

        c.packages.delete(p.id)

        with pytest.raises(CDRouterError, match='no such package'):
            c.packages.get(p.id)

    def test_get_shares(self, c):
        u = User(
            admin=True,
            name='admin2',
            description='im an admin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u = c.users.create(u)

        p = Package(
            name='My package',
        )
        p = c.packages.create(p)

        assert len(c.packages.get_shares(p.id)) == 0

        c.packages.edit_shares(p.id, [u.id])

        shares = c.packages.get_shares(p.id)
        assert len(shares) == 1
        assert shares[0].user_id == u.id
        assert shares[0].read is True
        assert shares[0].write is False
        assert shares[0].execute is False

    def test_edit_shares(self, c):
        u = User(
            admin=True,
            name='admin2',
            description='im an admin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u = c.users.create(u)

        u2 = User(
            admin=True,
            name='admin3',
            description='im an admin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u2 = c.users.create(u2)

        p = Package(
            name='My package',
        )
        p = c.packages.create(p)

        assert len(c.packages.get_shares(p.id)) == 0

        c.packages.edit_shares(p.id, [u.id, u2.id])

        shares = c.packages.get_shares(p.id)
        assert len(shares) == 2
        assert shares[0].user_id == u.id
        assert shares[0].read is True
        assert shares[0].write is False
        assert shares[0].execute is False
        assert shares[1].user_id == u2.id
        assert shares[1].read is True
        assert shares[1].write is False
        assert shares[1].execute is False

        c.packages.edit_shares(p.id, [u.id])

        shares = c.packages.get_shares(p.id)
        assert len(shares) == 1
        assert shares[0].user_id == u.id
        assert shares[0].read is True
        assert shares[0].write is False
        assert shares[0].execute is False

        c.packages.edit_shares(p.id, [])

        shares = c.packages.get_shares(p.id)
        assert len(shares) == 0

    def test_export(self, c, tmp_path):
        import_all_from_file(c, 'tests/testdata/example.gz')

        p = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')

        (b, filename) = c.packages.export(p.id)

        filename = '{}/{}'.format(tmp_path, 'example.gz')
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

        c.packages.delete(p.id)

        with pytest.raises(CDRouterError, match='no such package'):
            c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')

        import_all_from_file(c, filename)

        p = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')

    def test_analyze(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        p = c.packages.get_by_name('example')
        p.testlist = ['ipv6_basic_1', 'ipv6_basic_2', 'ipv6_basic_3']
        p = c.packages.edit(p)

        analysis = c.packages.analyze(p.id)
        assert analysis.total_count == 3
        assert analysis.run_count == 0
        assert analysis.skipped_count == 3
        assert len(analysis.skipped_tests) == 3
        assert analysis.skipped_tests[0].name == 'ipv6_basic_1'
        assert analysis.skipped_tests[1].name == 'ipv6_basic_2'
        assert analysis.skipped_tests[2].name == 'ipv6_basic_3'

    def test_testlist_expanded(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        p = c.packages.get_by_name('example')

        testlist = c.packages.testlist_expanded(p.id)
        assert len(testlist) > 0
        assert testlist[0] == 'v4_wan_tcp_connect_info'
        assert testlist[1] == 'v4_wan_tcp_syn_info'

    def test_get_interfaces(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        p = c.packages.get_by_name('example')

        intfs = c.packages.get_interfaces(p)
        assert len(intfs) == 1
        assert intfs[0].name == 'wan'
        assert intfs[0].value == 'eth0'
        assert intfs[0].is_wireless is False
        assert intfs[0].is_ics is False

    def test_bulk_export(self, c, tmp_path):
        packages = []
        for ii in range(1, 6):
            p = Package(
                name='My package {}'.format(ii),
            )
            p = c.packages.create(p)
            packages.append(p)

        for p in packages:
            c.packages.get(p.id)

        (b, filename) = c.packages.bulk_export([p.id for p in packages])

        filename = '{}/{}'.format(tmp_path, 'example.gz')
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

        c.packages.bulk_delete([p.id for p in packages])

        for p in packages:
            with pytest.raises(CDRouterError, match='no such package'):
                c.packages.get(p.id)

        import_all_from_file(c, filename)

        for p in packages:
            p = c.packages.get_by_name(p.name)

    def test_bulk_copy(self, c):
        packages = []
        for ii in range(1, 4):
            p = Package(
                name='My package {}'.format(ii),
            )
            p = c.packages.create(p)
            packages.append(p)

        packages = c.packages.bulk_copy([p.id for p in packages])
        assert len(packages) == 3
        assert packages[0].name == 'My package 1 (copy 1)'
        assert packages[1].name == 'My package 2 (copy 1)'
        assert packages[2].name == 'My package 3 (copy 1)'

    def test_bulk_edit(self, c):
        packages = []
        for ii in range(1, 4):
            p = Package(
                name='My package {}'.format(ii),
                testlist=['cdrouter_basic_1']
            )
            p = c.packages.create(p)
            packages.append(p)

        new=['cdrouter_basic_2']
        c.packages.bulk_edit(Package(testlist=new), [p.id for p in packages])

        for p in packages:
            assert c.packages.get(p.id).testlist == new

        new=['cdrouter_basic_10']
        c.packages.bulk_edit(Package(testlist=new), [p.id for p in packages])

        for p in packages:
            assert c.packages.get(p.id).testlist == new

    def test_bulk_delete(self, c):
        p = Package(
            name='My package',
        )
        p = c.packages.create(p)

        p2 = Package(
            name='My package 2',
        )
        p2 = c.packages.create(p2)

        p3 = Package(
            name='My package 3',
        )
        p3 = c.packages.create(p3)

        p4 = Package(
            name='My package 4',
        )
        p4 = c.packages.create(p4)

        p5 = Package(
            name='My package 5',
        )
        p5 = c.packages.create(p5)

        c.packages.bulk_delete([p2.id, p3.id])
        c.packages.get(p.id)
        with pytest.raises(CDRouterError, match='no such package'):
            c.packages.get(p2.id)
        with pytest.raises(CDRouterError, match='no such package'):
            c.packages.get(p3.id)

        c.packages.bulk_delete(filter=[field('id').ge(p4.id)])
        c.packages.get(p.id)
        with pytest.raises(CDRouterError, match='no such package'):
            c.packages.get(p4.id)
        with pytest.raises(CDRouterError, match='no such package'):
            c.packages.get(p5.id)
