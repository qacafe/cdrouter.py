#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

from os import environ
import shutil

import pytest

from cdrouter.cdrouter import CDRouterError

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestCaptures:
    def test_list(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        caps = c.captures.list(idd, seq)
        assert len(caps) == 3
        assert caps[0].type == 'device'
        assert caps[0].interface == 'ics'
        assert caps[0].filename == 'start-ics.cap'
        assert caps[1].type == 'device'
        assert caps[1].interface == 'lan-eth1'
        assert caps[1].filename == 'start-lan-eth1.cap'
        assert caps[2].type == 'device'
        assert caps[2].interface == 'wan-eth2'
        assert caps[2].filename == 'start-wan-eth2.cap'


        caps = c.captures.list(idd, seq, detailed=True)
        assert len(caps) == 3
        assert caps[0].id == idd
        assert caps[0].seq == seq
        assert caps[0].type == 'device'
        assert caps[0].interface == 'ics'
        assert caps[0].filename == 'start-ics.cap'
        assert caps[1].id == idd
        assert caps[1].seq == seq
        assert caps[1].type == 'device'
        assert caps[1].interface == 'lan-eth1'
        assert caps[1].filename == 'start-lan-eth1.cap'
        assert caps[2].id == idd
        assert caps[2].seq == seq
        assert caps[2].type == 'device'
        assert caps[2].interface == 'wan-eth2'
        assert caps[2].filename == 'start-wan-eth2.cap'

    def test_get(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        cap = c.captures.get(idd, seq, 'lan-eth1')
        assert cap.type == 'device'
        assert cap.interface == 'lan-eth1'
        assert cap.filename == 'start-lan-eth1.cap'

        with pytest.raises(CDRouterError, match='no such capture'):
            c.captures.get(idd, seq, 'foo')

    def test_download(self, c, tmp_path):
        import_all_from_file(c, 'tests/testdata/example.gz')

        idd = 20220821222306
        seq = 1

        (b, filename) = c.captures.download(idd, seq, 'lan-eth1')

        filename = '{}/{}'.format(tmp_path, filename)
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

    @pytest.mark.skipif('CLOUDSHARK_URL' not in environ, reason="requires CLOUDSHARK_URL env var")
    @pytest.mark.skipif('CLOUDSHARK_TOKEN' not in environ, reason="requires CLOUDSHARK_TOKEN env var")
    def test_send_to_cloudshark(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        prefs = c.system.get_preferences()
        prefs.cloudshark_appliance_url = environ.get('CLOUDSHARK_URL')
        prefs.cloudshark_appliance_token = environ.get('CLOUDSHARK_TOKEN')
        c.system.edit_preferences(prefs)

        idd = 20220821222306
        seq = 1

        cs = c.captures.send_to_cloudshark(idd, seq, 'lan-eth1')
        assert cs.url.startswith(environ.get('CLOUDSHARK_URL'))
