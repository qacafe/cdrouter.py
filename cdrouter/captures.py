#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Captures."""

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
        return self.service.list(self._base(id, seq), filter)

    def get(self, id, seq, intf): # pylint: disable=invalid-name,redefined-builtin
        """Get a capture."""
        return self.service.get_id(self._base(id, seq), intf)

    def download(self, id, seq, intf, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Download a capture as a PCAP file."""
        return self.service.get_id(self._base(id, seq), intf, params={'format': format, 'inline': inline})

    def summary(self, id, seq, intf, filter=None, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Get a capture's summary."""
        return self.service.get(self._base(id, seq)+str(intf)+'/summary/',
                                params={'filter': filter, 'inline': inline})

    def decode(self, id, seq, intf, filter=None, frame=None, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Get a capture's decode."""
        return self.service.get(self._base(id, seq)+str(intf)+'/decode/',
                                params={'filter': filter, 'frame': frame, 'inline': inline})

    def ascii(self, id, seq, intf, filter=None, frame=None, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Get a capture's ASCII (hex dump)."""
        return self.service.get(self._base(id, seq)+str(intf)+'/ascii/',
                                params={'filter': filter, 'frame': frame, 'inline': inline})

    def send_to_cloudshark(self, id, seq, intf, inline=False): # pylint: disable=invalid-name,redefined-builtin
        """Send a capture to a CloudShark Appliance. Both
        cloudshark_appliance_url and cloudshark_appliance_token must
        be properly configured via system preferences.
        """
        return self.service.post(self._base(id, seq)+str(intf)+'/cloudshark/', params={'inline': inline})
