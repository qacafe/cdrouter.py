#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Configs."""

import collections

from marshmallow import Schema, fields, post_load
from .cdr_error import CDRouterError
from .cdr_datetime import DateTime
from .filters import Field as field

class ConfigError(object):
    """Model for CDRouter Check Config Error.

    :param lines: (optional) Line numbers as string list.
    :param error: (optional) Error message as string.
    """
    def __init__(self, **kwargs):
        self.lines = kwargs.get('lines', None)
        self.error = kwargs.get('error', None)

class ConfigErrorSchema(Schema):
    lines = fields.List(fields.Str())
    error = fields.Str()

    @post_load
    def post_load(self, data):
        return ConfigError(**data)

class CheckConfig(object):
    """Model for CDRouter Check Config.

    :param errors: (optional) :class:`configs.ConfigError <configs.ConfigError>` list
    """
    def __init__(self, **kwargs):
        self.errors = kwargs.get('errors', None)

class CheckConfigSchema(Schema):
    errors = fields.Nested(ConfigErrorSchema, many=True)

    @post_load
    def post_load(self, data):
        return CheckConfig(**data)

class UpgradeConfig(object):
    """Model for CDRouter Config Upgrades.

    :param success: (optional) Bool `True` if successful.
    :param output: (optional) Output as string.
    """
    def __init__(self, **kwargs):
        self.success = kwargs.get('success', None)
        self.output = kwargs.get('output', None)

class UpgradeConfigSchema(Schema):
    success = fields.Bool()
    output = fields.Str()

    @post_load
    def post_load(self, data):
        return UpgradeConfig(**data)

class Networks(object):
    """Model for CDRouter Config Networks.

    :param name: (optional) Network name as string.
    :param type: (optional) Network type as string.
    :param side: (optional) Network side as string.
    :param title: (optional) Network title as string.
    :param children: (optional) :class:`configs.Networks <configs.Networks>` list.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.type = kwargs.get('type', None)
        self.side = kwargs.get('side', None)
        self.title = kwargs.get('title', None)
        self.children = kwargs.get('children', None)

class NetworksSchema(Schema):
    name = fields.Str()
    type = fields.Str()
    side = fields.Str()
    title = fields.Str()
    children = fields.Nested('self', many=True)

    @post_load
    def post_load(self, data):
        return Networks(**data)

class Testvar(object):
    """Model for CDRouter Config Testvars.

    :param group: (optional) Testvar group name as string.
    :param name: (optional) Testvar name as string.
    :param value: (optional) Testvar value as string.
    :param default: (optional) Testvar default value as string.
    :param isdefault: (optional) Bool `True` if testvar is set to default value.
    :param line: (optional) Config file line number as int.
    """
    def __init__(self, **kwargs):
        self.group = kwargs.get('group', None)
        self.name = kwargs.get('name', None)
        self.value = kwargs.get('value', None)
        self.default = kwargs.get('default', None)
        self.isdefault = kwargs.get('isdefault', None)
        self.line = kwargs.get('line', None)

class TestvarSchema(Schema):
    group = fields.Str()
    name = fields.Str()
    value = fields.Str()
    default = fields.Str()
    isdefault = fields.Bool()
    line = fields.Int()

    @post_load
    def post_load(self, data):
        return Testvar(**data)

class Config(object):
    """Model for CDRouter Configs.

    :param id: (optional) Config ID as an int.
    :param name: (optional) Config name as string.
    :param description: (optional) Config description as string.
    :param created: (optional) Creation time as `DateTime`.
    :param updated: (optional) Last-updated time as `DateTime`.
    :param contents: (optional) Config contents as string.
    :param user_id: (optional) User ID as an int.
    :param result_id: (optional) Result ID as an int (if a config snapshot).
    :param tags: (optional) Tags as string list.
    :param note: (optional) Note as string.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)
        self.contents = kwargs.get('contents', None)
        self.user_id = kwargs.get('user_id', None)
        self.result_id = kwargs.get('result_id', None)
        self.tags = kwargs.get('tags', None)
        self.note = kwargs.get('note', None)

class Page(collections.namedtuple('Page', ['data', 'links'])):
    """Named tuple for a page of list response data.

    :param data: :class:`configs.Config <configs.Config>` list
    :param links: :class:`cdrouter.Links <cdrouter.Links>` object
    """

