#
# Copyright (c) 2023 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Metrics."""

from collections import namedtuple

from marshmallow import Schema, fields, post_load, EXCLUDE
from .cdr_datetime import DateTime

class Metric(object):
    """Model for CDRouter Metrics.

    :param id: (optional) Result ID as an int.
    :param seq: (optional) TestResult sequence ID as an int.
    :param created: (optional) Creation time as `DateTime`.
    :param updated: (optional) Last-updated time as `DateTime`.
    :param test_name: (optional) Test name as a string.
    :param metric: (optional) Metric name as a string.
    :param filename: (optional) Filename as a string.
    :param log_file: (optional) Log file as a string.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.seq = kwargs.get('seq', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)
        self.test_name = kwargs.get('test_name', None)
        self.metric = kwargs.get('metric', None)
        self.filename = kwargs.get('filename', None)
        self.log_file = kwargs.get('log_file', None)

class MetricSchema(Schema):
    id = fields.Int(as_string=True)
    seq = fields.Int(as_string=True)
    created = DateTime()
    updated = DateTime()
    test_name = fields.Str()
    metric = fields.Str()
    filename = fields.Str()
    log_file = fields.Str(load_default=None)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return Metric(**data)

class Bandwidth(object):
    """Model for CDRouter Bandwidth Metrics.

    :param log_file: (optional) Filepath to logfile as a string.
    :param timestamp: (optional) Timestamp for metric as a `DateTime`.
    :param metric: (optional) Metric name as a string.
    :param bandwidth: (optional) Bandwidth value as a float.
    :param bandwidth_units: (optional) Bandwidth value units as a string.
    :param result: (optional) Metric result as a string.
    :param client_interface: (optional) Client interface as a string.
    :param server_interface: (optional) Server interface as a string.
    :param streams: (optional) Stream count as an int.
    :param protocol: (optional) Protocol as a string.
    :param direction: (optional) Direction as a string.
    :param loss_percentage: (optional) Loss percentage value as a float.
    :param loss_percentage_units: (optional) Loss percentage units as a string.
    :param client_device: (optional) Client device as a string.
    :param server_device: (optional) Server device as a string.
    :param seq: (optional) TestResult sequence ID as an int.
    """
    def __init__(self, **kwargs):
        self.log_file = kwargs.get('log_file', None)
        self.timestamp = kwargs.get('timestamp', None)
        self.metric = kwargs.get('metric', None)
        self.bandwidth = kwargs.get('bandwidth', None)
        self.bandwidth_units = kwargs.get('bandwidth_units', None)
        self.result = kwargs.get('result', None)
        self.client_interface = kwargs.get('client_interface', None)
        self.server_interface = kwargs.get('server_interface', None)
        self.streams = kwargs.get('streams', None)
        self.protocol = kwargs.get('protocol', None)
        self.direction = kwargs.get('direction', None)
        self.loss_percentage = kwargs.get('loss_percentage', None)
        self.loss_percentage_units = kwargs.get('loss_percentage_units', None)
        self.client_device = kwargs.get('client_device', None)
        self.server_device = kwargs.get('server_device', None)
        self.seq = kwargs.get('seq', None)

class BandwidthSchema(Schema):
    log_file = fields.Str()
    timestamp = DateTime()
    metric = fields.Str()
    bandwidth = fields.Float()
    bandwidth_units = fields.Str()
    result = fields.Str()
    client_interface = fields.Str()
    server_interface = fields.Str()
    streams = fields.Int()
    protocol = fields.Str()
    direction = fields.Str()
    loss_percentage = fields.Float(load_default=None)
    loss_percentage_units = fields.Str(load_default=None)
    client_device = fields.Str(load_default=None)
    server_device = fields.Str(load_default=None)
    seq = fields.Int(as_string=True, load_default=None)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return Bandwidth(**data)

class Latency(object):
    """Model for CDRouter Latency Metrics.

    :param log_file: (optional) Filepath to logfile as a string.
    :param timestamp: (optional) Timestamp for metric as a `DateTime`.
    :param metric: (optional) Metric name as a string.
    :param total_latency: (optional) Total latency value as an int.
    :param total_latency_units: (optional) Total latency units as a string.
    :param result: (optional) Metric result as a string.
    :param interface: (optional) Interface as a string.
    :param download_latency: (optional) Download latency as an int.
    :param download_latency_units: (optional) Download latency units as a string.
    :param upload_latency: (optional) Upload latency as an int.
    :param upload_latency_units: (optional) Upload latency units as a string.
    :param seq: (optional) TestResult sequence ID as an int.
    """
    def __init__(self, **kwargs):
        self.log_file = kwargs.get('log_file', None)
        self.timestamp = kwargs.get('timestamp', None)
        self.metric = kwargs.get('metric', None)
        self.total_latency = kwargs.get('total_latency', None)
        self.total_latency_units = kwargs.get('total_latency_units', None)
        self.result = kwargs.get('result', None)
        self.interface = kwargs.get('interface', None)
        self.download_latency = kwargs.get('download_latency', None)
        self.download_latency_units = kwargs.get('download_latency_units', None)
        self.upload_latency = kwargs.get('upload_latency', None)
        self.upload_latency_units = kwargs.get('upload_latency_units', None)
        self.seq = kwargs.get('seq', None)

class LatencySchema(Schema):
    log_file = fields.Str()
    timestamp = DateTime()
    metric = fields.Str()
    total_latency = fields.Int()
    total_latency_units = fields.Str()
    result = fields.Str()
    interface = fields.Str()
    download_latency = fields.Int(load_default=None)
    download_latency_units = fields.Str(load_default=None)
    upload_latency = fields.Int(load_default=None)
    upload_latency_units = fields.Str(load_default=None)
    seq = fields.Int(as_string=True, load_default=None)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return Latency(**data)

class ClientBandwidth(object):
    """Model for CDRouter Client Bandwidth Metrics.

    :param timestamp: (optional) Timestamp for metric as a `DateTime`.
    :param num_rates: (optional) Size of metric bandwidth rates list as an int.
    :param rate: (optional) Metric bandwidth rates as a float list.
    """
    def __init__(self, **kwargs):
        self.timestamp = kwargs.get('timestamp', None)
        self.num_rates = kwargs.get('num_rates', None)
        self.rates = kwargs.get('rates', None)

class ClientBandwidthSchema(Schema):
    timestamp = DateTime()
    num_rates = fields.Int()
    rates = fields.List(fields.Float())

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return ClientBandwidth(**data)

class ClientLatency(object):
    """Model for CDRouter Client Latency Metrics.

    :param timestamp: (optional) Timestamp for metric as a `DateTime`.
    :param num_rates: (optional) Size of metric latency rates list as an int.
    :param rate: (optional) Metric latency rates as an int list.
    """
    def __init__(self, **kwargs):
        self.timestamp = kwargs.get('timestamp', None)
        self.num_rates = kwargs.get('num_rates', None)
        self.rates = kwargs.get('rates', None)

class ClientLatencySchema(Schema):
    timestamp = DateTime()
    num_rates = fields.Int()
    rates = fields.List(fields.Int())

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return ClientLatency(**data)

class GraphMetric(object):
    """Model for CDRouter Graph Metrics.

    :param log_file: (optional) Filepath to logfile as a string.
    :param timestamp: (optional) Timestamp for metric as a `DateTime`.
    :param metric: (optional) Metric name as a string.
    :param value: (optional) First metric value as a float.
    :param units: (optional) First metric units as a string.
    :param result: (optional) Metric result as a string.
    :param interface_1: (optional) First interface as a string.
    :param interface_2: (optional) Second interface as a string.
    :param streams: (optional) Stream count as an int.
    :param protocol: (optional) Protocol as a string.
    :param direction: (optional) Direction as a string.
    :param value_2: (optional) Second metric value as a float.
    :param units_2: (optional) Second metric units as a string.
    :param device_1: (optional) First device as a string.
    :param device_2: (optional) Second device as a string.
    :param seq: (optional) TestResult sequence ID as an int.
    """
    def __init__(self, **kwargs):
        self.log_file = kwargs.get('log_file', None)
        self.timestamp = kwargs.get('timestamp', None)
        self.metric = kwargs.get('metric', None)
        self.value = kwargs.get('value', None)
        self.units = kwargs.get('units', None)
        self.result = kwargs.get('result', None)
        self.interface_1 = kwargs.get('interface_1', None)
        self.interface_2 = kwargs.get('interface_2', None)
        self.streams = kwargs.get('streams', None)
        self.protocol = kwargs.get('protocol', None)
        self.direction = kwargs.get('direction', None)
        self.value_2 = kwargs.get('value_2', None)
        self.units_2 = kwargs.get('units_2', None)
        self.device_1 = kwargs.get('device_1', None)
        self.device_2 = kwargs.get('device_2', None)
        self.seq = kwargs.get('seq', None)

class GraphMetricSchema(Schema):
    log_file = fields.Str()
    timestamp = DateTime()
    metric = fields.Str()
    value = fields.Float(as_string=True)
    units = fields.Str()
    result = fields.Str()
    interface_1 = fields.Str()
    interface_2 = fields.Str()
    streams = fields.Int(as_string=True)
    protocol = fields.Str()
    direction = fields.Str()
    value_2 = fields.Float(as_string=True)
    units_2 = fields.Str()
    device_1 = fields.Str()
    device_2 = fields.Str()
    seq = fields.Int(as_string=True, load_default=None)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, **kwargs): # pylint: disable=unused-argument
        return GraphMetric(**data)

class Page(namedtuple('Page', ['data', 'links'])):
    """Named tuple for a page of list response data.

    :param data: :class:`metrics.Metric <metrics.Metric>` list
    :param links: :class:`cdrouter.Links <cdrouter.Links>` object
    """
