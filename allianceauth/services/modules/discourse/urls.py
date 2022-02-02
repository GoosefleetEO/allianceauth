from django.urls import re_path

from . import views

urlpatterns = [
    # Discourse Service Control
    re_path(r'^discourse/sso$', views.discourse_sso, name='auth_discourse_sso'),
]
