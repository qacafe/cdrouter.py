#
# Copyright (c) 2022-2023 by QA Cafe.
# All Rights Reserved.
#

from os import environ
import pytest
import requests
from requests.exceptions import SSLError

from cdrouter.cdrouter import CDRouter, CDRouterError
from cdrouter.configs import ConfigSchema

from .utils import my_cdrouter, my_c, my_c_https, import_all_from_file # pylint: disable=unused-import

getuser_count = 0
getpass_count = 0

class TestCDRouter:
    def test_cdrouter(self, c, c_https):
        u = c.users.get_by_name('admin')
        assert u.name == 'admin'
        u = c_https.users.get_by_name('admin')
        assert u.name == 'admin'

        c2 = CDRouter(c.base+'////', insecure=c.insecure, token=u.token)
        u = c2.users.get_by_name('admin')
        assert u.name == 'admin'

    def test_token(self, c):
        u = c.users.get_by_name('admin')

        prefs = c.system.get_preferences()
        prefs.automatic_login = False
        c.system.edit_preferences(prefs)

        c2 = CDRouter(c.base, insecure=c.insecure, token=u.token)
        c2.system.hostname()

        orig_cdrouter_api_token = None
        if 'CDROUTER_API_TOKEN' in environ:
            orig_cdrouter_api_token = environ.get('CDROUTER_API_TOKEN')
        environ['CDROUTER_API_TOKEN'] = u.token
        c2 = CDRouter(c.base, insecure=c.insecure)
        del environ['CDROUTER_API_TOKEN']
        if orig_cdrouter_api_token is not None:
            environ['CDROUTER_API_TOKEN'] = orig_cdrouter_api_token
        c2.system.hostname()

        c2 = CDRouter(c.base, insecure=c.insecure, token='invalid')
        with pytest.raises(CDRouterError, match='invalid token'):
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

    def test_exclude_unknown_fields_single_response(self, c):
        resp = requests.models.Response()
        resp.status_code = 200
        resp._content = '{"data": {"name": "foo.conf"}}'.encode("utf-8") # pylint: disable=protected-access
        resp.encoding = "utf-8"
        schema = ConfigSchema()
        cfg = c.decode(schema, resp)
        assert cfg.name == 'foo.conf'

        resp = requests.models.Response()
        resp.status_code = 200
        resp._content = '{"data": {"name": "foo.conf", "unknown_field": "unknown_value"}}'.encode("utf-8") # pylint: disable=protected-access
        resp.encoding = "utf-8"
        schema = ConfigSchema()
        cfg = c.decode(schema, resp)
        assert cfg.name == 'foo.conf'

    def test_exclude_unknown_fields_many_response(self, c):
        resp = requests.models.Response()
        resp.status_code = 200
        resp._content = '{"data": [{"name": "foo.conf"}]}'.encode("utf-8") # pylint: disable=protected-access
        resp.encoding = "utf-8"
        schema = ConfigSchema()
        cfgs = c.decode(schema, resp, many=True)
        assert len(cfgs) == 1
        assert cfgs[0].name == 'foo.conf'

        resp = requests.models.Response()
        resp.status_code = 200
        resp._content = '{"data": [{"name": "foo.conf", "unknown_field": "unknown_value"}]}'.encode("utf-8") # pylint: disable=protected-access
        resp.encoding = "utf-8"
        schema = ConfigSchema()
        cfgs = c.decode(schema, resp, many=True)
        assert len(cfgs) == 1
        assert cfgs[0].name == 'foo.conf'

    def test_exclude_unknown_fields_error_response(self, c):
        resp = requests.models.Response()
        resp.status_code = 400
        resp._content = '{"error": "foobar"}'.encode("utf-8") # pylint: disable=protected-access
        resp.encoding = "utf-8"
        with pytest.raises(CDRouterError, match='foobar'):
            c.raise_for_status(resp)

        resp = requests.models.Response()
        resp.status_code = 400
        resp._content = '{"error": "foobar", "unknown_field": "unknown_value"}'.encode("utf-8") # pylint: disable=protected-access
        resp.encoding = "utf-8"
        with pytest.raises(CDRouterError, match='foobar'):
            c.raise_for_status(resp)
