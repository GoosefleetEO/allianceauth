from django.conf.urls import include
from django.urls import re_path

from . import views

app_name = 'phpbb3'

module_urls = [
    # Forum Service Control
    re_path(r'^activate/$', views.activate_forum, name='activate'),
    re_path(r'^deactivate/$', views.deactivate_forum, name='deactivate'),
    re_path(r'^reset_password/$', views.reset_forum_password, name='reset_password'),
    re_path(r'^set_password/$', views.set_forum_password, name='set_password'),
]

urlpatterns = [
    re_path(r'^phpbb3/', include((module_urls, app_name), namespace=app_name))
]
