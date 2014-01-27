from django.conf.urls import patterns, url
from sensor_data_exploration.apps.explorer import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/', views.about, name='about'),
                       url(r'^map/', views.map, name='map'),
                       url(r'^get_data_ajax/', views.get_data_ajax, name='get_data_ajax'),
                       url(r'^get_point_ajax/', views.get_point_ajax, name='get_point_ajax'),
                       url(r'^tests3', views.tests3, name='tests3'),
                       )
