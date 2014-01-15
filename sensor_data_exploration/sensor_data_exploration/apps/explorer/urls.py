from django.conf.urls import patterns, url
from sensor_data_exploration.apps.explorer import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/', views.about, name='about'),
                       url(r'^get_data_ajax/', views.get_data_ajax, name='get_data_ajax'),
                       )
