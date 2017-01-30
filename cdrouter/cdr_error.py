#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for handling CDRouter Web API errors."""

from requests.exceptions import HTTPError

class CDRouterError(HTTPError):
    """Class for representing CDRouter Web API errors."""
