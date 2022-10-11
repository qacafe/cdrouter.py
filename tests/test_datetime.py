#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import datetime

import pytest

from marshmallow import Schema, fields, post_load
from marshmallow.exceptions import ValidationError

from .utils import my_cdrouter, my_c, import_all_from_file # pylint: disable=unused-import

class TestDateTime:
    def test_datetime(self, c):
        import_all_from_file(c, 'tests/testdata/example.gz')

        config = c.configs.get_by_name('Cisco E4200')
        assert config.created.year == 2016
        assert config.created.month == 12
        assert config.created.day == 14
        assert config.created.hour == 16
        assert config.created.minute == 18
        assert config.created.second == 14
        assert config.created.microsecond == 515626
        device = c.devices.get_by_name('Cisco E4200')
        assert device.created.year == 2016
        assert device.created.month == 12
        assert device.created.day == 15
        assert device.created.hour == 11
        assert device.created.minute == 3
        assert device.created.second == 3
        assert device.created.microsecond == 235051
        package = c.packages.get_by_name('Cisco E4200 DHCPv4 relay-nofatal')
        assert package.created.year == 2019
        assert package.created.month == 4
        assert package.created.day == 30
        assert package.created.hour == 11
        assert package.created.minute == 58
        assert package.created.second == 11
        assert package.created.microsecond == 530826
        result = c.results.get(20220821222306)
        assert result.created.year == 2022
        assert result.created.month == 8
        assert result.created.day == 21
        assert result.created.hour == 22
        assert result.created.minute == 23
        assert result.created.second == 6
        assert result.created.microsecond == 458665

    def test_serialize(self):
        timestamp = Timestamp()
        schema = TimestampSchema()
        data = schema.dumps(timestamp)
        assert data in ('{"created": null, "cdr_created": null}',
                        '{"cdr_created": null, "created": null}')

        timestamp = Timestamp(
            created=datetime.datetime(2022, 9, 27, 10, 55, 0),
            cdr_created=datetime.datetime(2022, 9, 27, 10, 55, 0)
        )
        schema = TimestampSchema()
        data = schema.dumps(timestamp)
        assert data in ('{"created": "2022-09-27T10:55:00", "cdr_created": "2022-09-27T10:55:00"}',
                        '{"cdr_created": "2022-09-27T10:55:00", "created": "2022-09-27T10:55:00"}')

        timestamp = Timestamp(
            created=datetime.datetime(2022, 9, 27, 10, 55, 0, 0, tzinfo=datetime.timezone.utc),
            cdr_created=datetime.datetime(2022, 9, 27, 10, 55, 0, 0, tzinfo=datetime.timezone.utc)
        )
        schema = TimestampSchema()
        data = schema.dumps(timestamp)
        assert data in ('{"created": "2022-09-27T10:55:00+00:00", "cdr_created": "2022-09-27T10:55:00+00:00"}',
                        '{"cdr_created": "2022-09-27T10:55:00+00:00", "created": "2022-09-27T10:55:00+00:00"}')

    def test_deserialize(self):
        data = {
            'created': '0001-01-01T00:00:00Z',
            'cdr_created': None
        }
        schema = TimestampSchema()
        with pytest.raises(ValidationError, match='Field may not be null'):
            schema.load(data)

        data = {
            'created': None,
            'cdr_created': '0001-01-01T00:00:00Z',
        }
        schema = TimestampSchema()
        with pytest.raises(ValidationError, match='Field may not be null'):
            schema.load(data)

        data = {
            'created': '0001-01-01T00:00:00Z',
            'cdr_created': '0001-01-01T00:00:00Z'
        }
        schema = TimestampSchema()
        timestamp = schema.load(data)
        assert timestamp.created.year == 1
        assert timestamp.created.month == 1
        assert timestamp.created.day == 1
        assert timestamp.created.hour == 0
        assert timestamp.created.minute == 0
        assert timestamp.created.second == 0
        assert timestamp.created.microsecond == 0
        assert timestamp.cdr_created.year == 1
        assert timestamp.cdr_created.month == 1
        assert timestamp.cdr_created.day == 1
        assert timestamp.cdr_created.hour == 0
        assert timestamp.cdr_created.minute == 0
        assert timestamp.cdr_created.second == 0
        assert timestamp.cdr_created.microsecond == 0

        data = {
            'created': '2022-09-27T10:31:23.109739534-04:00',
            'cdr_created': '2022-09-27T10:31:23.109739534-04:00'
        }
        schema = TimestampSchema()
        timestamp = schema.load(data)
        assert timestamp.created.year == 2022
        assert timestamp.created.month == 9
        assert timestamp.created.day == 27
        assert timestamp.created.hour == 10
        assert timestamp.created.minute == 31
        assert timestamp.created.second == 23
        assert timestamp.created.microsecond == 109739
        assert timestamp.cdr_created.year == 2022
        assert timestamp.cdr_created.month == 9
        assert timestamp.cdr_created.day == 27
        assert timestamp.cdr_created.hour == 10
        assert timestamp.cdr_created.minute == 31
        assert timestamp.cdr_created.second == 23
        assert timestamp.cdr_created.microsecond == 109739

# this is a copy of the custom DateTime class that used to be in
# cdrouter/cdr_datetime.py and which we used for all timestamps before
# fields.DateTime worked the way we needed it to.
class DateTime(fields.DateTime):
    def __init__(self, format=None, **kwargs): # pylint: disable=invalid-name,redefined-builtin
        super(DateTime, self).__init__(format=format, **kwargs) # pylint: disable=super-with-arguments

    def _serialize(self, value, attr, obj): # pylint: disable=arguments-differ
        try:
            return super(DateTime, self)._serialize(value, attr, obj) # pylint: disable=super-with-arguments
        except ValidationError:
            return datetime.datetime.min

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return super(DateTime, self)._deserialize(value, attr, data) # pylint: disable=super-with-arguments
        except ValidationError:
            return datetime.datetime.min

class Timestamp(object):
    def __init__(self, **kwargs):
        self.created = kwargs.get('created', None)
        self.cdr_created = kwargs.get('cdr_created', None)

class TimestampSchema(Schema):
    created = fields.DateTime()
    cdr_created = DateTime()

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return Timestamp(**data)
