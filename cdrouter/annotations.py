#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Annotations."""

from marshmallow import Schema, fields, post_load

class Annotation(object):
    """Model for CDRouter Annotations.

    :param id: (optional) Result ID as an int.
    :param seq: (optional) TestResult sequence ID as an int.
    :param line: (optional) Line number in TestResult's logfile as an int.
    :param comment: (optional) Comment text as string.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.seq = kwargs.get('seq', None)
        self.line = kwargs.get('line', None)
        self.comment = kwargs.get('comment', None)

class AnnotationSchema(Schema):
    id = fields.Int(as_string=True)
    seq = fields.Int(as_string=True)
    line = fields.Int(as_string=True)
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
        return 'results/'+str(id)+'/tests/'+str(seq)+'/'+self.BASE

    def list(self, id, seq, detailed=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of annotations.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`annotations.Annotation <annotations.Annotation>` list
        """
        schema = AnnotationSchema()
        if not detailed:
            schema = AnnotationSchema(exclude=('id', 'seq'))
        resp = self.service.list(self._base(id, seq), detailed=detailed)
        return self.service.decode(schema, resp, many=True)

    def get(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        """Get an annotation.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param line: Line number in TestResult's logfile as an int.
        :return: :class:`annotations.Annotation <annotations.Annotation>` object
        :rtype: annotations.Annotation
        """
        schema = AnnotationSchema()
        resp = self.service.get_id(self._base(id, seq), line)
        return self.service.decode(schema, resp)

    def create_or_edit(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        """Create or edit an annotation.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param resource: :class:`annotations.Annotation <annotations.Annotation>` object
        :return: :class:`annotations.Annotation <annotations.Annotation>` object
        :rtype: annotations.Annotation
        """
        schema = AnnotationSchema(exclude=('id', 'seq'))
        json = self.service.encode(schema, resource)

        schema = AnnotationSchema()
        resp = self.service.edit(self._base(id, seq), resource.line, json)
        return self.service.decode(schema, resp)

    def create(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        """Create an annotation.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param resource: :class:`annotations.Annotation <annotations.Annotation>` object
        :return: :class:`annotations.Annotation <annotations.Annotation>` object
        :rtype: annotations.Annotation
        """
        return self.create_or_edit(id, seq, resource)

    def edit(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        """Edit an annotation.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param resource: :class:`annotations.Annotation <annotations.Annotation>` object
        :return: :class:`annotations.Annotation <annotations.Annotation>` object
        :rtype: annotations.Annotation
        """
        return self.create_or_edit(id, seq, resource)

    def delete(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        """Delete an annotation.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param line: Line number in TestResult's logfile as an int.
        """
        return self.service.delete_id(self._base(id, seq), line)
