from django.contrib import admin
from sensor_data_exploration.explorer.models import DataSource, Sensor, SensorData

# Register your models here.
admin.site.register(DataSource);
admin.site.register(Sensor);
admin.site.register(SensorData);
