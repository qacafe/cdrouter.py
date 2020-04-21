#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Testsuites."""

from marshmallow import Schema, fields, post_load

class Info(object):
    """Model for CDRouter Testsuite Info.

    :param build_info: (optional) CDRouter build info as string.
    :param copyright: (optional) CDRouter copyright info as string.
    :param customer: (optional) Customer name from license as string.
    :param lifetime: (optional) License lifetime as string.
    :param os: (optional) OS name as string.
    :param serial_number: (optional) NTA serial number as string.
    :param system_id: (optional) CDRouter system ID as string.
    :param testsuite: (optional) CDRouter testsuite name as string.
    :param release: (optional) CDRouter release as string.
    :param addons: (optional) Enabled CDRouter addons as string list.
    :param all_addons: (optional) All CDRouter addons as string list.
    """
    def __init__(self, **kwargs):
        self.build_info = kwargs.get('build_info', None)
        self.copyright = kwargs.get('copyright', None)
        self.customer = kwargs.get('customer', None)
        self.lifetime = kwargs.get('lifetime', None)
        self.os = kwargs.get('os', None)
        self.serial_number = kwargs.get('serial_number', None)
        self.system_id = kwargs.get('system_id', None)
        self.testsuite = kwargs.get('testsuite', None)
        self.release = kwargs.get('release', None)
        self.addons = kwargs.get('addons', None)
        self.all_addons = kwargs.get('all_addons', None)

class InfoSchema(Schema):
    build_info = fields.Str()
    copyright = fields.Str()
    customer = fields.Str()
    lifetime = fields.Str()
    os = fields.Str()
    serial_number = fields.Str()
    system_id = fields.Str()
    testsuite = fields.Str()
    release = fields.Str()
    addons = fields.List(fields.Str())
    all_addons = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return Info(**data)

class Group(object):
    """Model for CDRouter Groups.

    :param id: (optional) Testsuite ID as an int.
    :param name: (optional) Name as string.
    :param index: (optional) Index as int.
    :param test_count: (optional) Test count as int.
    :param modules: (optional) Modules as string list.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.test_count = kwargs.get('test_count', None)
        self.modules = kwargs.get('modules', None)

class GroupSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    test_count = fields.Int()
    modules = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return Group(**data)

class Module(object):
    """Model for CDRouter Modules.

    :param id: (optional) Testsuite ID as an int.
    :param name: (optional) Name as string.
    :param index: (optional) Index as int.
    :param group: (optional) Group name as string.
    :param description: (optional) Module description as string.
    :param test_count: (optional) Test count as int.
    :param tests: (optional) Tests as string list.
    :param labels: (optional) Labels as string list.
    :param aliases: (optional) Aliases as string list.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.group = kwargs.get('group', None)
        self.description = kwargs.get('description', None)
        self.test_count = kwargs.get('test_count', None)
        self.tests = kwargs.get('tests', None)
        self.labels = kwargs.get('labels', None)
        self.aliases = kwargs.get('aliases', None)

class ModuleSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    group = fields.Str()
    description = fields.Str()
    test_count = fields.Int()
    tests = fields.List(fields.Str())
    labels = fields.List(fields.Str())
    aliases = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return Module(**data)

