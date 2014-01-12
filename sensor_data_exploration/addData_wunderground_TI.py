#! /usr/bin/env python
# 12.January.2014 Liz Brooks
# script to add to the database SensorData values
# from Weather Underground Thompson Island

# *** very much still a work in progress, 
# but will load some temperature data into the DB for testing ***

import os
from datetime import datetime,tzinfo,timedelta
debug = True

class gmt5(tzinfo):
    """ """
    def utcoffset(self, dt):
        return timedelta(hours=-5)

## note: "observation_time_rfc822":"Fri, 10 Jan 2014 11:52:09 -0500"
## mytime=datetime.strptime("Fri, 10 Jan 2014 09:52:09 -0500", "%a, %d %b %Y %H:%M:%S %z")
## grrrr, %z is not available!
## substring obs time?


if __name__ == '__main__':
    # environment setup ---------------------------------------------------
    if debug: print "Starting Weather Underground population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensor_data_exploration.settings')
    from sensor_data_exploration.apps.explorer.models import *

    # -------------
    try:
        sensor = Sensor.objects.get(sensor_id="wu_ti_temp_f")
    except Sensor.DoesNotExist:
        print "This sensor does not exist!"

    tz = gmt5()

    mytime = datetime(2014,1,5,9,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=10, sensor_id=sensor)
    mytime = datetime(2014,1,5,12,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=15, sensor_id=sensor)
    mytime = datetime(2014,1,6,9,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=15, sensor_id=sensor)
    mytime = datetime(2014,1,6,12,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=25, sensor_id=sensor)
    mytime = datetime(2014,1,7,9,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=20, sensor_id=sensor)
    mytime = datetime(2014,1,7,12,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=25, sensor_id=sensor)
    mytime = datetime(2014,1,8,9,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=25, sensor_id=sensor)
    mytime = datetime(2014,1,8,12,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=25, sensor_id=sensor)
    mytime = datetime(2014,1,9,9,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=40, sensor_id=sensor)
    mytime = datetime(2014,1,9,12,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=50, sensor_id=sensor)
    mytime = datetime(2014,1,10,9,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=-5, sensor_id=sensor)
    mytime = datetime(2014,1,10,12,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=-2, sensor_id=sensor)
    mytime = datetime(2014,1,11,9,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=5, sensor_id=sensor)
    mytime = datetime(2014,1,11,12,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=25, sensor_id=sensor)
    mytime = datetime(2014,1,12,9,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=25, sensor_id=sensor)
    mytime = datetime(2014,1,12,12,52,9,tzinfo=tz)
    x=SensorData.objects.create(time_stamp=mytime, num_value=55, sensor_id=sensor)
