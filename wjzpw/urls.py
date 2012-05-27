from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

# Landing
urlpatterns = patterns('wjzpw.web.controllers.landing',
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

# Personal
urlpatterns += patterns('wjzpw.web.controllers.personal',
    url(r'^personal/register/$', 'personal_register', name='personal_register'),
    url(r'^personal/resume_detail/$', 'resume_detail', name='resume_detail'),
    url(r'^personal/position/list/$', 'ajax_get_positions', name='ajax_get_positions'),
)

# Company
urlpatterns += patterns('wjzpw.web.controllers.company',
    url(r'^company/register/$', 'company_register', name='company_register'),
)

urlpatterns += patterns('', url(r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),)
