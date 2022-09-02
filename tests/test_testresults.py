#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import pytest

from cdrouter.cdrouter import CDRouterError

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
        new_note = 'i am a not'
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
