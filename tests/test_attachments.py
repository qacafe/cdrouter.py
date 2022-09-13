#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import shutil

import pytest

from cdrouter.cdrouter import CDRouterError

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestAttachments:
    def test_list(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        d = c.devices.get_by_name('Cisco E4200')

        (attachments, links) = c.attachments.list(d.id)
        assert len(attachments) == 0
        assert links.total == 0

        with open('tests/testdata/example.gz', 'rb') as fd:
            c.attachments.create(d.id, fd, filename='example1.gz')
            c.attachments.create(d.id, fd, filename='example2.gz')
            c.attachments.create(d.id, fd, filename='example3.gz')
            c.attachments.create(d.id, fd, filename='example4.gz')
            c.attachments.create(d.id, fd, filename='example5.gz')

        (attachments, links) = c.attachments.list(d.id)
        assert len(attachments) == 5
        assert links.total == 5

    def test_iter_list(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        d = c.devices.get_by_name('Cisco E4200')

        assert len(list(c.attachments.iter_list(d.id, limit=1))) == 0

        with open('tests/testdata/example.gz', 'rb') as fd:
            c.attachments.create(d.id, fd, filename='example1.gz')
            c.attachments.create(d.id, fd, filename='example2.gz')
            c.attachments.create(d.id, fd, filename='example3.gz')
            c.attachments.create(d.id, fd, filename='example4.gz')
            c.attachments.create(d.id, fd, filename='example5.gz')

        assert len(list(c.attachments.iter_list(d.id, limit=1))) == 5

    def test_get(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        d = c.devices.get_by_name('Cisco E4200')

        with open('tests/testdata/example.gz', 'rb') as fd:
            a = c.attachments.create(d.id, fd, filename='example.gz')

        a2 = c.attachments.get(d.id, a.id)
        assert a2.id == a.id
        assert a2.name == a.name
        assert a2.description == a.description
        assert a2.size == a.size
        assert a2.path == a.path
        assert a2.device_id == a.device_id

        with pytest.raises(CDRouterError, match='no such attachment'):
            c.attachments.get(d.id, 9999)

    def test_create(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        d = c.devices.get_by_name('Cisco E4200')

        with open('tests/testdata/example.gz', 'rb') as fd:
            a = c.attachments.create(d.id, fd, filename='example.gz')

        assert a.id == 1
        assert a.name == 'example.gz'
        assert a.description == ''
        assert a.size == 118814
        assert a.path == '/usr/cdrouter-data/attachments/1/example.gz'
        assert a.device_id == d.id

        with open('tests/testdata/example.gz', 'rb') as fd:
            a = c.attachments.create(d.id, fd, filename='example2.gz')

        assert a.id == 2
        assert a.name == 'example2.gz'
        assert a.description == ''
        assert a.size == 118814
        assert a.path == '/usr/cdrouter-data/attachments/1/example2.gz'
        assert a.device_id == d.id

    def test_download(self, c, tmp_path):
        import_all_from_file(c, 'tests/testdata/example.gz')

        d = c.devices.get_by_name('Cisco E4200')

        with open('tests/testdata/example.gz', 'rb') as fd:
            a = c.attachments.create(d.id, fd, filename='example.gz')

        (b, filename) = c.attachments.download(d.id, a.id)

        filename = '{}/{}'.format(tmp_path, filename)
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

    def test_thumbnail(self, c, tmp_path):
        import_all_from_file(c, 'tests/testdata/example.gz')

        d = c.devices.get_by_name('Cisco E4200')

        with open('tests/testdata/cdrouter-logo-title.png', 'rb') as fd:
            a = c.attachments.create(d.id, fd, filename='cdrouter-logo-title.png')

        (b, filename) = c.attachments.thumbnail(d.id, a.id)

        filename = '{}/{}'.format(tmp_path, filename)
        with open(filename, 'wb') as fd:
            shutil.copyfileobj (b, fd)

    def test_edit(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        d = c.devices.get_by_name('Cisco E4200')

        with open('tests/testdata/example.gz', 'rb') as fd:
            a = c.attachments.create(d.id, fd, filename='example.gz')

        a = c.attachments.get(d.id, a.id)

        new_name = 'foo.gz'
        new_description = 'i am a description'
        a.name = new_name
        a.description = new_description

        a = c.attachments.edit(a)

        assert a.name == new_name
        assert a.description == new_description

        a = c.attachments.get(d.id, a.id)

        assert a.name == new_name
        assert a.description == new_description

    def test_delete(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        d = c.devices.get_by_name('Cisco E4200')

        assert len(list(c.attachments.iter_list(d.id))) == 0

        with open('tests/testdata/example.gz', 'rb') as fd:
            a = c.attachments.create(d.id, fd, filename='example.gz')
            a2 = c.attachments.create(d.id, fd, filename='example2.gz')
            a3 = c.attachments.create(d.id, fd, filename='example3.gz')

        assert len(list(c.attachments.iter_list(d.id))) == 3

        c.attachments.delete(d.id, a2.id)
        c.attachments.delete(d.id, a3.id)

        assert len(list(c.attachments.iter_list(d.id))) == 1

        c.attachments.delete(d.id, a.id)

        assert len(list(c.attachments.iter_list(d.id))) == 0
