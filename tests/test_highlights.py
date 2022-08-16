#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import pytest

from cdrouter.cdrouter import CDRouterError
from cdrouter.highlights import Highlight

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestHighlights:
    def test_list(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        for line in range(1, 6):
            c.highlights.create(idd, seq, Highlight(
                line=line,
                color='red'
            ))

        highlights = c.highlights.list(idd, seq)
        assert len(highlights) == 5

        highlights = c.highlights.list(idd, seq, detailed=True)
        assert len(highlights) == 5
        assert highlights[0].id is not None
        assert highlights[0].seq is not None

    def test_get(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        for line in range(1, 6):
            c.highlights.create(idd, seq, Highlight(
                line=line,
                color='red'
            ))

        for line in range(1, 6):
            assert c.highlights.get(idd, seq, line).color == 'red'

    def test_create_or_edit(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        for line in range(1, 6):
            c.highlights.create_or_edit(idd, seq, Highlight(
                line=line,
                color='red'
            ))

        for line in range(4, 11):
            c.highlights.create_or_edit(idd, seq, Highlight(
                line=line,
                color='green'
            ))

        for line in range(1, 11):
            highlight = c.highlights.get(idd, seq, line)
            want = 'red'
            if line >= 4:
                want = 'green'
            assert highlight.color == want

    def test_create(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        for line in range(1, 6):
            c.highlights.create_or_edit(idd, seq, Highlight(
                line=line,
                color='red'
            ))

        for line in range(4, 11):
            c.highlights.create_or_edit(idd, seq, Highlight(
                line=line,
                color='green'
            ))

        for line in range(1, 11):
            highlight = c.highlights.get(idd, seq, line)
            want = 'red'
            if line >= 4:
                want = 'green'
            assert highlight.color == want

    def test_edit(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        c.highlights.create(idd, seq, Highlight(
               line=1,
               color='red'
        ))

        highlight = c.highlights.get(idd, seq, 1)
        assert highlight.color == 'red'

        highlight.color = 'green'
        c.highlights.edit(idd, seq, highlight)

        highlight = c.highlights.get(idd, seq, 1)
        assert highlight.color == 'green'

    def test_delete(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        c.highlights.create(idd, seq, Highlight(
               line=1,
               color='red'
        ))

        highlight = c.highlights.get(idd, seq, 1)
        assert highlight.color == 'red'

        c.highlights.delete(idd, seq, 1)

        with pytest.raises(CDRouterError, match='no such highlight'):
            c.highlights.get(idd, seq, 1)
