from django.urls import re_path

from . import views

app_name = 'hrapplications'

urlpatterns = [
    re_path(r'^$', views.hr_application_management_view,
        name="index"),
    re_path(r'^create/$', views.hr_application_create_view,
        name="create_view"),
    re_path(r'^create/(\d+)', views.hr_application_create_view,
        name="create_view"),
    re_path(r'^remove/(\w+)', views.hr_application_remove,
        name="remove"),
    re_path(r'^view/(\w+)', views.hr_application_view,
        name="view"),
    re_path(r'^personal/view/(\w+)', views.hr_application_personal_view,
        name="personal_view"),
    re_path(r'^personal/removal/(\w+)',
        views.hr_application_personal_removal,
        name="personal_removal"),
    re_path(r'^approve/(\w+)', views.hr_application_approve,
        name="approve"),
    re_path(r'^reject/(\w+)', views.hr_application_reject,
        name="reject"),
    re_path(r'^search/', views.hr_application_search,
        name="search"),
    re_path(r'^mark_in_progress/(\w+)', views.hr_application_mark_in_progress,
        name="mark_in_progress"),
    ]
