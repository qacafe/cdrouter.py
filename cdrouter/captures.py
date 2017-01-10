#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Captures."""

from marshmallow import Schema, fields, post_load

class Section(object):
    def __init__(self, **kwargs):
        self.value = kwargs.get('value', None)

class SectionSchema(Schema):
    value = fields.Str()

    @post_load
    def post_load(self, data):
        return Section(**data)

class Structure(object):
    def __init__(self, **kwargs):
        self.sections = kwargs.get('sections', None)

class StructureSchema(Schema):
    sections = fields.Nested(SectionSchema, many=True)

    @post_load
    def post_load(self, data):
        return Structure(**data)

class SummaryPacket(object):
    def __init__(self, **kwargs):
        self.sections = kwargs.get('sections', None)

class SummaryPacketSchema(Schema):
    sections = fields.Nested(SectionSchema, many=True)

    @post_load
    def post_load(self, data):
        return SummaryPacket(**data)

class Summary(object):
    def __init__(self, **kwargs):
        self.structure = kwargs.get('structure', None)
        self.summaries = kwargs.get('summaries', None)

class SummarySchema(Schema):
    structure = fields.Nested(StructureSchema)
    summaries = fields.Nested(SummaryPacketSchema, many=True)

    @post_load
    def post_load(self, data):
        return Summary(**data)

