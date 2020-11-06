#
# Copyright (c) 2017-2020 by QA Cafe.
# All Rights Reserved.
#

"""Module for (de)serializing complex dictionaries."""

import collections

from marshmallow import fields

class DictField(fields.Field):
    def __init__(self, key_field, nested_field, *args, **kwargs):
        super(DictField, self).__init__()
        self.key_field = key_field
        self.nested_field = nested_field

    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, collections.Mapping):
            self.fail('invalid')

        ret = {}
        for key, val in value.items():
            k = self.key_field._deserialize(key, attr, data)
            data = self.nested_field.load(val)
            v = data
            ret[k] = v

        return ret

    def _serialize(self, value, attr, obj):
        ret = {}
        for key, val in value.items():
            k = self.key_field._serialize(key, attr, obj)
            result = self.nested_field.load(val)
            result = self.nested_field.dump(result)
            ret[k] = result
        return ret
