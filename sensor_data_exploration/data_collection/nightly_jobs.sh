#!/bin/sh
DATE=`date +%Y-%m-%d --date=yesterday`
/var/www/vhtdocs/userweb51163/website/sensor_data_exploration_full/sensor_data_exploration/data_collection/wunderground_TI_addData.py --history --start $DATE --end $DATE  
/var/www/vhtdocs/userweb51163/website/sensor_data_exploration_full/sensor_data_exploration/data_collection/nortek_addData.py --history --start $DATE --end $DATE  
# Songstream has not been added to the data base yet
#/var/www/vhtdocs/userweb51163/website/sensor_data_exploration_full/sensor_data_exploration/data_collection/songstream_addData.py --history --start $DATE --end $DATE  
