#! /usr/bin/env python
# 12.January.2014 Liz Brooks

# script to add SensorData values to the database
# from Weather Underground Thompson Island
# (run with -h to see full usage message)
# as new sensors are added, add them to the list of sensors (keys) in main.

import os
import sys
import argparse
import urllib2
import json
from datetime import datetime,tzinfo,timedelta,date
from time import sleep
import populate

debug = True
APIkey=os.environ.get('WU_API_KEY')
stationID='KMABOSTO32'

def get_args():
    parser = argparse.ArgumentParser(description='Load data from Weather Underground into the database.')
    parser.add_argument('--current', action='store_true',
                        help='Collect current conditions.')
    parser.add_argument('--history', action='store_true',
                        help='Collect data from start date to end date, inclusive.')
    parser.add_argument('--start',metavar='YYYY-MM-DD',
                        help='Retrieve and load data starting from this date.')
    parser.add_argument('--end',metavar='YYYY-MM-DD',
                        help='Retrieve and load data ending on this date.')
    parser.add_argument('--yesterday', action='store_true',
                        help="Retrieve and load yesterday's data.")
    parser.add_argument('--today', action='store_true',
                        help="Retrieve and load today's data.")
    args = parser.parse_args()
    if args.history == args.current:
        sys.exit("You must specify either --history OR --current")
    if args.history:
        if not ((args.start and args.end) or args.yesterday or args.today):
            sys.exit("You must specify start & end dates, or yesterday or today.")
        if args.start:
            try:
                datetime.strptime(args.start,'%Y-%m-%d')
                datetime.strptime(args.end,'%Y-%m-%d')
            except Exception as e:
                sys.exit("Start or end %s" % e,)
    return args

def next_day(day):
    date = datetime.strptime(day,'%Y%m%d') + timedelta(1)
    day = date.strftime('%Y%m%d')
    return day

def get_date_list(args):
    dates = []
    if args.start:
        start_day = args.start.replace('-','')
        end_day = args.end.replace('-','')
        dates.append(start_day)
        tomorrow = next_day(start_day)
        while tomorrow <= end_day:
            dates.append(tomorrow)
            tomorrow = next_day(tomorrow)
    if args.yesterday:
        yday = date.today() + timedelta(-1)
        dates.append(yday.strftime('%Y%m%d'))
    if args.today:
        today = date.today()
        dates.append(today.strftime('%Y%m%d'))
    return dates

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

class EDT(tzinfo):
    '''returns an object representing EDT time zone offset'''
    def utcoffset(self, dt):
        return timedelta(hours=-4)


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
    tz = EDT() # changed for testing. This should not be hard-coded
    # "observation_time_rfc822":"Fri, 10 Jan 2014 11:52:09 -0500"
    ## grrrr, %z is not available!
    dt_string = dt_string[:-6]
    x=datetime.strptime(dt_string, "%a, %d %b %Y %H:%M:%S")
    dt=datetime(int(x.year),int(x.month),int(x.day),int(x.hour),int(x.minute),int(x.second),tzinfo=tz)
    return dt


if __name__ == '__main__':
    args = get_args()
    dates = get_date_list(args)  # might be an empty list

    if debug: print "Starting Weather Underground population script..."

    # list of sensors for this source 
    # (sensor_id, field name current-conditions, field name history)
    keys=[("wu_ti_temp_c","temp_c","tempm"),
          ("wu_ti_relative_humidity","relative_humidity","hum"),
          ("wu_ti_wind_dir","wind_dir","wdire"),
          ("wu_ti_wind_degrees","wind_degrees","wdird"),
          ("wu_ti_wind_kph","wind_kph","wspdm"),
          ("wu_ti_wind_gust_kph","wind_gust_kph","wgustm"),
          ("wu_ti_pressure_mb","pressure_mb","pressurem"),
          ("wu_ti_dewpoint_c","dewpoint_c","dewptm"),
          ("wu_ti_precip_1hr_metric","precip_1hr_metric","precip_ratem"),
          ("wu_ti_precip_today_metric","precip_today_metric","precip_totalm"),
    ]

    # get sensor objects for each sensor
    if debug: print "Getting sensor information..."
    sensors=populate.get_sensors(keys)

    # load historical sensor data
    if args.history:
        for date in dates:
            if debug: print "Reading data for date %s...\n"% date,
            url='http://api.wunderground.com/api/%s/history_%s/q/pws:%s.json' % (APIkey,date,stationID)
            data = get_data(url)
            #sleep for 10 seconds to avoid hitting the wunderground API too frequently
            sleep(10) 

            if debug: print "Loading data for date %s...\n"% date,
            for entry in data["history"]["observations"]:
                timestamp = assemble_dt(entry["date"])
                for key in keys:
                    value = entry[ key[2] ]
                    numeric = sensors[key[0]].data_is_number
                    if numeric:
                        value = float(value)
                        populate.load_data(sensor_id=sensors[key[0]], time_stamp=timestamp, num_value=value, value_is_number=True)
                    else:
                        populate.load_data(sensor_id=sensors[key[0]], time_stamp=timestamp, string_value=value)

    # load current sensor data
    elif args.current:
        if debug: print "Reading current data..."
        url='http://api.wunderground.com/api/%s/conditions/q/pws:%s.json' % (APIkey,stationID)
        data = get_data(url)

        if debug: print "Loading current data..."
        entry = data["current_observation"]
        timestamp = parse_dt(entry["observation_time_rfc822"])
        for key in keys:
            value = entry[ key[1] ]
            if key[1] == "relative_humidity":
                value = value.rstrip(' %')
            numeric = sensors[key[0]].data_is_number
            if numeric:
                value = float(value)
                populate.load_data(sensor_id=sensors[key[0]], time_stamp=timestamp, num_value=value, value_is_number=True)
            else:
                populate.load_data(sensor_id=sensors[key[0]], time_stamp=timestamp, string_value=value)

    if debug: print "Finishing Weather Underground population script..."
