# Notifications

Alliance Auth has a build in notification system. The purpose of the notification system is to provide an easy and quick way to send messages to users of Auth. For example some apps are using it to inform users about results after long running tasks have completed and admins will automatically get notifications about system errors.

The number of unread notifications is shown to the user in the top menu. And the user can click on the notification count to open the notifications app.

![notification app](/_static/images/features/core/notifications.png)

## Settings

The notifications app can be configured through settings.

- `NOTIFICATIONS_REFRESH_TIME`: The unread count in the top menu is automatically refreshed to keep the user informed about new notifications. This setting allows to set the time between each refresh in seconds. You can also set it to `0` to turn off automatic refreshing. Default: `30`
- `NOTIFICATIONS_MAX_PER_USER`: Maximum number of notifications that are stored per user. Older notifications are replaced by newer once. Default: `50`
