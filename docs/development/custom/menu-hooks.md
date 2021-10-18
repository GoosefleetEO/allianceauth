# Menu Hooks

The menu hooks allow you to dynamically specify menu items from your plugin app or service. To achieve this you should subclass or instantiate the `services.hooks.MenuItemHook` class and then register the menu item with one of the hooks.

To register a MenuItemHook class you would do the following:

```Python
@hooks.register('menu_item_hook')
def register_menu():
    return MenuItemHook('Example Item', 'glyphicon glyphicon-heart', 'example_url_name',150)
```

The `MenuItemHook` class specifies some parameters/instance variables required for menu item display.

## MenuItemHook(text, classes, url_name, order=None)

### text

The text shown as menu item, e.g. usually the name of the app.

### classes

The classes that should be applied to the bootstrap menu item icon

### url_name

The name of the Django URL to use

### order

An integer which specifies the order of the menu item, lowest to highest. Community apps are free ot use an oder above `1000`. Numbers below are served for Auth.

### navactive

A list of views or namespaces the link should be highlighted on. See [django-navhelper](https://github.com/geelweb/django-navhelper#navactive) for usage. Defaults to the supplied `url_name`.

### count

`count` is an integer shown next to the menu item as badge when `count` is not `None`.

This is a great feature to signal the user, that he has some open issues to take care of within an app. For example Auth uses this feature to show the specific number of open group request to the current user.

```eval_rst
.. hint::
    Here is how to stay consistent with the Auth design philosophy for using this feature:
    1. Use it to display open items that the current user can close by himself only. Do not use it for items, that the user has no control over.
    2. If there are currently no open items, do not show a badge at all.
```

To use it set count the `render()` function of your subclass in accordance to the current user. Here is an example:

```Python
def render(self, request):
    # ...
    self.count = calculate_count_for_user(request.user)
    # ...
```

## Customization

If you cannot get the menu item to look the way you wish, you are free to subclass and override the default render function and the template used.
