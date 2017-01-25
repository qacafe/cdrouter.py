#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for (de)serializing complex dictionaries."""

import collections

from marshmallow import fields
from marshmallow.exceptions import ValidationError

class DictField(fields.Field):
    def __init__(self, key_field, nested_field, *args, **kwargs):
        super(DictField, self).__init__(self, *args, **kwargs)
        self.key_field = key_field
        self.nested_field = nested_field

    def _deserialize(self, value, attr, data):
        if not isinstance(value, collections.Mapping):
            self.fail('invalid')

        ret = {}
        for key, val in value.items():
            k = self.key_field._deserialize(key, attr, data)
            data, errors = self.nested_field.load(val)
            if errors:
                raise ValidationError(errors, data=data)
            v = data
            ret[k] = v

        return ret

    def _serialize(self, value, attr, obj):
        ret = {}
        for key, val in value.items():
            k = self.key_field._serialize(key, attr, obj)
            data, errors = self.nested_field.dump(val)
            if errors:
                raise ValidationError(errors, data=data)
            v = data
            ret[k] = v
        return ret
