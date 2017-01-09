#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Testsuites."""

class TestsuitesService(object):
    """Service for accessing CDRouter Testsuites."""

    RESOURCE = 'testsuites'
    BASE = '/' + RESOURCE + '/1/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def info(self):
        """Get testsuite info."""
        return self.service.get(self.base)

    def search(self, query):
        """Perform full text search of testsuite."""
        return self.service.get(self.base+'search/', params={'q': query})

    def list_groups(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of groups."""
        return self.service.list(self.base+'groups/', filter, sort)

    def get_group(self, name):
        """Get a group."""
        return self.service.get(self.base+'tests/'+name+'/')

    def list_modules(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of modules."""
        return self.service.list(self.base+'modules/', filter, sort)

    def get_module(self, name):
        """Get a module."""
        return self.service.get(self.base+'modules/'+name+'/')

    def list_tests(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of tests."""
        return self.service.list(self.base+'tests/', filter, sort)

    def get_test(self, name):
        """Get a test."""
        return self.service.get(self.base+'tests/'+name+'/')

    def list_labels(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of labels."""
        return self.service.list(self.base+'labels/', filter, sort)

    def get_label(self, name):
        """Get a label."""
        return self.service.get(self.base+'labels/'+name+'/')

    def list_errors(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of errors."""
        return self.service.list(self.base+'errors/', filter, sort)

    def get_error(self, name):
        """Get a error."""
        return self.service.get(self.base+'errors/'+name+'/')

    def list_testvars(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of testvars."""
        return self.service.list(self.base+'testvars/', filter, sort)

    def get_testvar(self, name):
        """Get a testvar."""
        return self.service.get(self.base+'testvars/'+name+'/')
