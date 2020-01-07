from allianceauth.authentication.signals import state_changed
from .managers import GroupManager
from .models import Group
from django.dispatch import receiver
import logging
logger = logging.getLogger(__name__)

@receiver(state_changed)
def check_groups_on_state_change(sender, user, state, **kwargs):
    logger.debug("Updating auth groups for {}".format(user))
    visible_groups = GroupManager.get_joinable_groups(state)
    visible_groups = visible_groups | Group.objects.select_related('authgroup').filter(authgroup__internal=True)
    groups = user.groups.all()
    for g in groups:
        if g not in visible_groups:
            user.groups.remove(g)
