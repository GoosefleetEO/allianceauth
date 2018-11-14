# Alliance Market

## Deprecation

Alliance Market relies on the now non-functional XML API.

Please remove this service data with `python manage.py migrate appname zero` and then remove from your  `INSTALLED_APPS` list.
