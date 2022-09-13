#
# Copyright (c) 2017-2022 by QA Cafe.
# All Rights Reserved.
#

"""Module for processing CDRouter datetime strings."""

from datetime import datetime

from marshmallow import fields
from marshmallow.exceptions import ValidationError

class DateTime(fields.DateTime):
    def __init__(self, format=None, **kwargs): # pylint: disable=invalid-name,redefined-builtin
        super(DateTime, self).__init__(format=format, **kwargs) # pylint: disable=super-with-arguments

    def _serialize(self, value, attr, obj):
        try:
            return super(DateTime, self)._serialize(value, attr, obj) # pylint: disable=super-with-arguments
        except ValidationError:
            return datetime.min

    def _deserialize(self, value, attr, data):
        try:
            return super(DateTime, self)._deserialize(value, attr, data) # pylint: disable=super-with-arguments
        except ValidationError:
            return datetime.min
