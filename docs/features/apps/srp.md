# Ship Replacement

Ship Replacement helps you to organize ship replacement programs (SRP) for your alliance.

![srp](/_static/images/features/apps/srp.png)

## Installation

Add `'allianceauth.srp',` to your `INSTALLED_APPS` list in your auth project's settings file. Run migrations to complete installation.

## Permissions

To use and administer this feature, users will require some of the following.

```eval_rst
+----------------------+------------------+------------------------------------------------------------+
| Permission           | Admin Site       | Auth Site                                                  |
+======================+==================+============================================================+
| auth.access_srp      | None             | Can create an SRP request from a fleet                     |
+----------------------+------------------+------------------------------------------------------------+
| auth.srp_management  | None             | Can Approve and Deny SRP requests, Can create an SRP Fleet |
+----------------------+------------------+------------------------------------------------------------+
| srp.add_srpfleetmain | Can Add Model    | Can Create an SRP Fleet                                    |
+----------------------+------------------+------------------------------------------------------------+
```
