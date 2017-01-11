#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Configs."""

from marshmallow import Schema, fields, post_load

class Config(object):
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

class ConfigSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    created = fields.Date()
    updated = fields.Date()
    contents = fields.Str()
    user_id = fields.Str()
    result_id = fields.Str(missing=None)
    tags = fields.List(fields.Str())
    note = fields.Str()

    @post_load
    def post_load(self, data):
        return Config(**data)

class ConfigsService(object):
    """Service for accessing CDRouter Configs."""

    RESOURCE = 'configs'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of configs."""
        schema = ConfigSchema(exclude=('contents', 'note'))
        resp = self.service.list(self.base, filter, sort, limit, page)
        return self.service.decode(schema, resp, many=True)

    def get_new(self):
        """Get output of cdrouter-cli -new-config."""
        return self.service.get(self.base, params={'template': 'default'})

    def get(self, id, format=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a config."""
        schema = ConfigSchema()
        resp = self.service.get_id(self.base, id, params={'format': format})
        return self.service.decode(schema, resp)

    def get_plaintext(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a config as plaintext."""
        return self.service.get_id(self.base, id, params={'format': 'text'})

    def create(self, resource):
        """Create a new config."""
        schema = ConfigSchema(exclude=('id', 'created', 'updated', 'result_id'))
        json = self.service.encode(schema, resource)

        schema = ConfigSchema()
        resp = self.service.create(self.base, json)
        return self.service.decode(schema, resp)

    def edit(self, resource):
        """Edit a config."""
        schema = ConfigSchema(exclude=('id', 'created', 'updated', 'result_id'))
        json = self.service.encode(schema, resource)

        schema = ConfigSchema()
        resp = self.service.edit(self.base, resource.id, json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a config."""
        return self.service.delete_id(self.base, id)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get shares for a config."""
        return self.service.shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Edit shares for a config."""
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Export a config."""
        return self.service.export(self.base, id)

    def check_config(self, contents):
        """Process config contents with cdrouter-cli -check-config."""
        return self.service.post(self.base,
                                 params={'process': 'check'}, json={'contents': contents})

    def upgrade_config(self, contents):
        """Process config contents with cdrouter-cli -upgrade-config."""
        return self.service.post(self.base,
                                 params={'process': 'upgrade'}, json={'contents': contents})

    def get_networks(self, contents):
        """Process config contents with cdrouter-cli -print-networks-json."""
        return self.service.post(self.base,
                                 params={'process': 'networks'}, json={'contents': contents})

    def bulk_export(self, ids):
        """Bulk export a set of configs."""
        return self.service.bulk_export(self.base, ids)

    def bulk_copy(self, ids):
        """Bulk copy a set of configs."""
        return self.service.bulk_copy(self.base, self.RESOURCE, ids)

    def bulk_edit(self, fields, ids=None, filter=None, all=False, testvars=None): # pylint: disable=redefined-builtin
        """Bulk edit a set of configs."""
        return self.service.bulk_edit(self.base, self.RESOURCE,
                                      fields, ids=ids, filter=filter, all=all, testvars=testvars)

    def bulk_delete(self, ids=None, filter=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of configs."""
        return self.service.bulk_delete(self.base, self.RESOURCE,
                                        ids=ids, filter=filter, all=all)

    def list_testvars(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of a config's testvars."""
        return self.service.get(self.base+str(id)+'/testvars/')

    def get_testvar(self, id, name, group=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a testvar from a config."""
        return self.service.get(self.base+str(id)+'/testvars/'+name+'/', params={'group': group})

    def edit_testvar(self, id, name, value, group=None): # pylint: disable=invalid-name,redefined-builtin
        """Edit a testvar in a config."""
        return self.service.patch(self.base+str(id)+'/testvars/'+name+'/',
                                  params={'group': group}, json={'value': value})

    def delete_testvar(self, id, name, group=None): # pylint: disable=invalid-name,redefined-builtin
        """Delete a testvar in a config. Deleting a testvar unsets any
        explicitly configured value for it in the config.
        """
        return self.service.delete(self.base+str(id)+'/testvars/'+name+'/', params={'group': group})

    def bulk_edit_testvars(self, id, testvars): # pylint: disable=invalid-name,redefined-builtin
        """Bulk edit a config's testvars."""
        return self.service.post(self.base+str(id)+'/testvars/',
                                 params={'bulk': 'edit'}, json=testvars)
