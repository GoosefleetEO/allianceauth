from django.conf.urls import include
from django.urls import re_path

from . import views

app_name = 'openfire'

module_urls = [
    # Jabber Service Control
    re_path(r'^activate/$', views.activate_jabber, name='activate'),
    re_path(r'^deactivate/$', views.deactivate_jabber, name='deactivate'),
    re_path(r'^reset_password/$', views.reset_jabber_password, name='reset_password'),
    re_path(r'^set_password/$', views.set_jabber_password, name='set_password'),
    re_path(r'^broadcast/$', views.jabber_broadcast_view, name='broadcast'),
]

urlpatterns = [
    re_path(r'^openfire/', include((module_urls, app_name), namespace=app_name)),
]
