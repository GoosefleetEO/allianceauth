# Fleet Operations

Fleet Operations is an app for organizing and communicating fleet schedules.

![optimer](/_static/images/features/apps/optimer.png)

## Installation

Add `'allianceauth.optimer',` to your `INSTALLED_APPS` list in your auth project's settings file. Run migrations to complete installation.

## Permissions

To use and administer this feature, users will require some of the following.

```eval_rst
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| Permission                            | Admin Site       | Auth Site                                                                |
+=======================================+==================+==========================================================================+
| auth.optimer_view                     | None             | Can view Fleet Operation Timers                                          |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| auth.optimer_manage                   | None             | Can Manage Fleet Operation timers                                        |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
```
