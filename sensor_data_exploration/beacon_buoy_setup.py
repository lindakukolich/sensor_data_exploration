#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 15.January.2014 Liz Brooks
# script to populate the database with DataSource and Sensor information 
# from Beacon Buoys.

import populate
debug = True


if __name__ == '__main__':
    if debug: print "Starting Beacon Buoy setup script..."

    # create Buoy 5 data source ------------------------------
    if debug: print "Creating Datasource..."
    mysource = populate.add_datasource(
        datasource_id = "Beacon Buoy 5 Thompson Island",
        desc="Beacon Buoy - Boston Harbor, Thompson Island Mooring Field - Dorchester Bay",
        owner = "cesn - Coastal Environmental Sensing Networks",
        latitude=42.3196,
        longitude=-71.0219,
        access_info="deviceID='2232583' station_type='cdombuoy'",
    )

    # create Sensors from this datasource ---------------------------------
    if debug: print "Creating Sensors..."
    s1 = populate.add_sensor( sensor_id = "buoy5_Salinity",
                     source = mysource,
                     short_name="Salinity",
                     data_type = "float",
                     is_number = True,
                     units_long = "practical salinity units",
                     units_short = "PSU",
                     is_headliner = False,
                     kind = "hydrological",
                     line_color = populate.hex_color('orange'),
                 )
    s2 = populate.add_sensor( sensor_id = "buoy5_CDOM",
                     source = mysource,
                     short_name="CDOM",
                     data_type = "float",
                     is_number = True,
                     units_long = "QSU",
                     units_short = "QSU",
                     kind = "hydrological",
                     line_color = populate.hex_color('brown'),
                 )
    s3 = populate.add_sensor( sensor_id = "buoy5_WaterTemp",
                     source = mysource,
                     short_name="Water Temperature",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees farenheit",
                     units_short = "°F",
                     is_headliner = False,
                     kind = "hydrological",
                     line_color = populate.hex_color('purple'),
                 )
    s4 = populate.add_sensor( sensor_id = "buoy5_AirTemp",
                     source = mysource,
                     short_name="Air Temperature",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees farenheit",
                     units_short = "°F",
                     kind = "meteorological",
                     line_color = populate.hex_color('red'),
                 )
    s5 = populate.add_sensor( sensor_id = "buoy5_WindSpeed",
                     source = mysource,
                     short_name="Wind Speed",
                     data_type = "float",
                     is_number = True,
                     units_long = "miles per hour",
                     units_short = "mph",
                     kind = "meteorological",
                     line_color = populate.hex_color('dark_blue'),
                 )
    s6 = populate.add_sensor( sensor_id = "buoy5_GustSpeed",
                     source = mysource,
                     short_name="Gust Speed",
                     data_type = "float",
                     is_number = True,
                     units_long = "miles per hour",
                     units_short = "mph",
                     kind = "meteorological",
                     line_color = populate.hex_color('blue'),
                 )
    s7 = populate.add_sensor( sensor_id = "buoy5_WindDir",
                     source = mysource,
                     short_name="Wind Direction",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees",  
                     units_short = "°",
                     line_color = populate.hex_color('black'),
                 )
    s8 = populate.add_sensor( sensor_id = "buoy5_BuoyDir",
                     source = mysource,
                     short_name="Buoy Direction",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees",
                     units_short = "°",
                     line_color = populate.hex_color('black'),
                 )
    s9 = populate.add_sensor( sensor_id = "buoy5_Pressure",
                     source = mysource,
                     short_name="Air Pressure",
                     data_type = "float",
                     is_number = True,
                     units_long = "inches mercury",
                     units_short = "inHg",
                     kind = "meteorological",
                     line_color = populate.hex_color('gray'),
                 )
    s10 = populate.add_sensor( sensor_id = "buoy5_RelHumidity",
                     source = mysource,
                     short_name="Relative Humidity",
                     data_type = "float",
                     is_number = True,
                     units_long = "percent",
                     units_short = "%",
                     kind = "meteorological",
                     line_color = populate.hex_color('light_green'),
                  )
    s11 = populate.add_sensor( sensor_id = "buoy5_DewPt",
                     source = mysource,
                     short_name="Dew Point",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees farenheit",
                     units_short = "°F",
                     kind = "meteorological",
                     line_color = populate.hex_color('green'),
                  )
    s12 = populate.add_sensor( sensor_id = "buoy5_PAR",
                     source = mysource,
                     short_name="PAR",
                     desc="PAR - Photosynthetically active radiation",
                     data_type = "float",
                     is_number = True,
                     units_long = "microeinsteins per second per square meter",
                     units_short = "uE",
                     kind = "hydrological",
                     line_color = populate.hex_color('yellow'),
                  )

    if debug: print "Finished Beacon Buoy setup script!"
