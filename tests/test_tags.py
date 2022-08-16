#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import pytest

from cdrouter.cdrouter import CDRouterError

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestTags:
    def test_list(self, c):
        tags = c.tags.list()
        assert len(tags) == 0

        import_all_from_file(c, 'tests/testdata/example.gz')

        tags = c.tags.list()
        assert len(tags) == 5
        assert tags[0].name == '13.6.0 27b3196 release_13_6'
        assert tags[0].count == 1
        assert tags[3].name == 'nofatal'
        assert tags[3].count == 2

    def test_get(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        tag = c.tags.get('nofatal')
        assert tag.configs is None
        assert len(tag.packages) == 1
        assert len(tag.results) == 1

    def test_edit(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        old_name = 'nofatal'
        tag = c.tags.get(old_name)
        assert tag.results[0].id == '20220821222306'

        new_name = 'nofatal123'
        tag.name = new_name
        tag2 = c.tags.edit(tag, old_name=old_name)
        assert tag2.name == new_name

        tag = c.tags.get(new_name)
        assert tag.results[0].id == '20220821222306'

    def test_delete(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        tag = c.tags.get('nofatal')
        assert tag.results[0].id == '20220821222306'

        c.tags.delete('nofatal')

        with pytest.raises(CDRouterError, match='no such tag'):
            c.tags.get('nofatal')
