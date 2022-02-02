from django.conf.urls import include
from django.urls import re_path

from . import views

app_name = 'teamspeak3'

module_urls = [
    # Teamspeak3 service control
    re_path(r'^activate/$', views.activate_teamspeak3, name='activate'),
    re_path(r'^deactivate/$', views.deactivate_teamspeak3, name='deactivate'),
    re_path(r'^reset_perm/$', views.reset_teamspeak3_perm, name='reset_perm'),
    re_path(
        r'^admin_update_ts3_groups/$',
        views.admin_update_ts3_groups,
        name='admin_update_ts3_groups'
    ),

    # Teamspeak Urls
    re_path(r'^verify/$', views.verify_teamspeak3, name='verify'),
]

urlpatterns = [
    re_path(r'^teamspeak3/', include((module_urls, app_name), namespace=app_name)),
]
