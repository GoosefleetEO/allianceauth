# Adding and Removing Apps

Your auth project is just a regular Django project - you can add in [other Django apps](https://djangopackages.org/) as desired. Most come with dedicated setup guides, but here is the general procedure:

1. add `'appname',` to your `INSTALLED_APPS` setting in `local.py`
2. run `python manage.py migrate`
3. run `python manage.py collectstatic`
4. restart AA with `supervisorctl restart myauth:`

If you ever want to remove an app, you should first clear it from the database to avoid dangling foreign keys: `python manage.py migrate appname zero`. Then you can remove it from your auth project's `INSTALLED_APPS` list.
