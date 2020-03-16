from .models import Notification
from django.core.cache import cache

def user_notification_count(request):
    notification_count = cache.get("u-note:{}".format(request.user.id), -1)
    if notification_count<0:
        notification_count = Notification.objects.filter(user__id=request.user.id).filter(viewed=False).count()
        cache.set("u-note:{}".format(request.user.id),notification_count,5)

    return {'notifications': notification_count}
