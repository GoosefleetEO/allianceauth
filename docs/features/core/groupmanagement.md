# Group Management

In order to access group management, users need to be either a superuser, granted the `auth | user | group_management ( Access to add members to groups within the alliance )` permission or a group leader (discussed later).

## Group Requests

When a user joins or leaves a group which is not marked as "Open", their group request will have to be approved manually by a user with the `group_management` permission or by a group leader of the group they are requesting.

## Group Membership

The group membership tab gives an overview of all of the non-internal groups.

![Group overview](/_static/images/features/core/groupmanagement/group-membership.png)

### Group Member Management

Clicking on the blue eye will take you to the group member management screen. Here you can see a list of people who are in the group, and remove members where necessary.

![Group overview](/_static/images/features/core/groupmanagement/group-member-management.png)

### Group Audit Log

Whenever a user Joins, Leaves, or is Removed from a group, this is logged. To find the audit log for a given group, click the light-blue button to the right of the Group Member Management (blue eye) button.

These logs contain the Date and Time the action was taken (in EVE/UTC), the user which submitted the request being acted upon (requestor), the user's main character, the type of request (join, leave or removed), the action taken (accept, reject or remove), and the user that took the action (actor).

![Audit Log Example](/_static/images/features/core/groupmanagement/group_audit_log.png)

## Group Leaders

Group leaders have the same abilities as users with the `group_management` permission, _however_, they will only be able to:

- Approve requests for groups they are a leader of.
- View the Group Membership and Group Members of groups they are leaders of.

This allows you to more finely control who has access to manage which groups. Currently it is not possible to add a Group as group leaders.
