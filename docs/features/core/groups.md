# Groups

Group Management is one of the core tasks of Alliance Auth. Many of Alliance Auth's services allow for synchronizing of group membership, allowing you to grant permissions or roles in services to access certain aspects of them.

## Creating groups

Administrators can create custom groups for users to join. Examples might be groups like `Leadership`, `CEO` or `Scouts`.

When you create a `Group` additional settings are available beyond the normal Django group model. The admin page looks like this:

![AuthGroup Admin page](/_static/images/features/core/groupmanagement/group-admin.png)

Here you have several options:

### Internal

Users cannot see, join or request to join this group. This is primarily used for Auth's internally managed groups, though can be useful if you want to prevent users from managing their membership of this group themselves. This option will override the Hidden, Open and Public options when enabled.

By default, every new group created will be an internal group.

### Hidden

Group is hidden from the user interface, but users can still join if you give them the appropriate join link. The URL will be along the lines of `https://example.com/en/group/request_add/{group_id}`. You can get the Group ID from the admin page URL.

This option still respects the Open option.

### Open

When a group is toggled open, users who request to join the group will be immediately added to the group.

If the group is not open, their request will have to be approved manually by someone with the group management role, or a group leader of that group.

### Public

Group is accessible to any registered user, even when they do not have permission to join regular groups.

The key difference is that the group is completely unmanaged by Auth. **Once a member joins they will not be removed unless they leave manually, you remove them manually, or their account is deliberately set inactive or deleted.**

Most people won't have a use for public groups, though it can be useful if you wish to allow public access to some services. You can grant service permissions on a public group to allow this behavior.

```eval_rst
.. _ref-reserved-group-names:
```

## Reserved group names

When using Alliance Auth to manage external services like Discord, Auth will automatically duplicate groups on those services. E.g. on Discord Auth will create roles of the same name as groups. However, there may be cases where you want to manage groups on external services by yourself or by another bot. For those cases you can define a list of reserved group names. Auth will ensure that you can not create groups with a reserved name. You will find this list on the admin site under groupmanagement.

```eval_rst
.. note::
    While this feature can help to avoid naming conflicts with groups on external services, the respective service component in Alliance Auth also needs to be build in such a way that it knows how to prevent these conflicts. Currently only the Discord and Teamspeak3 services have this ability.
```

## Managing groups

In order to access group management, users need to be either a superuser, granted the `auth | user | group_management ( Access to add members to groups within the alliance )` permission or a group leader (discussed later).

### Group Requests

When a user joins or leaves a group which is not marked as "Open", their group request will have to be approved manually by a user with the `group_management` permission or by a group leader of the group they are requesting.

### Group Membership

The group membership tab gives an overview of all of the non-internal groups.

![Group overview](/_static/images/features/core/groupmanagement/group-membership.png)

#### Group Member Management

Clicking on the blue eye will take you to the group member management screen. Here you can see a list of people who are in the group, and remove members where necessary.

![Group overview](/_static/images/features/core/groupmanagement/group-member-management.png)

#### Group Audit Log

Whenever a user Joins, Leaves, or is Removed from a group, this is logged. To find the audit log for a given group, click the light-blue button to the right of the Group Member Management (blue eye) button.

These logs contain the Date and Time the action was taken (in EVE/UTC), the user which submitted the request being acted upon (requestor), the user's main character, the type of request (join, leave or removed), the action taken (accept, reject or remove), and the user that took the action (actor).

![Audit Log Example](/_static/images/features/core/groupmanagement/group_audit_log.png)

### Group Leaders

Group leaders have the same abilities as users with the `group_management` permission, _however_, they will only be able to:

- Approve requests for groups they are a leader of.
- View the Group Membership and Group Members of groups they are leaders of.

This allows you to more finely control who has access to manage which groups.

### Auto Leave

By default, in AA both requests and leaves for non-open groups must be approved by a group manager. If you wish to allow users to leave groups without requiring approvals, add the following lines to your `local.py`

```python
## Allows users to freely leave groups without requiring approval.
GROUPMANAGEMENT_AUTO_LEAVE = True
```

```eval_rst
.. note::
    Before you set `GROUPMANAGEMENT_AUTO_LEAVE = True`, make sure there are no pending leave requests, as this option will hide the "Leave Requests" tab.
```

## Settings

Here is a list of available settings for Group Management. They can be configured by adding them to your AA settings file (``local.py``).
Note that all settings are optional and the app will use the documented default settings if they are not used.

```eval_rst
+---------------------------------------------+---------------------------------------------------------------------------+------------+
| Name                                        | Description                                                               | Default    |
+=============================================+===========================================================================+============+
| ``GROUPMANAGEMENT_REQUESTS_NOTIFICATION``   | Send Auth notifications to all group leaders for join and leave requests. | ``False``  |
+---------------------------------------------+---------------------------------------------------------------------------+------------+
| ``GROUPMANAGEMENT_AUTO_LEAVE``              | Allows users to freely leave groups without requiring approval..          | ``False``  |
+---------------------------------------------+---------------------------------------------------------------------------+------------+
```

## Permissions

In order to join a group other than a public group, the permission `groupmanagement.request_groups` (`Can request non-public groups` in the admin panel) must be active on their account, either via a group or directly applied to their User account.

When a user loses this permission, they will be removed from all groups _except_ Public groups.

```eval_rst
.. note::
    By default, the ``groupmanagement.request_groups`` permission is applied to the ``Member`` group. In most instances this, and perhaps adding it to the ``Blue`` group, should be all that is ever needed. It is unsupported and NOT advisable to apply this permission to a public group. See #697 for more information.
```

Group Management should be mostly done using group leaders, a series of permissions are included below for thoroughness:

```eval_rst
+--------------------------------+-------------------+------------------------------------------------------------------------------------+
| Permission                     | Admin Site        | Auth Site                                                                          |
+================================+===================+====================================================================================+
| auth.group_management          | None              | Can Approve and Deny all Group Requests, Can view and manage all group memberships |
+--------------------------------+-------------------+------------------------------------------------------------------------------------+
| groupmanagement.request_groups | None              | Can Request Non-Public Groups                                                      |
+--------------------------------+-------------------+------------------------------------------------------------------------------------+
```
