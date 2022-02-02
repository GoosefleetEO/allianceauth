import allianceauth.urls
from django.urls import path
from . import views

urlpatterns = allianceauth.urls.urlpatterns

urlpatterns += [
    # Navhelper test urls
    path("main-page/", views.page, name="p1"),
    path("main-page/sub-section/", views.page, name="p1-s1"),
    path("second-page/", views.page, name="p1"),
]

handler500 = "allianceauth.views.Generic500Redirect"
handler404 = "allianceauth.views.Generic404Redirect"
handler403 = "allianceauth.views.Generic403Redirect"
handler400 = "allianceauth.views.Generic400Redirect"
