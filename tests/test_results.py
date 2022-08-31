#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import shutil
import time

import pytest

from cdrouter.cdrouter import CDRouterError
from cdrouter.jobs import Job
from cdrouter.results import Result
from cdrouter.users import User

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestResults:
    def test_list(self, c):
        (results, links) = c.results.list()
        assert links.total == 0
        assert len(results) == 0

        import_all_from_file(c, 'tests/testdata/example.gz')

        (results, links) = c.results.list()
        assert links.total == 1
        assert len(results) == 1

    def test_iter_list(self, c):
        assert len(list(c.results.iter_list())) == 0

        import_all_from_file(c, 'tests/testdata/example.gz')

        assert len(list(c.results.iter_list())) == 1

    def test_list_csv(self, c):
        assert len(list(c.results.iter_list())) == 0

        import_all_from_file(c, 'tests/testdata/example.gz')

        assert len(list(c.results.iter_list())) == 1

        csv = c.results.list_csv()
        assert '20220821222306,' in csv

    def test_get(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)
        assert r.id == 20220821222306
        assert r.result == 'The package completed successfully'
        assert r.active is False
        assert r.status == 'completed'
        assert r.loops == 1
        assert r.tests == 4
        assert r.passed == 1
        assert r.fail == 1
        assert r.alerts == 0
        assert r.duration == 236
        assert r.size_on_disk == 549937
        assert r.starred is False
        assert r.archived is False
        assert r.result_dir == '/usr/cdrouter-data/results/20220821/20220821222306'
        assert r.package_name == 'Cisco E4200 DHCPv4 relay-nofatal'
        assert r.device_name == 'Cisco E4200'
        assert r.config_name == 'Cisco E4200'
        assert r.package_id == 10
        assert r.device_id == 2
        assert r.config_id == 2
        assert r.note == ''
        assert 'Version 13' in r.build_info
        assert r.tags == ['13.6.0 27b3196 release_13_6', 'DHCP relay', 'DHCPv6 relay', 'nofatal', 'podbrain-20220821.1']
        assert r.testcases == ['cdrouter_app_14', 'dns_45', 'final', 'start']
        assert r.options.tags == ['13.6.0 27b3196 release_13_6', 'podbrain-20220821.1']
        assert r.options.skip_tests is None
        assert r.options.begin_at == ''
        assert r.options.end_at == ''
        assert r.options.extra_cli_args == ''
        assert 'alerts' in r.features
        assert r.features['alerts'].feature == 'alerts'
        assert r.features['alerts'].enabled is True
        assert len(r.interfaces) == 3
        assert r.interfaces[0].name == 'ics'
        assert r.interfaces[0].value == 'eth0'
        assert r.interfaces[0].is_wireless is False
        assert r.interfaces[0].is_ics is True
        assert r.interfaces[1].name == 'lan'
        assert r.interfaces[1].value == 'eth1'
        assert r.interfaces[1].is_wireless is False
        assert r.interfaces[1].is_ics is False
        assert r.interfaces[2].name == 'wan'
        assert r.interfaces[2].value == 'eth2'
        assert r.interfaces[2].is_wireless is False
        assert r.interfaces[2].is_ics is False

        with pytest.raises(CDRouterError, match='no such result'):
            c.results.get(9999)

    def test_updates(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')
        j = c.jobs.launch(Job(package_id=package.id))

        while j.result_id is None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        r = c.results.get(j.result_id)

        update = c.results.updates(r.id)
        assert update.id == 0
        assert update.progress.finished == 0
        assert update.progress.total == 0
        assert update.progress.progress == 0
        assert update.progress.unit == 'percentage'
        assert update.running is None
        assert update.updates is None

        time.sleep(5)

        update = c.results.updates(r.id, update.id)
        assert update.id == 0
        assert len(update.updates) > 0
        assert isinstance(update.updates[0], Result)
        assert update.updates[0].status == 'error'

    def test_stop(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')
        j = c.jobs.launch(Job(package_id=package.id))

        while j.result_id is None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        r = c.results.get(j.result_id)
        c.results.stop(r.id)

    def test_stop_end_of_test(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')
        j = c.jobs.launch(Job(package_id=package.id))

        while j.result_id is None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        r = c.results.get(j.result_id)
        c.results.stop_end_of_test(r.id)

    def test_stop_end_of_loop(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')
        j = c.jobs.launch(Job(package_id=package.id))

        while j.result_id is None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        r = c.results.get(j.result_id)
        c.results.stop_end_of_loop(r.id)

    def test_pause(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')
        j = c.jobs.launch(Job(package_id=package.id))

        while j.result_id is None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        r = c.results.get(j.result_id)
        c.results.pause(r.id)

    def test_pause_end_of_test(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')
        j = c.jobs.launch(Job(package_id=package.id))

        while j.result_id is None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        r = c.results.get(j.result_id)
        c.results.pause_end_of_test(r.id)

    def test_pause_end_of_loop(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')
        j = c.jobs.launch(Job(package_id=package.id))

        while j.result_id is None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        r = c.results.get(j.result_id)
        c.results.pause_end_of_loop(r.id)

    def test_unpause(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')
        j = c.jobs.launch(Job(package_id=package.id))

        while j.result_id is None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        r = c.results.get(j.result_id)
        c.results.unpause(r.id)

    def test_edit(self, c):
        import_all_from_file(c, 'tests/testdata/example2.gz')

        package = c.packages.get_by_name('example')
        j = c.jobs.launch(Job(package_id=package.id))

        while j.result_id is None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        r = c.results.get(j.result_id)
        new_starred = True
        new_archived = True
        new_note = 'i am a new note'
        new_tags = ['bar', 'buz', 'foo']
        r.starred = new_starred
        r.archived = new_archived
        r.note = new_note
        r.tags = new_tags
        r = c.results.edit(r)
        assert r.starred is new_starred
        assert r.archived is new_archived
        assert r.note == new_note
        assert r.tags == new_tags

        r = c.results.get(r.id)
        assert r.starred is new_starred
        assert r.archived is new_archived
        assert r.note == new_note
        assert r.tags == new_tags

    def test_delete(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        c.results.delete(r.id)

        with pytest.raises(CDRouterError, match='no such result'):
            c.results.get(r.id)

    def test_get_shares(self, c):
        u = User(
            admin=True,
            name='admin2',
            description='im an admin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u = c.users.create(u)

        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        assert len(c.results.get_shares(r.id)) == 0

        c.results.edit_shares(r.id, [u.id])

        shares = c.results.get_shares(r.id)
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

        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        assert len(c.results.get_shares(r.id)) == 0

        c.results.edit_shares(r.id, [u.id, u2.id])

        shares = c.results.get_shares(r.id)
        assert len(shares) == 2
        assert shares[0].user_id == u.id
        assert shares[0].read is True
        assert shares[0].write is False
        assert shares[0].execute is False
        assert shares[1].user_id == u2.id
        assert shares[1].read is True
        assert shares[1].write is False
        assert shares[1].execute is False

        c.results.edit_shares(r.id, [u.id])

        shares = c.results.get_shares(r.id)
        assert len(shares) == 1
        assert shares[0].user_id == u.id
        assert shares[0].read is True
        assert shares[0].write is False
        assert shares[0].execute is False

        c.results.edit_shares(r.id, [])

        shares = c.results.get_shares(r.id)
        assert len(shares) == 0

    def test_export(self, c, tmp_path):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        (b, filename) = c.results.export(r.id)

        filename = '{}/{}'.format(tmp_path, 'example.gz')
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

        c.results.delete(r.id)

        with pytest.raises(CDRouterError, match='no such result'):
            c.results.get(20220821222306)

        import_all_from_file(c, filename)

        r = c.results.get(20220821222306)

    def test_bulk_export(self, c, tmp_path):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        (b, filename) = c.results.bulk_export([r.id])

        filename = '{}/{}'.format(tmp_path, 'example.gz')
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

        c.results.delete(r.id)

        with pytest.raises(CDRouterError, match='no such result'):
            c.results.get(r.id)

        import_all_from_file(c, filename)

        c.results.get(r.id)

    def test_bulk_edit(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)
        assert r.starred is False

        c.results.bulk_edit(Result(starred=True), ids=[r.id])

        r = c.results.get(20220821222306)
        assert r.starred is True

    def test_bulk_delete(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        c.results.bulk_delete(ids=[r.id])

        with pytest.raises(CDRouterError, match='no such result'):
            c.results.get(r.id)

    def test_all_stats(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        p = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')
        d = c.devices.get_by_name('Cisco E4200')

        stats = c.results.all_stats()
        assert len(stats.frequent_packages) == 1
        assert stats.frequent_packages[0].package_name == p.name
        assert stats.frequent_packages[0].count == 1
        assert len(stats.package_names) == 1
        assert stats.package_names[0].package_name == p.name
        assert len(stats.frequent_devices) == 1
        assert stats.frequent_devices[0].device_name == d.name
        assert stats.frequent_devices[0].count == 1
        assert len(stats.device_names) == 1
        assert stats.device_names[0].device_name == d.name

    def test_set_stats(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        stats = c.results.set_stats(ids=[r.id])
        assert len(stats.frequent_failures) == 1
        assert stats.frequent_failures[0].name == 'cdrouter_app_14'
        assert stats.frequent_failures[0].count == 1
        assert len(stats.longest_tests) == 4
        assert stats.longest_tests[0].name == 'cdrouter_app_14'
        assert stats.longest_tests[0].duration == 121
        assert stats.result_breakdown.passed == 3
        assert stats.result_breakdown.failed == 1
        assert stats.result_breakdown.skipped == 0
        assert stats.result_breakdown.alerted == 0
        assert stats.time_breakdown.passed == 108
        assert stats.time_breakdown.failed == 121

    def test_diff_stats(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        stats = c.results.diff_stats(ids=[r.id, r.id])
        assert len(stats.tests) == 2
        assert stats.tests[0].name == 'cdrouter_app_14'
        assert len(stats.tests[0].summaries) == 2
        assert stats.tests[0].summaries[0].id == 20220821222306
        assert stats.tests[0].summaries[0].seq == 2
        assert stats.tests[0].summaries[0].result == 'fail'
        assert stats.tests[0].summaries[0].alerts == 0
        assert stats.tests[0].summaries[0].duration == 121
        assert stats.tests[0].summaries[0].flagged is False
        assert stats.tests[0].summaries[0].name == 'cdrouter_app_14'
        assert 'Verify route' in stats.tests[0].summaries[0].description

    def test_single_stats(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        stats = c.results.single_stats(r.id)
        assert len(stats.result_breakdown.failed_at_least_once) == 1
        assert stats.result_breakdown.failed_at_least_once[0].name == 'cdrouter_app_14'
        assert stats.result_breakdown.failed_at_least_once[0].count == 1
        assert len(stats.result_breakdown.passed_every_time) == 1
        assert stats.result_breakdown.passed_every_time[0].name == 'dns_45'
        assert stats.result_breakdown.passed_every_time[0].count == 1
        assert stats.progress.finished == 2
        assert stats.progress.total == 2
        assert stats.progress.progress == 100
        assert stats.progress.unit == 'percentage'

    def test_progress_stats(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        progress = c.results.progress_stats(r.id)
        assert progress.finished == 2
        assert progress.total == 2
        assert progress.progress == 100
        assert progress.unit == 'percentage'

    def test_summary_stats(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        stats = c.results.summary_stats(r.id)
        assert stats.result_breakdown.passed == 3
        assert stats.result_breakdown.failed == 1
        assert stats.result_breakdown.skipped == 0
        assert stats.result_breakdown.alerted == 0
        assert len(stats.test_summaries) == 4
        assert stats.test_summaries[0].id == 20220821222306
        assert stats.test_summaries[0].seq == 1

    def test_list_logdir(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        files = c.results.list_logdir(r.id)
        assert len(files) == 32
        assert files[0].name == 'CDROUTER-INSTALL'
        assert files[0].size == 212

    def test_get_logdir_file(self, c, tmp_path):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        (b, filename) = c.results.get_logdir_file(r.id, 'CDROUTER-INSTALL')

        filename = '{}/{}'.format(tmp_path, filename)
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

    def test_download_logdir_archive(self, c, tmp_path):
        import_all_from_file(c, 'tests/testdata/example.gz')

        r = c.results.get(20220821222306)

        (b, filename) = c.results.download_logdir_archive(r.id)

        filename = '{}/{}'.format(tmp_path, filename)
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

    def test_get_test_metric(self, c):
        import_all_from_file(c, 'tests/testdata/example3.gz')

        r = c.results.get(20220721151446)

        metrics = c.results.get_test_metric(r.id, 'perf_multi_4', 'bandwidth')
        assert len(metrics) == 23
        assert metrics[0].log_file == 'perf_multi_4.txt'
        assert metrics[0].metric == 'bandwidth'
        assert metrics[0].value == 279.455
        assert metrics[0].units == 'Mbits/sec'
        assert metrics[0].result == 'pass'
        assert metrics[0].interface_1 == 'lan.*'
        assert metrics[0].interface_2 == 'wan'
        assert metrics[0].streams == 128
        assert metrics[0].protocol == 'UDP'
        assert metrics[0].direction == 'upload'
        assert metrics[0].value_2 == 0.0
        assert metrics[0].units_2 == 'Percentage'
        assert metrics[0].device_1 == '0'
        assert metrics[0].device_2 == '0'

        with pytest.raises(CDRouterError, match='no such metric'):
            c.results.get_test_metric(r.id, 'invalid', 'bandwidth')

    def test_get_test_metric_csv(self, c):
        import_all_from_file(c, 'tests/testdata/example3.gz')

        r = c.results.get(20220721151446)

        csv = c.results.get_test_metric_csv(r.id, 'perf_multi_4', 'bandwidth')
        assert 'perf_multi_4.txt,' in csv

        with pytest.raises(CDRouterError):
            c.results.get_test_metric_csv(r.id, 'invalid', 'bandwidth')
