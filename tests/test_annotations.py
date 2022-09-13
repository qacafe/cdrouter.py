#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import pytest

from cdrouter.cdrouter import CDRouterError
from cdrouter.annotations import Annotation

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestAnnotations:
    def test_list(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        for line in range(1, 6):
            c.annotations.create(idd, seq, Annotation(
                line=line,
                comment='hello'
            ))

        annotations = c.annotations.list(idd, seq)
        assert len(annotations) == 5

        annotations = c.annotations.list(idd, seq, detailed=True)
        assert len(annotations) == 5
        assert annotations[0].id is not None
        assert annotations[0].seq is not None

    def test_get(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        for line in range(1, 6):
            c.annotations.create(idd, seq, Annotation(
                line=line,
                comment='hello'
            ))

        for line in range(1, 6):
            a = c.annotations.get(idd, seq, line)
            assert a.id == idd
            assert a.seq == seq
            assert a.line == line
            assert a.comment == 'hello'

        with pytest.raises(CDRouterError, match='no such annotation'):
            c.annotations.get(idd, seq, 9999)

    def test_create_or_edit(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        for line in range(1, 6):
            c.annotations.create_or_edit(idd, seq, Annotation(
                line=line,
                comment='hello'
            ))

        for line in range(4, 11):
            c.annotations.create_or_edit(idd, seq, Annotation(
                line=line,
                comment='goodbye'
            ))

        for line in range(1, 11):
            annotation = c.annotations.get(idd, seq, line)
            want = 'hello'
            if line >= 4:
                want = 'goodbye'
            assert annotation.comment == want

    def test_create(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        for line in range(1, 6):
            c.annotations.create_or_edit(idd, seq, Annotation(
                line=line,
                comment='hello'
            ))

        for line in range(4, 11):
            c.annotations.create_or_edit(idd, seq, Annotation(
                line=line,
                comment='goodbye'
            ))

        for line in range(1, 11):
            annotation = c.annotations.get(idd, seq, line)
            want = 'hello'
            if line >= 4:
                want = 'goodbye'
            assert annotation.comment == want

    def test_edit(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        c.annotations.create(idd, seq, Annotation(
               line=1,
               comment='hello'
        ))

        annotation = c.annotations.get(idd, seq, 1)
        assert annotation.comment == 'hello'

        annotation.comment = 'goodbye'
        c.annotations.edit(idd, seq, annotation)

        annotation = c.annotations.get(idd, seq, 1)
        assert annotation.comment == 'goodbye'

    def test_delete(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        c.annotations.create(idd, seq, Annotation(
               line=1,
               comment='hello'
        ))

        annotation = c.annotations.get(idd, seq, 1)
        assert annotation.comment == 'hello'

        c.annotations.delete(idd, seq, 1)

        with pytest.raises(CDRouterError, match='no such annotation'):
            c.annotations.get(idd, seq, 1)
