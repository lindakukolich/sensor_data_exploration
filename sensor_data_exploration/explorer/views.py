from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Caroline and Linda and Liz and Max say hello Buoy!")

# Create your views here.
