from django.urls import re_path

from . import views

app_name = 'srp'

urlpatterns = [
    # SRP URLS
    re_path(r'^$', views.srp_management, name='management'),
    re_path(r'^all/$', views.srp_management, {'all': True}, name='all'),
    re_path(r'^(\w+)/view$', views.srp_fleet_view, name='fleet'),
    re_path(r'^add/$', views.srp_fleet_add_view, name='add'),
    re_path(r'^(\w+)/edit$', views.srp_fleet_edit_view, name='edit'),
    re_path(r'^(\w+)/request', views.srp_request_view, name='request'),

    # SRP URLS
    re_path(r'^(\w+)/remove$', views.srp_fleet_remove, name='remove'),
    re_path(r'^(\w+)/disable$', views.srp_fleet_disable, name='disable'),
    re_path(r'^(\w+)/enable$', views.srp_fleet_enable, name='enable'),
    re_path(r'^(\w+)/complete$', views.srp_fleet_mark_completed,
        name='mark_completed'),
    re_path(r'^(\w+)/incomplete$', views.srp_fleet_mark_uncompleted,
        name='mark_uncompleted'),
    re_path(r'^request/remove/', views.srp_request_remove,
        name="request_remove"),
    re_path(r'^request/approve/', views.srp_request_approve,
        name='request_approve'),
    re_path(r'^request/reject/', views.srp_request_reject,
        name='request_reject'),
    re_path(r'^request/(\w+)/update', views.srp_request_update_amount,
        name="request_update_amount"),
]
