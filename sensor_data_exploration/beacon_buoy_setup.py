#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 15.January.2014 Liz Brooks
# script to populate the database with DataSource and Sensor information 
# from Beacon Buoys.

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

    # create Buoy 5 data source ------------------------------
    if debug: print "Creating Datasource..."
    mysource = add_datasource( datasource_id = "Beacon Buoy 5 Thompson Island",
                               desc="Beacon Buoy - Boston Harbor, Thompson Island Mooring Field - Dorchester Bay",
                               owner = "cesn - Coastal Environmental Sensing Networks",
                               latitude=42.3196,
                               longitude=-71.0219,
                               access_info="deviceID='2232583' station_type='cdombuoy'",
                           )

    # create Sensors from this datasource ---------------------------------
    if debug: print "Creating sensors..."
    s1 = add_sensor( sensor_id = "bouy5_Salinity",
                     source = mysource,
                     short_name="Salinity",
                     data_type = "float",
                     is_number = True,
                     units_long = "PSU, practical salinity units",
                     units_short = "PSU",
                     kind = "salinity",
                 )
    s2 = add_sensor( sensor_id = "buoy5_CDOM",
                     source = mysource,
                     short_name="CDOM",
                     data_type = "float",
                     is_number = True,
                     units_long = "QSU",
                     units_short = "QSU",
                 )
    s3 = add_sensor( sensor_id = "bouy5_WaterTemp",
                     source = mysource,
                     short_name="Water Temperature F",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees farenheit",
                     units_short = "°F",
                     kind = "water temperature",
                 )
    s4 = add_sensor( sensor_id = "bouy5_AirTemp",
                     source = mysource,
                     short_name="Air Temperature F",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees farenheit",
                     units_short = "°F",
                     kind = "air temperature",
                 )
    s5 = add_sensor( sensor_id = "buoy5_WindSpeed",
                     source = mysource,
                     short_name="Wind Speed",
                     data_type = "float",
                     is_number = True,
                     units_long = "miles per hour",
                     units_short = "mph",
                 )
    s6 = add_sensor( sensor_id = "buoy5_GustSpeed",
                     source = mysource,
                     short_name="Gust Speed",
                     data_type = "float",
                     is_number = True,
                     units_long = "miles per hour",
                     units_short = "mph",
                 )
    s7 = add_sensor( sensor_id = "buoy5_WindDir",
                     source = mysource,
                     short_name="Wind Direction",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees",  
                     units_short = "°",
                 )
    s8 = add_sensor( sensor_id = "buoy5_BuoyDir",
                     source = mysource,
                     short_name="Buoy Direction",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees",
                     units_short = "°",
                 )
    s9 = add_sensor( sensor_id = "buoy5_Pressure",
                     source = mysource,
                     short_name="Pressure",
                     data_type = "float",
                     is_number = True,
                     units_long = "inches mercury",
                     units_short = "inHg",
                 )
    s10 = add_sensor( sensor_id = "buoy5_RelHumidity",
                      source = mysource,
                      short_name="Relative Humidity",
                      data_type = "float",
                      is_number = True,
                      units_long = "percent",
                      units_short = "%",
                  )
    s11 = add_sensor( sensor_id = "buoy5_DewPt",
                      source = mysource,
                      short_name="Dew Point",
                      data_type = "float",
                      is_number = True,
                      units_long = "degrees farenheit",
                      units_short = "°F",
                  )
    s12 = add_sensor( sensor_id = "buoy5_PAR",
                      source = mysource,
                      short_name="PAR",
                      desc="PAR - Photosynthetically active radiation",
                      data_type = "float",
                      is_number = True,
                      units_long = "uE - microeinsteins per second per square meter",
                      units_short = "uE",
                  )

    if debug: print "Finished Weather Underground population script!"
