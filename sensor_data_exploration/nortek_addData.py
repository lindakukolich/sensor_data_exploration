#! /usr/bin/env python
# 25.January.2014 Liz Brooks

# script to add SensorData values to the database
# from Nortek sensors

import sys
import argparse
import urllib2
import urllib
from datetime import datetime,tzinfo,timedelta,date
from bs4 import BeautifulSoup
import populate

debug = True
stationID = 'e22a07ba'

def get_args():
    parser = argparse.ArgumentParser(description='Load historical data into the database.')
    parser.add_argument('--history', action='store_true',
                        help='Collect data from start date to end date, inclusive.')
    parser.add_argument('--current', action='store_true',
                        help='Collect data from dates more recent than those already in the database.')
    parser.add_argument('--startdate',metavar='YYYY-MM-DD',
                        help='Retrieve and load data from this date.')
    parser.add_argument('--enddate',metavar='YYYY-MM-DD',
                        help='Retrieve and load data from this date.')
    args = parser.parse_args()
    if args.history == args.current:
        sys.exit("You must specify either --history OR --current")
    if args.history and not (args.startdate and args.enddate):
        sys.exit("You must specify --startdate and --enddate (YYYY-MM-DD)")
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
    rows = rows[7:]    #skip header first 6 lines
    for row in rows:
        entry = []
        for c in row.contents:
            entry.append(c.text)
        data.append(entry)
    return data

class EST(tzinfo):
    '''returns an object representing EST time zone offset'''
    def utcoffset(self, dt):
        return timedelta(hours=-5)

def parse_dt(dt_string):
    '''takes a string and returns a datetime object'''
    tz = EST()
    # 24.01.2014 04:50:08
    x=datetime.strptime(dt_string, "%d.%m.%Y %H:%M:%S")
    dt=datetime(int(x.year),int(x.month),int(x.day),int(x.hour),int(x.minute),int(x.second),tzinfo=tz)
    return dt


if __name__ == '__main__':
    args = get_args()
    if debug: print "Starting Nortek population script..."

    # (groups of) list of sensors for this source: (sensor_id, field_#)
    groupkeys = { 'MetData':[ ("nor_Wind_speed_avg",2),
                              ("nor_Wind_speed_max",3),
                              ("nor_Wind_direction",4),
                              ("nor_Temperature",5),
                              ("nor_Humidity",6),
                              ("nor_Pressure",7),
                              ("nor_Rain",8),
                          ],
                  'Profile':[ ("nor_Cell_Temperature",3),
                              ("nor_Cell_Tilt",4),
                              ("nor_Cell1_Speed",5),
                              ("nor_Cell1_Direction",6),
                              ("nor_Cell1_Amplitude",7),
                              ("nor_Cell2_Speed",8),
                              ("nor_Cell2_Direction",9),
                              ("nor_Cell2_Amplitude",10),
                              ("nor_Cell3_Speed",11),
                              ("nor_Cell3_Direction",12),
                              ("nor_Cell3_Amplitude",13),
                              ("nor_Cell4_Speed",14),
                              ("nor_Cell4_Direction",15),
                              ("nor_Cell4_Amplitude",16),
                              ("nor_Cell5_Speed",17),
                              ("nor_Cell5_Direction",18),
                              ("nor_Cell5_Amplitude",19),
                          ],
              }

    # assemble start and end times for url request
    timestr='T05:00:00Z'  # somewhat arbitrary
    if args.history:
        startdate = args.startdate + timestr
        enddate = args.enddate + timestr
    else:
        yesterday = date.today() + timedelta(-1)
        tomorrow = date.today() + timedelta(1)
        startdate = yesterday.strftime('%Y-%m-%d') + timestr
        enddate = tomorrow.strftime('%Y-%m-%d') + timestr

    start=urllib.quote_plus(startdate)
    end=urllib.quote_plus(enddate)

    for group in ['MetData','Profile']:
        keys = groupkeys[group]

        # get sensor objects for each sensor
        if debug: print "Getting sensor information..."
        sensors=populate.get_sensors(keys)

        # get data list
        if debug: print "Reading data %s...\n" % group,
        url='http://aos.nortek.no/Station/ExcelFileExport/%s?from=%s&to=%s&what=%s' % (stationID,start,end,group)
        d = get_data(url)
        data = parse_data(d)

        # get the latest date already in the database
        previous_load_date = None
        if args.current:
            previous_load_date = populate.database_latest_date(keys)

        # load sensor data
        if debug: print "Loading data %s ...\n" % group,
        for entry in data:
            timestamp = parse_dt(entry[1])
            if args.current:
                if previous_load_date and timestamp <= previous_load_date:
                    continue
            for key in keys:
                value = entry[ key[1] ]
                if not value:    # skip empty cells
                    continue
                numeric = sensors[key[0]].data_is_number
                if numeric:
                    value = float(value)
                    populate.load_data(sensor_id=sensors[key[0]], time_stamp=timestamp, num_value=value, value_is_number=True)
                else:
                    populate.load_data(sensor_id=sensors[key[0]], time_stamp=timestamp, string_value=value)


    if debug: print "Finishing Nortek population script..."
