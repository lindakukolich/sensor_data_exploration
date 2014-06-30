#!/bin/sh
date >> newlog.txt
/var/www/vhtdocs/userweb51163/website/sensor_data_exploration_full/sensor_data_exploration/data_collection/wunderground_TI_addData.py --current >> newlog.txt 
/var/www/vhtdocs/userweb51163/website/sensor_data_exploration_full/sensor_data_exploration/data_collection/nortek_addData.py --current  >> newlog.txt
