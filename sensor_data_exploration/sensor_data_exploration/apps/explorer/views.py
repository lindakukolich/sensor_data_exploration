

import json
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from sensor_data_exploration.apps.explorer.models import *
from django.utils import simplejson
import time
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime

import mimetypes

from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key


# Create your views here.

def index(request):
    ''' The main page for the explorer app '''
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    context_dict = {}

    #Get the available sensors to print out buttons for them
    #    context_dict['sensor_list'] = get_sensors()
    
    sensor_list = Sensor.objects.order_by('sensor_short_name')

    datasource_list = DataSource.objects.order_by('datasource_id')

    context_dict = {
        'sensor_list': sensor_list,
        'datasource_list': datasource_list
    }

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('explorer/index.html', context_dict, context)

def about(request):
    ''' About page, mostly to practice having links '''
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('explorer/about.html', context_dict, context)

def map(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('explorer/map.html', context_dict, context)

def get_data_ajax(request):
    '''Read data from the database, preparing to make a plot'''

    print "starting get_data_ajax with plot_sensor_id= "
    plot_sensor_id = request.GET.get('sensorid')
    print plot_sensor_id
    print "start and end times are= "
    plot_starttime = request.GET.get('starttime')
    plot_endtime = request.GET.get('endtime')
    print plot_starttime + ", " + plot_endtime

    # Make sure we have a sensor_id that is in the sensor table
    if Sensor.objects.filter(sensor_id=plot_sensor_id) == False:
        data_to_dump = {'goodPlotData': False,
                        'plotError': "Error retrieving plot data for sensor " + plot_sensor_id + ": No such sensor",
                        'data_array1': dataArray1, 
                        'plot_short_name': plot_sensor_id,
                        'plot_source_id': plot_sensor_id,
                        'plot_units_long': "",
                        'plot_units_short': "",
                        'line_color': "",
                        'sensor_id': data_source_id,
                    }
        print "data_to_dump"
        print data_to_dump
        json_data = json.dumps(data_to_dump, cls=DjangoJSONEncoder)
        print json_data
        return HttpResponse(json_data, mimetype='application/json')

    # We know there is at least one sensor that matches our given id.
    # just take the first one.  That'll teach them to repeat values!
    s = Sensor.objects.filter(
        sensor_id=plot_sensor_id
    )
    plot_sensor = s.values()[0]
    print plot_sensor
    # Pick out Sensor fields to display as part of the plot
    

    
    # Retrieve the actual data for the plot
    q = SensorData.objects.filter(
        sensor_id_id=plot_sensor_id
        ).filter(time_stamp__range=[plot_starttime, plot_endtime]).order_by('time_stamp')

    # Pick out the times of the observations, and convert them to JavaScript
    # timestamps, which are in milliseconds

    xdata = []
    xdata_datetime = q.values_list('time_stamp', flat=True)
    for i in range(0, len(xdata_datetime)):
        xdata.append(time.mktime(xdata_datetime[i].timetuple()) * 1000)
        xdata = list(xdata)

    # Pick out the values for each observation
    status = []
    plotError = ""

    status.append("before if ")
    dataArray1 = []    
    url_list = []
    ydata = []
    if plot_sensor['data_is_number']:
        #Putting in 0 for ones that are not numberical. Will use ajax to get the urls out of the string.
        status.append(" data_is_number true")
        ydata = q.values_list('num_value', flat=True)
        ydata = list(ydata)

    n_points = 0
    n_points = len(xdata)

    # Make sure that we actually got some data, or this plot is no good
    if n_points == 0:
        print "get_data_ajax: Error retrieving plot data for plot " + plot_sensor_id + ": No data"
        goodPlotData = False
        plotError =  "Error retrieving plot data for plot " + plot_sensor_id + ": No data for time range [" + plot_starttime + ", " + plot_endtime + "]"

    else:

        for i in range (0, n_points) :
            if plot_sensor['data_is_number']:
                dataArray1.append( [xdata[i], ydata[i]] );
            else:
                dataArray1.append([xdata[i], 0])

        goodPlotData = True
        
    symbol = DataSource.objects.filter(datasource_id = plot_sensor['data_source_id']).values_list('symbol')
    symbol = symbol[0]

    
    # We need to dump data for both the good and the badPlots.    
    data_to_dump = {'data_array1': dataArray1, 
                    'url_list': url_list,
                    'plot_short_name': plot_sensor['sensor_short_name'],
                        'status': status,
                        'plot_source_id': plot_sensor['data_source_id'],
                        'plot_units_long': plot_sensor['units_long'],
                        'plot_units_short': plot_sensor['units_short'],
                        'dataIsNumber': plot_sensor['data_is_number'],
                        'dataType': plot_sensor['data_type'],
                        'line_color': plot_sensor['line_color'],
                        'goodPlotData': goodPlotData,
                        'plotError': plotError,
                        'sensor_id': plot_sensor['sensor_id'],
                        'dataSourceSymbol':symbol
                    }
    
    #send back the data or error as created above.
#    print "data_to_dump"
#    print data_to_dump
    json_data = json.dumps(data_to_dump, cls=DjangoJSONEncoder)
    return HttpResponse(json_data, mimetype='application/json')

def get_point_ajax(request):
    plot_sensor_id = request.GET.get('sensorid')

    x = request.GET.get('x')
    x = float(x)/1000.0

    pointTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x))   

    q = SensorData.objects.filter(sensor_id_id=plot_sensor_id).filter(time_stamp=pointTime)

    point = q.values()[0]

    s = Sensor.objects.filter(
        sensor_id=plot_sensor_id
    )
    plot_sensor = s.values()[0]

    if point['value_is_number']:
        url = ""
    else:
        url = point['string_value']

    data_to_dump = {
        'value_is_number': point['value_is_number'],
        'url': url,
        'dataType': plot_sensor['data_type']
    }

    print point
    json_data = json.dumps(data_to_dump, cls=DjangoJSONEncoder)
    return HttpResponse(json_data, mimetype='application/json')

def get_sensors():
    '''Make a list of the available sensors'''
    #Eventually put more logic in here about what we actually want to
    #show and maybe make categories of different types of sensors
    sensors = SensorData.objects.values_list('sensor_id', flat=True).distinct()
    sensor = list(sensors)
    return sensors

def tests3(request):
    aws_bucket = settings.AWS_STORAGE_BUCKET_NAME

    def store_in_s3(filename, content):
        conn = S3Connection(settings.ACCESS_KEY, settings.PASS_KEY)
        b = conn.create_bucket(aws_bucket)
        mime = mimetypes.guess_type(filename)[0]
        k = Key(b)
        k.key = filename
        k.set_metadata("Content-Type", mime)
        k.set_contents_from_string(content)
        k.set_acl("public-read")

    print "Running AWS Test PAge"
    context = RequestContext(request)
    context_dict = {}

        
    test_file_name = "TI-Buoy.jpg"


    url = "http://s3.amazonaws.com/" + aws_bucket + "/" + test_file_name
    context_dict = {
        'url': url 
    }

    #Next step. Upload a file 
    # Liz this isn't working, my current theory is because we don't have a Model for it.  We don't actually need it to work via a POST right now. Can you get it to work reading a file from the file system?
    
    if request.method == "POST":
        print "In Post"
        file = request.FILES["file"]
        filename = file["filename"]
        content = file["content"]
        print filename
        store_in_s3(filename, content)

    print context_dict
    return render_to_response('explorer/tests3.html', context_dict, context)
