#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Highlights."""

from marshmallow import Schema, fields, post_load

class Highlight(object):
    """Model for CDRouter Highlights.

    :param id: (optional) Result ID as an int.
    :param seq: (optional) TestResult sequence ID as an int.
    :param line: (optional) Line number in TestResult's logfile as an int.
    :param color: (optional) Highlight color as string.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.seq = kwargs.get('seq', None)
        self.line = kwargs.get('line', None)
        self.color = kwargs.get('color', None)

class HighlightSchema(Schema):
    id = fields.Int(as_string=True)
    seq = fields.Int(as_string=True)
    line = fields.Int(as_string=True)
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
        return 'results/'+str(id)+'/tests/'+str(seq)+'/'+self.BASE

    def list(self, id, seq, detailed=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of highlights.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`highlights.Highlight <highlights.Highlight>` list
        """
        schema = HighlightSchema()
        if not detailed:
            schema = HighlightSchema(exclude=('id', 'seq'))
        resp = self.service.list(self._base(id, seq), detailed=detailed)
        return self.service.decode(schema, resp, many=True)

    def get(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        """Get a highlight.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param line: Line number in TestResult's logfile as an int.
        :return: :class:`highlights.Highlight <highlights.Highlight>` object
        """
        schema = HighlightSchema()
        resp = self.service.get_id(self._base(id, seq), line)
        return self.service.decode(schema, resp)

    def create_or_edit(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        """Create or edit a highlight.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param resource: :class:`highlights.Highlight <highlights.Highlight>` object
        :return: :class:`highlights.Highlight <highlights.Highlight>` object
        :rtype: highlights.Highlight
        """
        schema = HighlightSchema(exclude=('id', 'seq'))
        json = self.service.encode(schema, resource)

        schema = HighlightSchema()
        resp = self.service.edit(self._base(id, seq), resource.line, json)
        return self.service.decode(schema, resp)

    def create(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        """Create a highlight.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param resource: :class:`highlights.Highlight <highlights.Highlight>` object
        :return: :class:`highlights.Highlight <highlights.Highlight>` object
        :rtype: highlights.Highlight
        """
        return self.create_or_edit(id, seq, resource)

    def edit(self, id, seq, resource): # pylint: disable=invalid-name,redefined-builtin
        """Edit a highlight.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param resource: :class:`highlights.Highlight <highlights.Highlight>` object
        :return: :class:`highlights.Highlight <highlights.Highlight>` object
        :rtype: highlights.Highlight
        """
        return self.create_or_edit(id, seq, resource)

    def delete(self, id, seq, line): # pylint: disable=invalid-name,redefined-builtin
        """Delete a highlight.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param line: Line number in TestResult's logfile as an int.
        """
        return self.service.delete_id(self._base(id, seq), line)
