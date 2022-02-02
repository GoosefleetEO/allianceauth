from django.urls import re_path

from . import views
app_name = 'fleetactivitytracking'

urlpatterns = [
    # FleetActivityTracking (FAT)
    re_path(r'^$', views.fatlink_view, name='view'),
    re_path(r'^statistics/$', views.fatlink_statistics_view, name='statistics'),
    re_path(r'^statistics/corp/(\w+)$', views.fatlink_statistics_corp_view,
        name='statistics_corp'),
    re_path(r'^statistics/corp/(?P<corpid>\w+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/',
        views.fatlink_statistics_corp_view,
        name='statistics_corp_month'),
    re_path(r'^statistics/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.fatlink_statistics_view,
        name='statistics_month'),
    re_path(r'^user/statistics/$', views.fatlink_personal_statistics_view,
        name='personal_statistics'),
    re_path(r'^user/statistics/(?P<year>[0-9]+)/$', views.fatlink_personal_statistics_view,
        name='personal_statistics_year'),
    re_path(r'^user/statistics/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',
        views.fatlink_monthly_personal_statistics_view,
        name='personal_statistics_month'),
    re_path(r'^user/(?P<char_id>[0-9]+)/statistics/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',
        views.fatlink_monthly_personal_statistics_view,
        name='user_statistics_month'),
    re_path(r'^create/$', views.create_fatlink_view, name='create'),
    re_path(r'^modify/(?P<fat_hash>[a-zA-Z0-9_-]+)/$', views.modify_fatlink_view, name='modify'),
    re_path(r'^link/(?P<fat_hash>[a-zA-Z0-9]+)/$', views.click_fatlink_view, name='click'),
]
