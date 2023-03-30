#
# Copyright (c) 2022-2023 by QA Cafe.
# All Rights Reserved.
#

import shutil
import pytest

from cdrouter.cdrouter import CDRouterError
from cdrouter.devices import Device
from cdrouter.filters import Field as field
from cdrouter.users import User

from .utils import cdrouter_version, my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestDevices:
    def test_list(self, c):
        (devices, links) = c.devices.list()
        assert links.total == 0
        assert len(devices) == 0

        for ii in range(1, 6):
            d = Device(
                name='My device {}'.format(ii),
            )
            c.devices.create(d)

        (devices, links) = c.devices.list(limit=1)
        assert links.total == 5
        assert links.last == 5

    def test_iter_list(self, c):
        assert len(list(c.devices.iter_list(limit=1))) == 0

        for ii in range(1, 51):
            d = Device(
                name='My device {}'.format(ii),
            )
            c.devices.create(d)

        assert len(list(c.devices.iter_list(limit=1))) == 50

    def test_get(self, c):
        d = Device(
            name='My device',
        )
        d = c.devices.create(d)

        d2 = c.devices.get(d.id)
        assert d2.name == d.name

        with pytest.raises(CDRouterError, match='no such device'):
            c.devices.get(9999)

    def test_get_by_name(self, c):
        d = Device(
            name='My device',
        )
        d = c.devices.create(d)

        d2 = c.devices.get_by_name('My device')
        assert d2.name == d.name

    def test_create(self, c):
        d = Device(
            name='My device',
            tags=['bar', 'buz', 'foo'],
            default_ip='1.1.1.1',
            default_login='admin',
            default_password='cdrouter',
            default_ssid='qacafe',
            location='here',
            device_category='device',
            manufacturer='some company',
            manufacturer_oui='00:11:22',
            model_name='cool device',
            model_number='12345',
            description='such a cool device',
            product_class='device class',
            serial_number='NTA1000vY-NNN',
            hardware_version='v1.2.3',
            software_version='v3.2.1',
            provisioning_code='12345',
            note='my note',
            insecure_mgmt_url=False,
            mgmt_url='https://device.lan',
            add_mgmt_addr=True,
            mgmt_interface='eth0',
            mgmt_addr='1.1.1.2/24',
            power_on_cmd='./power on',
            power_off_cmd='./power off',
        )
        d2 = c.devices.create(d)

        d2 = c.devices.get(d2.id)
        assert d2.name == d.name
        assert d2.tags == d.tags
        assert d2.default_ip == d.default_ip
        assert d2.default_login == d.default_login
        assert d2.default_password == d.default_password
        # default_ssid field added in 13.8.1
        if cdrouter_version() >= (13, 8, 1):
            assert d2.default_ssid == d.default_ssid
        assert d2.location == d.location
        assert d2.device_category == d.device_category
        assert d2.manufacturer == d.manufacturer
        assert d2.manufacturer_oui == d.manufacturer_oui
        assert d2.model_name == d.model_name
        assert d2.model_number == d.model_number
        assert d2.description == d.description
        assert d2.product_class == d.product_class
        assert d2.serial_number == d.serial_number
        assert d2.hardware_version == d.hardware_version
        assert d2.software_version == d.software_version
        assert d2.provisioning_code == d.provisioning_code
        assert d2.note == d.note
        assert d2.insecure_mgmt_url == d.insecure_mgmt_url
        assert d2.mgmt_url == d.mgmt_url
        assert d2.add_mgmt_addr == d.add_mgmt_addr
        assert d2.mgmt_interface == d.mgmt_interface
        assert d2.mgmt_addr == d.mgmt_addr
        assert d2.power_on_cmd == d.power_on_cmd
        assert d2.power_off_cmd == d.power_off_cmd

    def test_edit(self, c):
        d = Device(
            name='My device',
            tags=['bar', 'buz', 'foo'],
            default_ip='1.1.1.1',
            default_login='admin',
            default_password='cdrouter',
        )
        d2 = c.devices.create(d)

        d = c.devices.get_by_name('My device')
        d.name = 'My other device'
        d.tags = ['bar2', 'buz2', 'foo2']
        d2 = c.devices.edit(d)
        assert d2.name == d.name
        assert d2.tags == d.tags

    def test_delete(self, c):
        assert len(list(c.devices.iter_list())) == 0

        d = Device(
            name='My device',
            tags=['bar', 'buz', 'foo'],
            default_ip='1.1.1.1',
            default_login='admin',
            default_password='cdrouter',
        )
        d2 = c.devices.create(d)

        assert len(list(c.devices.iter_list())) == 1

        c.devices.delete(d2.id)

        assert len(list(c.devices.iter_list())) == 0

        with pytest.raises(CDRouterError, match='no such device'):
            c.devices.get(d2.id)

    def test_lock(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        d = c.devices.get_by_name('Cisco E4200')
        assert d.locked is False

        d = c.devices.lock(d.id)
        assert d.locked is True

        # locking a locked resource is a no-op, not an error
        c.devices.lock(d.id)
        c.devices.lock(d.id)
        c.devices.lock(d.id)

        d = c.devices.get(d.id)
        assert d.locked is True

        with pytest.raises(CDRouterError, match='cannot delete locked device'):
            c.devices.delete(d.id)

    def test_unlock(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        d = c.devices.get_by_name('Cisco E4200')
        assert d.locked is False

        d = c.devices.lock(d.id)
        assert d.locked is True

        with pytest.raises(CDRouterError, match='cannot delete locked device'):
            c.devices.delete(d.id)

        d = c.devices.unlock(d.id)
        assert d.locked is False

        # unlocking an unlocked resource is a no-op, not an error
        c.devices.unlock(d.id)
        c.devices.unlock(d.id)
        c.devices.unlock(d.id)

        d = c.devices.get(d.id)
        assert d.locked is False

        c.devices.delete(d.id)

        with pytest.raises(CDRouterError, match='no such device'):
            c.devices.get(d.id)

    def test_get_shares(self, c):
        u = User(
            admin=True,
            name='admin2',
            description='im an admin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u = c.users.create(u)

        d = Device(
            name='My device',
            tags=['bar', 'buz', 'foo'],
            default_ip='1.1.1.1',
            default_login='admin',
            default_password='cdrouter',
        )
        d = c.devices.create(d)

        assert len(c.devices.get_shares(d.id)) == 0

        c.devices.edit_shares(d.id, [u.id])

        shares = c.devices.get_shares(d.id)
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

        d = Device(
            name='My device',
            tags=['bar', 'buz', 'foo'],
            default_ip='1.1.1.1',
            default_login='admin',
            default_password='cdrouter',
        )
        d = c.devices.create(d)

        assert len(c.devices.get_shares(d.id)) == 0

        c.devices.edit_shares(d.id, [u.id, u2.id])

        shares = c.devices.get_shares(d.id)
        assert len(shares) == 2
        assert shares[0].user_id == u.id
        assert shares[0].read is True
        assert shares[0].write is False
        assert shares[0].execute is False
        assert shares[1].user_id == u2.id
        assert shares[1].read is True
        assert shares[1].write is False
        assert shares[1].execute is False

        c.devices.edit_shares(d.id, [u.id])

        shares = c.devices.get_shares(d.id)
        assert len(shares) == 1
        assert shares[0].user_id == u.id
        assert shares[0].read is True
        assert shares[0].write is False
        assert shares[0].execute is False

        c.devices.edit_shares(d.id, [])

        shares = c.devices.get_shares(d.id)
        assert len(shares) == 0

    def test_export(self, c, tmp_path):
        import_all_from_file(c, 'tests/testdata/example.gz')

        d = c.devices.get_by_name('Cisco E4200')

        (b, filename) = c.devices.export(d.id)

        filename = '{}/{}'.format(tmp_path, 'example.gz')
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

        c.devices.delete(d.id)

        with pytest.raises(CDRouterError, match='no such device'):
            c.devices.get_by_name('Cisco E4200')

        import_all_from_file(c, filename)

        d = c.devices.get_by_name('Cisco E4200')

    def test_get_connection(self, c):
        d = Device(
            name='My device',
            mgmt_url='http://1.1.1.1',
            add_mgmt_addr=True,
            mgmt_interface='eth0',
            mgmt_addr='1.1.1.2/24'
        )
        d = c.devices.create(d)

        with pytest.raises(CDRouterError, match='no device connection'):
            c.devices.get_connection(d.id)

        c.devices.connect(d.id)

        conn = c.devices.get_connection(d.id)
        assert conn.proxy_port > 0
        assert conn.proxy_https > 0

    def test_connect(self, c):
        d = Device(
            name='My device',
            mgmt_url='http://1.1.1.1',
            add_mgmt_addr=True,
            mgmt_interface='eth0',
            mgmt_addr='1.1.1.2/24'
        )
        d = c.devices.create(d)

        conn = c.devices.connect(d.id)
        assert conn.proxy_port > 0
        assert conn.proxy_https > 0

    def test_disconnect(self, c):
        d = Device(
            name='My device',
            mgmt_url='http://1.1.1.1',
            add_mgmt_addr=True,
            mgmt_interface='eth0',
            mgmt_addr='1.1.1.2/24'
        )
        d = c.devices.create(d)

        with pytest.raises(CDRouterError, match='no device connection'):
            c.devices.get_connection(d.id)

        c.devices.connect(d.id)
        c.devices.get_connection(d.id)
        c.devices.disconnect(d.id)

        with pytest.raises(CDRouterError, match='no device connection'):
            c.devices.get_connection(d.id)

    def test_power_on(self, c):
        d = Device(
            name='My device',
            power_on_cmd='echo -n hello',
        )
        d = c.devices.create(d)

        cmd = c.devices.power_on(d.id)
        assert cmd.output == 'hello'

    def test_power_off(self, c):
        d = Device(
            name='My device',
            power_off_cmd='echo -n hello',
        )
        d = c.devices.create(d)

        cmd = c.devices.power_off(d.id)
        assert cmd.output == 'hello'

    def test_bulk_export(self, c, tmp_path):
        devices = []
        for ii in range(1, 6):
            d = Device(
                name='My device {}'.format(ii),
            )
            d = c.devices.create(d)
            devices.append(d)

        for d in devices:
            c.devices.get(d.id)

        (b, filename) = c.devices.bulk_export([d.id for d in devices])

        filename = '{}/{}'.format(tmp_path, 'example.gz')
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

        c.devices.bulk_delete([d.id for d in devices])

        for d in devices:
            with pytest.raises(CDRouterError, match='no such device'):
                c.devices.get(d.id)

        import_all_from_file(c, filename)

        for d in devices:
            d = c.devices.get_by_name(d.name)

    def test_bulk_copy(self, c):
        devices = []
        for ii in range(1, 4):
            d = Device(
                name='My device {}'.format(ii),
            )
            d = c.devices.create(d)
            devices.append(d)

        devices = c.devices.bulk_copy([d.id for d in devices])
        assert len(devices) == 3
        assert devices[0].name == 'My device 1 (copy 1)'
        assert devices[1].name == 'My device 2 (copy 1)'
        assert devices[2].name == 'My device 3 (copy 1)'

    def test_bulk_edit(self, c):
        devices = []
        for ii in range(1, 4):
            d = Device(
                name='My device {}'.format(ii),
                mgmt_url='http://3.3.3.3',
            )
            d = c.devices.create(d)
            devices.append(d)

        new = 'http://1.1.1.1'
        c.devices.bulk_edit(Device(mgmt_url=new), [d.id for d in devices])

        for d in devices:
            assert c.devices.get(d.id).mgmt_url == new

        new = 'http://2.2.2.2'
        c.devices.bulk_edit(Device(mgmt_url=new), [d.id for d in devices])

        for d in devices:
            assert c.devices.get(d.id).mgmt_url == new

    def test_bulk_delete(self, c):
        d = Device(
            name='My device',
        )
        d = c.devices.create(d)

        d2 = Device(
            name='My device 2',
        )
        d2 = c.devices.create(d2)

        d3 = Device(
            name='My device 3',
        )
        d3 = c.devices.create(d3)

        d4 = Device(
            name='My device 4',
        )
        d4 = c.devices.create(d4)

        d5 = Device(
            name='My device 5',
        )
        d5 = c.devices.create(d5)

        c.devices.bulk_delete([d2.id, d3.id])
        c.devices.get(d.id)
        with pytest.raises(CDRouterError, match='no such device'):
            c.devices.get(d2.id)
        with pytest.raises(CDRouterError, match='no such device'):
            c.devices.get(d3.id)

        c.devices.bulk_delete(filter=[field('id').ge(d4.id)])
        c.devices.get(d.id)
        with pytest.raises(CDRouterError, match='no such device'):
            c.devices.get(d4.id)
        with pytest.raises(CDRouterError, match='no such device'):
            c.devices.get(d5.id)
