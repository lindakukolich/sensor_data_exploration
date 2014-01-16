#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 12.January.2014 Liz Brooks
# script to populate the database with Datasource and Sensor information 
# from Weather Underground Thompson Island.

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
    if debug: print "Starting Weather Underground population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensor_data_exploration.settings')
    from sensor_data_exploration.apps.explorer.models import *

    # create Weather Underground data source ------------------------------
    if debug: print "Creating Datasource..."
    mysource = add_datasource( datasource_id = "Weather Underground Thompson Island",
                               owner = "Weather Underground",
                               latitude=42.317165,
                               longitude=-71.007622,
                               elevation=100.0,
                               access_info="stationID='KMABOSTO32' APIkey='2cbf77167bf2fe35'",
                           )

    # create Sensors from this datasource ---------------------------------
    if debug: print "Creating sensors..."
    s1 = add_sensor( sensor_id = "wu_ti_temp_f",
                     source = mysource,
                     short_name="Temperature F",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees farenheit",
                     units_short = "°F",
                     kind = "air temperature",
                 )
    s2 = add_sensor( sensor_id = "wu_ti_wind_mph",
                     source = mysource,
                     short_name="Wind Speed",
                     data_type = "float",
                     is_number = True,
                     units_long = "miles per hour",
                     units_short = "mph",
                     kind = "wind speed",
                 )
    s3 = add_sensor( sensor_id = "wu_ti_wind_dir",
                     source = mysource,
                     short_name="Wind Direction",
                     data_type = "string",
                 )
    s4 = add_sensor( sensor_id = "wu_ti_precip_1hr_in",
                     source = mysource,
                     short_name="Precipitation 1hr",
                     data_type = "float",
                     is_number = True,
                     units_long = "inches",
                     units_short = '"',
                 )
    s5 = add_sensor( sensor_id = "wu_ti_sunrise",
                     source = mysource,
                     short_name="Sunrise",
                     data_type = "string",
                     units_long = "h:mm",
                     units_short = "",
                     desc = "Predicted time for sunrise on this date.",
                     is_prediction = True,
                 )

    if debug: print "Finished Weather Underground population script!"
