#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

from .utils import my_cdrouter, my_c, import_all_from_file, my_copy_file_to_container # pylint: disable=unused-import

class TestImports:
    def test_list(self, c):
        assert len(c.imports.list()) == 0

        with open('tests/testdata/example.gz', 'rb') as fd: # pylint: disable=unspecified-encoding
            c.imports.stage_import_from_file(fd)

        assert len(c.imports.list()) == 1

    def test_stage_import_from_file(self, c):
        with open('tests/testdata/example.gz', 'rb') as fd: # pylint: disable=unspecified-encoding
            imp = c.imports.stage_import_from_file(fd, 'example.gz')

        assert imp.id == 1
        assert imp.user_id == 1
        assert imp.size == 118814
        assert imp.archive == 'example.gz'

    def test_stage_import_from_filesystem(self, cdrouter, copy_file_to_container):
        container = cdrouter['container']
        c = cdrouter['c']

        filepath = copy_file_to_container(container, 'tests/testdata/example.gz')
        imp = c.imports.stage_import_from_filesystem(filepath)

        assert imp.id == 1
        assert imp.user_id == 1
        assert imp.size == 118814

    def test_stage_import_from_url(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        url = '{}/results/{}'.format(c.base, 20220821222306)
        imp = c.imports.stage_import_from_url(url)

        assert imp.id == 2
        assert imp.user_id == 1
        assert imp.url == url
        assert imp.insecure is False
        assert imp.size >= 110000 and imp.size <= 120000

    def test_get(self, c):
        with open('tests/testdata/example.gz', 'rb') as fd: # pylint: disable=unspecified-encoding
            imp = c.imports.stage_import_from_file(fd)

        imp = c.imports.get(imp.id)
        assert imp.id == 1
        assert imp.user_id == 1
        assert imp.size == 118814

    def test_get_commit_request(self, c):
        with open('tests/testdata/example.gz', 'rb') as fd: # pylint: disable=unspecified-encoding
            imp = c.imports.stage_import_from_file(fd)

        impreq = c.imports.get_commit_request(imp.id)
        assert len(impreq.configs) == 1
        assert len(impreq.devices) == 1
        assert len(impreq.packages) == 1
        assert len(impreq.results) == 1

    def test_commit(self, c):
        impreq = import_all_from_file(c, 'tests/testdata/example.gz')

        assert len(impreq.configs) == 1
        assert len(impreq.devices) == 1
        assert len(impreq.packages) == 1
        assert len(impreq.results) == 1

        for x in impreq.configs:
            assert impreq.configs[x].response.imported is True
        for x in impreq.devices:
            assert impreq.devices[x].response.imported is True
        for x in impreq.packages:
            assert impreq.packages[x].response.imported is True
        for x in impreq.results:
            assert impreq.results[x].response.imported is True

    def test_delete(self, c):
        assert len(c.imports.list()) == 0

        with open('tests/testdata/example.gz', 'rb') as fd: # pylint: disable=unspecified-encoding
            imp = c.imports.stage_import_from_file(fd)

        assert len(c.imports.list()) == 1

        c.imports.delete(imp.id)

        assert len(c.imports.list()) == 0
