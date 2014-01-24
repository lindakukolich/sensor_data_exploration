#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 15.January.2014 Liz Brooks
# script to populate the database with DataSource and Sensor information 
# from the Salt Pond hydrologic sensor.

import populate
debug = True


if __name__ == '__main__':
    if debug: print "Starting Salt Pond setup script..."

    # create Salt Pond data source ------------------------------
    if debug: print "Creating Datasource..."
    mysource = populate.add_datasource( datasource_id = "Thompson Island Salt Pond",
                               desc="Thompson Island Salt Pond hydrologic sensor",
                               owner = "cesn - Coastal Environmental Sensing Networks",
                               access_info="https://datagarrison.com/ thompson,thompson",
                                symbol="SP"
                           )

    # create Sensors from this datasource ---------------------------------
    if debug: print "Creating Sensors..."
    s1 = populate.add_sensor( sensor_id = "sp_air_pressure",
                     source = mysource,
                     short_name="Air Pressure",
                     data_type = "float",
                     is_number = True,
                     units_long = "decibars",
                     units_short = "dbar",
                     kind = "meteorological",
                     line_color = populate.hex_color('gray'),
                 )
    s2 = populate.add_sensor( sensor_id = "sp_water_temp",
                     source = mysource,
                     short_name="Water Temperature",
                     data_type = "float",
                     is_number = True,
                     units_long = "degrees Celsius",
                     units_short = "°C",
                     kind = "hydrological",
                     line_color = populate.hex_color('purple'),
                 )
    s3 = populate.add_sensor( sensor_id = "sp_salinity",
                     source = mysource,
                     short_name="Salinity",
                     data_type = "float",
                     is_number = True,
                     units_long = "ppt",
                     units_short = "ppt",
                     is_headliner = False,
                     kind = "hydrological",
                     line_color = populate.hex_color('orange'),
                 )
    s4 = populate.add_sensor( sensor_id = "sp_water_pressure",
                     source = mysource,
                     short_name="Water Pressure",
                     data_type = "float",
                     is_number = True,
                     units_long = "decibars",
                     units_short = "dbar",
                     kind = "hydrological",
                     line_color = populate.hex_color('lilac'),
                 )
    s5 = populate.add_sensor( sensor_id = "sp_chlorophyll",
                     source = mysource,
                     short_name="Chlorophyll",
                     data_type = "float",
                     is_number = True,
                     units_long = "ug/L",
                     units_short = "ug/L",
                     is_headliner = False,
                     kind = "hydrological",
                     line_color = populate.hex_color('dark_green'),
                 )
    s6 = populate.add_sensor( sensor_id = "sp_disolved_oxygen",
                     source = mysource,
                     short_name=" Disolved Oxygen",
                     data_type = "float",
                     is_number = True,
                     units_long = "percent",
                     units_short = "%",
                     kind = "hydrological",
                     line_color = populate.hex_color('cyan'),
                 )
    s7 = populate.add_sensor( sensor_id = "sp_rel_pressure",
                     source = mysource,
                     short_name="Relative Pressure",
                     data_type = "float",
                     is_number = True,
                     units_long = "decibars",
                     units_short = "dbar",
                     kind = "meteorological",
                     line_color = populate.hex_color('brown'),
                 )

    if debug: print "Finished Salt Pond setup script!"
