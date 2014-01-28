#! /usr/bin/env python
# 25.January.2014 Liz Brooks

# script to add SensorData values to the database
# from ftp Images

import os
import sys
import argparse
import urllib2
import urllib
from datetime import datetime,tzinfo,timedelta,date
from bs4 import BeautifulSoup
import populate
import tempfile
from boto.s3.connection import S3Connection
from boto.s3.key import Key

debug = True
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'ti_dev'

account = 'THOMPSON_ISLAND'
user = 'STUDENT'
password = os.environ.get('SS_PASSWORD')
site='https://songstream.wildlifeacoustics.com'

def get_args():
    parser = argparse.ArgumentParser(description='Load data from Song Stream into the database.')
    parser.add_argument('--current', action='store_true',
                        help='Collect data from yesterday and today.')
    parser.add_argument('--history', action='store_true',
                        help='Collect data from start date to end date, inclusive.')
    parser.add_argument('--start',metavar='YYYY-MM-DD',
                        help='Retrieve and load data starting from this date.')
    parser.add_argument('--end',metavar='YYYY-MM-DD',
                        help='Retrieve and load data ending on this date.')
    args = parser.parse_args()
    if args.history == args.current:
        sys.exit("You must specify either --history OR --current")
    if args.history:
        if not (args.start and args.end):
            sys.exit("You must specify --start and --end (YYYY-MM-DD)")
        try:
            datetime.strptime(args.start,'%Y-%m-%d')
            datetime.strptime(args.end,'%Y-%m-%d')
        except Exception as e:
            sys.exit("Start or end %s" % e,)
    return args

def get_data(url):
    '''fetch data from this url'''
    f = urllib2.urlopen(url)
    data=f.read()
    f.close()
    return data

def parse_data(html):
    data = []
    soup = BeautifulSoup(html)
    rows = soup.find_all('tr')
    for row in rows:
        if len(row.contents) != 8:
            continue
        download = row.contents[4].a['href']
        name = row.contents[4].text
        datestr = row.contents[5].text
        dt = parse_dt(datestr)
        if row.contents[7].text.startswith('On Server'):
            data.append((name,download,dt))
    return data

class EST(tzinfo):
    '''returns an object representing EST time zone offset'''
    def utcoffset(self, dt):
        return timedelta(hours=-4)

def parse_dt(dt_string):
    '''takes a string and returns a datetime object'''
    tz = EST()
    # 2013-12-20 09:08:00 (-4:00)
    dt_string = dt_string[:-8]
    x=datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
    dt=datetime(int(x.year),int(x.month),int(x.day),int(x.hour),int(x.minute),int(x.second),tzinfo=tz)
    return dt

def get_image_dt(line,tmpdir):
    return datetime.now()

def get_s3_bucket():
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
    return bucket

def store_in_s3(filename, fh, bucket):
    k = Key(bucket)
    k.key = filename
    k.set_metadata("Content-Type", "audio/wav")
    k.set_contents_from_file(fh, replace=False)
    k.set_acl("public-read")

def store_data(entry, tmpdir, bucket):
        name = entry[0]
        song_url = site + entry[1]
        songhandle = urllib2.urlopen(song_url)

        filehandle = open(os.path.join(tmpdir,name),'wb')
        filehandle.write( songhandle.read() )
        filehandle.close()

        fh = open(os.path.join(tmpdir,name),'rb')
        store_in_s3(name, fh, bucket)


if __name__ == '__main__':
    args = get_args()
    if debug: print "Starting Song Stream population script..."

    # list of sensors for this source: (sensor_id, )
    keys=[ ("ss_wav", ),
         ]

    # get sensor objects for each sensor
    if debug: print "Getting sensor information..."
    sensors=populate.get_sensors(keys)

    # get data list
    if debug: print "Reading data..."
    tmpdir = tempfile.mkdtemp()
    
    #url='https://songstream.wildlifeacoustics.com/Files.php?account=THOMPSON_ISLAND&u=THOMPSON_ISLAND%2FSTUDENT&t=1390860617&a=55788a978829bb9e66becbf31879384f&fromyear=2013&frommonth=12&fromday=19&fromhour=0&toyear=2013&tomonth=12&today=21&tohour=23'
    #songurl='https://songstream.wildlifeacoustics.com/download.php?filename=THOMPSON_ISLAND/DEFAULT/00409D6B0F57/THOMPSON_20131219_060700.wav&u=THOMPSON_ISLAND/STUDENT&t=1390860677&a=f47b8167fc655feb06ffc06eaf0a601b'
    #url='https://songstream.wildlifeacoustics.com/Files.php?account=THOMPSON_ISLAND&u=THOMPSON_ISLAND%2FSTUDENT&t=1390866711&a=4052b662deda911f957b297adfc30ba6&fromyear=2013&frommonth=12&fromday=1&fromhour=0&toyear=2013&tomonth=12&today=31&tohour=23'
    url='https://songstream.wildlifeacoustics.com/Files.php?account=THOMPSON_ISLAND&u=THOMPSON_ISLAND%2FSTUDENT&t=1390868580&a=f758ce12e921b842233b2bf6968f2c26&fromyear=2013&frommonth=12&fromday=27&fromhour=0&toyear=2013&tomonth=12&today=28&tohour=23'
    url='https://songstream.wildlifeacoustics.com/Files.php?account=THOMPSON_ISLAND&u=THOMPSON_ISLAND%2FSTUDENT&t=1390872760&a=0e2ec73ca1a6754726f02005cc875a33&fromyear=2013&frommonth=12&fromday=1&fromhour=0&toyear=2013&tomonth=12&today=31&tohour=23'

    d = get_data(url)
    data = parse_data(d)

    # get the latest date already in the database
    previous_load_date = None
    if args.current:
        previous_load_date = populate.database_latest_date(keys)

    # store images on S3 & load into database
    if debug: print "Storing & loading data..."
    bucket = get_s3_bucket()
    for entry in data:
        print 'Trying', entry[0]
        if not bucket.get_key(entry[0]):
            print 'writing to S3', entry[0]
            store_data(entry, tmpdir, bucket)
        timestamp = entry[2]
        if args.current:
            if previous_load_date and timestamp <= previous_load_date:
                continue
        populate.load_data(sensor_id=sensors[keys[0][0]], time_stamp=timestamp, string_value=entry[0])

    os.removedirs(tmpdir)
    if debug: print "Finishing Song Stream population script..."

