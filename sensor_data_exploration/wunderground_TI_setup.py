#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 12.January.2014 Liz Brooks
# script to populate the database with Datasource and Sensor information 
# from Weather Underground Thompson Island.

import populate
debug = True


if __name__ == '__main__':
    if debug: print "Starting Weather Underground population script..."

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
    if debug: print "Creating sensors..."
    s1 = populate.add_sensor( sensor_id = "wu_ti_temp_f",
                     source = mysource,
                     short_name="Air Temperature",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees farenheit",
                     units_short = "°F",
                     is_headliner = True,
                     kind = "meteorological",
                     line_color = populate.hex_color('blue'),
                 )
    s2 = populate.add_sensor( sensor_id = "wu_ti_wind_mph",
                     source = mysource,
                     short_name="Wind Speed",
                     data_type = "float",
                     is_number = True,
                     units_long = "miles per hour",
                     units_short = "mph",
                     kind = "meteorological",
                     line_color = populate.hex_color('green'),
                 )
    s3 = populate.add_sensor( sensor_id = "wu_ti_wind_dir",
                     source = mysource,
                     short_name="Wind Direction",
                     data_type = "string",
                     kind = "meteorological",
                     line_color = populate.hex_color('black'),
                 )
    s4 = populate.add_sensor( sensor_id = "wu_ti_precip_1hr_in",
                     source = mysource,
                     short_name="Precipitation 1hr",
                     data_type = "float",
                     is_number = True,
                     units_long = "inches",
                     units_short = '"',
                     kind = "meteorological",
                     line_color = populate.hex_color('green'),
                 )
    s5 = populate.add_sensor( sensor_id = "wu_ti_sunrise",
                     source = mysource,
                     short_name="Sunrise",
                     data_type = "string",
                     units_long = "h:mm",
                     units_short = "",
                     desc = "Predicted time for sunrise on this date.",
                     is_prediction = True,
                     line_color = populate.hex_color('red'),
                 )

    if debug: print "Finished Weather Underground population script!"
