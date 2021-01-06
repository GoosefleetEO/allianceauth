# Structure Timers

Structure Timers helps you keep track of both offensive and defensive structure timers in your space.

![timerboard](/_static/images/features/apps/timerboard.png)

## Installation

Add `'allianceauth.timerboard',` to your `INSTALLED_APPS` list in your auth project's settings file. Run migrations to complete installation.

## Permissions

To use and administer this feature, users will require some of the following.

```eval_rst
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| Permission                            | Admin Site       | Auth Site                                                                |
+=======================================+==================+==========================================================================+
| auth.timer_view                       | None             | Can view Timerboard Timers                                               |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| auth.timer_manage                     | None             | Can Manage Timerboard timers                                             |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
```
