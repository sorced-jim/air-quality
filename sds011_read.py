#!/usr/bin/python3
"""A module for reading from a SDS011 sensor."""

import datetime
import serial
import time


sensors = {}


def median_read(device, reads=5, delay=None):
  """Read the device `reads` times and return the median values."""
  if delay is None:
    delay = datetime.timedelta(seconds=1)

  pm25 = []
  pm10 = []
  for _ in range(reads):
    v = single_read(device)
    pm25.append(v[0])
    pm10.append(v[0])
    if delay:
      time.sleep(delay.total_seconds())

  median = reads/2
  return sorted(pm25)[median], sorted(pm10)[median]


def single_read(device):
  sensor = sensors.get(device)
  if not sensor:
    sensor = serial.Serial(device)
    sensors[device] = sensor

  data = []
  for _ in range(10):
    data.append(sensor.read())

  pm2_5 = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
  pm10 = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
  return pm2_5, pm10


if __name__ == '__main__':
  print('PM2.5 %s, PM10 %s' % single_read('/dev/ttyUSB0'))