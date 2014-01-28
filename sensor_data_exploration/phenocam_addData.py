#! /usr/bin/env python
# 25.January.2014 Liz Brooks

# script to add SensorData values to the database
# from plant phenology camera

import os
import sys
import argparse
from datetime import datetime,tzinfo,timedelta
import exifread
import populate
from boto.s3.connection import S3Connection
from boto.s3.key import Key

debug = True
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'ti_dev'
s3_path ='https://s3.amazonaws.com/ti_dev/'

def get_args():
    parser = argparse.ArgumentParser(description='Load data from Phenocam into the database.')
    parser.add_argument('--dir',metavar='PATH',
                        help='Directory folder containing the files to upload.')
    parser.add_argument('--ext',metavar='jpg',default='JPG',
                        help='File extension on the files to upload, default "JPG".')
    args = parser.parse_args()
    if not args.dir:
        sys.exit("You must specify a directory to upload from. Type -h for help.")
    if not os.path.isdir(args.dir):
        sys.exit("%s is not a valid directory" % args.dir,)
    return args

def get_s3_bucket():
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
    return bucket

def store_in_s3(filename, fh, bucket):
    k = Key(bucket)
    k.key = filename
    k.set_metadata("Content-Type", "image/jpg")
    k.set_contents_from_file(fh, replace=False)
    k.set_acl("public-read")

class EST(tzinfo):
    '''returns an object representing EST time zone offset'''
    def utcoffset(self, dt):
        return timedelta(hours=-5)

def parse_dt(dt_string):
    '''takes a string and returns a datetime object'''
    tz = EST()
    # 2011:03:12 14:19:00
    x=datetime.strptime(dt_string, "%Y:%m:%d %H:%M:%S")
    dt=datetime(int(x.year),int(x.month),int(x.day),int(x.hour),int(x.minute),int(x.second),tzinfo=tz)
    return dt

def get_datetime(fh):
    tags = exifread.process_file(fh, details=False)
    try:
        dt_string = tags['Image DateTime']
        dt_string = str(dt_string)  # value was an 'instance' type object
        dt = parse_dt(dt_string)
    except Exception as e:
        if debug: print "Error reading datetime from file metadata.\n%s" % e,
        return None
    return dt


if __name__ == '__main__':
    args = get_args()
    if debug: print "Starting Phenocam population script..."

    # list of sensors for this source: (sensor_id, )
    keys=[ ("pp_camera", ),
         ]

    # get sensor objects for each sensor
    if debug: print "Getting sensor information..."
    sensors=populate.get_sensors(keys)

    # get list of filenames
    if debug: print "Getting filenames..."
    allfiles = os.listdir(args.dir)
    filenames = [f for f in allfiles if f.endswith(args.ext)]

    # store images on S3 & load into database
    if debug: print "Storing & loading data..."
    bucket = get_s3_bucket()
    for name in filenames:
        pname = 'phenocam_'+name
        s3_url = s3_path + pname
        if debug: print 'checking', pname
        if not bucket.get_key(pname):
            if debug: print 'writing to S3', pname
            fh = open(os.path.join(args.dir,name),'rb')
            store_in_s3(pname, fh, bucket)
            fh.close()
        fh = open(os.path.join(args.dir,name),'rb')
        timestamp = get_datetime(fh)
        if timestamp:
            if debug: print 'storing', pname
            populate.load_data(sensor_id=sensors[keys[0][0]], time_stamp=timestamp, string_value=s3_url)

    if debug: print "Finishing Phenocam population script..."
