from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from wjzpw import settings

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
    url(r'^ajax_forget_password/', 'ajax_forget_password', name='ajax_forget_password'),
    url(r'^activated_password/(?P<token>\w+)/', 'activated_password', name='activated_password'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Personal
urlpatterns += patterns('wjzpw.web.controllers.personal',
    url(r'^personal/register/$', 'personal_register', name='personal_register'),
    url(r'^personal/resume_detail/$', 'resume_detail', name='resume_detail'),
    url(r'^personal/resume_view/(?P<resume_id>\d+)/$', 'resume_view', name='resume_view'),
    url(r'^personal/position/list/$', 'ajax_get_positions', name='ajax_get_positions'),
    url(r'^personal/search_job/(?P<is_vip>\w+)$', 'search_job', name='search_job'),
    url(r'^personal/search_job/$', 'search_job', name='search_job'),
    url(r'^personal/apply/(?P<job_id>\d+)/$', 'ajax_apply_job', name='ajax_apply_job'),
    url(r'^personal/store/(?P<job_id>\d+)/$', 'ajax_store_job', name='ajax_store_job'),
    url(r'^personal/dashboard/$', 'dashboard', name='personal_dashboard')
)

# Company
urlpatterns += patterns('wjzpw.web.controllers.company',
    url(r'^company/register/$', 'company_register', name='company_register'),
    url(r'^company/add_job/$', 'add_job', name='add_job'),
    url(r'^company/search_person/$', 'search_person', name='search_person'),
    url(r'^company/invite/(?P<resume_id>\d+)/$', 'ajax_invite_resume', name='ajax_invite_resume'),
    url(r'^company/store/(?P<resume_id>\d+)/$', 'ajax_store_resume', name='ajax_store_resume'),
    url(r'^company/dashboard/$', 'dashboard', name='company_dashboard')
)

# System
urlpatterns += patterns('wjzpw.web.controllers.system',
    url(r'^system/foot_item/(?P<item_id>\d+)/$', 'get_foot_item', name='get_foot_item'),
    url(r'^system/announcement/(?P<announcement_id>\d+)/$', 'get_announce_list', name='get_announce_list'),

)

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + "/static"}),
    url(r'^tinymce/', include('tinymce.urls')),
)
