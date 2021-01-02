import os
import time

from google.api import metric_pb2 as ga_metric
from google.api import label_pb2
from google.cloud import monitoring_v3


PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT']
PROJECT = f'projects/{PROJECT_ID}'
client = monitoring_v3.MetricServiceClient()


def point(location, name, value):
    series = monitoring_v3.TimeSeries()
    series.metric.type = 'custom.googleapis.com/air_quality/particulates/' + name
    series.resource.type = 'global'
    series.metric.labels['location'] = location
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {'end_time': {'seconds': seconds, 'nanos': nanos}}
    )
    point = monitoring_v3.Point({'interval': interval,
                                 'value': {'double_value': value}})
    series.points = [point]
    return series


def write_time_series(location, pm25, pm10):
    client.create_time_series(
        name=PROJECT, time_series=[point(location, '2.5', pm25)])
    client.create_time_series(
        name=PROJECT, time_series=[point(location, '10', pm10)])


def create_metric(name):
    descriptor = ga_metric.MetricDescriptor()
    descriptor.type = 'custom.googleapis.com/air_quality/particulates/' + name
    descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
    descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
    descriptor.description = 'Air quality particulates'
    descriptor.labels.extend([
      label_pb2.LabelDescriptor(
          key='location',
          value_type=label_pb2.LabelDescriptor.ValueType.STRING,
          description='Location where the measurement was made.')
    ])
    descriptor = client.create_metric_descriptor(
        name=PROJECT, metric_descriptor=descriptor
    )
    print('Created {}.'.format(descriptor.name))


def create_metrics():
  create_metric('2.5')
  create_metric('10')


if __name__ == '__main__':
  create_metrics()
  write_time_series('test', 0.1, 0.2)
