#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import pytest
from requests.exceptions import SSLError

from cdrouter.cdrouter import CDRouter, CDRouterError

from .utils import my_cdrouter, my_c, my_c_https, import_all_from_file # pylint: disable=unused-import

getuser_count = 0
getpass_count = 0

class TestCDRouter:
    def test_cdrouter(self, c, c_https):
        u = c.users.get_by_name('admin')
        assert u.name == 'admin'
        u = c_https.users.get_by_name('admin')
        assert u.name == 'admin'

    def test_token(self, c):
        u = c.users.get_by_name('admin')

        prefs = c.system.get_preferences()
        prefs.automatic_login = False
        c.system.edit_preferences(prefs)

        c2 = CDRouter(c.base, insecure=c.insecure, token=u.token)
        c2.system.hostname()

    def test_username_password(self, c):
        u = c.users.get_by_name('admin')

        new_password = 'cdrouter2'
        c.users.change_password(u.id, new_password)

        prefs = c.system.get_preferences()
        prefs.automatic_login = False
        c.system.edit_preferences(prefs)

        c2 = CDRouter(c.base, insecure=c.insecure, username=u.name, password=new_password)
        c2.system.hostname()

    def test_getuser_getpass(self, c):
        u = c.users.get_by_name('admin')

        new_password = 'cdrouter2'
        c.users.change_password(u.id, new_password)

        prefs = c.system.get_preferences()
        prefs.automatic_login = False
        c.system.edit_preferences(prefs)

        def my_getuser(base): # pylint: disable=unused-argument
            return u.name

        def my_getpass(base, username): # pylint: disable=unused-argument
            return new_password

        c2 = CDRouter(c.base, insecure=c.insecure, _getuser=my_getuser, _getpass=my_getpass)
        c2.system.hostname()

    def test_retries(self, c):
        u = c.users.get_by_name('admin')

        prefs = c.system.get_preferences()
        prefs.automatic_login = False
        c.system.edit_preferences(prefs)

        c2 = CDRouter(c.base, insecure=c.insecure, token=u.token)
        c2.system.hostname()

        retries = 5

        global getuser_count # pylint: disable=global-statement
        getuser_count = 0
        def my_getuser(base): # pylint: disable=unused-argument
            global getuser_count # pylint: disable=global-statement
            getuser_count += 1
            return 'admin'

        global getpass_count # pylint: disable=global-statement
        getpass_count = 0
        def my_getpass(base, username): # pylint: disable=unused-argument
            global getpass_count # pylint: disable=global-statement
            getpass_count += 1
            return 'invalid'

        c2 = CDRouter(c.base, insecure=c.insecure, _getuser=my_getuser, _getpass=my_getpass, retries=retries)

        with pytest.raises(CDRouterError, match='invalid username or password'):
            c2.system.hostname()

        assert getuser_count == 1
        assert getpass_count == retries + 1

    def test_insecure(self, c_https):
        c2 = CDRouter(c_https.base, insecure=True)
        c2.system.hostname()

        c2 = CDRouter(c_https.base, insecure=False)

        with pytest.raises(SSLError, match='certificate verify failed'):
            c2.system.hostname()
