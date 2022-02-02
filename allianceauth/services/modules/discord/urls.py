from django.conf.urls import include
from django.urls import re_path

from . import views

app_name = 'discord'

module_urls = [
    # Discord Service Control
    re_path(r'^activate/$', views.activate_discord, name='activate'),
    re_path(r'^deactivate/$', views.deactivate_discord, name='deactivate'),
    re_path(r'^reset/$', views.reset_discord, name='reset'),
    re_path(r'^callback/$', views.discord_callback, name='callback'),
    re_path(r'^add_bot/$', views.discord_add_bot, name='add_bot'),
]

urlpatterns = [
    re_path(r'^discord/', include((module_urls, app_name), namespace=app_name))
]
