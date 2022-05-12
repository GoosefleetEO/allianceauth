# Admin Site

The admin site allows administrators to configure, manage and trouble shoot Alliance Auth and all it's applications and services. E.g. you can create new groups and assign groups to users.

You can open the admin site by clicking on "Admin" in the drop down menu for a user that has access.

![Admin Site](/_static/images/features/core/admin_site.png)

## Setup for small to medium size installations

For small to medium size alliances it is often sufficient to have no more then two superuser admins (admins that also are superusers). Having two admins usually makes sense, so you can have one primary and one backup.

```eval_rst
.. warning::
    Superusers have read & write access to everything on your AA installation. Superusers also automatically have all permissions and therefore access to all features of your apps. Therefore we recommend to be very careful to whom you give superuser privileges.
```

## Setup for large installations

For large alliances and coalitions you may want to have a couple of administrators to be able to distribute and handle the work load. However, having a larger number of superusers may be a security concern.

As an alternative to superusers admins you can define staff admins. Staff admins can perform most of the daily admin work, but are not superusers and therefore can be restricted in what they can access.

To create a staff admin you need to do two things:

1. Enable the `is_staff` property for a user
1. Give the user permissions for admin tasks

```eval_rst
.. note::
    Note that staff admins have the following limitations:

    - Can not promote users to staff
    - Can not promote users to superuser
    - Can not add/remove permissions for users, groups and states

    These limitations exist to prevent staff admins to promote themselves to quasi superusers. Only superusers can perform these actions.
```

### Staff property

Access to the admin site is restricted. Users needs to have the `is_staff` property to be able to open the site at all. The superuser that is created during the installation
process will automatically have access to the admin site.

```eval_rst
.. hint::
    Without any permissions a "staff user" can open the admin site, but can neither view nor edit anything except for viewing the list of permissions.
```

### Permissions for common admin tasks

Here is a list of permissions a staff admin would need to perform some common admin tasks:

#### Edit users

- auth | user | Can view user
- auth | user | Can change user
- authentication | user | Can view user
- authentication | user | Can change user
- authentication | user profile | Can change profile

#### Delete users

- auth | user | Can view user
- auth | user | Can delete user
- authentication | user | Can delete user
- authentication | user profile | Can delete user profile

#### Add & edit states

- authentication | state | Can add state
- authentication | state | Can change state
- authentication | state | Can view state

#### Delete states

- authentication | state | Can delete state
- authentication | state | Can view state

#### Add & edit groups

- auth | group | Can add group
- auth | group | Can change group
- auth | group | Can view group
- authentication | group | Can add group
- authentication | group | Can change group
- authentication | group | Can view group

#### Delete groups

- auth | group | Can delete group
- authentication | group | Can delete group

### Permissions for other apps

The permissions a staff admin needs to perform tasks for other applications depends on how the applications are configured. the default is to have four permissions (change, delete, edit view) for each model of the applications. The view permission is usually required to see the model list on the admin site and the other three permissions are required to perform the respective action to an object of that model. However, app developer can chose to define permissions differently.
