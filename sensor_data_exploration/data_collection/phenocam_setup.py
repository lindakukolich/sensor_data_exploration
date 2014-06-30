#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 28.January.2014 Liz Brooks
# script to populate the database with Datasource and Sensor information 
# from the NPS plant phenology camera.

import populate
debug = True


if __name__ == '__main__':
    if debug: print "Starting Phenocam setup script..."

    # create Weather Underground data source ------------------------------
    if debug: print "Creating Datasource..."
    mysource = populate.add_datasource( datasource_id = "Plant Phenology Camera",
                                        owner = "NPS - National Parks Service",
                                        access_info="manual",
                                        symbol="PP"
                                    )

    # create Sensors from this datasource ---------------------------------
    if debug: print "Creating Sensors..."
    s1 = populate.add_sensor( sensor_id = "pp_camera",
                     source = mysource,
                     short_name="Plant Phenology",
                     data_type = "jpg",
                     is_headliner = False,
                     kind = "hide",
                 )

    if debug: print "Finished Phenocam setup script."