class Field(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.show_name = kwargs.get('show_name', None)
        self.hide = kwargs.get('hide', None)
        self.size = kwargs.get('size', None)
        self.pos = kwargs.get('pos', None)
        self.show = kwargs.get('show', None)
        self.fields = kwargs.get('fields', None)
        self.protos = kwargs.get('protos', None)

class FieldSchema(Schema):
    name = fields.Str()
    show_name = fields.Str()
    hide = fields.Str()
    size = fields.Str()
    pos = fields.Str()
    show = fields.Str()
    _fields = fields.Nested('self', attribute='fields', load_from='fields', dump_to='fields', many=True)
    protos = fields.Nested('ProtoSchema', many=True)

    @post_load
    def post_load(self, data):
        return Field(**data)

class Proto(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.pos = kwargs.get('pos', None)
        self.show = kwargs.get('show', None)
        self.show_name = kwargs.get('show_name', None)
        self.value = kwargs.get('value', None)
        self.size = kwargs.get('size', None)
        self.fields = kwargs.get('fields', None)
        self.protos = kwargs.get('protos', None)

class ProtoSchema(Schema):
    name = fields.Str()
    pos = fields.Str()
    show = fields.Str()
    show_name = fields.Str()
    value = fields.Str()
    size = fields.Str()
    # _fields = fields.Nested(FieldSchema, attribute='fields', load_from='fields', dump_to='fields', many=True)
    # protos = fields.Nested('self', many=True)

    @post_load
    def post_load(self, data):
        return Proto(**data)

class Packet(object):
    def __init__(self, **kwargs):
        self.protos = kwargs.get('protos', None)

class PacketSchema(Schema):
    protos = fields.Nested(ProtoSchema, many=True)

    @post_load
    def post_load(self, data):
        return Packet(**data)

class Decode(object):
    def __init__(self, **kwargs):
        self.packets = kwargs.get('packets', None)

class DecodeSchema(Schema):
    packets = fields.Nested(PacketSchema, many=True)

    @post_load
    def post_load(self, data):
        return Decode(**data)

class ASCIIByte(object):
    def __init__(self, **kwargs):
        self.byte = kwargs.get('byte', None)
        self.pos = kwargs.get('pos', None)

class ASCIIByteSchema(Schema):
    byte = fields.Str()
    pos = fields.Int()

    @post_load
    def post_load(self, data):
        return ASCIIByte(**data)

class ASCIILine(object):
    def __init__(self, **kwargs):
        self.raw = kwargs.get('raw', None)
        self.offset = kwargs.get('offset', None)
        self.ascii = kwargs.get('ascii', None)
        self.hex = kwargs.get('hex', None)

class ASCIILineSchema(Schema):
    raw = fields.Str()
    offset = fields.Str()
    ascii = fields.Nested(ASCIIByteSchema, many=True)
    hex = fields.Nested(ASCIIByteSchema, many=True)

    @post_load
    def post_load(self, data):
        return ASCIILine(**data)

class ASCIIFrame(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.lines = kwargs.get('lines', None)

class ASCIIFrameSchema(Schema):
    name = fields.Str(missing=None)
    lines = fields.Nested(ASCIILineSchema, many=True)

    @post_load
    def post_load(self, data):
        return ASCIIFrame(**data)

class ASCII(object):
    def __init__(self, **kwargs):
        self.frame = kwargs.get('frame', None)
        self.reassembled = kwargs.get('reassembled', None)

class ASCIISchema(Schema):
    frame = fields.Nested(ASCIIFrameSchema, missing=None)
    reassembled = fields.Nested(ASCIIFrameSchema, missing=None)

    @post_load
    def post_load(self, data):
        return ASCII(**data)

class Capture(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.seq = kwargs.get('seq', None)
        self.interface = kwargs.get('interface', None)
        self.filename = kwargs.get('filename', None)

class CaptureSchema(Schema):
    id = fields.Str()
    seq = fields.Str()
    interface = fields.Str()
    filename = fields.Str()

    @post_load
    def post_load(self, data):
        return Capture(**data)

class CloudShark(object):
    def __init__(self, **kwargs):
        self.url = kwargs.get('url', None)

class CloudSharkSchema(Schema):
    url = fields.Str()

    @post_load
    def post_load(self, data):
        return CloudShark(**data)

class CapturesService(object):
    """Service for accessing CDRouter Captures."""

    RESOURCE = 'captures'
    BASE = '/' + RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        return '/results/'+str(id)+'/tests/'+str(seq)+self.BASE

    def list(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of captures."""
        schema = CaptureSchema(exclude=('id', 'seq'))
        resp = self.service.list(self._base(id, seq), filter)
        return self.service.decode(schema, resp, many=True)

    def get(self, id, seq, intf): # pylint: disable=invalid-name,redefined-builtin
        """Get a capture."""
        schema = CaptureSchema()
        resp = self.service.get_id(self._base(id, seq), intf)
        return self.service.decode(schema, resp)

    def download(self, id, seq, intf, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Download a capture as a PCAP file."""
        return self.service.get_id(self._base(id, seq), intf, params={'format': format, 'inline': inline})

    def summary(self, id, seq, intf, filter=None, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Get a capture's summary."""
        schema = SummarySchema()
        resp = self.service.get(self._base(id, seq)+str(intf)+'/summary/',
                                params={'filter': filter, 'inline': inline})
        return self.service.decode(schema, resp)

    def decode(self, id, seq, intf, filter=None, frame=None, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Get a capture's decode."""
        schema = DecodeSchema()
        resp = self.service.get(self._base(id, seq)+str(intf)+'/decode/',
                                params={'filter': filter, 'frame': frame, 'inline': inline})
        return self.service.decode(schema, resp)

    def ascii(self, id, seq, intf, filter=None, frame=None, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Get a capture's ASCII (hex dump)."""
        schema = ASCIISchema()
        resp = self.service.get(self._base(id, seq)+str(intf)+'/ascii/',
                                params={'filter': filter, 'frame': frame, 'inline': inline})
        return self.service.decode(schema, resp)

    def send_to_cloudshark(self, id, seq, intf, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Send a capture to a CloudShark Appliance. Both
        cloudshark_appliance_url and cloudshark_appliance_token must
        be properly configured via system preferences.
        """
        schema = CloudSharkSchema()
        resp = self.service.post(self._base(id, seq)+str(intf)+'/cloudshark/', params={'inline': inline})
        return self.service.decode(schema, resp)
