#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

class TestsuitesService(object):
    RESOURCE = 'testsuites'
    BASE = '/' + RESOURCE + '/1/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def info(self):
        return self.service.get(self.base)

    def search(self, query):
        return self.service.get(self.base+'search/', params={'q': query})

    def list_groups(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        return self.service.list(self.base+'groups/', filter, sort)

    def get_group(self, name):
        return self.service.get(self.base+'groups/'+name+'/')

    def list_modules(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        return self.service.list(self.base+'modules/', filter, sort)

    def get_module(self, name):
        return self.service.get(self.base+'modules/'+name+'/')

    def list_tests(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        return self.service.list(self.base+'tests/', filter, sort)

    def get_test(self, name):
        return self.service.get(self.base+'tests/'+name+'/')

    def list_labels(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        return self.service.list(self.base+'labels/', filter, sort)

    def get_label(self, name):
        return self.service.get(self.base+'labels/'+name+'/')

    def list_errors(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        return self.service.list(self.base+'errors/', filter, sort)

    def get_error(self, name):
        return self.service.get(self.base+'errors/'+name+'/')

    def list_testvars(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        return self.service.list(self.base+'testvars/', filter, sort)

    def get_testvar(self, name):
        return self.service.get(self.base+'testvars/'+name+'/')
