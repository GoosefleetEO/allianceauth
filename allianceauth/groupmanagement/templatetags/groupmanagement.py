from django import template
from django.contrib.auth.models import User

from allianceauth.groupmanagement.managers import GroupManager


register = template.Library()


@register.filter
def can_manage_groups(user: User) -> bool:
    """returns True if the given user can manage groups. Returns False otherwise."""
    if not isinstance(user, User):
        return False
    return GroupManager.can_manage_groups(user)
