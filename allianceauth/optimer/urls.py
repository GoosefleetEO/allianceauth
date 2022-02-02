from django.urls import re_path

from . import views

app_name = 'optimer'

urlpatterns = [
    re_path(r'^$', views.optimer_view, name='view'),
    re_path(r'^add$', views.add_optimer_view, name='add'),
    re_path(r'^(\w+)/remove$', views.remove_optimer, name='remove'),
    re_path(r'^(\w+)/edit$', views.edit_optimer, name='edit'),
    ]
