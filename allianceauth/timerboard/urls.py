from django.urls import re_path

from . import views

app_name = 'timerboard'

urlpatterns = [
    re_path(r'^$', views.TimerView.as_view(), name='view'),
    re_path(r'^add/$', views.AddTimerView.as_view(), name='add'),
    re_path(r'^remove/(?P<pk>\w+)$', views.RemoveTimerView.as_view(), name='delete'),
    re_path(r'^edit/(?P<pk>\w+)$', views.EditTimerView.as_view(), name='edit'),
]
