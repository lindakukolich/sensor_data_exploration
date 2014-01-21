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
debug = True

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
    data = []
    urls = ['https://datagarrison.com/users/011998000354656/011998000354839/temp/DataGarrison_Cell_Station_047.txt',
            'https://datagarrison.com/users/011998000354656/011998000354839/temp/DataGarrison_Cell_Station_048.txt',
            'https://datagarrison.com/users/011998000354656/011998000354839/temp/DataGarrison_Cell_Station_049.txt',
            'https://datagarrison.com/users/011998000354656/011998000354839/temp/DataGarrison_Cell_Station_050.txt',
    ]
    if args.history:
        for url in urls:
            d = get_data(url)
            data.extend(clean_data(d))
    else:
        d = get_data(urls[-1])
        data.extend(clean_data(d))

    # load data
    if debug: print "Loading data..."
    for i,entry in enumerate(data):
        if debug: print i,
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

    if debug: print "\nFinishing population script..."

