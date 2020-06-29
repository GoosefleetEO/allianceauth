from unittest.mock import Mock, patch

from django.contrib.auth.models import User, Group
from django.test import TestCase
from allianceauth.tests.auth_utils import AuthUtils

from ..backends import StateBackend

MODULE_PATH = 'allianceauth.authentication'

PERMISSION_1 = "authentication.add_user"
PERMISSION_2 = "authentication.change_user"


class TestStatePermissions(TestCase):

    def setUp(self):
        # permissions
        self.permission_1 = AuthUtils.get_permission_by_name(PERMISSION_1)
        self.permission_2 = AuthUtils.get_permission_by_name(PERMISSION_2)

        # group
        self.group_1 = Group.objects.create(name="Group 1")        
        self.group_2 = Group.objects.create(name="Group 2")

        # state
        self.state_1 = AuthUtils.get_member_state()        
        self.state_2 = AuthUtils.create_state("Other State", 75)
        
        # user
        self.user = AuthUtils.create_user("Bruce Wayne")
        self.main = AuthUtils.add_main_character_2(self.user, self.user.username, 123)

    def test_user_has_user_permissions(self):
        self.user.user_permissions.add(self.permission_1)
        
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.has_perm(PERMISSION_1))

    def test_user_has_group_permissions(self):        
        self.group_1.permissions.add(self.permission_1)
        self.user.groups.add(self.group_1)
        
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.has_perm(PERMISSION_1))

    def test_user_has_state_permissions(self):
        self.state_1.permissions.add(self.permission_1)
        self.state_1.member_characters.add(self.main)
        user = User.objects.get(pk=self.user.pk)

        self.assertTrue(user.has_perm(PERMISSION_1))

    def test_when_user_changes_state_perms_change_accordingly(self):
        self.state_1.permissions.add(self.permission_1)        
        self.state_1.member_characters.add(self.main)
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.has_perm(PERMISSION_1))

        self.state_2.permissions.add(self.permission_2)
        self.state_2.member_characters.add(self.main)
        self.state_1.member_characters.remove(self.main)
        user = User.objects.get(pk=self.user.pk)
        self.assertFalse(user.has_perm(PERMISSION_1))
        self.assertTrue(user.has_perm(PERMISSION_2))

    def test_state_permissions_are_returned_for_current_user_object(self):
        # verify state permissions are returns for the current user object 
        # and not for it's instance in the database, which might be outdated        
        self.state_1.permissions.add(self.permission_1)
        self.state_2.permissions.add(self.permission_2)        
        self.state_1.member_characters.add(self.main)
        user = User.objects.get(pk=self.user.pk)
        user.profile.state = self.state_2
        self.assertFalse(user.has_perm(PERMISSION_1))
        self.assertTrue(user.has_perm(PERMISSION_2))
    





    

    
