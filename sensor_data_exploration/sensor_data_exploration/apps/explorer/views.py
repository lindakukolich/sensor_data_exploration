from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("The Girls and Max says hello Buoy!")

# Create your views here.
