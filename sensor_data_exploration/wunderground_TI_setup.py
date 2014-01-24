#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 12.January.2014 Liz Brooks
# script to populate the database with Datasource and Sensor information 
# from Weather Underground Thompson Island.

import populate
debug = True


if __name__ == '__main__':
    if debug: print "Starting Weather Underground setup script..."

    # create Weather Underground data source ------------------------------
    if debug: print "Creating Datasource..."
    mysource = populate.add_datasource( datasource_id = "Weather Underground Thompson Island",
                               owner = "Weather Underground",
                               latitude=42.317165,
                               longitude=-71.007622,
                               elevation=100.0,
                               access_info="stationID='KMABOSTO32' APIkey='2cbf77167bf2fe35'",
                           )

    # create Sensors from this datasource ---------------------------------
    if debug: print "Creating Sensors..."
    s1 = populate.add_sensor( sensor_id = "wu_ti_temp_c",
                     source = mysource,
                     short_name="Air Temperature",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees Celsius",
                     units_short = "°C",
                     is_headliner = True,
                     kind = "meteorological",
                     line_color = populate.hex_color('red'),
                 )
    s2 = populate.add_sensor( sensor_id = "wu_ti_relative_humidity",
                     source = mysource,
                     short_name="Relative Humidity",
                     data_type = "float",
                     is_number = True,
                     units_long = "percent",
                     units_short = "%",
                     kind = "meteorological",
                     line_color = populate.hex_color('light_green'),
                 )
    s3 = populate.add_sensor( sensor_id = "wu_ti_wind_dir",
                     source = mysource,
                     short_name="Wind Direction",
                     data_type = "string",
                     kind = "meteorological",
                     line_color = populate.hex_color('black'),
                 )
    s4 = populate.add_sensor( sensor_id = "wu_ti_wind_degrees",
                     source = mysource,
                     short_name="",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees",
                     units_short = "°",
                     kind = "meteorological",
                     line_color = populate.hex_color('black'),
                 )
    s5 = populate.add_sensor( sensor_id = "wu_ti_wind_kph",
                     source = mysource,
                     short_name="Wind Speed",
                     data_type = "float",
                     is_number = True,
                     units_long = "kilometers per hour",
                     units_short = "kph",
                     kind = "meteorological",
                     line_color = populate.hex_color('dark_blue'),
                 )
    s6 = populate.add_sensor( sensor_id = "wu_ti_wind_gust_kph",
                     source = mysource,
                     short_name="Gust Speed",
                     data_type = "float",
                     is_number = True,
                     units_long = "kilometers per hour",
                     units_short = "kph",
                     kind = "meteorological",
                     line_color = populate.hex_color('blue'),
                 )
    s7 = populate.add_sensor( sensor_id = "wu_ti_pressure_mb",
                     source = mysource,
                     short_name="Air Pressure",
                     data_type = "float",
                     is_number = True,
                     units_long = "millibars",
                     units_short = "mb",
                     kind = "meteorological",
                     line_color = populate.hex_color('gray'),
                 )
    s8 = populate.add_sensor( sensor_id = "wu_ti_dewpoint_c",
                     source = mysource,
                     short_name="Dew Point",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees Celsius",
                     units_short = "°C",
                     kind = "meteorological",
                     line_color = populate.hex_color('green'),
                 )
    s9 = populate.add_sensor( sensor_id = "wu_ti_precip_1hr_metric",
                     source = mysource,
                     short_name="Precipitation Rate",
                     data_type = "float",
                     is_number = True,
                     units_long = "millimeters",
                     units_short = 'mm',
                     kind = "meteorological",
                     line_color = populate.hex_color('cyan'),
                 )
    s10 = populate.add_sensor( sensor_id = "wu_ti_precip_today_metric",
                     source = mysource,
                     short_name="Precipitation Total",
                     data_type = "float",
                     is_number = True,
                     units_long = "millimeters",
                     units_short = 'mm',
                     kind = "meteorological",
                     line_color = populate.hex_color('cyan'),
                 )

    if debug: print "Finished Weather Underground setup script!"

##### English units ##################################
#
#    s1 = populate.add_sensor( sensor_id = "wu_ti_temp_f",
#                     source = mysource,
#                     short_name="Air Temperature",
#                     data_type = "float",
#                     is_number = True,
#                     units_long = "degrees farenheit",
#                     units_short = "°F",
#                     is_headliner = True,
#                     kind = "meteorological",
#                     line_color = populate.hex_color('red'),
#                 )
#    s5 = populate.add_sensor( sensor_id = "wu_ti_wind_mph",
#                     source = mysource,
#                     short_name="Wind Speed",
#                     data_type = "float",
#                     is_number = True,
#                     units_long = "miles per hour",
#                     units_short = "mph",
#                     kind = "meteorological",
#                     line_color = populate.hex_color('dark_blue'),
#                 )
#    s6 = populate.add_sensor( sensor_id = "wu_ti_wind_gust_mph",
#                     source = mysource,
#                     short_name="Gust Speed",
#                     data_type = "float",
#                     is_number = True,
#                     units_long = "miles per hour",
#                     units_short = "mph",
#                     kind = "meteorological",
#                     line_color = populate.hex_color('blue'),
#                 )
#    s7 = populate.add_sensor( sensor_id = "wu_ti_pressure_in",
#                     source = mysource,
#                     short_name="Air Pressure",
#                     data_type = "float",
#                     is_number = True,
#                     units_long = "inches mercury",
#                     units_short = "inHg",
#                     kind = "meteorological",
#                     line_color = populate.hex_color('gray'),
#                 )
#    s8 = populate.add_sensor( sensor_id = "wu_ti_dewpoint_f",
#                     source = mysource,
#                     short_name="Dew Point",
#                     data_type = "float",
#                     is_number = True,
#                     units_long = "degrees Farenheit",
#                     units_short = "°F",
#                     kind = "meteorological",
#                     line_color = populate.hex_color('green'),
#                 )
#    s9 = populate.add_sensor( sensor_id = "wu_ti_precip_1hr_in",
#                     source = mysource,
#                     short_name="Precipitation Rate",
#                     data_type = "float",
#                     is_number = True,
#                     units_long = "inches",
#                     units_short = '"',
#                     kind = "meteorological",
#                     line_color = populate.hex_color('cyan'),
#                 )
#    s10 = populate.add_sensor( sensor_id = "wu_ti_precip_today_in",
#                     source = mysource,
#                     short_name="Precipitation Total",
#                     data_type = "float",
#                     is_number = True,
#                     units_long = "inches",
#                     units_short = '"',
#                     kind = "meteorological",
#                     line_color = populate.hex_color('cyan'),
#                 )
###############
