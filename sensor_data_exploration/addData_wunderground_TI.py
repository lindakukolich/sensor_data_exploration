#! /usr/bin/env python
# 12.January.2014 Liz Brooks

# script to add SensorData values to the database
# from Weather Underground Thompson Island
# (run with -h to see full usage message)
# as new sensors are added, add them to the list of sensors (keys) in main.

import os,sys
import argparse
import urllib2
import json
from datetime import datetime,tzinfo,timedelta

debug = True
APIkey='2cbf77167bf2fe35'
stationID='KMABOSTO32'

def get_args():
    parser = argparse.ArgumentParser(description='Load historical data from wunderground into the database.')
    parser.add_argument('-d','--date',metavar='YYYYMMDD', nargs='+',
                        help='Retrieve and load data from this date.')
    parser.add_argument('--history', action='store_true',
                        help='Collect historical data from the specified dates.')
    parser.add_argument('--current', action='store_true',
                        help='Collect current conditions. (-d is ignored)')
    args = parser.parse_args()
    if args.history == args.current:
        sys.exit("You must specify either --history OR --current")
    if args.history and not args.date:
        sys.exit("You must specify at least one date: '-d YYYYMMDD'")
    if args.date:
        for d in args.date:
            if not (len(d)==8 and d.isdigit()):
                sys.exit("%s is not in proper date format: YYYYMMDD"% d,)
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
    j=f.read()
    data=json.loads(j)
    f.close()
    return data

class EST(tzinfo):
    '''returns an object representing EST time zone offset'''
    def utcoffset(self, dt):
        return timedelta(hours=-5)

def assemble_dt(date_dict):
    '''takes a date dictionary and returns a datetime object'''
    tz = EST()
    # "observations": [ { "date": { "pretty": "12:05 AM EST on December 31, 2013", 
    #   "year": "2013","mon": "12","mday": "31","hour": "00","min": "05","tzname": "America/New_York" },
    #  x=datetime.strptime(dt_string, "%I:%M %p %Z on %B %d, %Y")
    dt=datetime(int(date_dict['year']),int(date_dict['mon']),int(date_dict['mday']),
                int(date_dict['hour']),int(date_dict['min']),tzinfo=tz)
    return dt

def parse_dt(dt_string):
    '''takes a string and returns a datetime object'''
    tz = EST()
    # "observation_time_rfc822":"Fri, 10 Jan 2014 11:52:09 -0500"
    ## grrrr, %z is not available!
    dt_string = dt_string[:-6]
    x=datetime.strptime(dt_string, "%a, %d %b %Y %H:%M:%S")
    dt=datetime(x.year,x.month,x.day,x.hour,x.minute,x.second, tz)
    return dt

def load(sensor_id,time_stamp,num_value=None,string_value=None,value_is_number=False):
    '''creates a sensorData entry (unless already exists)'''
    result=SensorData.objects.get_or_create(sensor_id=sensor_id,
                                            time_stamp=time_stamp,
                                            num_value=num_value,
                                            string_value=string_value,
                                            value_is_number=value_is_number)
    return result


if __name__ == '__main__':
    if debug: print "Starting Weather Underground population script..."
    args = get_args()

    # environment setup ---------------------------------------------------
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensor_data_exploration.settings')
    from sensor_data_exploration.apps.explorer.models import *

    # list of sensors for this source
    keys=[("wu_ti_temp_f","tempi"),
          ("wu_ti_wind_mph","wspdi"),
          ("wu_ti_wind_dir","wdire"),
          ("wu_ti_precip_1hr_in","precip_ratei"),
    ]

    # get sensor objects for each sensor
    if debug: print "Getting sensor information..."
    sensors=get_sensors(keys)

    # process history
    if args.history:
        for date in args.date:
            if debug: print "Reading data for date %s...\n"% date,
            url='http://api.wunderground.com/api/%s/history_%s/q/pws:%s.json' % (APIkey,date,stationID)
            data = get_data(url)

            if debug: print "Loading data for date %s...\n"% date,
            for entry in data["history"]["observations"]:
                ts = assemble_dt(entry["date"])
                for key in keys:
                    value = entry[ key[1] ]
                    numeric = sensors[key[0]].data_is_number
                    if numeric:
                        value = float(value)
                        load(sensor_id=sensors[key[0]], time_stamp=ts, num_value=value, value_is_number=True)
                    else:
                        load(sensor_id=sensors[key[0]], time_stamp=ts, string_value=value)

    # process current
    elif args.current:
        pass

    if debug: print "Finishing Weather Underground population script..."
