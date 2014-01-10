#! /usr/bin/env python

# 10.Jan.14 Liz Brooks
# Collect Weather Underground data from Thompson Island station and place in the DB

import urllib2
import json

APIkey='2cbf77167bf2fe35'
stationID='KMABOSTO32'

def getCurrent():
    url='http://api.wunderground.com/api/'+APIkey+'/conditions/q/pws:'+stationID+'.json'
    f = urllib2.urlopen(url)
    json_string = f.read()
    current = json.loads(json_string)
    f.close()
    return current

def getHistory():
    pass

def writeScreen(current):
    location = current['current_observation']['observation_location']['city']
    time=current['current_observation']['observation_time_rfc822']
    temp_f = current['current_observation']['temp_f']
    print "Current temperature at %s in %s is: %s F" % (time, location, temp_f)

def writeCSV():
    pass

def writeDB():
    pass

def initDB():
    pass

if __name__ == "__main__":
    current_conditions = getCurrent()
    writeScreen(current_conditions)
