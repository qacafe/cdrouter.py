#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

from .utils import my_cdrouter, my_c # pylint: disable=unused-import

class TestTestsuites:
    def test_info(self, c):
        info = c.testsuites.info()
        assert 'Version' in info.build_info
        assert 'QA Cafe' in info.copyright
        assert 'ipv6' in info.all_addons

    def test_search(self, c):
        results = c.testsuites.search('ipv6')
        assert len(results.addons) > 0
        assert len(results.modules) > 0
        assert len(results.tests) > 0
        assert len(results.reasons) > 0
        assert len(results.errors) > 0
        assert len(results.testvars) > 0

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
        assert group.name == 'CDRouter'
        assert group.test_count > 0
        assert 'basic.tcl' in group.modules

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
        assert module.name == 'basic.tcl'
        assert 'cdrouter_basic_1' in module.tests

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
        assert test.name == 'cdrouter_basic_1'
        assert test.synopsis == 'Router responds to ARP request on LAN interface'

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
        assert label.name == 'requires-ipv6'

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
        assert error.name == 'incompatible-package-versions'

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
        assert testvar.name == 'lanip'
        assert testvar.display == 'lanIp'
