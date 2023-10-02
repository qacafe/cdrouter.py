#
# Copyright (c) 2022-2023 by QA Cafe.
# All Rights Reserved.
#

import pytest

from cdrouter.cdrouter import CDRouterError
from cdrouter.filters import Field as field
from cdrouter.metrics import Bandwidth, Latency, ClientBandwidth

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestTestResults:
    def test_list(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        (trs, links) = c.tests.list(20220821222306)
        assert links.total == 4
        assert len(trs) == 4

    def test_iter_list(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        assert len(list(c.tests.iter_list(20220821222306, limit=1))) == 4

    def test_list_csv(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        csv = c.tests.list_csv(20220821222306)
        assert 'cdrouter_app_14,' in csv

    def test_get(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        tr = c.tests.get(20220821222306, 1)
        assert tr.id == 20220821222306
        assert tr.seq == 1
        assert tr.loop == 1
        assert tr.active is False
        assert tr.result == 'pass'
        assert tr.alerts == 0
        assert tr.retries == 0
        assert tr.duration == 92
        assert tr.flagged is False
        assert tr.name == 'start'
        assert tr.description == 'CDRouter Startup'
        assert tr.skip_name == ''
        assert tr.skip_reason == ''
        assert tr.log == 'start.txt'
        assert tr.keylog == ''
        assert tr.note == ''

        with pytest.raises(CDRouterError, match='no such test'):
            c.tests.get(20220821222306, 9999)

        with pytest.raises(CDRouterError, match='no such test'):
            c.tests.get(9999, 9999)

    def test_edit(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        tr = c.tests.get(20220821222306, 1)
        assert tr.flagged is False
        assert tr.note == ''

        new_flagged = True
        new_note = 'i am a note'
        tr.flagged = new_flagged
        tr.note = new_note

        tr = c.tests.edit(tr)
        assert tr.flagged is new_flagged
        assert tr.note == new_note

        tr = c.tests.get(20220821222306, 1)
        assert tr.flagged is new_flagged
        assert tr.note == new_note

    def test_list_log(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        log = c.tests.list_log(20220821222306, 1)
        assert log.offset == 0
        assert log.limit == 700000
        assert len(log.lines) == 558
        assert log.total == 558
        assert log.more is False
        assert 'Started cdrouter-cli' in log.lines[53].raw
        assert log.lines[53].line == 54
        assert log.lines[53].section is True
        assert log.lines[53].prefix == 'SECTION'
        assert log.lines[53].name == 'setup'
        assert log.lines[53].timestamp == '2022-08-21 22:23:12.722'
        assert log.lines[53].timestamp_display == ' 22:23:12.722'
        assert log.lines[53].message == 'Started cdrouter-cli Sun Aug 21 22:23:08 EDT 2022'
        assert log.lines[53].summary.errors == 0
        assert log.lines[53].summary.fails == 0
        assert log.lines[53].summary.passes == 0
        assert log.lines[53].summary.warnings == 0
        assert log.lines[53].summary.alerts == 0
        assert 'Who is 5.5.5.1' in log.lines[142].raw
        assert log.lines[142].line == 143
        assert log.lines[142].prefix == 'O>>>'
        assert log.lines[142].name == 'wan'
        assert log.lines[142].timestamp == '2022-08-21 22:23:35.364'
        assert log.lines[142].timestamp_display == ' 22:23:35.364'
        assert 'Who is 5.5.5.1' in log.lines[142].message
        assert log.lines[142].interface == 'wan'
        assert log.lines[142].packet == 1
        assert log.lines[142].src == 'b0:75:0c:40:41:26'
        assert log.lines[142].dst == 'ff:ff:ff:ff:ff:ff'
        assert log.lines[142].proto == 'ARP'
        assert log.lines[142].info == 'Who is 5.5.5.1, tell 5.5.5.1'

    def test_iter_list_log(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        lines = list(c.tests.iter_list_log(20220821222306, 1, limit=1))
        assert len(lines) == 558
        assert 'Started cdrouter-cli' in lines[53].raw
        assert lines[53].line == 54
        assert lines[53].section is True
        assert lines[53].prefix == 'SECTION'
        assert lines[53].name == 'setup'
        assert lines[53].timestamp == '2022-08-21 22:23:12.722'
        assert lines[53].timestamp_display == ' 22:23:12.722'
        assert lines[53].message == 'Started cdrouter-cli Sun Aug 21 22:23:08 EDT 2022'
        assert lines[53].summary.errors == 0
        assert lines[53].summary.fails == 0
        assert lines[53].summary.passes == 0
        assert lines[53].summary.warnings == 0
        assert lines[53].summary.alerts == 0
        assert 'Who is 5.5.5.1' in lines[142].raw
        assert lines[142].line == 143
        assert lines[142].prefix == 'O>>>'
        assert lines[142].name == 'wan'
        assert lines[142].timestamp == '2022-08-21 22:23:35.364'
        assert lines[142].timestamp_display == ' 22:23:35.364'
        assert 'Who is 5.5.5.1' in lines[142].message
        assert lines[142].interface == 'wan'
        assert lines[142].packet == 1
        assert lines[142].src == 'b0:75:0c:40:41:26'
        assert lines[142].dst == 'ff:ff:ff:ff:ff:ff'
        assert lines[142].proto == 'ARP'
        assert lines[142].info == 'Who is 5.5.5.1, tell 5.5.5.1'

    def test_get_log_plaintext(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        text = c.tests.get_log_plaintext(20220821222306, 1)
        assert 'Started cdrouter-cli' in text

    def test_list_metrics(self, c):
        import_all_from_file(c, 'tests/testdata/example5.gz')

        r = c.results.get(20230310111705)

        (metrics, links) = c.tests.list_metrics(r.id, 2)
        assert links.total == 2
        assert len(metrics) == 2

        assert metrics[0].id == 20230310111705
        assert metrics[0].seq == 2
        assert metrics[0].test_name == 'perf_multi_1'
        assert metrics[0].metric == 'bandwidth'
        assert metrics[0].filename == 'perf_multi_1_bandwidth_graph.csv'
        assert metrics[0].log_file is None
        assert metrics[1].id == 20230310111705
        assert metrics[1].seq == 2
        assert metrics[1].test_name == 'perf_multi_1'
        assert metrics[1].metric == 'client_bandwidth'
        assert metrics[1].filename == 'perf_multi_1_client_bandwidth_details_graph.1.csv'
        assert metrics[1].log_file is None

        (metrics, links) = c.tests.list_metrics(r.id, 2, filter=[field('metric').eq('client_bandwidth')], limit='none')
        assert links.total == 1
        assert len(metrics) == 1

        assert metrics[0].id == 20230310111705
        assert metrics[0].seq == 2
        assert metrics[0].test_name == 'perf_multi_1'
        assert metrics[0].metric == 'client_bandwidth'
        assert metrics[0].filename == 'perf_multi_1_client_bandwidth_details_graph.1.csv'
        assert metrics[0].log_file is None

        with pytest.raises(CDRouterError, match='no such test'):
            c.tests.list_metrics(999999, 2)

        with pytest.raises(CDRouterError, match='no such test'):
            c.tests.list_metrics(r.id, 999999)

    def test_get_test_metric(self, c):
        import_all_from_file(c, 'tests/testdata/example5.gz')

        r = c.results.get(20230310111705)

        metrics = c.tests.get_test_metric(r.id, 2, 'bandwidth')
        assert len(metrics) == 10
        assert isinstance(metrics[0], Bandwidth)
        assert metrics[0].log_file == 'perf_multi_1.txt'
        assert metrics[0].metric == 'bandwidth'
        assert metrics[0].bandwidth == 9416.015
        assert metrics[0].bandwidth_units == 'Mbits/sec'
        assert metrics[0].result == 'pass'
        assert metrics[0].client_interface == 'lan.*'
        assert metrics[0].server_interface == 'wan'
        assert metrics[0].streams == 10
        assert metrics[0].protocol == 'TCP'
        assert metrics[0].direction == 'download'
        assert metrics[0].loss_percentage == 0.0
        assert metrics[0].loss_percentage_units == 'Percentage'
        assert metrics[0].client_device is None
        assert metrics[0].server_device is None
        assert metrics[0].seq is None

        metrics = c.tests.get_test_metric(r.id, 2, 'client_bandwidth')
        assert len(metrics) == 33
        assert isinstance(metrics[0], ClientBandwidth)
        assert metrics[0].num_rates == 10
        assert len(metrics[0].rates) == 10
        assert metrics[0].rates[0] == 941.608

        import_all_from_file(c, 'tests/testdata/example6.gz')

        r = c.results.get(20230310115215)

        metrics = c.tests.get_test_metric(r.id, 6, 'latency')
        assert len(metrics) == 1
        assert isinstance(metrics[0], Latency)
        assert metrics[0].log_file == 'perf_9.txt'
        assert metrics[0].metric == 'latency'
        assert metrics[0].total_latency == 83
        assert metrics[0].total_latency_units == 'usec'
        assert metrics[0].result == 'pass'
        assert metrics[0].interface == 'lan'
        assert metrics[0].download_latency == 54
        assert metrics[0].download_latency_units == 'usec'
        assert metrics[0].upload_latency == 29
        assert metrics[0].upload_latency_units == 'usec'
        assert metrics[0].seq is None

        with pytest.raises(ValueError, match='unknown metric invalid'):
            c.tests.get_test_metric(r.id, 2, 'invalid')

    def test_get_test_metric_csv(self, c):
        import_all_from_file(c, 'tests/testdata/example5.gz')

        r = c.results.get(20230310111705)

        csv = c.tests.get_test_metric_csv(r.id, 2, 'bandwidth')
        assert 'perf_multi_1.txt,' in csv

        csv = c.tests.get_test_metric_csv(r.id, 2, 'client_bandwidth')
        assert '941.608,' in csv

        with pytest.raises(CDRouterError):
            c.tests.get_test_metric_csv(r.id, 2, 'invalid')
