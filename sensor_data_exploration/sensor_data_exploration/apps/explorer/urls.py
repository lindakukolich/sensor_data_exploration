from django.conf.urls import patterns, url
from sensor_data_exploration.apps.explorer import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))
