from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'sensor_data_exploration.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^explorer/', include('explorer.urls')), # This says read in the url in apps.explorer
                       url(r'^admin/', include(admin.site.urls)),
                   )
