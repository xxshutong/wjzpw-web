from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


#landing
urlpatterns = patterns('webverse.controllers.landing',
    # Landing page.
    url(r'^$', 'index', name='index'),

)

staticdir= settings.PROJECT_DIR + settings.WEBVERSE_DIR + "/static"
urlpatterns += patterns('', url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': staticdir}),)
