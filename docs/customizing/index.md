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
from django.urls import re_path
from django.urls import include

import allianceauth.urls

urlpatterns = [
    re_path(r'', include(allianceauth.urls)),
]
```

This means every request gets passed to the Alliance Auth URL config to be interpreted.

If you wanted to add a URL pointing to a custom view, it can be added anywhere in the list if not already used by Alliance Auth:

```python
from django.urls import re_path
from django.urls import include, path

import allianceauth.urls
import myauth.views

urlpatterns = [
    re_path(r'', include(allianceauth.urls)),
    path('myview/', myauth.views.myview, name='myview'),
]
```

Additionally you can override URLs used by Alliance Auth here:

```python
from django.urls import re_path
from django.urls import include, path

import allianceauth.urls
import myauth.views

urlpatterns = [
    path('account/login/', myauth.views.login, name='auth_login_user'),
    re_path(r'', include(allianceauth.urls)),
]
```

## Example: Adding an external link to the sidebar

As an example we are adding an external links to the Alliance Auth sidebar using the template overrides feature. For our example let's add a link to Google's start page.

### Step 1 - Create the template override folder

First you need to create the folder for the template on your server. For AA to pick it up it has to match a specific structure.

If you have a default installation you can create the folder like this:

```sh
mkdir -p /home/allianceserver/myauth/myauth/templates/allianceauth
```

### Step 2 - Download the original template

Next you need to download a copy of the original template file we want to change. For that let's move into the above folder and then download the file into the current folder with:

```sh
cd /home/allianceserver/myauth/myauth/templates/allianceauth
wget <https://gitlab.com/allianceauth/allianceauth/-/raw/master/allianceauth/templates/allianceauth/side-menu.html>
```

### Step 3 - Modify the template

Now you can modify the template to add your custom link. To create the google link we can add this snippet *between* the `{% menu_items %}` and the `</ul>` tag:

```sh
nano /home/allianceserver/myauth/myauth/templates/allianceauth/side-menu.html
```

```jinja
    <li>
        <a href="https://www.google.com/" target="_blank">
            <i class="fab fa-google fa-fw"></i>Google
        </a>
    </li>
```

```eval_rst
.. hint::
    You can find other icons with a matching style on the `Font Awesome site <https://fontawesome.com/v5/search?m=free>`_ . AA currently uses Font Awesome version 5. You also want to keep the ``fa-fw`` tag to ensure all icons have the same width.
```

### Step 4 - Restart your AA services

Finally, restart your AA services and your custom link should appear in the sidebar.
