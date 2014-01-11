from django.db import models

class DataSource(models.Model):
    name = models.TextField("Human readable name for use in the page describing the sensor or other type of data source")
    access_info = models.TextField("For use by the scripts that load the data",blank=True)
    owner = models.TextField("who owns the equiptment eg. UMassBoston, NPS")
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)

class SensorID(models.Model):
    sensor_id = models.CharField("A short, unique description for use by programmers.", max_length = 64, unique=True)
    sensor_short_name = models.CharField("Human readable field that  we will use in drop down menus", max_length = 64, unique="true")
    sensor_desc = models.TextField("Human readable description for use in the page describing this sensor", blank=True, null=True)
    #Might use a choices type for units.
    units = models.CharField(max_length = 64, blank=True, null=True)
    kind = models.CharField("A human readable description of the kind of sensor, e.g.like Air Temp, Salinity", max_length=64, blank=True, null=True)
    type = models.CharField("float, string, mp3, jpg, etc.", max_length = 20)
    data_is_prediction_p = models.BooleanField()
    data_source = models.ForeignKey(DataSource)
    
class SensorData(models.Model):
    time_stamp = models.DateTimeField()
    num_value = models.FloatField(blank=True, null=True)
    string_value = models.TextField(blank=True, null=True)
    sensor_id = models.ForeignKey(SensorID)
