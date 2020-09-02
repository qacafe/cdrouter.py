#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Devices."""

import collections

from marshmallow import Schema, fields, post_load
from .cdr_error import CDRouterError
from .cdr_datetime import DateTime
from .filters import Field as field

class PowerCmd(object):
    """Model for CDRouter Device Power command result.

    :param output: (optional) Output from power on/off command as string.
    """

    def __init__(self, **kwargs):
        self.output = kwargs.get('output', None)

class PowerCmdSchema(Schema):
    output = fields.Str()

    @post_load
    def post_load(self, data):
        return PowerCmd(**data)

class Connection(object):
    """Model for CDRouter Device Connections.

    :param proxy_port: (optional) HTTP proxy port as an int.
    :param proxy_https: (optional) HTTPS proxy port as an int.
    """

    def __init__(self, **kwargs):
        self.proxy_port = kwargs.get('proxy_port', None)
        self.proxy_https = kwargs.get('proxy_https', None)


class ConnectionSchema(Schema):
    proxy_port = fields.Int()
    proxy_https = fields.Int()

    @post_load
    def post_load(self, data):
        return Connection(**data)

class Device(object):
    """Model for CDRouter Devices.

    :param id: (optional) Device ID as an int.
    :param name: (optional) Name as string.
    :param created: (optional) Creation time as `DateTime`.
    :param updated: (optional) Last-updated time as `DateTime`.
    :param user_id: (optional) User ID as an int.
    :param result_id: (optional) Result ID as an int (if a device snapshot).
    :param attachments_dir: (optional) Filepath for attachments as string.
    :param picture_id: (optional) Attachment ID for used for device picture as an int.
    :param tags: (optional) Tags as string list.
    :param default_ip: (optional) Default IP as a string
    :param default_login: (optional) Default login as a string
    :param default_password: (optional) Default password as a string
    :param location: (optional) Location as a string
    :param device_category: (optional) Device category as a string
    :param manufacturer: (optional) Manufacturer as a string
    :param manufacturer_oui: (optional) Manufacturer OUI as a string
    :param model_name: (optional) Model name as a string
    :param model_number: (optional) Model number as a string
    :param description: (optional) Description as a string
    :param product_class: (optional) Product class as a string
    :param serial_number: (optional) Serial number as a string
    :param hardware_version: (optional) Hardware version as a string
    :param software_version: (optional) Software version as a string
    :param provisioning_code: (optional) Provisioning code as a string
    :param note: (optional) Note as a string
    :param insecure_mgmt_url: (optional) `True` if insecure HTTPS management URLs are allowed
    :param mgmt_url: (optional) Management URL as a string
    :param add_mgmt_addr: (optional) `True` if address should be configured when opening proxy connection
    :param mgmt_interface: (optional) Interface on which to configure address as string
    :param mgmt_addr: (optional) Address to configure as string
    :param power_on_cmd: (optional) Command to run to power on device as string
    :param power_off_cmd: (optional) Command to run to power off device as string

    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)
        self.user_id = kwargs.get('user_id', None)
        self.result_id = kwargs.get('result_id', None)
        self.attachments_dir = kwargs.get('attachments_dir', None)
        self.picture_id = kwargs.get('picture_id', None)
        self.tags = kwargs.get('tags', None)

        self.default_ip = kwargs.get('default_ip', None)
        self.default_login = kwargs.get('default_login', None)
        self.default_password = kwargs.get('default_password', None)
        self.location = kwargs.get('location', None)

        self.device_category = kwargs.get('device_category', None)
        self.manufacturer = kwargs.get('manufacturer', None)
        self.manufacturer_oui = kwargs.get('manufacturer_oui', None)
        self.model_name = kwargs.get('model_name', None)
        self.model_number = kwargs.get('model_number', None)
        self.description = kwargs.get('description', None)
        self.product_class = kwargs.get('product_class', None)
        self.serial_number = kwargs.get('serial_number', None)
        self.hardware_version = kwargs.get('hardware_version', None)
        self.software_version = kwargs.get('software_version', None)
        self.provisioning_code = kwargs.get('provisioning_code', None)

        self.note = kwargs.get('note', None)

        self.insecure_mgmt_url = kwargs.get('insecure_mgmt_url', None)
        self.mgmt_url = kwargs.get('mgmt_url', None)
        self.add_mgmt_addr = kwargs.get('add_mgmt_addr', None)
        self.mgmt_interface = kwargs.get('mgmt_interface', None)
        self.mgmt_addr = kwargs.get('mgmt_addr', None)
        self.power_on_cmd = kwargs.get('power_on_cmd', None)
        self.power_off_cmd = kwargs.get('power_off_cmd', None)

class DeviceSchema(Schema):
    id = fields.Int(as_string=True)
    name = fields.Str()
    created = DateTime()
    updated = DateTime()
    user_id = fields.Int(as_string=True)
    result_id = fields.Int(as_string=True, missing=None)
    attachments_dir = fields.Str(missing=None)
    picture_id = fields.Int(as_string=True)
    tags = fields.List(fields.Str())

    default_ip = fields.Str()
    default_login = fields.Str()
    default_password = fields.Str()
    location = fields.Str()

    device_category = fields.Str()
    manufacturer = fields.Str()
    manufacturer_oui = fields.Str()
    model_name = fields.Str()
    model_number = fields.Str()
    description = fields.Str()
    product_class = fields.Str()
    serial_number = fields.Str()
    hardware_version = fields.Str()
    software_version = fields.Str()
    provisioning_code = fields.Str()

    note = fields.Str()

    insecure_mgmt_url = fields.Bool(missing=None)
    mgmt_url = fields.Str(missing=None)
    add_mgmt_addr = fields.Bool(missing=None)
    mgmt_interface = fields.Str(missing=None)
    mgmt_addr = fields.Str(missing=None)
    power_on_cmd = fields.Str(missing=None)
    power_off_cmd = fields.Str(missing=None)

    @post_load
    def post_load(self, data):
        return Device(**data)

class Page(collections.namedtuple('Page', ['data', 'links'])):
    """Named tuple for a page of list response data.

    :param data: :class:`devices.Device <devices.Device>` list
    :param links: :class:`cdrouter.Links <cdrouter.Links>` object
    """

class DevicesService(object):
    """Service for accessing CDRouter Devices."""

    RESOURCE = 'devices'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, type=None, sort=None, limit=None, page=None, detailed=None): # pylint: disable=redefined-builtin
        """Get a list of devices.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`devices.Page <devices.Page>` object
        """
        schema = DeviceSchema()
        if not detailed:
            schema = DeviceSchema(exclude=('attachments_dir', 'default_ip', 'default_login', 'default_password',
                                           'location', 'device_category', 'manufacturer', 'manufacturer_oui',
                                           'model_name', 'model_number', 'product_class', 'serial_number',
                                           'hardware_version', 'software_version', 'provisioning_code', 'note',
                                           'insecure_mgmt_url', 'mgmt_url', 'add_mgmt_addr', 'mgmt_interface',
                                           'mgmt_addr', 'power_on_cmd', 'power_off_cmd'))
        resp = self.service.list(self.base, filter, type, sort, limit, page, detailed=detailed)
        ds, l = self.service.decode(schema, resp, many=True, links=True)
        return Page(ds, l)

    def iter_list(self, *args, **kwargs):
        """Get a list of devices.  Whereas ``list`` fetches a single page of
        devices according to its ``limit`` and ``page`` arguments,
        ``iter_list`` returns all devices by internally making
        successive calls to ``list``.

        :param args: Arguments that ``list`` takes.
        :param kwargs: Optional arguments that ``list`` takes.
        :return: :class:`devices.Device <devices.Device>` list

        """
        return self.service.iter_list(self.list, *args, **kwargs)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a device.

        :param id: Device ID as an int.
        :return: :class:`devices.Device <devices.Device>` object
        :rtype: devices.Device
        """
        schema = DeviceSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def get_by_name(self, name): # pylint: disable=invalid-name,redefined-builtin
        """Get a device by name.

        :param name: Device name as string.
        :return: :class:`devices.Device <devices.Device>` object
        :rtype: devices.Device
        """
        rs, _ = self.list(filter=field('name').eq(name), limit=1)
        if len(rs) == 0:
            raise CDRouterError('no such device')
        return rs[0]

    def create(self, resource):
        """Create a new device.

        :param resource: :class:`devices.Device <devices.Device>` object
        :return: :class:`devices.Device <devices.Device>` object
        :rtype: devices.Device
        """
        schema = DeviceSchema(exclude=('id', 'created', 'updated', 'result_id', 'attachments_dir'))
        json = self.service.encode(schema, resource)

        schema = DeviceSchema()
        resp = self.service.create(self.base, json)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a device.

        :param resource: :class:`devices.Device <devices.Device>` object
        :return: :class:`devices.Device <devices.Device>` object
        :rtype: devices.Device
        """
        schema = DeviceSchema(exclude=('id', 'created', 'updated', 'result_id', 'attachments_dir'))
        json = self.service.encode(schema, resource)

        schema = DeviceSchema()
        resp = self.service.edit(self.base, resource.id, json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a device.

        :param id: Device ID as an int.
        """
        return self.service.delete_id(self.base, id)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get shares for a device.

        :param id: Device ID as an int.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.get_shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Edit shares for a device.

        :param id: Device ID as an int.
        :param user_ids: User IDs as int list.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Export a device.

        :param id: Device ID as an int.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.export(self.base, id)

    def get_connection(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get information on proxy connection to a device's management interface.

        :param id: Device ID as an int.
        :return: :class:`devices.Connection <devices.Connection>` object
        :rtype: devices.Connection
        """
        schema = ConnectionSchema()
        resp = self.service.get(self.base+str(id)+'/connect/')
        return self.service.decode(schema, resp)

    def connect(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Open proxy connection to a device's management interface.

        :param id: Device ID as an int.
        :return: :class:`devices.Connection <devices.Connection>` object
        :rtype: devices.Connection
        """
        schema = ConnectionSchema()
        resp = self.service.post(self.base+str(id)+'/connect/')
        return self.service.decode(schema, resp)

    def disconnect(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Close proxy connection to a device's management interface.

        :param id: Device ID as an int.
        """
        return self.service.post(self.base+str(id)+'/disconnect/')

    def power_on(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Power on a device using it's power on command.

        :param id: Device ID as an int.
        :return: :class:`devices.PowerCmd <devices.PowerCmd>` object
        :rtype: devices.PowerCmd
        """
        schema = PowerCmdSchema()
        resp = self.service.post(self.base+str(id)+'/power/on/')
        return self.service.decode(schema, resp)

    def power_off(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Power off a device using it's power off command.

        :param id: Device ID as an int.
        :return: :class:`devices.PowerCmd <devices.PowerCmd>` object
        :rtype: devices.PowerCmd
        """
        schema = PowerCmdSchema()
        resp = self.service.post(self.base+str(id)+'/power/off/')
        return self.service.decode(schema, resp)

    def bulk_export(self, ids):
        """Bulk export a set of devices.

        :param ids: Int list of device IDs.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        """Bulk copy a set of devices.

        :param ids: Int list of device IDs.
        :return: :class:`devices.Device <devices.Device>` list
        """
        schema = DeviceSchema()
        return self.service.bulk_copy(self.base, self.RESOURCE, ids, schema)

    def bulk_edit(self, _fields, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of devices.

        :param _fields: :class:`devices.Device <devices.Device>` object
        :param ids: (optional) Int list of device IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        schema = DeviceSchema(exclude=('id', 'created', 'updated', 'result_id', 'attachments_dir'))
        _fields = self.service.encode(schema, _fields, skip_none=True)
        return self.service.bulk_edit(self.base, self.RESOURCE, _fields, ids=ids,
                                      filter=filter, type=type, all=all)

    def bulk_delete(self, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of devices.

        :param ids: (optional) Int list of device IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids,
                                        filter=filter, type=type, all=all)
