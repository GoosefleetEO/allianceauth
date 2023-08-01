# URL Hooks

## Base functionality

The URL hooks allow you to dynamically specify URL patterns from your plugin app or service. To achieve this you should subclass or instantiate the `services.hooks.UrlHook` class and then register the URL patterns with the hook.

To register a UrlHook class you would do the following:

```python
@hooks.register('url_hook')
def register_urls():
    return UrlHook(app_name.urls, 'app_name', r^'app_name/')
```

### Public views

In addition is it possible to make views public. Normally, all views are automatically decorated with the `main_character_required` decorator. That decorator ensures a user needs to be logged in and have a main before he can access that view. This feature protects against a community app sneaking in a public view without the administrator knowing about it.

An app can opt-out of this feature by adding a list of views to be excluded when registering the URLs. See the `excluded_views` parameter for details.

```eval_rst
.. note::
    Note that for a public view to work, administrators need to also explicitly allow apps to have public views in their AA installation, by adding the apps label to ``APPS_WITH_PUBLIC_VIEWS`` setting.
```

## Examples

An app called `plugin` provides a single view:

```python
def index(request):
    return render(request, 'plugin/index.html')
```

The app's `urls.py` would look like so:

```python
from django.urls import path
import plugin.views

urlpatterns = [
    path('index/', plugins.views.index, name='index'),
]
```

Subsequently it would implement the UrlHook in a dedicated `auth_hooks.py` file like so:

```python
from alliance_auth import hooks
from services.hooks import UrlHook
import plugin.urls

@hooks.register('url_hook')
def register_urls():
    return UrlHook(plugin.urls, 'plugin', r^'plugin/')
```

When this app is included in the project's `settings.INSTALLED_APPS` users would access the index view by navigating to `https://example.com/plugin/index`.

## API

```eval_rst
.. autoclass:: allianceauth.services.hooks.UrlHook
    :members:
```
