#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import datetime
from os.path import basename
import shutil
import tarfile

from .utils import my_cdrouter, my_c, my_copy_file_from_container # pylint: disable=unused-import

class TestSystem:
    def test_manual_upgrade(self, cdrouter, copy_file_from_container):
        container = cdrouter['container']
        c = cdrouter['c']

        path = copy_file_from_container(container, '/cdrouter-*.rpm')
        with open(path, 'rb') as fd: # pylint: disable=unspecified-encoding
            upgrade = c.system.manual_upgrade(fd, basename(path))

        assert 'Complete!' in upgrade.output

        c.system.hostname()

    def test_manual_update_license(self, cdrouter, copy_file_from_container):
        container = cdrouter['container']
        c = cdrouter['c']

        path = copy_file_from_container(container, '/usr/cdrouter-data/etc/*.lic')
        with open(path, 'rb') as fd: # pylint: disable=unspecified-encoding
            c.system.manual_update_license(fd, basename(path))

        c.system.hostname()

    def test_shutdown(self, c):
        c.system.shutdown()

    def test_poweroff(self, c):
        c.system.poweroff()

    def test_restart(self, c):
        c.system.restart()

    def test_reboot(self, c):
        c.system.reboot()

    def test_info(self, c):
        assert 'Started cdrouter-cli' in c.system.info()

    def test_diagnostics(self, c, tmp_path):
        tmp_path = str(tmp_path)
        (b, filename) = c.system.diagnostics()
        path = '{}/{}'.format(tmp_path, basename(filename))
        with open(path, 'wb') as fd:
            shutil.copyfileobj(b, fd)

        with tarfile.open(path, mode='r') as tar:
            for member in tar.getmembers():
                print(member)

    def test_time(self, c):
        time = c.system.time()
        assert str(datetime.date.today().year) in time

    def test_space(self, c):
        space = c.system.space()
        assert space.avail > 0
        assert space.path == '/usr/cdrouter-data'
        assert space.pcent > 0
        assert space.size > 0
        assert space.unit == 'bytes'
        assert space.used > 0

    def test_hostname(self, c):
        assert c.system.hostname() != ''

    def test_interfaces(self, c):
        intfs = c.system.interfaces()
        assert len(intfs) == 2
        assert intfs[0].name == 'lo'
        assert intfs[1].name == 'eth0'

        intfs = c.system.interfaces(addresses=True)
        assert len(intfs) == 2
        assert intfs[0].name == 'lo'
        assert len(intfs[0].addresses) == 2
        assert intfs[0].addresses[0].address == '127.0.0.1/8'

    def test_in_use_interfaces(self, c):
        intfs = c.system.in_use_interfaces()
        assert len(intfs) == 1
        assert intfs[0].name == 'eth0'
        assert intfs[0].flags.in_use is False
        assert intfs[0].flags.is_wireless is False
        assert intfs[0].flags.is_ics is False

    def test_get_preferences(self, c):
        prefs = c.system.get_preferences()
        assert prefs.automatic_login is True
        assert prefs.port == 80
        assert prefs.https == 443

    def test_edit_preferences(self, c):
        prefs = c.system.get_preferences()
        new = 'invalid'
        prefs.lounge_url = new
        prefs = c.system.edit_preferences(prefs)
        assert prefs.lounge_url == new
        prefs = c.system.get_preferences()
        assert prefs.lounge_url == new
