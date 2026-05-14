#
# Copyright (c) 2026 by QA Cafe.
# All Rights Reserved.
#

import datetime
import io
import shutil

import pytest

from cdrouter.cdrouter import CDRouterError

from .utils import my_cdrouter, my_c # pylint: disable=unused-import

class TestCustomFiles:
    def test_list(self, c):
        c.custom_files.mkdir('test-dir')

        with io.BytesIO(b'hello world') as fd:
            c.custom_files.upload('test-dir', fd, filename='hello.txt')
        with io.BytesIO(b'hello world') as fd:
            c.custom_files.upload('test-dir', fd, filename='world.txt')

        entries = c.custom_files.list('test-dir')
        assert len(entries) == 2
        names = [e.name for e in entries]
        assert 'hello.txt' in names
        assert 'world.txt' in names

    def test_get(self, c):
        c.custom_files.mkdir('test-dir')

        content = b'hello world'
        with io.BytesIO(content) as fd:
            c.custom_files.upload('test-dir', fd, filename='hello.txt')

        f = c.custom_files.get('test-dir/hello.txt')
        assert f.name == 'hello.txt'
        assert isinstance(f.path, str)
        assert f.size == len(content)
        assert isinstance(f.modified, datetime.datetime)
        assert f.is_dir is False

    def test_download(self, c, tmp_path):
        c.custom_files.mkdir('test-dir')

        content = b'hello world'
        with io.BytesIO(content) as fd:
            c.custom_files.upload('test-dir', fd, filename='hello.txt')

        (b, filename) = c.custom_files.download('test-dir/hello.txt')
        assert filename == 'hello.txt'

        path = '{}/{}'.format(tmp_path, filename)
        with open(path, 'wb') as fd:
            shutil.copyfileobj(b, fd)

        with open(path, 'rb') as fd:
            assert fd.read() == content

    def test_upload(self, c):
        c.custom_files.mkdir('test-dir')

        content = b'hello world'
        with io.BytesIO(content) as fd:
            f = c.custom_files.upload('test-dir', fd, filename='hello.txt')

        assert f.name == 'hello.txt'
        assert isinstance(f.path, str)
        assert f.size == len(content)
        assert isinstance(f.modified, datetime.datetime)
        assert f.is_dir is False

    def test_mkdir(self, c):
        d = c.custom_files.mkdir('test-dir')
        assert d.name == 'test-dir'
        assert isinstance(d.path, str)
        assert isinstance(d.size, int)
        assert isinstance(d.modified, datetime.datetime)
        assert d.is_dir is True

    def test_rename(self, c):
        c.custom_files.mkdir('test-dir')

        content = b'hello world'
        with io.BytesIO(content) as fd:
            c.custom_files.upload('test-dir', fd, filename='hello.txt')

        f = c.custom_files.rename('test-dir/hello.txt', 'renamed.txt')
        assert f.name == 'renamed.txt'
        assert f.size == len(content)
        assert f.is_dir is False

        with pytest.raises(CDRouterError):
            c.custom_files.get('test-dir/hello.txt')

        f2 = c.custom_files.get('test-dir/renamed.txt')
        assert f2.name == 'renamed.txt'

    def test_delete(self, c):
        c.custom_files.mkdir('test-dir')

        with io.BytesIO(b'hello world') as fd:
            c.custom_files.upload('test-dir', fd, filename='hello.txt')

        entries = c.custom_files.list('test-dir')
        assert len(entries) == 1

        c.custom_files.delete('test-dir/hello.txt')

        entries = c.custom_files.list('test-dir')
        assert len(entries) == 0

        c.custom_files.delete('test-dir')

        with pytest.raises(CDRouterError):
            c.custom_files.list('test-dir')

    def test_delete_recursive(self, c):
        c.custom_files.mkdir('test-dir')

        with io.BytesIO(b'hello world') as fd:
            c.custom_files.upload('test-dir', fd, filename='hello.txt')

        c.custom_files.delete('test-dir', recursive=True)

        with pytest.raises(CDRouterError):
            c.custom_files.list('test-dir')
