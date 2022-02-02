from django.conf.urls import include
from django.urls import re_path

app_name = 'example'

module_urls = [
    # Add your module URLs here
]

urlpatterns = [
    re_path(r'^example/', include((module_urls, app_name), namespace=app_name)),
]
