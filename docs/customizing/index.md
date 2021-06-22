# Customizing

It is possible to customize your **Alliance Auth** instance.

```eval_rst
.. warning::
    Keep in mind that you may need to update some of your customizations manually after new Auth releases (e.g. when replacing templates).
```

## Site name

You can replace the default name shown on the web site with your own, e.g. the name of your Alliance.

Just update `SITE_NAME` in your `local.py` settings file accordingly, e.g.:

```python
SITE_NAME = 'Awesome Alliance'
```

## Custom Static and Templates

Within your auth project exists two folders named `static` and `templates`. These are used by Django for rendering web pages. Static refers to content Django does not need to parse before displaying, such as CSS styling or images. When running via a WSGI worker such as Gunicorn static files are copied to a location for the web server to read from. Templates are always read from the template folders, rendered with additional context from a view function, and then displayed to the user.

You can add extra static or templates by putting files in these folders. Note that changes to static requires running the `python manage.py collectstatic` command to copy to the web server directory.

It is possible to overload static and templates shipped with Django or Alliance Auth by including a file with the exact path of the one you wish to overload. For instance if you wish to add extra links to the menu bar by editing the template, you would make a copy of the `allianceauth/templates/allianceauth/base.html` file to `myauth/templates/allianceauth/base.html` and edit it there. Notice the paths are identical after the `templates/` directory - this is critical for it to be recognized. Your custom template would be used instead of the one included with Alliance Auth when Django renders the web page. Similar idea for static: put CSS or images at an identical path after the `static/` directory and they will be copied to the web server directory instead of the ones included.

## Custom URLs and Views

It is possible to add or override URLs with your auth project's URL config file. Upon install it is of the form:

```python
import allianceauth.urls

urlpatterns = [
    url(r'', include(allianceauth.urls)),
]
```

This means every request gets passed to the Alliance Auth URL config to be interpreted.

If you wanted to add a URL pointing to a custom view, it can be added anywhere in the list if not already used by Alliance Auth:

```python
import allianceauth.urls
import myauth.views

urlpatterns = [
    url(r'', include(allianceauth.urls)),
    url(r'myview/$', myauth.views.myview, name='myview'),
]
```

Additionally you can override URLs used by Alliance Auth here:

```python
import allianceauth.urls
import myauth.views

urlpatterns = [
    url(r'account/login/$', myauth.views.login, name='auth_login_user'),
    url(r'', include(allianceauth.urls)),
]
```