class ConfigSchema(Schema):
    id = fields.Int(as_string=True)
    name = fields.Str()
    description = fields.Str()
    created = DateTime()
    updated = DateTime()
    contents = fields.Str()
    user_id = fields.Int(as_string=True, )
    result_id = fields.Int(as_string=True, missing=None)
    tags = fields.List(fields.Str())
    note = fields.Str()

    @post_load
    def post_load(self, data):
        return Config(**data)

class ConfigsService(object):
    """Service for accessing CDRouter Configs."""

    RESOURCE = 'configs'
    BASE = RESOURCE + '/'

    GET_SCHEMA = ConfigSchema()
    LIST_SCHEMA = ConfigSchema(exclude=('contents', 'note'))
    CREATE_SCHEMA = ConfigSchema(exclude=('id', 'created', 'updated', 'result_id'))
    EDIT_SCHEMA = CREATE_SCHEMA

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, type=None, sort=None, limit=None, page=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of configs.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`configs.Page <configs.Page>` object
        """
        schema = self.GET_SCHEMA
        if not detailed:
            schema = self.LIST_SCHEMA
        resp = self.service.list(self.base, filter, type, sort, limit, page, detailed=detailed)
        cs, l = self.service.decode(schema, resp, many=True, links=True)
        return Page(cs, l)

    def iter_list(self, *args, **kwargs):
        """Get a list of configs.  Whereas ``list`` fetches a single page of
        configs according to its ``limit`` and ``page`` arguments,
        ``iter_list`` returns all configs by internally making
        successive calls to ``list``.

        :param args: Arguments that ``list`` takes.
        :param kwargs: Optional arguments that ``list`` takes.
        :return: :class:`configs.Config <configs.Config>` list

        """
        return self.service.iter_list(self.list, *args, **kwargs)

    def get_new(self):
        """Get output of cdrouter-cli -new-config.

        :rtype: string
        """
        return self.service.get(self.base, params={'template': 'default'}).text

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a config.

        :param id: Config ID as an int.
        :return: :class:`configs.Config <configs.Config>` object
        :rtype: configs.Config
        """
        schema = self.GET_SCHEMA
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def get_plaintext(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a config as plaintext.

        :param id: Config ID as an int.
        :rtype: string
        """
        return self.service.get_id(self.base, id, params={'format': 'text'}).text

    def get_by_name(self, name): # pylint: disable=invalid-name,redefined-builtin
        """Get a config by name.

        :param name: Config name as string.
        :return: :class:`configs.Config <configs.Config>` object
        :rtype: configs.Config
        """
        rs, _ = self.list(filter=field('name').eq(name), limit=1)
        if len(rs) == 0:
            raise CDRouterError('no such config')
        return rs[0]

    def create(self, resource):
        """Create a new config.

        :param resource: :class:`configs.Config <configs.Config>` object
        :return: :class:`configs.Config <configs.Config>` object
        :rtype: configs.Config
        """
        schema = self.CREATE_SCHEMA
        json = self.service.encode(schema, resource)

        schema = self.GET_SCHEMA
        resp = self.service.create(self.base, json)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a config.

        :param resource: :class:`configs.Config <configs.Config>` object
        :return: :class:`configs.Config <configs.Config>` object
        :rtype: configs.Config
        """
        schema = self.EDIT_SCHEMA
        json = self.service.encode(schema, resource)

        schema = self.GET_SCHEMA
        resp = self.service.edit(self.base, resource.id, json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a config.

        :param id: Config ID as an int.
        """
        return self.service.delete_id(self.base, id)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get shares for a config.

        :param id: Config ID as an int.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.get_shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Edit shares for a config.

        :param id: Config ID as an int.
        :param user_ids: User IDs as int list.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Export a config.

        :param id: Config ID as an int.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.export(self.base, id)

    def check_config(self, contents):
        """Process config contents with cdrouter-cli -check-config.

        :param contents: Config contents as string.
        :return: :class:`configs.CheckConfig <configs.CheckConfig>` object
        :rtype: configs.CheckConfig
        """
        schema = CheckConfigSchema()
        resp = self.service.post(self.base,
                                 params={'process': 'check'}, json={'contents': contents})
        return self.service.decode(schema, resp)

    def upgrade_config(self, contents):
        """Process config contents with cdrouter-cli -upgrade-config.

        :param contents: Config contents as string.
        :return: :class:`configs.UpgradeConfig <configs.UpgradeConfig>` object
        :rtype: configs.UpgradeConfig
        """
        schema = UpgradeConfigSchema()
        resp = self.service.post(self.base,
                                 params={'process': 'upgrade'}, json={'contents': contents})
        return self.service.decode(schema, resp)

    def get_networks(self, contents):
        """Process config contents with cdrouter-cli -print-networks-json.

        :param contents: Config contents as string.
        :return: :class:`configs.Networks <configs.Networks>` object
        :rtype: configs.Networks
        """
        schema = NetworksSchema()
        resp = self.service.post(self.base,
                                 params={'process': 'networks'}, json={'contents': contents})
        return self.service.decode(schema, resp)

    def bulk_export(self, ids):
        """Bulk export a set of configs.

        :param ids: Int list of config IDs.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        """Bulk copy a set of configs.

        :param ids: Int list of config IDs.
        :return: :class:`configs.Config <configs.Config>` list
        """
        schema = self.GET_SCHEMA
        return self.service.bulk_copy(self.base, self.RESOURCE, ids, schema)

    def bulk_edit(self, _fields, ids=None, filter=None, type=None, all=False, testvars=None): # pylint: disable=redefined-builtin
        """Bulk edit a set of configs.

        :param _fields: :class:`configs.Config <configs.Config>` object
        :param ids: (optional) Int list of config IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        :param testvars: (optional) :class:`configs.ConfigTestvars <configs.ConfigTestvars>` list
        """
        schema = self.EDIT_SCHEMA
        _fields = self.service.encode(schema, _fields, skip_none=True)
        return self.service.bulk_edit(self.base, self.RESOURCE,
                                      _fields, ids=ids, filter=filter, type=type, all=all, testvars=testvars)

    def bulk_delete(self, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of configs.

        :param ids: (optional) Int list of config IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_delete(self.base, self.RESOURCE,
                                        ids=ids, filter=filter, type=type, all=all)

    def list_testvars(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of a config's testvars.

        :param id: Config ID as an int.
        :return: :class:`configs.Testvar <configs.Testvar>` list
        """
        schema = TestvarSchema()
        resp = self.service.get(self.base+str(id)+'/testvars/')
        return self.service.decode(schema, resp, many=True)

    def get_testvar(self, id, name, group=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a testvar from a config.

        :param id: Config ID as an int.
        :param name: Testvar name as string.
        :param group: (optional) Testvar group as string.
        :return: :class:`configs.Testvar <configs.Testvar>` object
        :rtype: configs.Testvar
        """
        schema = TestvarSchema()
        resp = self.service.get(self.base+str(id)+'/testvars/'+name+'/', params={'group': group})
        return self.service.decode(schema, resp)

    def edit_testvar(self, id, resource): # pylint: disable=invalid-name,redefined-builtin
        """Edit a testvar in a config.

        :param id: Config ID as an int.
        :param resource: :class:`configs.Testvar <configs.Testvar>` object.
        :return: :class:`configs.Testvar <configs.Testvar>` object
        :rtype: configs.Testvar
        """
        schema = TestvarSchema()
        json = self.service.encode(schema, resource)

        schema = TestvarSchema()
        resp = self.service.patch(self.base+str(id)+'/testvars/'+resource.name+'/',
                                  params={'group': resource.group}, json=json)
        return self.service.decode(schema, resp)

    def delete_testvar(self, id, name, group=None): # pylint: disable=invalid-name,redefined-builtin
        """Delete a testvar in a config. Deleting a testvar unsets any
        explicitly configured value for it in the config.

        :param id: Config ID as an int.
        :param name: Testvar name as string.
        :param group: (optional) Testvar group as string.
        """
        return self.service.delete(self.base+str(id)+'/testvars/'+name+'/', params={'group': group})

    def bulk_edit_testvars(self, id, testvars): # pylint: disable=invalid-name,redefined-builtin
        """Bulk edit a config's testvars.

        :param id: Config ID as an int.
        :param testvars: :class:`configs.Testvar <configs.Testvar>` list
        :return: :class:`configs.Testvar <configs.Testvar>` list
        """
        schema = TestvarSchema()
        json = self.service.encode(schema, testvars, many=True)

        schema = TestvarSchema()
        resp = self.service.post(self.base+str(id)+'/testvars/',
                                 params={'bulk': 'edit'}, json=json)
        return self.service.decode(schema, resp, many=True)
