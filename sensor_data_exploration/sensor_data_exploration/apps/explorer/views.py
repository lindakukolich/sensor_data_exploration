from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Caroline and Linda say hello Buoy!")

# Create your views here.
