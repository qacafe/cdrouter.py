#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

from .utils import my_cdrouter, my_c # pylint: disable=unused-import

class TestHistory:
    def test_list(self, c):
        (history, links) = c.history.list()
        assert links.current == 1
        assert len(history) > 0
        assert history[0].user_id > 0

    def test_iter_list(self, c):
        assert len(list(c.history.iter_list())) > 0
