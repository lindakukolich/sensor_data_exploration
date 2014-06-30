#! /bin/bash

# shell script to re-populate the database with all data
# ** Need to set HEROKU_MODE by comment/uncomment'ing **
# ** the appropriate line below **
# Usage: ./loadDB_all.sh 2>&1 | tee -a log
# or Usage: ./loadDB_all.sh &> log

# set this! ------------------------------------------------------------
HEROKU_MODE=''           # use to run locally, or from within heroku bash
#HEROKU_MODE='heroku run' # use to run on remote server from local terminal

echo === Starting loadDB at: `date`
# create the Data Sources and Sensors ----------------------------------
$HEROKU_MODE sensor_data_exploration/data_collection/wunderground_TI_setup.py
$HEROKU_MODE sensor_data_exploration/data_collection/nortek_setup.py
$HEROKU_MODE sensor_data_exploration/data_collection/salt_pond_setup.py
$HEROKU_MODE sensor_data_exploration/data_collection/beacon_buoy_setup.py

# load Sensor Data -----------------------------------------------------
wu_history() 
{
    echo ---Starting WU load at: `date`
    $HEROKU_MODE sensor_data_exploration/data_collection/wunderground_TI_addData.py --history --start $START --end $END
    echo ---Finished WU load at: `date`
}

nor_history() 
{
    echo ---Starting NOR load at: `date`
    $HEROKU_MODE sensor_data_exploration/data_collection/nortek_addData.py --history --start $START --end $END
    echo ---Finished NOR load at: `date`
}

# SP available from 2013-09-27 through now (with some gaps)
echo ---Starting SP load at: `date`
$HEROKU_MODE sensor_data_exploration/data_collection/salt_pond_addData.py --history
echo ---Finished SP load at: `date`

# BB available from 2013-08-22 through 2014-01-04
echo ---Starting BB load at: `date`
$HEROKU_MODE sensor_data_exploration/data_collection/beacon_buoy_addData.py --history --cesn
echo ---Finished BB load at: `date`

MONTH=January
START=2013-01-01
END=2013-01-31
echo === $MONTH ==========
wu_history
nor_history
sleep 30

MONTH=February
START=2013-02-01
END=2013-02-29
echo === $MONTH ==========
wu_history
nor_history
sleep 30

MONTH=March
START=2013-03-01
END=2013-03-31
echo === $MONTH ==========
wu_history
nor_history
sleep 30

MONTH=April
START=2013-04-01
END=2013-04-30
echo === $MONTH ==========
wu_history
nor_history
sleep 30

MONTH=May
START=2013-05-01
END=2013-05-31
echo === $MONTH ==========
wu_history
nor_history
sleep 30

MONTH=June
START=2013-06-01
END=2013-06-30
echo === $MONTH ==========
wu_history
nor_history
sleep 30

MONTH=July
START=2013-07-01
END=2013-07-31
echo === $MONTH ==========
wu_history
nor_history
sleep 30

MONTH=August
START=2013-08-01
END=2013-08-31
echo === $MONTH ==========
wu_history
nor_history
sleep 30

MONTH=September
START=2013-09-01
END=2013-09-30
echo === $MONTH ==========
wu_history
nor_history
sleep 30

MONTH=October
START=2013-10-01
END=2013-10-31
echo === $MONTH ==========
wu_history
nor_history
sleep 30

MONTH=November
START=2013-11-01
END=2013-11-30
echo === $MONTH ==========
wu_history
nor_history
sleep 30

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

echo === Finished loadDB at: `date`

# return status is always true with heroku run :(
#if [ $? -ne 0 ]; then
#    echo "wunderground $MONTH did not complete."
#fi
