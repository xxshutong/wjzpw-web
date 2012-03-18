from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


#landing
urlpatterns = patterns('webverse.controllers.landing',
    # Landing page.
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^ajax_get_city_by_province/(\d+)/$', 'ajax_get_city_by_province', name='ajax_get_city_by_province'),

)

#personal
urlpatterns += patterns('webverse.controllers.personal',
    # Personal register page.
    url(r'^personal/register/$', 'register', name='personal_register'),

)

staticdir= settings.PROJECT_DIR + settings.WEBVERSE_DIR + "/static"
urlpatterns += patterns('', url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': staticdir}),)
