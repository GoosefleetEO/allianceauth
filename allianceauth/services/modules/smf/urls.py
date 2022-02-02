from django.conf.urls import include
from django.urls import re_path

from . import views

app_name = 'smf'

module_urls = [
    # SMF Service Control
    re_path(r'^activate/$', views.activate_smf, name='activate'),
    re_path(r'^deactivate/$', views.deactivate_smf, name='deactivate'),
    re_path(r'^reset_password/$', views.reset_smf_password, name='reset_password'),
    re_path(r'^set_password/$', views.set_smf_password, name='set_password'),
]

urlpatterns = [
    re_path(r'^smf/', include((module_urls, app_name), namespace=app_name)),
]
