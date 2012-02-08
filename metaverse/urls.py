from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from jsonrpc import jsonrpc_site

import re
import metaverse.rpc

admin.autodiscover()

#landing
urlpatterns = patterns('webverse.controllers.landing',
    # Landing page.
    url(r'^$', 'index', name='index'),
    url(r'^signup/$', 'signup', name = 'signup'),
    url(r'^login/$', 'login', name = 'login'),
    url(r'^logout/$', 'logout', name = 'logout'),
    url(r'^home/$', 'home', name = 'home'),
    url(r'^forgot_password/$', 'forgot_password', name = 'forgot_password'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
)

urlpatterns += patterns('',
    # JSON RPC calls
    url(r'^json/browse/$', 'jsonrpc.views.browse', name='jsonrpc_browser'),
    url(r'^json/', jsonrpc_site.dispatch, name='jsonrpc_mountpoint')
)

urlpatterns += patterns('webverse.controllers.facebook',
    url(r'^facebook/authentication_callback/$', 'authentication_callback'),
)


#parents
urlpatterns += patterns('webverse.controllers.parent',
    # Parent's inbox.
    url(r'^parent/inbox/$', 'inbox', name ='parent_inbox'),
    url(r'^parent/add-activity/$', 'add_activity', name ='parent_add_activity'),
    url(r'^parent/edit-activity/$', 'edit_activity', name ='parent_edit_activity'),
    url(r'^parent/approve-participation/(\d+)/$', 'approve', name = 'approve_participation'),
    url(r'^parent/reject-participation/(\d+)/$', 'reject', name = 'reject_participation'),
    url(r'^parent/approve-redemption/(\d+)/(\d)/$', 'approve_redemption', name = 'approve_redemption'),
    url(r'^parent/reject-redemption/(\d+)/(\d)/$', 'reject_redemption', name = 'reject_redemption'),
    url(r'^parent/badges/(\d+)/$', 'badges', name ='parent_badges'),
    url(r'^parent/rewards/$', 'rewards', name ='parent_rewards'),
    url(r'^parent/add-reward/$', 'add_reward', name ='add_reward'),
    url(r'^parent/edit-reward/$', 'edit_reward', name ='edit_reward'),
    url(r'^parent/delete-reward/(\d+)/$', 'delete_reward', name = 'delete_reward'),
    url(r'^parent/stats/$', 'stats', name ='parent-stats'),
    url(r'^parent/get-stats-by-child/$', 'get_stats_by_child', name ='get-stats-by-child'),
    url(r'^parent/settings/$', 'settings', name ='settings'),
    url(r'^parent/settings/update-kids/(\d+)/$', 'manage_update_kids', name ='manage_update_kids'),
    url(r'^parent/settings/change-password/$', 'manage_change_password', name ='manage_change_password'),
    url(r'^parent/settings/forward-change-email/$', 'manage_change_email', name ='manage_change_email'),
    url(r'^parent/settings/manage-kids/$', 'manage_kids', name ='manage_kids'),
    url(r'^parent/settings/manage-kids/(\d+)/$', 'manage_kids', name ='delete_kids'),
)

#kids
urlpatterns += patterns('webverse.controllers.kid',
    # Kid's inbox.
    url(r'^kid/activity/$', 'kid', name = 'kid'),
    url(r'^kid/badges/$', 'badges', name = 'kid_badges'),
    url(r'^kid/add-activity/$', 'add_activity', name = 'add_activity'),
    url(r'^kid/stats/$', 'kid_stats', name = 'kid_stats'),
    url(r'^kid/rewards/$', 'kid_rewards', name = 'kid_rewards'),
    url(r'^kid/redeem-reward/$', 'kid_redeem_reward', name = 'kid_redeem_reward'),
    url(r'^kid/remind-parent/$', 'kid_remind_parent', name = 'kid_remind_parent'),
)

staticdir= settings.PROJECT_DIR + settings.WEBVERSE_DIR + "/static"
urlpatterns += patterns('', url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': staticdir}),)
