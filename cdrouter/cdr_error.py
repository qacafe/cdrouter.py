#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for handling CDRouter Web API errors."""

class CDRouterError(BaseException):
    """Class for representing CDRouter Web API errors.

    :param message: Error message from API.
    :param response: (optional) Response object.
    """
    def __init__(self, message, response=None):
        self.message = message
        self.response = response

    def __str__(self):
        return self.message

