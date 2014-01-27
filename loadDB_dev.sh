#! /bin/bash

# shell script to re-populate the database with 1-2 months data
# ** Need to set HEROKU_MODE by comment/uncomment'ing **
# ** the appropriate line below **
# Usage: ./loadDB_dev.sh 2>&1 | tee -a log
# or Usage: ./loadDB_dev.sh &> log

# set this! ------------------------------------------------------------
HEROKU_MODE=''           # use to run locally, or from within heroku bash
#HEROKU_MODE='heroku run' # use to run on remote server from local terminal

echo === Starting loadDB at: `date`
# create the Data Sources and Sensors ----------------------------------
$HEROKU_MODE sensor_data_exploration/wunderground_TI_setup.py
$HEROKU_MODE sensor_data_exploration/nortek_setup.py
$HEROKU_MODE sensor_data_exploration/salt_pond_setup.py
$HEROKU_MODE sensor_data_exploration/beacon_buoy_setup.py

# load Sensor Data -----------------------------------------------------
wu_history() 
{
    echo ---Starting WU load at: `date`
    $HEROKU_MODE sensor_data_exploration/wunderground_TI_addData.py --history --start $START --end $END
    echo ---Finished WU load at: `date`
}

nor_history() 
{
    echo ---Starting NOR load at: `date`
    $HEROKU_MODE sensor_data_exploration/nortek_addData.py --history --start $START --end $END
    echo ---Finished NOR load at: `date`
}

MONTH=December
START=2013-12-01
END=2013-12-31
echo === $MONTH ==========
wu_history
nor_history
sleep 30

MONTH=January
START=2014-01-01
END=2014-01-31
echo === $MONTH ==========
wu_history
nor_history
sleep 30

# SP available from 2013-09-27 through now (with some gaps)
echo ---Starting SP load at: `date`
$HEROKU_MODE sensor_data_exploration/salt_pond_addData.py --history
echo ---Finished SP load at: `date`

# BB available from 2013-08-22 through 2014-01-04
echo ---Starting BB load at: `date`
$HEROKU_MODE sensor_data_exploration/beacon_buoy_addData.py --history --cesn
echo ---Finished BB load at: `date`

echo === Finished loadDB at: `date`

# return status is always true with heroku run :(
#if [ $? -ne 0 ]; then
#    echo "wunderground $MONTH did not complete."
#fi
