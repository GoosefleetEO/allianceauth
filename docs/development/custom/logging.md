# Logging from Custom Apps
Alliance Auth provides a logger for use with custom apps to make everyone's life a little easier.

## Using the Extensions Logger
The extensions logger should not be directly used by custom apps as the error messages logged to it 
will not be labeled with the correct name. In order to correctly use the extensions logger please follow
the code below.

```python
import logging

logger = logging.getLogger('extensions.' + __name__)
logger.name = __name__
```

This works by creating a child logger of the extension logger which propagates all log entries
to the parent (extensions) logger.