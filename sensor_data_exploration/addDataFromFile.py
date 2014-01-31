#! /usr/bin/env python
# 30.January.2014 Liz Brooks

# script to add SensorData values to the database
# given a file containing time_stamp and string_value's
# such as the output from a local sqlite database, e.g.:
#- select time_stamp,string_value from explorer_sensordata where sensor_id_id == 'pp_camera';
#- 2011-03-15 00:54:00|https://s3.amazonaws.com/ti_dev/phenocam_WSPC0034.JPG

import sys
import argparse
from datetime import datetime,tzinfo,timedelta
import populate
debug = True

def get_args():
    parser = argparse.ArgumentParser(description='Load data from a file into the database.')
    parser.add_argument('--file', metavar='NAME',
                        help='File containing data to be loaded.')
    parser.add_argument('--sensor',metavar='NAME',
                        help='Name of the sensor this data applies to.')
    parser.add_argument('--delim', metavar="'|'", default='|',
                        help='Field separator (delimeter) used in file, default is pipe.')
    args = parser.parse_args()
    if not (args.file and args.sensor):
        sys.exit("File name and Sensor name are required.")
    return args

class UTC(tzinfo):
    '''returns an object representing UTC time zone offset'''
    def utcoffset(self, dt):
        return timedelta(0)

def parse_dt(dt_string):
    '''takes a string and returns a datetime object'''
    tz = UTC()
    # 2011-03-15 00:54:00
    x=datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
    dt=datetime(int(x.year),int(x.month),int(x.day),int(x.hour),int(x.minute),int(x.second),tzinfo=tz)
    return dt


if __name__ == '__main__':
    args = get_args()
    if debug: print "Starting 'load data from file' population script..."

    # get sensor object
    if debug: print "Getting sensor information..."
    try:
        sensors=populate.get_sensors([(args.sensor,)])
    except:
        sys.exit("'%s' is not a sensor in the database." % args.sensor,)

    # read file
    data = []
    if debug: print "Reading file contents..."
    f = open(args.file,'r')
    data = f.readlines()

    # load data into sensordata table
    if debug: print "Loading data..."
    for line in data:
        datestr,value = line.strip().split(args.delim)
        dt = parse_dt(datestr)
        populate.load_data(sensor_id=sensors[args.sensor], time_stamp=dt, string_value=value)

    if debug: print "Finishing 'load data from file' population script..."
