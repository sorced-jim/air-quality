import os
import single_read
import monitoring

DEVICE = os.environ.get('AIR_QUALITY_DEVICE', '/dev/ttyUSB0')
LOCATION = os.environ.get(
    'AIR_QUALITY_LOCATION', os.environ['HOSTNAME'])


pm25, pm10 = single_read.single_read(DEVICE)
monitoring.write_time_series(LOCATION, pm25, pm10)
