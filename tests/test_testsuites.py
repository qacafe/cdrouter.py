#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import pytest

from cdrouter.cdrouter import CDRouterError

from .utils import my_cdrouter, my_c # pylint: disable=unused-import

class TestTestsuites:
    def test_info(self, c):
        info = c.testsuites.info()
        assert 'Version' in info.build_info
        assert 'QA Cafe' in info.copyright
        assert isinstance(info.id, int)
        assert isinstance(info.license_type, str)
        assert isinstance(info.customer, str)
        assert isinstance(info.lifetime, str)
        assert isinstance(info.killtime, str)
        assert isinstance(info.nag, bool)
        assert isinstance(info.os, str)
        assert isinstance(info.os_type, str)
        assert isinstance(info.serial_number, str)
        assert isinstance(info.system_id, str)
        assert isinstance(info.testsuite, str)
        assert isinstance(info.release, str)
        assert 'ipv6' in info.addons
        assert 'ipv6' in info.all_addons
        assert len(info.interfaces) == 1
        assert info.interfaces[0].name is None
        assert info.interfaces[0].value == 'eth0'
        assert info.interfaces[0].is_wireless is False
        assert info.interfaces[0].is_ics is False
        assert isinstance(info.execute_instances, int)
        assert isinstance(info.license_info.is_expired, bool)
        assert isinstance(info.license_info.expires_date, str)
        assert isinstance(info.license_info.expires_in, int)

    def test_search(self, c):
        results = c.testsuites.search('ipv6')
        assert len(results.addons) > 0
        assert results.addons[0].id > 0
        assert len(results.modules) > 0
        assert results.modules[0].id > 0
        assert len(results.tests) > 0
        assert results.tests[0].id > 0
        assert len(results.reasons) > 0
        assert results.reasons[0].id > 0
        assert len(results.errors) > 0
        assert results.errors[0].id > 0
        assert len(results.testvars) > 0
        assert results.testvars[0].id > 0

        c.testsuites.search('asdfasdfasdfaasflkjhasdflkjasdflk')

    def test_update(self, c):
        c.testsuites.update()

    def test_list_groups(self, c):
        names = []
        for x in c.testsuites.list_groups(sort='+name'):
            names.append(x.name)
        names2 = []
        for x in c.testsuites.list_groups(sort='-name'):
            names2.append(x.name)
        names2.reverse()
        assert names == names2

    def test_get_group(self, c):
        group = c.testsuites.get_group('CDRouter')
        assert group.id > 0
        assert group.name == 'CDRouter'
        assert group.index > 0
        assert group.test_count > 0
        assert 'basic.tcl' in group.modules

        with pytest.raises(CDRouterError, match='no such group'):
            c.testsuites.get_group('foo')

    def test_list_modules(self, c):
        names = []
        for x in c.testsuites.list_modules(sort='+name'):
            names.append(x.name)
        names2 = []
        for x in c.testsuites.list_modules(sort='-name'):
            names2.append(x.name)
        names2.reverse()
        assert names == names2

    def test_get_module(self, c):
        module = c.testsuites.get_module('basic.tcl')
        assert module.id > 0
        assert module.name == 'basic.tcl'
        assert module.index == 0
        assert module.group == 'CDRouter'
        assert 'Initial connectivity tests' in module.description
        assert module.test_count > 0
        assert 'cdrouter_basic_1' in module.tests
        assert 'requires-ipv4' in module.labels
        assert isinstance(module.aliases, list)

        with pytest.raises(CDRouterError, match='no such module'):
            c.testsuites.get_module('foo')

    def test_list_tests(self, c):
        names = []
        for x in c.testsuites.list_tests(sort='+name'):
            names.append(x.name)
        names2 = []
        for x in c.testsuites.list_tests(sort='-name'):
            names2.append(x.name)
        names2.reverse()
        assert names == names2

    def test_get_test(self, c):
        test = c.testsuites.get_test('cdrouter_basic_1')
        assert test.id > 0
        assert test.name == 'cdrouter_basic_1'
        assert test.index == 0
        assert test.group == 'CDRouter'
        assert test.module == 'basic.tcl'
        assert test.synopsis == 'Router responds to ARP request on LAN interface'
        assert 'step 1' in test.description
        assert isinstance(test.labels, list)
        assert isinstance(test.aliases, list)
        assert isinstance(test.testvars, list)
        assert test.skip_name is None
        assert test.skip_reason is None

        with pytest.raises(CDRouterError, match='no such test'):
            c.testsuites.get_test('foo')

    def test_list_labels(self, c):
        names = []
        for x in c.testsuites.list_labels(sort='+name'):
            names.append(x.name)
        names2 = []
        for x in c.testsuites.list_labels(sort='-name'):
            names2.append(x.name)
        names2.reverse()
        assert names == names2

    def test_get_label(self, c):
        label = c.testsuites.get_label('requires-ipv6')
        assert label.id > 0
        assert label.name == 'requires-ipv6'
        assert label.index > 0
        assert 'IPv6' in label.reason
        assert 'IPv6' in label.description
        assert 'dslite.tcl' in label.modules
        assert 'tr143_http_101' in label.tests

        with pytest.raises(CDRouterError, match='no such label'):
            c.testsuites.get_label('foo')

    def test_list_errors(self, c):
        names = []
        for x in c.testsuites.list_errors(sort='+name'):
            names.append(x.name)
        names2 = []
        for x in c.testsuites.list_errors(sort='-name'):
            names2.append(x.name)
        names2.reverse()
        assert names == names2

    def test_get_error(self, c):
        error = c.testsuites.get_error('incompatible-package-versions')
        assert error.id > 0
        assert error.name == 'incompatible-package-versions'
        assert error.index > 0
        assert 'versions' in error.description

        with pytest.raises(CDRouterError, match='no such error'):
            c.testsuites.get_error('foo')

    def test_list_testvars(self, c):
        names = []
        for x in c.testsuites.list_testvars(sort='+name'):
            names.append(x.name)
        names2 = []
        for x in c.testsuites.list_testvars(sort='-name'):
            names2.append(x.name)
        names2.reverse()
        assert names == names2

    def test_get_testvar(self, c):
        testvar = c.testsuites.get_testvar('lanIp')
        assert testvar.id > 0
        assert testvar.name == 'lanip'
        assert testvar.index > 0
        assert testvar.humanname == 'DUT\'s LAN Address'
        assert testvar.display == 'lanIp'
        assert testvar.dataclass == 'IPv4'
        assert testvar.addedin == ''
        assert testvar.deprecatedin == ''
        assert testvar.obsoletedin == ''
        assert testvar.min == ''
        assert testvar.max == ''
        assert testvar.length == ''
        assert 'This parameter' in testvar.description
        assert testvar.default == '192.168.1.1'
        assert testvar.defaultdisabled is False
        assert testvar.dyndefault is True
        assert isinstance(testvar.keywords, list)
        assert len(testvar.alsoaccept) == 0
        assert testvar.wildcard is False
        assert testvar.instances == 0
        assert testvar.parent == ''
        assert isinstance(testvar.children, list)
        assert isinstance(testvar.tests, list)

        with pytest.raises(CDRouterError, match='no such testvar'):
            c.testsuites.get_testvar('foo')
