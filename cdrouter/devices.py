#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Devices."""

import collections

from marshmallow import Schema, fields, post_load
from .cdr_error import CDRouterError
from .cdr_datetime import DateTime
from .filters import Field as field

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
    :param default_ip: Default IP as a string (optional)
    :param default_login: Default login as a string (optional)
    :param default_password: Default password as a string (optional)
    :param location: Location as a string (optional)
    :param device_category: Device category as a string (optional)
    :param manufacturer: Manufacturer as a string (optional)
    :param manufacturer_oui: Manufacturer OUI as a string (optional)
    :param model_name: Model name as a string (optional)
    :param model_number: Model number as a string (optional)
    :param description: Description as a string (optional)
    :param product_class: Product class as a string (optional)
    :param serial_number: Serial number as a string (optional)
    :param hardware_version: Hardware version as a string (optional)
    :param software_version: Software version as a string (optional)
    :param provisioning_code: Provisioning code as a string (optional)
    :param note: Note as a string (optional)
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

    def list(self, filter=None, type=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of devices.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :return: :class:`devices.Page <devices.Page>` object
        """
        schema = DeviceSchema(exclude=('attachments_dir', 'default_ip', 'default_login', 'default_password',
                                       'location', 'device_category', 'manufacturer', 'manufacturer_oui',
                                       'model_name', 'model_number', 'product_class', 'serial_number',
                                       'hardware_version', 'software_version', 'provisioning_code', 'note'))
        resp = self.service.list(self.base, filter, type, sort, limit, page)
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
        resp = self.service.get(self.base, id)
        return self.service.decode(schema, resp)

    def get_by_name(self, name): # pylint: disable=invalid-name,redefined-builtin
        """Get a device by name.

        :param name: Device name as string.
        :return: :class:`devices.Device <devices.Device>` object
        :rtype: devices.Device
        """
        rs, _ = self.list(filter=field('name').eq(name), limit=1)
        if len(rs) is 0:
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

    def bulk_export(self, ids):
        """Bulk export a set of devices.

        :param ids: String list of device IDs.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        """Bulk copy a set of devices.

        :param ids: String list of device IDs.
        :return: :class:`devices.Device <devices.Device>` list
        """
        schema = DeviceSchema()
        return self.service.bulk_copy(self.base, self.RESOURCE, ids, schema)

    def bulk_edit(self, _fields, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of devices.

        :param _fields: :class:`devices.Device <devices.Device>` object
        :param ids: (optional) String list of device IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_edit(self.base, self.RESOURCE, _fields, ids=ids,
                                      filter=filter, type=type, all=all)

    def bulk_delete(self, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of devices.

        :param ids: (optional) String list of device IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids,
                                        filter=filter, type=type, all=all)
