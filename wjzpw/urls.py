from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

#landing
urlpatterns = patterns('web.controllers.landing',
    # Landing page.
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^feedback/$', 'feedback', name='feedback'),
    url(r'^ajax_get_city_by_province/(\d+)/$', 'ajax_get_city_by_province', name='ajax_get_city_by_province'),
    url(r'^verify_image/$', 'verify_image', name='verify_image'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

#personal
urlpatterns += patterns('web.controllers.personal',
    # Personal register page.
    url(r'^personal/register/$', 'personal_register', name='personal_register'),
    url(r'^personal/resume_detail/$', 'resume_detail', name='resume_detail'),

)

staticdir= settings.PROJECT_DIR + settings.WEBVERSE_DIR + "/static"
urlpatterns += patterns('', url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': staticdir}),)
