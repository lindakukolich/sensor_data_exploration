#! /bin/bash

# shell script to run all the setup scripts

./wunderground_TI_setup.py
./beacon_buoy_setup.py
./salt_pond_setup.py
./nortek_setup.py

time ./wunderground_TI_addData.py --current
# 1/1/14 - 1/22/14
time ./wunderground_TI_addData.py --history --date 20140101 20140102 20140103 20140104 20140105 20140106 20140107 20140108 20140109 20140110 20140111 20140112 20140113 20140114 20140115 20140116 20140117 20140118 20140119 20140120 20140121 20140122  20140123 
# 1/15/14 - 1/23/14
time ./salt_pond_addData.py --current
# ok to overshoot
time ./nortek_addData.py --history --startdate 2014-01-01 --enddate 2014-01-31
# 2013-08-22 - 2014-01-04
time ./beacon_buoy_addData.py --history
