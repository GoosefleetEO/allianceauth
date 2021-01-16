======================
notifications
======================

The notifications package has an API for sending notifications.

Location: ``allianceauth.notifications``

.. automodule:: allianceauth.notifications.__init__
    :members: notify
    :undoc-members:

models
===========

.. autoclass:: allianceauth.notifications.models.Notification
    :members: view, set_level, LEVEL_CHOICES
    :undoc-members:

managers
===========

.. autoclass:: allianceauth.notifications.managers.NotificationManager
    :members: notify_user, user_unread_count
    :undoc-members:
