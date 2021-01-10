#!/usr/bin/python3

import os
import sds011_read
import monitoring

DEVICE = os.environ.get('AIR_QUALITY_DEVICE', '/dev/ttyUSB0')
LOCATION = os.environ.get(
    'AIR_QUALITY_LOCATION', os.uname().nodename)


pm25, pm10 = sds011_read.outlier_read(DEVICE)
monitoring.write_time_series(LOCATION, pm25, pm10)
