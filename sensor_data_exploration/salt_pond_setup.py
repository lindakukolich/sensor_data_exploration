#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 15.January.2014 Liz Brooks
# script to populate the database with DataSource and Sensor information 
# from the Salt Pond hydrologic sensor.

import os
debug = True

def add_datasource(datasource_id,owner,desc="",access_info="",latitude=None,
                   longitude=None,elevation=None):
    source,created = DataSource.objects.get_or_create(datasource_id=datasource_id,
                                                      datasource_desc=desc,
                                                      access_info=access_info,
                                                      owner=owner,
                                                      latitude=latitude, 
                                                      longitude=longitude, 
                                                      elevation=elevation)
    return source

def add_sensor(sensor_id, source, short_name, data_type, desc="",units_long="",
               units_short="",kind=None,is_number=False,is_prediction=False,
               update_granularity_sec=60,data_min=None,data_max=None):
    sensor,created = Sensor.objects.get_or_create(sensor_id=sensor_id,
                                                  sensor_short_name=short_name,
                                                  sensor_desc=desc,
                                                  units_long=units_long,
                                                  units_short=units_short,
                                                  kind=kind,
                                                  data_type=data_type,
                                                  data_is_number=is_number,
                                                  data_is_prediction=is_prediction,
                                                  data_source=source,
                                                  update_granularity_sec=update_granularity_sec,
                                                  data_min=data_min,
                                                  data_max=data_max,)
    return sensor


if __name__ == '__main__':
    # environment setup ---------------------------------------------------
    if debug: print "Starting setup script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensor_data_exploration.settings')
    from sensor_data_exploration.apps.explorer.models import *

    # create Salt Pond data source ------------------------------
    if debug: print "Creating Datasource..."
    mysource = add_datasource( datasource_id = "Thompson Island Salt Pond",
                               desc="Thompson Island Salt Pond hydrologic sensor",
                               owner = "cesn - Coastal Environmental Sensing Networks",
                               access_info="https://datagarrison.com/ thompson,thompson",
                           )

    # create Sensors from this datasource ---------------------------------
    if debug: print "Creating Sensors..."
    s1 = add_sensor( sensor_id = "sp_air_pressure",
                     source = mysource,
                     short_name="Air Pressure",
                     data_type = "float",
                     is_number = True,
                     units_long = "decibars",
                     units_short = "dbar",
                 )
    s2 = add_sensor( sensor_id = "sp_water_temp",
                     source = mysource,
                     short_name="Water Temperature C",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees Celsius",
                     units_short = "°C",
                     kind = "water temperature",
                 )
    s3 = add_sensor( sensor_id = "sp_salinity",
                     source = mysource,
                     short_name="Salinity",
                     data_type = "float",
                     is_number = True,
                     units_long = "ppt",
                     units_short = "ppt",
                     kind = "salinity",
                 )
    s4 = add_sensor( sensor_id = "sp_water_pressure",
                     source = mysource,
                     short_name="Water Pressure",
                     data_type = "float",
                     is_number = True,
                     units_long = "decibars",
                     units_short = "dbar",
                 )
    s5 = add_sensor( sensor_id = "sp_chlorophyll",
                     source = mysource,
                     short_name="Chlorophyll",
                     data_type = "float",
                     is_number = True,
                     units_long = "ug/L",
                     units_short = "ug/L",
                 )
    s6 = add_sensor( sensor_id = "sp_disolved_oxygen",
                     source = mysource,
                     short_name=" Disolved Oxygen",
                     data_type = "float",
                     is_number = True,
                     units_long = "percent",
                     units_short = "%",
                 )
    s7 = add_sensor( sensor_id = "sp_rel_pressure",
                     source = mysource,
                     short_name="Relative Pressure",
                     data_type = "float",
                     is_number = True,
                     units_long = "decibars",
                     units_short = "dbar",
                 )

    if debug: print "Finished setup script!"
