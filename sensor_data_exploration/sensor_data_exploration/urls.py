from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = patterns('',
                       # This says read in the urls.py file in sensor_data_exploration/explorer
                       url(r'^admin/', include(admin.site.urls)),
                       # html is generates in views.py file by the index method
                       url(r'^$', views.index, name='index'),
                       url(r'^about/', views.about, name='about'),
                       url(r'^map/', views.map, name='map'),
                       url(r'^sensors/', views.sensors, name='sensors'),
                       url(r'^get_data_ajax/', views.get_data_ajax, name='get_data_ajax'),
                       url(r'^get_point_ajax/', views.get_point_ajax, name='get_point_ajax'),
                       url(r'^tests3', views.tests3, name='tests3'),
		       url(r'^shortTest$', views.shortTest, name='shortTest'),
                   )

# prep to handle uploaded media (people's login photo) in debug mode
# INSECURE AND SLOW.  THIS NEEDS TO BE DIFFERENT FOR DEPLOYMENT!!!
#if settings.DEBUG:
#        urlpatterns += patterns(
#               'django.views.static',
#                (r'media/(?P<path>.*)',
#                'serve',
#                {'document_root': settings.MEDIA_ROOT}), )

# Static files, both in DEBUG and not DEBUG mode
urlpatterns += patterns(
    'django.views.static',
    (r'static/(?P<path>.*)',
     'serve',
     {'document_root': settings.STATIC_ROOT}),
)
