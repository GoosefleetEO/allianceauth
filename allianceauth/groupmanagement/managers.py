from django.contrib.auth.models import Group
from django.db.models import Q


class GroupManager:
    def __init__(self):
        pass

    @staticmethod
    def get_joinable_groups(state):
        return Group.objects.select_related('authgroup').exclude(authgroup__internal=True)\
            .filter(Q(authgroup__states=state) | Q(authgroup__states=None))

    @staticmethod
    def get_all_non_internal_groups():
        return Group.objects.select_related('authgroup').exclude(authgroup__internal=True)

    @staticmethod
    def get_group_leaders_groups(user):
        return Group.objects.select_related('authgroup').filter(authgroup__group_leaders__in=[user])

    @staticmethod
    def joinable_group(group, state):
        """
        Check if a group is a user/state joinable group, i.e.
        not an internal group for Corp, Alliance, Members etc,
        or restricted from the user's current state.
        :param group: django.contrib.auth.models.Group object
        :param state: allianceauth.authentication.State object
        :return: bool True if its joinable, False otherwise
        """
        if len(group.authgroup.states.all()) != 0 and state not in group.authgroup.states.all():
            return False
        return not group.authgroup.internal

    @staticmethod
    def check_internal_group(group):
        """
        Check if a group is auditable, i.e not an internal group
        :param group: django.contrib.auth.models.Group object
        :return: bool True if it is auditable, false otherwise
        """
        return not group.authgroup.internal

    @staticmethod
    def check_internal_group(group):
        """
        Check if a group is auditable, i.e not an internal group
        :param group: django.contrib.auth.models.Group object
        :return: bool True if it is auditable, false otherwise
        """
        return not group.authgroup.internal

    @staticmethod
    def has_management_permission(user):
        return user.has_perm('auth.group_management')

    @classmethod
    def can_manage_groups(cls, user):
        """
        For use with user_passes_test decorator.
        Check if the user can manage groups. Either has the
        auth.group_management permission or is a leader of at least one group
        and is also a Member.
        :param user: django.contrib.auth.models.User for the request
        :return: bool True if user can manage groups, False otherwise
        """
        if user.is_authenticated:
            return cls.has_management_permission(user) or user.leads_groups.all()
        return False

    @classmethod
    def can_manage_group(cls, user, group):
        """
        Check user has permission to manage the given group
        :param user: User object to test permission of
        :param group: Group object the user is attempting to manage
        :return: True if the user can manage the group
        """
        if user.is_authenticated:
            return cls.has_management_permission(user) or user.leads_groups.filter(group=group).exists()
        return False
