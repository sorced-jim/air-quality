#!/usr/bin/python3
"""A module for single single reads from a SDS011 sensor."""

import serial


sensors = {}


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
