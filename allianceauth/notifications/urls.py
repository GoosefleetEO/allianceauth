from django.urls import re_path
from . import views

app_name = 'notifications'
# Notifications
urlpatterns = [
    re_path(r'^remove_notifications/(\w+)/$', views.remove_notification, name='remove'),
    re_path(r'^notifications/mark_all_read/$', views.mark_all_read, name='mark_all_read'),
    re_path(r'^notifications/delete_all_read/$', views.delete_all_read, name='delete_all_read'),
    re_path(r'^notifications/$', views.notification_list, name='list'),
    re_path(r'^notifications/(\w+)/$', views.notification_view, name='view'),
    re_path(
        r'^user_notifications_count/(?P<user_pk>\d+)/$',
        views.user_notifications_count,
        name='user_notifications_count'
    ),
]
