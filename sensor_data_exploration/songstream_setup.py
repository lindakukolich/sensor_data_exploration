#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 26.January.2014 Liz Brooks
# script to populate the database with DataSource and Sensor information 
# from Cameras.

import populate
debug = True


if __name__ == '__main__':
    if debug: print "Starting Song Stream setup script..."

    # create Salt Pond data source ------------------------------
    if debug: print "Creating Datasource..."
    mysource = populate.add_datasource( datasource_id = "Song Stream Audio",
                               desc="Wildlife Accoustics Song Stream Remote Access Audio Recording Station",
                               owner = "Wildlife Accoustics",
                               access_info="https://songstream.wildlifeacoustics.com/ account=THOMPSON_ISLAND user=STUDENT password=SS_PASSWORD",
                               symbol="SS"
                           )

    # create Sensors from this datasource ---------------------------------
    if debug: print "Creating Sensors..."
    s1 = populate.add_sensor( sensor_id = "ss_wav",
                     source = mysource,
                     short_name="Bird Song",
                     data_type = "wav",
                     is_headliner = True,
                 )
    if debug: print "Finished Song Stream setup script!"