class Test(object):
    """Model for CDRouter Tests.

    :param id: (optional) Testsuite ID as an int.
    :param name: (optional) Name as string.
    :param index: (optional) Index as int.
    :param group: (optional) Group name as string.
    :param module: (optional) Module name as string.
    :param synopsis: (optional) Test synopsis as string.
    :param description: (optional) Test description as string.
    :param labels: (optional) Labels as string list.
    :param aliases: (optional) Aliases as string list.
    :param testvars: (optional) Testvars as string list.
    :param skip_name: (optional) Skip name as string.
    :param skip_reason: (optional) Skip reason as string.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.group = kwargs.get('group', None)
        self.module = kwargs.get('module', None)
        self.synopsis = kwargs.get('synopsis', None)
        self.description = kwargs.get('description', None)
        self.labels = kwargs.get('labels', None)
        self.aliases = kwargs.get('aliases', None)
        self.testvars = kwargs.get('testvars', None)

        self.skip_name = kwargs.get('skip_name', None)
        self.skip_reason = kwargs.get('skip_reason', None)

class TestSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    group = fields.Str()
    module = fields.Str()
    synopsis = fields.Str()
    description = fields.Str()
    labels = fields.List(fields.Str())
    aliases = fields.List(fields.Str())
    testvars = fields.List(fields.Str())

    skip_name = fields.Str(missing=None)
    skip_reason = fields.Str(missing=None)

    @post_load
    def post_load(self, data):
        return Test(**data)

class Label(object):
    """Model for CDRouter Skip Labels.

    :param id: (optional) Testsuite ID as an int.
    :param name: (optional) Name as string.
    :param index: (optional) Index as int.
    :param reason: (optional) Skip reason as string.
    :param description: (optional) Description as string.
    :param modules: (optional) Modules as string list.
    :param tests: (optional) Tests as string list.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.reason = kwargs.get('reason', None)
        self.description = kwargs.get('description', None)
        self.modules = kwargs.get('modules', None)
        self.tests = kwargs.get('tests', None)

class LabelSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    reason = fields.Str()
    description = fields.Str()
    modules = fields.List(fields.Str())
    tests = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return Label(**data)

class Error(object):
    """Model for CDRouter Start Errors.

    :param id: (optional) Testsuite ID as an int.
    :param name: (optional) Name as string.
    :param index: (optional) Index as int.
    :param description: (optional) Description as string.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.description = kwargs.get('description', None)

class ErrorSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    description = fields.Str()

    @post_load
    def post_load(self, data):
        return Error(**data)

class Testvar(object):
    """Model for CDRouter Start Errors.

    :param id: (optional) Testsuite ID as an int.
    :param name: (optional) Name as a string.
    :param index: (optional) Index as an int.
    :param humanname: (optional) Human-readable name as a string.
    :param display: (optional) Display name as a string.
    :param dataclass: (optional) Data-type as a string.
    :param addedin: (optional) Added-in info as a string.
    :param deprecatedin: (optional) Deprecated-in info as a string.
    :param obsoletedin: (optional) Obsoleted-in info as a string.
    :param min: (optional) Minimum value as a string.
    :param max: (optional) Maximum value as a string.
    :param length: (optional) Required length as a string.
    :param description: (optional) Description as a string.
    :param default: (optional) Default value as a string.
    :param defaultdisabled: (optional) Bool `True` if testvar has no default value.
    :param dyndefault: (optional) Bool `True` if testvar's default value is dynamically calculated.
    :param keywords: (optional) Accepted values as a string list.
    :param alsoaccept: (optional) Also-accepted values as a string list.
    :param wildcard: (optional) Bool `True` if testvar is a wildcard testvar.
    :param instances: (optional) Number of allowed wildcard instances as an int.
    :param parent: (optional) Parent wildcard testvar name as a string.
    :param children: (optional) Child testvars as a string list.
    :param tests: (optional) Test names as a string list.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.humanname = kwargs.get('humanname', None)
        self.display = kwargs.get('display', None)
        self.dataclass = kwargs.get('dataclass', None)
        self.addedin = kwargs.get('addedin', None)
        self.deprecatedin = kwargs.get('deprecatedin', None)
        self.obsoletedin = kwargs.get('obsoletedin', None)
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)
        self.length = kwargs.get('length', None)
        self.description = kwargs.get('description', None)
        self.default = kwargs.get('default', None)
        self.defaultdisabled = kwargs.get('defaultdisabled', None)
        self.dyndefault = kwargs.get('dyndefault', None)
        self.keywords = kwargs.get('keywords', None)
        self.alsoaccept = kwargs.get('alsoaccept', None)
        self.wildcard = kwargs.get('wildcard', None)
        self.instances = kwargs.get('instances', None)
        self.parent = kwargs.get('parent', None)
        self.children = kwargs.get('children', None)
        self.tests = kwargs.get('tests', None)

class TestvarSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    humanname = fields.Str()
    display = fields.Str()
    dataclass = fields.Str()
    addedin = fields.Str()
    deprecatedin = fields.Str()
    obsoletedin = fields.Str()
    min = fields.Str()
    max = fields.Str()
    length = fields.Str()
    description = fields.Str()
    default = fields.Str()
    defaultdisabled = fields.Bool()
    dyndefault = fields.Bool()
    keywords = fields.List(fields.Str())
    alsoaccept = fields.List(fields.Str())
    wildcard = fields.Bool()
    instances = fields.Int()
    parent = fields.Str()
    children = fields.List(fields.Str())
    tests = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return Testvar(**data)

class Search(object):
    """Model for CDRouter Testsuite Searches.

    :param addons: (optional) :class:`testsuites.Group <testsuites.Group>` list
    :param modules: (optional) :class:`testsuites.Module <testsuites.Module>` list
    :param tests: (optional) :class:`testsuites.Test <testsuites.Test>` list
    :param reasons: (optional) :class:`testsuites.Label <testsuites.Label>` list
    :param errors: (optional) :class:`testsuites.Error <testsuites.Error>` list
    :param testvars: (optional) :class:`testsuites.Testvar <testsuites.Testvar>` list
    """
    def __init__(self, **kwargs):
        self.addons = kwargs.get('addons', None)
        self.modules = kwargs.get('modules', None)
        self.tests = kwargs.get('tests', None)
        self.reasons = kwargs.get('reasons', None)
        self.errors = kwargs.get('errors', None)
        self.testvars = kwargs.get('testvars', None)

class SearchSchema(Schema):
    addons = fields.Nested(GroupSchema, many=True, missing=None)
    modules = fields.Nested(ModuleSchema, many=True, missing=None)
    tests = fields.Nested(TestSchema, many=True, missing=None)
    reasons = fields.Nested(LabelSchema, many=True, missing=None)
    errors = fields.Nested(ErrorSchema, many=True, missing=None)
    testvars = fields.Nested(TestvarSchema, many=True, missing=None)

    @post_load
    def post_load(self, data):
        return Search(**data)

