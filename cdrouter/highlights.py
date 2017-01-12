#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Highlights."""

from marshmallow import Schema, fields, post_load

class Highlight(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.seq = kwargs.get('seq', None)
        self.line = kwargs.get('line', None)
        self.color = kwargs.get('color', None)

class HighlightSchema(Schema):
    id = fields.Str()
    seq = fields.Str()
    line = fields.Str()
    color = fields.Str()

    @post_load
    def post_load(self, data):
        return Highlight(**data)

class HighlightsService(object):
    """Service for accessing CDRouter Highlights."""

    RESOURCE = 'highlights'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        return 'results/'+str(id)+'/tests/'+str(seq)+self.BASE

    def list(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of highlights."""
        schema = HighlightSchema(exclude=('id', 'seq'))
        resp = self.service.list(self._base(id, seq), filter)
        return self.service.decode(schema, resp, many=True)

    def get(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        """Get a highlight."""
        schema = HighlightSchema()
        resp = self.service.get_id(self._base(id, seq), line)
        return self.service.decode(schema, resp)

    def create_or_edit(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        """Create or edit a highlight."""
        schema = HighlightSchema(exclude=('id', 'seq'))
        json = self.service.encode(schema, resource)

        schema = HighlightSchema()
        resp = self.service.edit(self._base(id, seq), resource.line, json)
        return self.service.decode(schema, resp)

    def create(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        return self.create_or_edit(id, seq, resource)

    def edit(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        return self.create_or_edit(id, seq, resource)

    def delete(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        """Get a highlight."""
        return self.service.delete_id(self._base(id, seq), line)
