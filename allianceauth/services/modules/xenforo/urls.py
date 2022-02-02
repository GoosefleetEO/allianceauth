from django.conf.urls import include
from django.urls import re_path

from . import views

app_name = 'xenforo'

module_urls = [
    # XenForo service control
    re_path(r'^activate/$', views.activate_xenforo_forum, name='activate'),
    re_path(r'^deactivate/$', views.deactivate_xenforo_forum, name='deactivate'),
    re_path(r'^reset_password/$', views.reset_xenforo_password, name='reset_password'),
    re_path(r'^set_password/$', views.set_xenforo_password, name='set_password'),
]

urlpatterns = [
    re_path(r'^xenforo/', include((module_urls, app_name), namespace=app_name)),
]
