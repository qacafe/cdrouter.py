#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import shutil
import pytest

from cdrouter.cdrouter import CDRouterError
from cdrouter.configs import Config, Testvar
from cdrouter.filters import Field as field
from cdrouter.users import User

from .utils import cdrouter_version, my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestConfigs:
    def test_list(self, c):
        (configs, links) = c.configs.list()
        assert links.current == 0
        assert len(configs) == 0

        for ii in range(1, 6):
            cfg = Config(
                name='My config {}'.format(ii)
            )
            c.configs.create(cfg)

        (configs, links) = c.configs.list(limit=1)
        assert links.total == 5
        assert links.last == 5

    def test_iter_list(self, c):
        assert len(list(c.configs.iter_list(limit=1))) == 0

        for ii in range(1, 6):
            cfg = Config(
                name='My config {}'.format(ii),
            )
            c.configs.create(cfg)

        assert len(list(c.configs.iter_list(limit=1))) == 5

    def test_get_new(self, c):
        contents = c.configs.get_new()
        assert 'SECTION "About"' in contents

    def test_get(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        u = c.users.get_by_name('admin')

        cfg = c.configs.get_by_name('Cisco E4200')
        cfg = c.configs.get(cfg.id)
        assert cfg.name == 'Cisco E4200'
        assert cfg.description == 'DHCPv4 and DHCPv6 relay config using ER-X as relay and E4200 as DUT'
        assert 'SECTION "About"' in cfg.contents
        assert cfg.user_id == u.id
        assert cfg.tags == ['DHCP relay', 'DHCPv6 relay']
        assert 'The interface names on this system' in cfg.note

        with pytest.raises(CDRouterError, match='no such config'):
            c.configs.get(99999)

    def test_get_plaintext(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        cfg = c.configs.get_by_name('Cisco E4200')
        contents = c.configs.get_plaintext(cfg.id)
        assert 'SECTION "About"' in contents

    def test_get_by_name(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        u = c.users.get_by_name('admin')

        cfg = c.configs.get_by_name('Cisco E4200')
        assert cfg.name == 'Cisco E4200'
        assert cfg.description == 'DHCPv4 and DHCPv6 relay config using ER-X as relay and E4200 as DUT'
        assert 'SECTION "About"' in cfg.contents
        assert cfg.user_id == u.id
        assert cfg.tags == ['DHCP relay', 'DHCPv6 relay']
        assert 'The interface names on this system' in cfg.note

    def test_create(self, c):
        assert len(list(c.configs.iter_list())) == 0

        u = c.users.get_by_name('admin')

        cfg = Config(
            name='My config',
            description='i am a description',
            contents='testvar lanIp 1.1.1.1',
            tags=['bar', 'buz', 'foo'],
            note='i am a note'
        )
        cfg2 = c.configs.create(cfg)
        assert cfg2.id > 0
        assert cfg2.name == cfg.name
        assert cfg2.description == cfg.description
        assert cfg2.contents == cfg.contents
        assert cfg2.user_id == u.id
        assert cfg2.tags == cfg.tags
        assert cfg2.note == cfg.note

        assert len(list(c.configs.iter_list())) == 1

    def test_edit(self, c):
        cfg = Config(
            name='My config',
            description='i am a description',
            contents='testvar lanIp 1.1.1.1',
            tags=['bar', 'buz', 'foo'],
            note='i am a note'
        )
        cfg = c.configs.create(cfg)

        new_contents='testvar lanIp 2.2.2.2'
        new_description = 'i am a different description'
        cfg.contents = new_contents
        cfg.description = new_description
        cfg = c.configs.edit(cfg)
        assert cfg.contents == new_contents
        assert cfg.description == new_description

        cfg = c.configs.get(cfg.id)
        assert cfg.contents == new_contents
        assert cfg.description == new_description

    def test_delete(self, c):
        assert len(list(c.configs.iter_list())) == 0

        cfg = Config(
            name='My config',
            description='i am a description',
            contents='testvar lanIp 1.1.1.1',
            tags=['bar', 'buz', 'foo'],
            note='i am a note'
        )
        cfg = c.configs.create(cfg)

        assert len(list(c.configs.iter_list())) == 1

        c.configs.delete(cfg.id)

        assert len(list(c.configs.iter_list())) == 0

        with pytest.raises(CDRouterError, match='no such config'):
            c.configs.get(cfg.id)

    def test_get_shares(self, c):
        u = User(
            admin=True,
            name='admin2',
            description='im an admin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u = c.users.create(u)

        cfg = Config(
            name='My config',
        )
        cfg = c.configs.create(cfg)

        assert len(c.configs.get_shares(cfg.id)) == 0

        c.configs.edit_shares(cfg.id, [u.id])

        shares = c.configs.get_shares(cfg.id)
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

        cfg = Config(
            name='My config',
        )
        cfg = c.configs.create(cfg)

        assert len(c.configs.get_shares(cfg.id)) == 0

        c.configs.edit_shares(cfg.id, [u.id, u2.id])

        shares = c.configs.get_shares(cfg.id)
        assert len(shares) == 2
        assert shares[0].user_id == u.id
        assert shares[0].read is True
        assert shares[0].write is False
        assert shares[0].execute is False
        assert shares[1].user_id == u2.id
        assert shares[1].read is True
        assert shares[1].write is False
        assert shares[1].execute is False

        c.configs.edit_shares(cfg.id, [u.id])

        shares = c.configs.get_shares(cfg.id)
        assert len(shares) == 1
        assert shares[0].user_id == u.id
        assert shares[0].read is True
        assert shares[0].write is False
        assert shares[0].execute is False

        c.configs.edit_shares(cfg.id, [])

        shares = c.configs.get_shares(cfg.id)
        assert len(shares) == 0

    def test_export(self, c, tmp_path):
        import_all_from_file(c, 'tests/testdata/example.gz')

        cfg = c.configs.get_by_name('Cisco E4200')

        (b, filename) = c.configs.export(cfg.id)

        filename = '{}/{}'.format(tmp_path, 'example.gz')
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

        c.configs.delete(cfg.id)

        with pytest.raises(CDRouterError, match='no such config'):
            c.configs.get_by_name('Cisco E4200')

        import_all_from_file(c, filename)

        cfg = c.configs.get_by_name('Cisco E4200')

    def test_check_config(self, c):
        cfg = Config(
            name='My config',
            contents='testvar lanIp i am not a valid testvar value'
        )
        cfg = c.configs.create(cfg)

        chk = c.configs.check_config(cfg.contents)
        assert len(chk.errors) == 1
        assert chk.errors[0].lines == ['1']
        assert 'wrong # args' in chk.errors[0].error

    def test_upgrade_config(self, c):
        cfg = Config(
            name='My config',
            contents='testvar lanIp 1.1.1.1'
        )
        cfg = c.configs.create(cfg)

        upg = c.configs.upgrade_config(cfg.contents)
        assert upg.success is True
        assert 'SECTION "About"' in upg.output

    @pytest.mark.flaky(reruns=5)
    def test_get_networks(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        cfg = c.configs.get_by_name('example.conf')

        networks = c.configs.get_networks(cfg.contents)
        assert networks.name == 'DUT'
        assert networks.type == 'root'
        assert networks.side == 'root'
        assert networks.title is None
        assert len(networks.children) == 2
        assert networks.children[0].name == 'lan (none)'
        assert networks.children[0].type == 'ethernet-interface'
        assert networks.children[0].side == 'lan'
        assert networks.children[0].title == 'lanMode: DHCP'
        assert networks.children[0].children is None
        assert networks.children[1].name == 'wan (eth0)'
        assert networks.children[1].type == 'ethernet-interface'
        assert networks.children[1].side == 'wan'
        assert networks.children[1].title == 'wanMode: DHCP | TR-069, Multicast, RADIUS interface'
        assert len(networks.children[1].children) == 12

    def test_get_interfaces(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        cfg = c.configs.get_by_name('example.conf')

        intfs = c.configs.get_interfaces(cfg.contents)
        assert len(intfs) == 1
        assert intfs[0].name == 'wan'
        assert intfs[0].value == 'eth0'
        assert intfs[0].is_wireless is False
        assert intfs[0].is_ics is False

    def test_bulk_export(self, c, tmp_path):
        configs = []
        for ii in range(1, 6):
            cfg = Config(
                name='My config {}'.format(ii),
            )
            cfg = c.configs.create(cfg)
            configs.append(cfg)

        for cfg in configs:
            c.configs.get(cfg.id)

        (b, filename) = c.configs.bulk_export([cfg.id for cfg in configs])

        filename = '{}/{}'.format(tmp_path, 'example.gz')
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

        c.configs.bulk_delete([cfg.id for cfg in configs])

        for cfg in configs:
            with pytest.raises(CDRouterError, match='no such config'):
                c.configs.get(cfg.id)

        import_all_from_file(c, filename)

        for cfg in configs:
            cfg = c.configs.get_by_name(cfg.name)

    def test_bulk_copy(self, c):
        configs = []
        for ii in range(1, 4):
            cfg = Config(
                name='My config {}'.format(ii),
            )
            cfg = c.configs.create(cfg)
            configs.append(cfg)

        configs = c.configs.bulk_copy([cfg.id for cfg in configs])
        assert len(configs) == 3
        assert configs[0].name == 'My config 1 (copy 1)'
        assert configs[1].name == 'My config 2 (copy 1)'
        assert configs[2].name == 'My config 3 (copy 1)'

    def test_bulk_edit(self, c):
        configs = []
        for ii in range(1, 4):
            cfg = Config(
                name='My config {}'.format(ii),
                contents='testvar lanIp 1.1.1.1'
            )
            cfg = c.configs.create(cfg)
            configs.append(cfg)

        new='testvar lanIp 2.2.2.2'
        c.configs.bulk_edit(Config(contents=new), [cfg.id for cfg in configs])

        for cfg in configs:
            assert c.configs.get(cfg.id).contents == new

        new='testvar lanIp 1.1.1.1'
        c.configs.bulk_edit(Config(contents=new), [cfg.id for cfg in configs])

        for cfg in configs:
            assert c.configs.get(cfg.id).contents == new

        new_tags=['bar', 'buz', 'foo']
        new_testvars=[Testvar(name='lanIp', value='3.3.3.3')]
        c.configs.bulk_edit(Config(tags=new_tags), [cfg.id for cfg in configs], testvars=new_testvars)

        for cfg in configs:
            assert c.configs.get(cfg.id).tags == new_tags
            assert c.configs.get_testvar(cfg.id, 'lanIp').value == '3.3.3.3'

    @pytest.mark.skipif(cdrouter_version() < (13, 9, 1), reason="bulk upgrade endpoint added in 13.9.1")
    def test_bulk_upgrade(self, c):
        for ii in range(1, 4):
            cfg = Config(
                name='My config {}'.format(ii),
                contents='# i have not been upgraded'
            )
            cfg = c.configs.create(cfg)

        c.configs.bulk_upgrade(ids=[1, 3])

        for ii in range(1, 4):
            cfg = c.configs.get(ii)
            if ii in (1, 3):
                assert 'SECTION' in cfg.contents
            else:
                assert cfg.contents == '# i have not been upgraded'

        for ii in range(1, 4):
            cfg = c.configs.get(ii)
            cfg.contents = '# i have not been upgraded'
            c.configs.edit(cfg)
            cfg = c.configs.get(ii)
            assert cfg.contents == '# i have not been upgraded'

        c.configs.bulk_upgrade(filter=[field('id').eq(1), field('id').eq(3)], type='union')

        for ii in range(1, 4):
            cfg = c.configs.get(ii)
            if ii in (1, 3):
                assert 'SECTION' in cfg.contents
            else:
                assert cfg.contents == '# i have not been upgraded'

        for ii in range(1, 4):
            cfg = c.configs.get(ii)
            cfg.contents = '# i have not been upgraded'
            c.configs.edit(cfg)
            cfg = c.configs.get(ii)
            assert cfg.contents == '# i have not been upgraded'

        c.configs.bulk_upgrade(all=True)

        for ii in range(1, 4):
            cfg = c.configs.get(ii)
            assert 'SECTION' in cfg.contents

    def test_bulk_delete(self, c):
        cfg = Config(
            name='My config',
        )
        cfg = c.configs.create(cfg)

        cfg2 = Config(
            name='My config 2',
        )
        cfg2 = c.configs.create(cfg2)

        cfg3 = Config(
            name='My config 3',
        )
        cfg3 = c.configs.create(cfg3)

        cfg4 = Config(
            name='My config 4',
        )
        cfg4 = c.configs.create(cfg4)

        cfg5 = Config(
            name='My config 5',
        )
        cfg5 = c.configs.create(cfg5)

        c.configs.bulk_delete([cfg2.id, cfg3.id])
        c.configs.get(cfg.id)
        with pytest.raises(CDRouterError, match='no such config'):
            c.configs.get(cfg2.id)
        with pytest.raises(CDRouterError, match='no such config'):
            c.configs.get(cfg3.id)

        c.configs.bulk_delete(filter=[field('id').ge(cfg4.id)])
        c.configs.get(cfg.id)
        with pytest.raises(CDRouterError, match='no such config'):
            c.configs.get(cfg4.id)
        with pytest.raises(CDRouterError, match='no such config'):
            c.configs.get(cfg5.id)

    def test_list_testvars(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        cfg = c.configs.get_by_name('example.conf')

        testvars = c.configs.list_testvars(cfg.id)
        assert len(testvars) > 0
        assert testvars[0].group == 'main'
        assert testvars[0].name == 'DNStoDHCP'
        assert testvars[0].value == 'no'
        assert testvars[0].default == 'no'
        assert testvars[0].isdefault is True
        assert testvars[0].line == 0

    def test_get_testvar(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        cfg = c.configs.get_by_name('example.conf')

        testvar = c.configs.get_testvar(cfg.id, 'wanInterface')
        assert testvar.group == 'main'
        assert testvar.name == 'wanInterface'
        assert testvar.value == 'eth0'
        assert testvar.default == 'eth2'
        assert testvar.isdefault is False
        assert testvar.line == 26

    def test_edit_testvar(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        cfg = c.configs.get_by_name('example.conf')

        testvar = c.configs.get_testvar(cfg.id, 'lanMode')
        assert testvar.value == 'DHCP'

        new = 'none'
        testvar.value = new
        testvar = c.configs.edit_testvar(cfg.id, testvar)
        assert testvar.value == new

        testvar = c.configs.get_testvar(cfg.id, 'lanMode')
        assert testvar.value == new

    def test_delete_testvar(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        cfg = c.configs.get_by_name('example.conf')

        testvar = c.configs.get_testvar(cfg.id, 'lanMode')
        assert testvar.value == 'DHCP'
        old = testvar.value

        new = 'none'
        testvar.value = new
        testvar = c.configs.edit_testvar(cfg.id, testvar)
        assert testvar.value == new

        testvar = c.configs.get_testvar(cfg.id, 'lanMode')
        assert testvar.value == new

        c.configs.delete_testvar(cfg.id, 'lanMode')

        testvar = c.configs.get_testvar(cfg.id, 'lanMode')
        assert testvar.value == old
        assert testvar.isdefault is True

    def test_bulk_edit_testvars(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        cfg = c.configs.get_by_name('example.conf')
        assert c.configs.get_testvar(cfg.id, 'lanIp').value == '192.168.1.1'
        assert c.configs.get_testvar(cfg.id, 'lanInterface').value == 'none'

        testvars = [
            Testvar(name='lanIp', value='1.2.3.4'),
            Testvar(name='lanInterface', value='eth0')
        ]

        testvars = c.configs.bulk_edit_testvars(cfg.id, testvars)
        assert len(testvars) > 0
        assert c.configs.get_testvar(cfg.id, 'lanIp').value == '1.2.3.4'
        assert c.configs.get_testvar(cfg.id, 'lanInterface').value == 'eth0'
