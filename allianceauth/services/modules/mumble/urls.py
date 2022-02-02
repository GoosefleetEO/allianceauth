from django.conf.urls import include
from django.urls import re_path

from . import views

app_name = 'mumble'

module_urls = [
    # Mumble service control
    re_path(r'^activate/$', views.CreateAccountMumbleView.as_view(), name='activate'),
    re_path(r'^deactivate/$', views.DeleteMumbleView.as_view(), name='deactivate'),
    re_path(r'^reset_password/$', views.ResetPasswordMumbleView.as_view(), name='reset_password'),
    re_path(r'^set_password/$', views.SetPasswordMumbleView.as_view(), name='set_password'),
]

urlpatterns = [
    re_path(r'^mumble/', include((module_urls, app_name), namespace=app_name))
]
