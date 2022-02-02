from django.conf.urls import include

from allianceauth.authentication import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^activate/complete/$', views.activation_complete, name='registration_activation_complete'),
    # The activation key can make use of any character from the
    # URL-safe base64 alphabet, plus the colon as a separator.
    re_path(r'^activate/(?P<activation_key>[-:\w]+)/$', views.ActivationView.as_view(), name='registration_activate'),
    re_path(r'^register/$', views.RegistrationView.as_view(), name='registration_register'),
    re_path(r'^register/complete/$', views.registration_complete, name='registration_complete'),
    re_path(r'^register/closed/$', views.registration_closed, name='registration_disallowed'),
    re_path(r'', include('django.contrib.auth.urls')),
]
