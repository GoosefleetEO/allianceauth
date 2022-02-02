from django.urls import re_path
from . import views

app_name = 'corputils'
urlpatterns = [
    re_path(r'^$', views.corpstats_view, name='view'),
    re_path(r'^add/$', views.corpstats_add, name='add'),
    re_path(r'^(?P<corp_id>(\d)*)/$', views.corpstats_view, name='view_corp'),
    re_path(r'^(?P<corp_id>(\d)+)/update/$', views.corpstats_update, name='update'),
    re_path(r'^search/$', views.corpstats_search, name='search'),
    ]
