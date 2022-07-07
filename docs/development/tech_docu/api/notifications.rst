======================
notifications
======================

The notifications package has an API for sending notifications.

Location: ``allianceauth.notifications``

.. automodule:: allianceauth.notifications.__init__
    :members: notify

models
===========

.. autoclass:: allianceauth.notifications.models.Notification
    :members:
    :exclude-members: DoesNotExist, MultipleObjectsReturned, save

managers
===========

.. autoclass:: allianceauth.notifications.managers.NotificationManager
    :members: notify_user, user_unread_count
