#
# Copyright (c) 2017-2023 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Captures."""

import io

from requests_toolbelt.downloadutils import stream
from marshmallow import Schema, post_load, EXCLUDE
from marshmallow import fields as mfields

class Capture(object):
    """Model for CDRouter Captures.

    :param id: (optional) Result ID as an int.
    :param seq: (optional) TestResult sequence ID as an int.
    :param type: (optional) Capture type as string.
    :param interface: (optional) Interface name as string.
    :param filename: (optional) Path to capture file as string.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.seq = kwargs.get('seq', None)
        self.type = kwargs.get('type', None)
        self.interface = kwargs.get('interface', None)
        self.filename = kwargs.get('filename', None)

class CaptureSchema(Schema):
    id = mfields.Int(as_string=True)
    seq = mfields.Int(as_string=True)
    type = mfields.Str(load_default=None)
    interface = mfields.Str()
    filename = mfields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return Capture(**data)

class CloudShark(object):
    """Model for CDRouter CloudShark uploads.

    :param url: (optional) CloudShark URL as a string.
    """
    def __init__(self, **kwargs):
        self.url = kwargs.get('url', None)

class CloudSharkSchema(Schema):
    url = mfields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return CloudShark(**data)

class CapturesService(object):
    """Service for accessing CDRouter Captures."""

    RESOURCE = 'captures'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service

    def _base(self, id, seq): # pylint: disable=invalid-name,redefined-builtin
        return 'results/'+str(id)+'/tests/'+str(seq)+'/'+self.BASE

    def list(self, id, seq, detailed=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of captures, using summary representation by default (see
        ``detailed`` parameter).

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param detailed: (optional) Return all fields if Bool `True`.
        :return: :class:`captures.Capture <captures.Capture>` list
        """
        schema = CaptureSchema()
        if not detailed:
            schema = CaptureSchema(exclude=('id', 'seq'))
        resp = self.service.list(self._base(id, seq), detailed=detailed)
        return self.service.decode(schema, resp, many=True)

    def get(self, id, seq, intf): # pylint: disable=invalid-name,redefined-builtin
        """Get a capture.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param intf: Interface name as string.
        :return: :class:`captures.Capture <captures.Capture>` object
        :rtype: captures.Capture
        """
        schema = CaptureSchema()
        resp = self.service.get_id(self._base(id, seq), intf)
        return self.service.decode(schema, resp)

    def download(self, id, seq, intf, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Download a capture as a PCAP file.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param intf: Interface name as string.
        :param inline: (optional) Use inline version of capture file.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        resp = self.service.get_id(self._base(id, seq), intf, params={'format': 'cap', 'inline': inline}, stream=True)
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        resp.close()
        b.seek(0)
        return (b, self.service.filename(resp))

    def send_to_cloudshark(self, id, seq, intf, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Send a capture to a CloudShark Appliance. Both
        cloudshark_appliance_url and cloudshark_appliance_token must
        be properly configured via system preferences.

        :param id: Result ID as an int.
        :param seq: TestResult sequence ID as an int.
        :param intf: Interface name as string.
        :param inline: (optional) Use inline version of capture file.
        :return: :class:`captures.CloudShark <captures.CloudShark>` object
        :rtype: captures.CloudShark
        """
        schema = CloudSharkSchema()
        resp = self.service.post(self._base(id, seq)+str(intf)+'/cloudshark/', params={'inline': inline})
        return self.service.decode(schema, resp)
