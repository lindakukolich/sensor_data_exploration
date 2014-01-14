from django.db import models

class DataSource(models.Model):
    datasource_id = models.CharField("Unique short name for identifying this source",  max_length = 64, primary_key=True)
    datasource_desc = models.TextField("Human readable name for use in the page describing the sensor or other type of data source", blank=True, null=True)
    access_info = models.TextField("For use by the scripts that load the data",blank=True)
    owner = models.TextField("who owns the equiptment eg. UMassBoston, NPS")
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    
    def __unicode__(self):
        return self.datasource_id + " " + self.latitude + "N, " + self.longitude + "W, " + self.elevation + "elev"

class Sensor(models.Model):
    sensor_id = models.CharField("A short, unique description for use by programmers.", max_length = 64, primary_key=True)
    sensor_short_name = models.CharField("Human readable field that  we will use in drop down menus", max_length = 64)
    sensor_desc = models.TextField("Human readable description for use in the page describing this sensor", blank=True, null=True)
    #Might use a choices type for units.
    units = models.CharField(max_length = 64, blank=True, null=True)
    kind = models.CharField("A human readable description of the kind of sensor, e.g.like Air Temp, Salinity", max_length=64, blank=True, null=True)
    data_type = models.CharField("float, string, mp3, jpg, etc.", max_length = 20)
    data_is_prediction_p = models.BooleanField()
    data_source = models.ForeignKey(DataSource)
    update_granularity_sec = models.FloatField("Check to be sure we don't add to the data table any more fequently then this. Setting the default to 60 sec", default = 60)
    data_min = models.FloatField("If set then check that the data value is more then this",  blank=True, null=True) 
    data_max = models.FloatField("If set then check that the data value is less then this",  blank=True, null=True) 

    def __unicode__(self):
        return self.data_source + ":" + self.sensor_id + " (" + self.sensor_short_name + ") " + self.sensor_desc + "updated every " + self.update_granularity_sec + " seconds"
    
class SensorData(models.Model):
    time_stamp = models.DateTimeField()
    num_value = models.FloatField(blank=True, null=True)
    string_value = models.TextField(blank=True, null=True)
    sensor_id = models.ForeignKey(Sensor)
    
    def __unicode__(self):
        # We need to jump through sensor_id to know what to show for value
        # And after we have done that we need to do string comparisons to see if the field is a float or something else
        output = self.time_stamp + ": " + sensor_id
        return output
    
