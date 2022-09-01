#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import pytest

from cdrouter.cdrouter import CDRouterError

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestAlerts:
    def test_list(self, c):
        import_all_from_file(c, 'tests/testdata/example4.gz')

        (alerts, links) = c.alerts.list(20220831203101)
        assert len(alerts) == 25
        assert links.total == 608

    def test_iter_list(self, c):
        import_all_from_file(c, 'tests/testdata/example4.gz')

        assert len(list(c.alerts.iter_list(20220831203101))) == 608

    def test_get(self, c):
        import_all_from_file(c, 'tests/testdata/example4.gz')

        a = c.alerts.get(20220831203101, 1)
        assert a.id == 20220831203101
        assert a.idx == 1
        assert a.seq == 10
        assert a.loop == 1
        assert a.test_name == 'cdrouter_dhcp_server_200'
        assert a.test_description == 'Verify DHCP server rejects DHCPREQUESTS with IP address of other clients'
        assert a.category == 'Potential Corporate Privacy Violation'
        assert 'CDRouter detected' in a.description
        assert a.dest_ip == '142.250.65.174'
        assert a.dest_port == 80
        assert a.interface == 'ics'
        assert 'SEVBRCA' in a.payload
        assert 'HEAD' in a.payload_ascii
        assert '48 45 41' in a.payload_hex
        assert a.proto == 'TCP'
        assert a.references == ['http://tools.ietf.org/html/rfc7435']
        assert a.rev == 1
        assert 'alert tcp any any' in a.rule
        assert a.rule_set == 'QACAFE POLICY'
        assert a.severity == 1
        assert a.sid == 3000007
        assert a.signature == 'CDRouter detected an unencrypted outbound HTTP connection'
        assert a.src_ip == '202.254.1.2'
        assert a.src_port == 38761

        with pytest.raises(CDRouterError, match='no such alert'):
            c.alerts.get(20220831203101, 99999)

        with pytest.raises(CDRouterError, match='no such result'):
            c.alerts.get(99999, 99999)

    def test_all_stats(self, c):
        import_all_from_file(c, 'tests/testdata/example4.gz')

        stats = c.alerts.all_stats(20220831203101)
        assert len(stats.severities) == 5
        assert stats.severities[1].name == 'High Severity'
        assert stats.severities[1].severity == 1
        assert stats.severities[1].count == 608
        assert len(stats.categories) == 1
        assert stats.categories[0].category == 'Potential Corporate Privacy Violation'
        assert stats.categories[0].severity == 1
        assert stats.categories[0].count == 608
        assert len(stats.rule_sets) == 1
        assert stats.rule_sets[0].name == 'QACAFE POLICY'
        assert stats.rule_sets[0].count == 608
        assert len(stats.signatures) == 3
        assert stats.signatures[0].signature == 'CDRouter detected an unencrypted outbound HTTP connection'
        assert stats.signatures[0].severity == 1
        assert stats.signatures[0].count == 530
        assert len(stats.tests) == 70
        assert stats.tests[0].name == 'cdrouter_dhcp_server_200'
        assert stats.tests[0].count == 6
        assert len(stats.frequent_sources) == 7
        assert stats.frequent_sources[0].addr == '202.254.1.2'
        assert stats.frequent_sources[0].count == 570
        assert len(stats.frequent_destinations) == 15
        assert stats.frequent_destinations[0].addr == '142.250.65.196'
        assert stats.frequent_destinations[0].count == 67

        with pytest.raises(CDRouterError, match='no such result'):
            c.alerts.all_stats(99999)
