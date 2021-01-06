# Groups

Group Management is one of the core tasks of Alliance Auth. Many of Alliance Auth's services allow for synchronising of group membership, allowing you to grant permissions or roles in services to access certain aspects of them.

## User Organized Groups

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

## Permission

In order to join a group other than a public group, the permission `groupmanagement.request_groups` (`Can request non-public groups` in the admin panel) must be active on their account, either via a group or directly applied to their User account.

When a user loses this permission, they will be removed from all groups _except_ Public groups.

```eval_rst
.. note::
    By default, the ``groupmanagement.request_groups`` permission is applied to the ``Member`` group. In most instances this, and perhaps adding it to the ``Blue`` group, should be all that is ever needed. It is unsupported and NOT advisable to apply this permission to a public group. See #697 for more information.
```

### Auto Leave

By default in AA, Both requests and leaves for non-open groups must be approved by a group manager. If you wish to allow users to leave groups without requiring approvals, add the following lines to your `local.py`

```python
## Allows users to freely leave groups without requiring approval.
AUTO_LEAVE = True
```