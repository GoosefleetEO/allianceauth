from django.conf.urls import include
from django.urls import re_path

from . import views

app_name = 'ips4'

module_urls = [
    # IPS4 Service Control
    re_path(r'^activate/$', views.activate_ips4, name='activate'),
    re_path(r'^deactivate/$', views.deactivate_ips4, name='deactivate'),
    re_path(r'^reset_password/$', views.reset_ips4_password, name='reset_password'),
    re_path(r'^set_password/$', views.set_ips4_password, name='set_password'),
]

urlpatterns = [
    re_path(r'^ips4/', include((module_urls, app_name), namespace=app_name))
]
