from django.urls import re_path
from . import views

app_name = "groupmanagement"

urlpatterns = [
    # groups
    re_path(r"^groups/$", views.groups_view, name="groups"),
    re_path(r"^group/request/join/(\w+)/$", views.group_request_add, name="request_add"),
    re_path(
        r"^group/request/leave/(\w+)/$", views.group_request_leave, name="request_leave"
    ),
    # group management
    re_path(r"^groupmanagement/requests/$", views.group_management, name="management"),
    re_path(r"^groupmanagement/membership/$", views.group_membership, name="membership"),
    re_path(
        r"^groupmanagement/membership/(\w+)/$",
        views.group_membership_list,
        name="membership",
    ),
    re_path(
        r"^groupmanagement/membership/(\w+)/audit-log/$",
        views.group_membership_audit,
        name="audit_log",
    ),
    re_path(
        r"^groupmanagement/membership/(\w+)/remove/(\w+)/$",
        views.group_membership_remove,
        name="membership_remove",
    ),
    re_path(
        r"^groupmanagement/request/join/accept/(\w+)/$",
        views.group_accept_request,
        name="accept_request",
    ),
    re_path(
        r"^groupmanagement/request/join/reject/(\w+)/$",
        views.group_reject_request,
        name="reject_request",
    ),
    re_path(
        r"^groupmanagement/request/leave/accept/(\w+)/$",
        views.group_leave_accept_request,
        name="leave_accept_request",
    ),
    re_path(
        r"^groupmanagement/request/leave/reject/(\w+)/$",
        views.group_leave_reject_request,
        name="leave_reject_request",
    ),
]
