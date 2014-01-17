import json
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from sensor_data_exploration.apps.explorer.models import *
from django.utils import simplejson
import time
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

def index(request):
    ''' The main page for the explorer app '''
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = get_data('wu_ti_temp_f')
    # We only need to convert the complicated things to JSON.
    # The strings for things like titles are fine the way they are
    context_dict['jsonydata'] = simplejson.dumps(context_dict['ydata'])
    context_dict['jsonxdata'] = simplejson.dumps(context_dict['xdata'])

    print "context_dict"
    print context_dict

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('explorer/index.html', context_dict, context)

def about(request):
    ''' About page, mostly to practice having links '''
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('explorer/about.html', context_dict, context)

# Does this want to move to another file?
# CM: I'm about to repeat a bunch of this code into get_data_ajax rather the break this but we will need to refactor to be DRY.
def get_data(plot_sensor_id):
    '''Read data from the database, preparing to make a plot'''

    # TODO
    # add data/time selectors
    # Improve feedback when the sensor_id is bad
    # Improve feedback when there is no plot data

    context_dict = {}
    context_dict['goodPlotData'] = True

    # Make sure we have a sensor_id that is in the sensor table
    if Sensor.objects.filter(sensor_id=plot_sensor_id) == False:
        context_dict['goodPlotData'] = False
        print "get_data: Error retrieving plot data for sensor " + plot_sendor_id + "No such sensor in explorer_sensor table"
        return context_dict

    # We know there is at least one sensor that matches our given id.
    # just take the first one.  That'll teach them to repeat values!
    s = Sensor.objects.filter(
        sensor_id=plot_sensor_id
        )
    plot_sensor = s.values()[0]
    print plot_sensor
    # Pick out Sensor fields to display as part of the plot
    context_dict['plot_title'] = plot_sensor['sensor_short_name']
    context_dict['plot_subtitle'] = plot_sensor['data_source_id']
    context_dict['plot_yaxis_label'] = plot_sensor['units_long']
    context_dict['point_label'] = plot_sensor['units_short']
    
    # Retrieve the actual data for the plot
    q = SensorData.objects.filter(
        sensor_id_id=plot_sensor_id
        )
    
    # Pick out the times of the observations, and convert them to JavaScript
    # timestamps, which are in milliseconds
    xdata = []
    xdata_datetime = q.values_list('time_stamp', flat=True)
    for i in range(0, len(xdata_datetime)):
        xdata.append(time.mktime(xdata_datetime[i].timetuple()) * 1000)
    context_dict['xdata'] = list(xdata)

    # Pick out the values for each observation
    ydata = q.values_list('num_value', flat=True)
    context_dict['ydata'] = list(ydata)

    # Make sure that we actually got some data, or this plot is no good
    if len(context_dict['xdata']) == 0 or len(context_dict['ydata']) == 0:
        print "get_data: Error retrieving plot data for plot " + plot_sensor_id + ": No data"
        context_dict['goodPlotData'] = 0

    return context_dict


def get_data_ajax(request):
    print "starting get_data_ajax with plot_sensor_id= "
    plot_sensor_id = request.GET.get('sensorid')
    print plot_sensor_id

    '''Read data from the database, preparing to make a plot'''

    # TODO
    # add data/time selectors
    # Improve feedback when the sensor_id is bad
    # Improve feedback when there is no plot data

    #CM: Q for Linda? Do we want to default to False then have the code change it to good when proven good?
    goodPlotData = True

    # Make sure we have a sensor_id that is in the sensor table
    if Sensor.objects.filter(sensor_id=plot_sensor_id) == False:
        goodPlotData = False
        print "get_data: Error retrieving plot data for sensor " + plot_sendor_id + "No such sensor in explorer_sensor table"
        return HttpResponse(json.dumps(goodPlotData), mimetype='application/json')

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
        )
    
    # Pick out the times of the observations, and convert them to JavaScript
    # timestamps, which are in milliseconds
    xdata = []
    xdata_datetime = q.values_list('time_stamp', flat=True)
    for i in range(0, len(xdata_datetime)):
        xdata.append(time.mktime(xdata_datetime[i].timetuple()) * 1000)
        xdata = list(xdata)

    # Pick out the values for each observation
    ydata = q.values_list('num_value', flat=True)
    ydata = list(ydata)

    # Make sure that we actually got some data, or this plot is no good
    if len(xdata) == 0 or len(ydata) == 0:
        print "get_data: Error retrieving plot data for plot " + plot_sensor_id + ": No data"
        goodPlotData = False

    #should this be in an else?    
    data_to_dump = {'xdata': xdata, 
                    'ydata': ydata,
                    'plot_title': plot_sensor['sensor_short_name'],
                    'plot_subtitle': plot_sensor['data_source_id'],
                    'plot_yaxis_label': plot_sensor['units_long'],
                    'point_label': plot_sensor['units_short'],
                    'goodPlotData': goodPlotData
                }
    print "data_to_dump"
    print data_to_dump
    json_data = json.dumps(data_to_dump, cls=DjangoJSONEncoder)
    print json_data
    return HttpResponse(json_data, mimetype='application/json')
