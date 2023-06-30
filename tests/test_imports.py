#
# Copyright (c) 2022-2023 by QA Cafe.
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
        assert imp.size > 0

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
        assert impreq.replace_existing is False
        assert len(impreq.configs) == 1
        assert impreq.configs['Cisco E4200'].name == ''
        assert impreq.configs['Cisco E4200'].should_import is True
        assert impreq.configs['Cisco E4200'].existing_id is None
        assert impreq.configs['Cisco E4200'].response.imported is False
        assert len(impreq.devices) == 1
        assert impreq.devices['Cisco E4200'].name == ''
        assert impreq.devices['Cisco E4200'].should_import is True
        assert impreq.devices['Cisco E4200'].existing_id is None
        assert impreq.devices['Cisco E4200'].response.imported is False
        assert len(impreq.packages) == 1
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].name == ''
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].should_import is True
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].existing_id is None
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].response.imported is False
        assert len(impreq.results) == 1
        assert impreq.results['20220821222306'].name is None
        assert impreq.results['20220821222306'].should_import is True
        assert impreq.results['20220821222306'].existing_id is None
        assert impreq.results['20220821222306'].response.imported is False
        assert impreq.tags is None

        c.imports.commit(imp.id, impreq)

        with open('tests/testdata/example.gz', 'rb') as fd: # pylint: disable=unspecified-encoding
            imp = c.imports.stage_import_from_file(fd)

        impreq = c.imports.get_commit_request(imp.id)
        assert impreq.replace_existing is False
        assert len(impreq.configs) == 1
        assert impreq.configs['Cisco E4200'].name == ''
        assert impreq.configs['Cisco E4200'].should_import is False
        assert impreq.configs['Cisco E4200'].existing_id == 1
        assert impreq.configs['Cisco E4200'].response.imported is False
        assert len(impreq.devices) == 1
        assert impreq.devices['Cisco E4200'].name == ''
        assert impreq.devices['Cisco E4200'].should_import is False
        assert impreq.devices['Cisco E4200'].existing_id == 1
        assert impreq.devices['Cisco E4200'].response.imported is False
        assert len(impreq.packages) == 1
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].name == ''
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].should_import is False
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].existing_id == 18
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].response.imported is False
        assert len(impreq.results) == 1
        assert impreq.results['20220821222306'].name is None
        assert impreq.results['20220821222306'].should_import is False
        assert impreq.results['20220821222306'].existing_id == 20220821222306
        assert impreq.results['20220821222306'].response.imported is False
        assert impreq.tags is None

    def test_commit(self, c):
        impreq = import_all_from_file(c, 'tests/testdata/example.gz')

        assert len(impreq.configs) == 1
        assert impreq.configs['Cisco E4200'].response.imported is True
        assert impreq.configs['Cisco E4200'].response.id == 1
        assert impreq.configs['Cisco E4200'].response.name == 'Cisco E4200'
        assert impreq.configs['Cisco E4200'].response.message is None
        assert len(impreq.devices) == 1
        assert impreq.devices['Cisco E4200'].response.imported is True
        assert impreq.devices['Cisco E4200'].response.id == 1
        assert impreq.devices['Cisco E4200'].response.name == 'Cisco E4200'
        assert impreq.devices['Cisco E4200'].response.message is None
        assert len(impreq.packages) == 1
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].response.imported is True
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].response.id == 18
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].response.name == 'Cisco E4200 DHCPv4 relay-nofatal'
        assert impreq.packages['Cisco E4200 DHCPv4 relay-nofatal'].response.message is None
        assert len(impreq.results) == 1
        assert impreq.results['20220821222306'].response.imported is True
        assert impreq.results['20220821222306'].response.id == 20220821222306
        assert impreq.results['20220821222306'].response.name == '20220821222306'
        assert impreq.results['20220821222306'].response.message is None

    def test_delete(self, c):
        assert len(c.imports.list()) == 0

        with open('tests/testdata/example.gz', 'rb') as fd: # pylint: disable=unspecified-encoding
            imp = c.imports.stage_import_from_file(fd)

        assert len(c.imports.list()) == 1

        c.imports.delete(imp.id)

        assert len(c.imports.list()) == 0
