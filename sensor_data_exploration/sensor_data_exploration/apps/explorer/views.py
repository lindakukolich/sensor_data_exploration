from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Caroline says hello Buoy!")

# Create your views here.
