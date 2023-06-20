# App Maintenance

## Adding Apps

Your auth project is just a regular Django project - you can add in [other Django apps](https://djangopackages.org/) as desired. Most come with dedicated setup guides, but here is the general procedure:

1. add `'appname',` to your `INSTALLED_APPS` setting in `local.py`
2. run `python manage.py migrate`
3. run `python manage.py collectstatic --noinput`
4. restart AA with `supervisorctl restart myauth:`

## Removing Apps

The following instructions will explain how you can remove an app properly fom your Alliance Auth installation.

```eval_rst
.. note::
    We recommend following these instructions to avoid dangling foreign keys or orphaned Python packages on your system, which might cause conflicts with other apps down the road.

```

### Step 1 - Removing database tables

First, we want to remove the app related tables from the database.

#### Automatic table removal

Let's first try the automatic approach by running the following command:

```sh
python manage.py migrate appname zero
```

If that worked you'll get a confirmation message.

If that did not work and you got error messages, you will need to remove the tables manually. This is pretty common btw, because many apps use sophisticated table setups, which can not be removed automatically by Django.

#### Manual table removal

First, tell Django that these migrations are no longer in effect (note the additional `--fake`):

```sh
python manage.py migrate appname zero --fake
```

Then, open the mysql tool and connect to your Alliance Auth database:

```sh
sudo mysql -u root
use alliance_auth;
```

Next disable foreign key check. This makes it much easier to drop tables in any order.

```sh
SET FOREIGN_KEY_CHECKS=0;
```

Then get a list of all tables. All tables belonging to the app in question will start with `appname_`.

```sh
show tables;
```

Now, drop the tables from the app one by one like so:

```sh
drop table appname_model_1;
drop table appname_model_2;
...
```

And finally, but very importantly, re-enable foreign key checks again and then exit:

```sh
SET FOREIGN_KEY_CHECKS=1;
exit;
```

### Step 2 - Remove the app from Alliance Auth

Once the tables have been removed, you you can remove the app from Alliance Auth. This is done by removing the applabel from the `INSTALLED_APPS` list in your local settings file.

### Step 3 - Remove the Python package

Finally, we want to remove the app's Python package. For that run the following command:

```sh
pip uninstall app-package-name
```

Congrats, you have now removed this app from your Alliance Auth installation.

## Permission Cleanup

Mature Alliance Auth installations, or those with actively developed extensions may find themselves with stale or duplicated Permission models.

This can make it confusing for admins to apply the right permissions, contribute to larger queries in backend management or simply look unsightly.

```shell
python manage.py remove_stale_contenttypes --include-stale-apps
```

This inbuilt Django command will step through each contenttype and offer to delete it, displaying what exactly this will cascade to delete. Pay attention and ensure you understand exactly what is being removed before answering `yes`.

This should only cleanup uninstalled apps, deprecated permissions within apps should be cleaned up using Data Migrations by each responsible application.