class TestsuitesService(object):
    """Service for accessing CDRouter Testsuites."""

    RESOURCE = 'testsuites'
    BASE = RESOURCE + '/1/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def info(self):
        """Get testsuite info.

        :return: :class:`testsuites.Info <testsuites.Info>` object
        :rtype: testsuites.Info
        """
        schema = InfoSchema()
        resp = self.service.get(self.base)
        return self.service.decode(schema, resp)

    def search(self, query):
        """Perform full text search of testsuite.

        :param query: Search query as a string.
        :return: :class:`testsuites.Search <testsuites.Search>` object
        :rtype: testsuites.Search
        """
        schema = SearchSchema()
        resp = self.service.get(self.base+'search/', params={'q': query})
        return self.service.decode(schema, resp)

    def update(self):
        """Update testsuite info."""
        return self.service.post(self.base)

    def list_groups(self, filter=None, type=None, sort=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of groups.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`testsuites.Group <testsuites.Group>` list
        """
        schema = GroupSchema()
        resp = self.service.list(self.base+'groups/', filter, type, sort, detailed=detailed)
        return self.service.decode(schema, resp, many=True)

    def get_group(self, name):
        """Get a group.

        :param name: Group name as string.
        :return: :class:`testsuites.Group <testsuites.Group>` object
        :rtype: testsuites.Group
        """
        schema = GroupSchema()
        resp = self.service.get(self.base+'groups/'+name+'/')
        return self.service.decode(schema, resp)

    def list_modules(self, filter=None, type=None, sort=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of modules.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`testsuites.Module <testsuites.Module>` list
        """
        schema = ModuleSchema()
        if not detailed:
            schema = ModuleSchema(exclude=('index', 'labels'))
        resp = self.service.list(self.base+'modules/', filter, type, sort, detailed=detailed)
        return self.service.decode(schema, resp, many=True)

    def get_module(self, name):
        """Get a module.

        :param name: Module name as string.
        :return: :class:`testsuites.Module <testsuites.Module>` object
        :rtype: testsuites.Module
        """
        schema = ModuleSchema()
        resp = self.service.get(self.base+'modules/'+name+'/')
        return self.service.decode(schema, resp)

    def list_tests(self, filter=None, type=None, sort=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of tests.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`testsuites.Test <testsuites.Test>` list
        """
        schema = TestSchema(exclude=('skip_name', 'skip_reason'))
        if not detailed:
            schema = TestSchema(exclude=('description', 'labels', 'testvars', 'skip_name', 'skip_reason'))
        resp = self.service.list(self.base+'tests/', filter, type, sort, detailed=detailed)
        return self.service.decode(schema, resp, many=True)

    def get_test(self, name):
        """Get a test.

        :param name: Test name as string.
        :return: :class:`testsuites.Test <testsuites.Test>` object
        :rtype: testsuites.Test
        """
        schema = TestSchema(exclude=('skip_name', 'skip_reason'))
        resp = self.service.get(self.base+'tests/'+name+'/')
        return self.service.decode(schema, resp)

    def list_labels(self, filter=None, type=None, sort=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of labels.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`testsuites.Label <testsuites.Label>` list
        """
        schema = LabelSchema()
        if not detailed:
            schema = LabelSchema(exclude=('index', 'description', 'modules', 'tests'))
        resp = self.service.list(self.base+'labels/', filter, type, sort, detailed=detailed)
        return self.service.decode(schema, resp, many=True)

    def get_label(self, name):
        """Get a label.

        :param name: Label name as string.
        :return: :class:`testsuites.Label <testsuites.Label>` object
        :rtype: testsuites.Label
        """
        schema = LabelSchema()
        resp = self.service.get(self.base+'labels/'+name+'/')
        return self.service.decode(schema, resp)

    def list_errors(self, filter=None, type=None, sort=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of errors.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`testsuites.Error <testsuites.Error>` list
        """
        schema = ErrorSchema()
        if not detailed:
            schema = ErrorSchema(exclude=('index', 'description'))
        resp = self.service.list(self.base+'errors/', filter, type, sort, detailed=detailed)
        return self.service.decode(schema, resp, many=True)

    def get_error(self, name):
        """Get an error.

        :param name: Error name as string.
        :return: :class:`testsuites.Error <testsuites.Error>` object
        :rtype: testsuites.Error
        """
        schema = ErrorSchema()
        resp = self.service.get(self.base+'errors/'+name+'/')
        return self.service.decode(schema, resp)

    def list_testvars(self, filter=None, type=None, sort=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of testvars.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`testsuites.Testvar <testsuites.Testvar>` list
        """
        schema = TestvarSchema()
        if not detailed:
            schema = TestvarSchema(exclude=('index', 'humanname', 'addedin', 'deprecatedin', 'obsoletedin',
                                            'min', 'max', 'length', 'dyndefault', 'keywords', 'alsoaccept',
                                            'wildcard', 'instances', 'parent', 'children', 'tests'))
        resp = self.service.list(self.base+'testvars/', filter, type, sort, detailed=detailed)
        return self.service.decode(schema, resp, many=True)

    def get_testvar(self, name):
        """Get a testvar.

        :param name: Testvar name as string.
        :return: :class:`testsuites.Testvar <testsuites.Testvar>` object
        :rtype: testsuites.Testvar
        """
        schema = TestvarSchema()
        resp = self.service.get(self.base+'testvars/'+name+'/')
        return self.service.decode(schema, resp)
