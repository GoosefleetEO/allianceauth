from django.contrib.auth.decorators import login_required
from django.urls import re_path
from django.views.generic.base import TemplateView

from . import views

app_name = 'authentication'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(
        r'^account/login/$',
        TemplateView.as_view(template_name='public/login.html'),
        name='login'
    ),
    re_path(
        r'^account/characters/main/$',
        views.main_character_change,
        name='change_main_character'
    ),
    re_path(
        r'^account/characters/add/$',
        views.add_character,
        name='add_character'
    ),
    re_path(r'^dashboard/$', views.dashboard, name='dashboard'),
]
