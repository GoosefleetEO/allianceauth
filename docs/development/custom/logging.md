# Logging from Custom Apps
Alliance Auth provides a logger for use with custom apps to make everyone's life a little easier.

## Using the Extensions Logger
AllianceAuth provides a helper function to get the logger for the current module to reduce the amount of
code you need to write.

```python
from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)
```

This works by creating a child logger of the extension logger which propagates all log entries
to the parent (extensions) logger.

## Changing the Logging Level
By default, the extension logger's level is set to `DEBUG`. 
To change this, uncomment (or add) the following line in `local.py`.

```python
LOGGING['handlers']['extension_file']['level'] = 'INFO'
```
*(Remember to restart your supervisor workers after changes to `local.py`)*

This will change the logger's level to the level you define.

Options are: *(all options accept entries of levels listed below them)*
* `DEBUG`
* `INFO`
* `WARNING`
* `ERROR`
* `CRITICAL`
