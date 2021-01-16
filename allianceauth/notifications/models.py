import logging

from django.db import models
from django.contrib.auth.models import User

from .managers import NotificationManager

logger = logging.getLogger(__name__)


class Notification(models.Model):
    """Notification to a user within Auth"""
    
    NOTIFICATIONS_MAX_PER_USER_DEFAULT = 50
    NOTIFICATIONS_REFRESH_TIME_DEFAULT = 30
    
    LEVEL_CHOICES = (
        ('danger', 'CRITICAL'),
        ('danger', 'ERROR'),
        ('warning', 'WARN'),
        ('info', 'INFO'),
        ('success', 'DEBUG'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=10)
    title = models.CharField(max_length=254)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    viewed = models.BooleanField(default=False, db_index=True)

    objects = NotificationManager()
  
    def __str__(self) -> str:
        return "%s: %s" % (self.user, self.title)

    def save(self, *args, **kwargs):
        # overriden save to ensure cache is invaidated on very call
        super().save(*args, **kwargs)        
        Notification.objects.invalidate_user_notification_cache(self.user.pk)

    def delete(self, *args, **kwargs):
        # overriden delete to ensure cache is invaidated on very call
        super().delete(*args, **kwargs)     
        Notification.objects.invalidate_user_notification_cache(self.user.pk)

    def mark_viewed(self) -> None:
        """mark notification as viewed"""
        logger.info("Marking notification as viewed: %s" % self)
        self.viewed = True
        self.save()

    def set_level(self, level_name: str) -> None:
        """set notification level according to level name, e.g. 'CRITICAL'
        
        raised exception on invalid level names
        """
        try:
            new_level = [
                item[0] for item in self.LEVEL_CHOICES if item[1] == level_name
            ][0]
        except IndexError:
            raise ValueError('Invalid level name: %s' % level_name)

        self.level = new_level
        self.save()
