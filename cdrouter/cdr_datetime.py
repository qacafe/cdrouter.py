#
# Copyright (c) 2017-2022 by QA Cafe.
# All Rights Reserved.
#

"""Module for processing CDRouter datetime strings."""

from datetime import datetime

from marshmallow import fields
from marshmallow.exceptions import ValidationError

# Go zero value time.Time sent to DB as 0001-01-01T00:00:00Z, DB
# converts timezone from UTC to US/Eastern which gets stored as
# 0000-12-31T19:03:58-04:56 (i.e. 0001-12-31 19:03:58-04:56:02 BC).
# marshmallow.fields.DateTime considers this an invalid datetime, so
# we wrap the class and, if we fail to serialize/deserialize a
# datetime, fallback to returning datetime.min = datetime(1, 1, 1,
# tzinfo=None).
class DateTime(fields.DateTime):
    def __init__(self, format=None, **kwargs): # pylint: disable=invalid-name,redefined-builtin
        super(DateTime, self).__init__(format=format, **kwargs) # pylint: disable=super-with-arguments

    def _serialize(self, value, attr, obj): # pylint: disable=arguments-differ
        try:
            return super(DateTime, self)._serialize(value, attr, obj) # pylint: disable=super-with-arguments
        except ValidationError:
            return datetime.min

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return super(DateTime, self)._deserialize(value, attr, data) # pylint: disable=super-with-arguments
        except ValidationError:
            return datetime.min
