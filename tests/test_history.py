#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestHistory:
    def test_list(self, c):
        u = c.users.get_by_name('admin')

        (history, links) = c.history.list()
        assert links.current == 1
        assert len(history) == 8

        import_all_from_file(c, 'tests/testdata/example.gz')

        (history, links) = c.history.list()
        assert links.current == 1
        assert len(history) == 12
        assert history[0].user_id == u.id
        assert history[0].resource == 'result'
        assert history[0].id == 20220821222306
        assert history[0].name == '20220821222306'
        assert history[0].action == 'imported'
        assert 'was imported' in history[0].description

    def test_iter_list(self, c):
        u = c.users.get_by_name('admin')

        assert len(list(c.history.iter_list(limit=1))) == 8

        import_all_from_file(c, 'tests/testdata/example.gz')

        history = list(c.history.iter_list(limit=1))
        assert len(history) == 12
        assert history[0].user_id == u.id
        assert history[0].resource == 'result'
        assert history[0].id == 20220821222306
        assert history[0].name == '20220821222306'
        assert history[0].action == 'imported'
        assert 'was imported' in history[0].description
