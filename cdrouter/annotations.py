#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Annotations."""

from marshmallow import Schema, fields, post_load

class Annotation(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.seq = kwargs.get('seq', None)
        self.line = kwargs.get('line', None)
        self.comment = kwargs.get('comment', None)

class AnnotationSchema(Schema):
    id = fields.Str()
    seq = fields.Str()
    line = fields.Str()
    comment = fields.Str()

    @post_load
    def post_load(self, data):
        return Annotation(**data)

class AnnotationsService(object):
    """Service for accessing CDRouter Annotations."""

    RESOURCE = 'annotations'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        return 'results/'+str(id)+'/tests/'+str(seq)+self.BASE

    def list(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of annotations."""
        schema = AnnotationSchema(exclude=('id', 'seq'))
        resp = self.service.list(self._base(id, seq))
        return self.service.decode(schema, resp, many=True)

    def get(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        """Get an annotation."""
        schema = AnnotationSchema()
        resp = self.service.get_id(self._base(id, seq), line)
        return self.service.decode(schema, resp)

    def create_or_edit(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        """Create or edit an annotation."""
        schema = AnnotationSchema(exclude=('id', 'seq'))
        json = self.service.encode(schema, resource)

        schema = AnnotationSchema()
        resp = self.service.edit(self._base(id, seq), resource.line, json)
        return self.service.decode(schema, resp)

    def create(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        return self.create_or_edit(id, seq, resource)

    def edit(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        return self.create_or_edit(id, seq, resource)

    def delete(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        """Delete an annotation."""
        return self.service.delete_id(self._base(id, seq), line)
