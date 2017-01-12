#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for processing CDRouter datetime strings."""

from datetime import datetime

from marshmallow import fields
from marshmallow.exceptions import ValidationError

class DateTime(fields.DateTime):
    def __init__(self, format=None, **kwargs):
        super(DateTime, self).__init__(format=format, **kwargs)
        
    def _serialize(self, value, attr, obj):
        try:
            return super(DateTime, self)._serialize(value, attr, obj)
        except ValidationError:
            return datetime.min

    def _deserialize(self, value, attr, data):
        try:
            return super(DateTime, self)._deserialize(value, attr, data)
        except ValidationError:
            return datetime.min
