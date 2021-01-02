import os
from google.api import metric_pb2 as ga_metric
from google.cloud import monitoring_v3


PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT']
PROJECT = f'projects/{PROJECT_ID}'
client = monitoring_v3.MetricServiceClient()


def point(name, value):
    series = monitoring_v3.TimeSeries()
    series.metric.type = 'custom.googleapis.com/air_quality/particulates'
    series.resource.type = '???'
    series.resource.labels['location'] = location
    series.resource.labels['size'] = name
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


def write_time_series(location, pm25, pm_10):
    client.create_time_series(name=PROJECT, time_series=[point('2.5', pm25)])
    client.create_time_series(name=PROJECT, time_series=[point('10', pm10)])


def create_metrics():
    descriptor = ga_metric.MetricDescriptor()
    descriptor.type = 'custom.googleapis.com/air_quality/particulates'
    descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
    descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
    descriptor.description = 'Air quality particulates'
    descriptor = client.create_metric_descriptor(
        name=PROJECT, metric_descriptor=descriptor
    )
    print('Created {}.'.format(descriptor.name))


if __name__ == '__main__':
  create_metrics()
