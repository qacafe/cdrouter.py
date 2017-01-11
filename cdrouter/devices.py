#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Devices."""

from marshmallow import Schema, fields, post_load

class Device(object):
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
    id = fields.Str()
    name = fields.Str()
    created = fields.DateTime()
    updated = fields.DateTime()
    user_id = fields.Str()
    result_id = fields.Str(missing=None)
    attachments_dir = fields.Str(missing=None)
    picture_id = fields.Str()
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

class DevicesService(object):
    """Service for accessing CDRouter Devices."""

    RESOURCE = 'devices'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of devices."""
        schema = DeviceSchema(exclude=('attachments_dir', 'default_ip', 'default_login', 'default_password',
                                       'location', 'device_category', 'manufacturer', 'manufacturer_oui',
                                       'model_name', 'model_number', 'product_class', 'serial_number',
                                       'hardware_version', 'software_version', 'provisioning_code', 'note'))
        resp = self.service.list(self.base, filter, sort, limit, page)
        return self.service.decode(schema, resp, many=True)

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a device."""
        schema = DeviceSchema()
        resp = self.service.get(self.base, id)
        return self.service.decode(schema, resp)

    def create(self, resource):
        """Create a new device."""
        schema = DeviceSchema(exclude=('id', 'created', 'updated', 'result_id', 'attachments_dir'))
        json = self.service.encode(schema, resource)

        schema = DeviceSchema()
        resp = self.service.create(self.base, json)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a device."""
        schema = DeviceSchema(exclude=('id', 'created', 'updated', 'result_id', 'attachments_dir'))
        json = self.service.encode(schema, resource)

        schema = DeviceSchema()
        resp = self.service.edit(self.base, resource.id, json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a device."""
        return self.service.delete_id(self.base, id)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get shares for a device."""
        return self.service.get_shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Edit shares for a device."""
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Export a device."""
        return self.service.export(self.base, id)

    def bulk_export(self, ids):
        """Bulk export a set of devices."""
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        """Bulk copy a set of devices."""
        schema = DeviceSchema()
        return self.service.bulk_copy(self.base, self.RESOURCE, ids, schema)

    def bulk_edit(self, _fields, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of devices."""
        return self.service.bulk_edit(self.base, self.RESOURCE, _fields, ids=ids,
                                      filter=filter, all=all)

    def bulk_delete(self, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of devices."""
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids,
                                        filter=filter, all=all)
