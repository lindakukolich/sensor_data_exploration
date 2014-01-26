#! /usr/bin/env python
# 15.January.2014 Liz Brooks

# script to add SensorData values to the database
# from Beacon Buoys
# (run with -h to see full usage message)
# as new sensors are added, add them to the list of sensors (keys) in main.

import sys
import argparse
import urllib2
from datetime import datetime,tzinfo,timedelta
import populate

debug = True
deviceID='2232583' # buoy #5 Thompson Island Mooring Field

def get_args():
    parser = argparse.ArgumentParser(description='Load historical data from beacon buoy into the database.')
    parser.add_argument('--history', action='store_true',
                        help='Collect all available data.')
    parser.add_argument('--current', action='store_true',
                        help='Collect data from dates more recent than those already in the database.')
    parser.add_argument('--cesn', action='store_true',
                        help='use alternate url - cesn, rather than hobolink, to get data.')
    args = parser.parse_args()
    if args.history == args.current:
        sys.exit("You must specify either --history OR --current")
    return args

def get_data(url):
    '''fetch data from this url'''
    f = urllib2.urlopen(url)
    datalist=f.readlines()
    f.close()
    return datalist

def clean_data(datalist,cesn_format):
    data = []
    if not cesn_format:
        for i,line in enumerate(datalist):
            if line.startswith('----'):
                datalist = datalist[i+2:]
                break
    for line in datalist:
        if line.startswith('#'): continue
        data.append(line.split(','))
    return data

class EST(tzinfo):
    '''returns an object representing EST time zone offset'''
    def utcoffset(self, dt):
        return timedelta(hours=-5)
    def dst(self, dt):
        return timedelta(0)

def parse_dt(dt_string):
    '''takes a string and returns a datetime object'''
    tz = EST()
    # '12/6/13 14:00:00', "Time, Eastern Daylight Time"
    # or '2013-08-22 12:00:00'
    if '/' in dt_string:
        x=datetime.strptime(dt_string, "%m/%d/%y %H:%M:%S")
    else:
        x=datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
    dt=datetime(int(x.year),int(x.month),int(x.day),int(x.hour),int(x.minute),int(x.second),tzinfo=tz)
    return dt


if __name__ == '__main__':
    args = get_args()
    if debug: print "Starting Beacon Buoy population script..."

    # list of sensors for this source: (sensor_id, field# Hobolink (default), field# Cesn)
    keys=[("buoy5_Salinity",13,2),
          ("buoy5_CDOM",12,3),
          ("buoy5_WaterTemp",2,5),
          ("buoy5_AirTemp",7,6),
          ("buoy5_WindSpeed",3,7),
          ("buoy5_GustSpeed",4,8),
          ("buoy5_WindDir",5,9),
          ("buoy5_BuoyDir",6,10),
          ("buoy5_Pressure",10,11),
          ("buoy5_RelHumidity",8,12),
          ("buoy5_DewPt",9,13),
          ("buoy5_PAR",11,14),
      ]

    # get sensor objects for each sensor
    if debug: print "Getting sensor information..."
    sensors=populate.get_sensors(keys)

    # get data list
    if debug: print "Reading data..."
    url='http://webservice.hobolink.com/rest/public/devices/%s/data_files/latest/txt' % (deviceID,)
    if args.cesn:
        url='http://cesn.org/live/archive_Thompson.txt'
    data = get_data(url)
    data = clean_data(data,args.cesn)

    # get the latest date already in the database
    previous_load_date = None
    if args.current:
        previous_load_date = populate.database_latest_date(keys)

    # load sensor data
    if debug: print "Loading data..."
    for entry in data:
        timestamp = parse_dt(entry[1])
        if args.current:
            if previous_load_date and timestamp <= previous_load_date:
                continue
        for key in keys:
            value = entry[ key[1] ]
            if args.cesn:
                value = entry[ key[2] ]
            if value.startswith('-888.') or value.startswith('-889.'):
                continue
            numeric = sensors[key[0]].data_is_number
            if numeric:
                value = float(value)
                populate.load_data(sensor_id=sensors[key[0]], time_stamp=timestamp, num_value=value, value_is_number=True)
            else:
                populate.load_data(sensor_id=sensors[key[0]], time_stamp=timestamp, string_value=value)

    if debug: print "Finishing Beacon Buoy population script..."

