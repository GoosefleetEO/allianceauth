# Dashboard

The dashboard is the main page of the **Alliance Auth** website and the first page every logged in user will see.

The content of the dashboard is specific to the logged in user. It has a sidebar, which will display the list of apps a user currently as access to based on his permissions. And it also shows which character the user has registered and to which group he belongs.

For admin users the dashboard shows additional technical information about the  AA instance.

![dashboard](/_static/images/features/core/dashboard/dashboard.png)

## Settings

Here is a list of available settings for the dashboard. They can be configured by adding them to your AA settings file (``local.py``).
Note that all settings are optional and the app will use the documented default settings if they are not used.

```eval_rst
+-----------------------------------------------------+-------------------------------------------------------------------------+-----------+
| Name                                                | Description                                                             | Default   |
+=====================================================+=========================================================================+===========+
| ``ALLIANCEAUTH_DASHBOARD_TASKS_MAX_HOURS``          | Statistics will be calculated for task events not older than max hours. | ``24``    |
+-----------------------------------------------------+-------------------------------------------------------------------------+-----------+
| ``ALLIANCEAUTH_DASHBOARD_TASK_STATISTICS_DISABLED`` | Disables recording of task statistics. Used mainly in development.      | ``False`` |
+-----------------------------------------------------+-------------------------------------------------------------------------+-----------+
```
