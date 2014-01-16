import json
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from sensor_data_exploration.apps.explorer.models import *
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = get_data()
    context_dict['jsonydata'] = simplejson.dumps(list(context_dict['ydata']))

    print "json_ydata: " + context_dict['jsonydata']
    print "context_dict"
    print context_dict

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('explorer/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('explorer/about.html', context_dict, context)

def get_data():
    q = SensorData.objects.filter(
        sensor_id_id='wu_ti_temp_f'
    )
    xdata = q.values_list('time_stamp', flat=True)
    ydata = q.values_list('num_value', flat=True)
    context_dict = {'xdata': xdata, 'ydata': ydata}
    return context_dict


def get_data_ajax(request):
    print "starting get_data_ajax"
    q = SensorData.objects.filter(
        sensor_id_id='wu_ti_temp_f'
    )
    
    xdata = list(q.values_list('time_stamp', flat=True))
    ydata = list(q.values_list('num_value', flat=True))
    data_to_dump = {'xdata': xdata, 'ydata': ydata}
    print "data_to_dump"
    print data_to_dump
    json_data = json.dumps(data_to_dump, cls=DjangoJSONEncoder)
    print json_data
    return HttpResponse(json_data, mimetype='application/json')
