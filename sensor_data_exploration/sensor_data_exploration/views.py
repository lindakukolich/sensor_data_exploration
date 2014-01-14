from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.

def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "Hello world from sensor_data_exploration website root!"}
    return render_to_response('index.html', context_dict, context)
#    return HttpResponse("Hello world from sensor_data_exploration website root!")
