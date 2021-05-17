# App Maintenance

## Adding and Removing Apps

Your auth project is just a regular Django project - you can add in [other Django apps](https://djangopackages.org/) as desired. Most come with dedicated setup guides, but here is the general procedure:

1. add `'appname',` to your `INSTALLED_APPS` setting in `local.py`
2. run `python manage.py migrate`
3. run `python manage.py collectstatic`
4. restart AA with `supervisorctl restart myauth:`

If you ever want to remove an app, you should first clear it from the database to avoid dangling foreign keys: `python manage.py migrate appname zero`. Then you can remove it from your auth project's `INSTALLED_APPS` list.

## Permission Cleanup

Mature Alliance Auth installations, or those with actively developed extensions may find themselves with stale or duplicated Permission models.

This can make it confusing for admins to apply the right permissions, contribute to larger queries in backend management or simply look unsightly.

```shell
python manage.py remove_stale_contenttypes --include-stale-apps
```

This inbuilt Django command will step through each contenttype and offer to delete it, displaying what exactly this will cascade to delete. Pay attention and ensure you understand exactly what is being removed before answering `yes`.

This should only cleanup uninstalled apps, deprecated permissions within apps should be cleaned up using Data Migrations by each responsible application.
