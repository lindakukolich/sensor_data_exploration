#! /usr/bin/env python

# 21.January.2014 Liz Brooks
# collection of functions used to populate the database

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensor_data_exploration.settings')
from sensor_data_exploration.apps.explorer.models import *

colors = { 'black':'#000000',
           'blue':'#0000CC',
           'red':'#CC0000',
           'green':'#00CC00',
}

def add_datasource(datasource_id,owner,desc="",access_info="",latitude=None,
                   longitude=None,elevation=None,symbol=None):
    source,created = DataSource.objects.get_or_create(datasource_id=datasource_id,
                                                      datasource_desc=desc,
                                                      access_info=access_info,
                                                      owner=owner,
                                                      latitude=latitude, 
                                                      longitude=longitude, 
                                                      elevation=elevation,
                                                      symbol=symbol,)
    return source

def add_sensor(sensor_id, source, short_name, data_type, desc="",units_long="",
               units_short="",kind=None,is_number=False,is_prediction=False,
               update_granularity_sec=60,data_min=None,data_max=None,
               is_headliner=False,line_color=colors["blue"]):
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
                                                  data_max=data_max,
                                                  is_headliner=is_headliner,
                                                  line_color=line_color,)
    return sensor

def hex_color(name):
    if name in colors:
        return colors[name]
    else:
        return None

def get_sensors(keys):
    '''return a dictionary containing the sensor object for each sensor name in the keys list'''
    sensors={}
    for key in keys:
        sid=key[0]
        try:
            sobj = Sensor.objects.get(sensor_id=sid)
        except Sensor.DoesNotExist:
            sys.exit("%s is not a sensor in the database." % sid)
        sensors[sid] = sobj
    return sensors

def load_data(sensor_id,time_stamp,num_value=None,string_value=None,value_is_number=False):
    '''creates a sensorData entry (unless already exists)'''
    result=SensorData.objects.get_or_create(sensor_id=sensor_id,
                                            time_stamp=time_stamp,
                                            num_value=num_value,
                                            string_value=string_value,
                                            value_is_number=value_is_number)
    return result
