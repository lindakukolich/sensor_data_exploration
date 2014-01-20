#! /usr/bin/env python
# 15.January.2014 Liz Brooks

# script to add SensorData values to the database
# from Salt Pond hydrologic sensor
# (run with -h to see full usage message)
# as new sensors are added, add them to the list of sensors (keys) in main.

import os,sys
import argparse
import urllib2
from datetime import datetime,tzinfo,timedelta
from time import time, ctime
debug = True

# data slices  start time, end time (local time)
# 047   09/27/13 10:30 am   10/11/13 10:40 pm	
data047='https://datagarrison.com/users/011998000354656/011998000354839/download.php?data_launch=47&data_start=1380277800&data_end=1381531200&data_desc=DataGarrison%20Cell%20Station&utc=0'
url047='https://datagarrison.com/users/011998000354656/011998000354839/temp/DataGarrison_Cell_Station_047.txt'

# 048   10/11/13 10:40 pm   11/18/13 6:50 pm	
data048='https://datagarrison.com/users/011998000354656/011998000354839/download.php?data_launch=48&data_start=1381531200&data_end=1384800600&data_desc=DataGarrison%20Cell%20Station&utc=0'
url048='https://datagarrison.com/users/011998000354656/011998000354839/temp/DataGarrison_Cell_Station_048.txt'

# 049   11/21/13 12:20 pm   01/03/14 10:35 am	
data049='https://datagarrison.com/users/011998000354656/011998000354839/download.php?data_launch=49&data_start=1385036400&data_end=1388745300&data_desc=DataGarrison%20Cell%20Station&utc=0'
url049='https://datagarrison.com/users/011998000354656/011998000354839/temp/DataGarrison_Cell_Station_049.txt'

# 050   01/15/14 1:50 pm   present
now=int(time())
data050='https://datagarrison.com/users/011998000354656/011998000354839/download.php?data_launch=50&data_start=1389793800&data_end='+str(now)+'&data_desc=DataGarrison%20Cell%20Station&utc=0'
url050='https://datagarrison.com/users/011998000354656/011998000354839/temp/DataGarrison_Cell_Station_050.txt'

def get_args():
    parser = argparse.ArgumentParser(description='Load historical data into the database.')
    parser.add_argument('--history', action='store_true',
                        help='Collect all available data.')
    parser.add_argument('--current', action='store_true',
                        help='Collect data from dates more recent than those already in the database.')
    args = parser.parse_args()
    if args.history == args.current:
        sys.exit("You must specify either --history OR --current")
    return args

def get_sensors(keys):
    '''return a dictionary containing the sensor object for each sensor name in the keys list'''
    sensors={}
    for key in keys:
        sid=key[0]
        try:
            sobj = Sensor.objects.get(sensor_id=sid)
        except Sensor.DoesNotExist:
            sys.exit("%s is not a sensor in the database." % sid)
        sensors[sid] = sobj
    return sensors

def get_data(url):
    '''fetch data from this url'''
    f = urllib2.urlopen(url)
    datalist=f.readlines()
    f.close()
    return datalist

def clean_data(datalist):
    data = []
    # skip first 3 header lines
    datalist = datalist[3:]
    for line in datalist:
        if line.startswith('#'): continue
        data.append(line.split('\t'))
    return data

class EST(tzinfo):
    '''returns an object representing EST time zone offset'''
    def utcoffset(self, dt):
        return timedelta(hours=-5)

def parse_dt(dt_string):
    '''takes a string and returns a datetime object'''
    tz = EST()
    # '01/15/14 15:05:00'
    x=datetime.strptime(dt_string, "%m/%d/%y %H:%M:%S")
    dt=datetime(int(x.year),int(x.month),int(x.day),int(x.hour),int(x.minute),int(x.second),tzinfo=tz)
    return dt

def load(sensor_id,time_stamp,num_value=None,string_value=None,value_is_number=False):
    '''creates a sensorData entry (unless already exists)'''
    result=SensorData.objects.get_or_create(sensor_id=sensor_id,
                                            time_stamp=time_stamp,
                                            num_value=num_value,
                                            string_value=string_value,
                                            value_is_number=value_is_number)
    return result

def check_date():
    pass

if __name__ == '__main__':
    args = get_args()
    if debug: print "Starting population script..."

    # environment setup ---------------------------------------------------
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensor_data_exploration.settings')
    from sensor_data_exploration.apps.explorer.models import *

    # list of sensors for this source: (sensor_id, field_#)
    keys=[ ("sp_air_pressure",1),
           ("sp_water_temp",2),
           ("sp_salinity",3),
           ("sp_water_pressure",4),
           ("sp_chlorophyll",5),
           ("sp_disolved_oxygen",6),
           ("sp_rel_pressure",7),
         ]

    # get sensor objects for each sensor
    if debug: print "Getting sensor information..."
    sensors=get_sensors(keys)

    # get data list
    if debug: print "Reading data..."
    url049='https://datagarrison.com/users/011998000354656/011998000354839/temp/DataGarrison_Cell_Station_049.txt'
    data = get_data(url049)  # TBD!!!!!!
    data = clean_data(data)

    # load data
    if debug: print "Loading data..."
    for entry in data:
        ts = parse_dt(entry[0])
        # if args.current check here for > max prev date
        for key in keys:
            value = entry[ key[1] ]
            numeric = sensors[key[0]].data_is_number
            if numeric:
                value = float(value)
                load(sensor_id=sensors[key[0]], time_stamp=ts, num_value=value, value_is_number=True)
            else:
                load(sensor_id=sensors[key[0]], time_stamp=ts, string_value=value)

    if debug: print "Finishing population script..."

