from unittest import mock

from django.test import TestCase
from allianceauth.tests.auth_utils import AuthUtils
from allianceauth.eveonline.models import EveCorporationInfo, EveAllianceInfo, EveCharacter
from django.contrib.auth.models import User, Group
from allianceauth.groupmanagement.managers import GroupManager

class GroupManagementVisibilityTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AuthUtils.create_user('test')
        AuthUtils.add_main_character(cls.user, 'test character', '1', corp_id='2', corp_name='test_corp', corp_ticker='TEST', alliance_id='3', alliance_name='TEST')
        cls.user.profile.refresh_from_db()
        cls.alliance = EveAllianceInfo.objects.create(alliance_id='3', alliance_name='test alliance', alliance_ticker='TEST', executor_corp_id='2')
        cls.corp = EveCorporationInfo.objects.create(corporation_id='2', corporation_name='test corp', corporation_ticker='TEST', alliance=cls.alliance, member_count=1)
        cls.group1 = Group.objects.create(name='group1')
        cls.group2 = Group.objects.create(name='group2')
        cls.group3 = Group.objects.create(name='group3')

    def setUp(self):
        self.user.refresh_from_db()

    def _refresh_user(self):
        self.user = User.objects.get(pk=self.user.pk)


    def test_can_manage_group(self):
        

        self.group1.authgroup.group_leaders.add(self.user)
        self.group2.authgroup.group_leader_groups.add(self.group1)
        self._refresh_user()
        groups = GroupManager.get_group_leaders_groups(self.user)

        self.assertIn(self.group1, groups) #avail due to user
        self.assertNotIn(self.group2, groups) #not avail due to group
        self.assertNotIn(self.group3, groups) #not avail at all 

        self.user.groups.add(self.group1)
        self._refresh_user()
        groups = GroupManager.get_group_leaders_groups(self.user)

        self.assertIn(self.group1, groups) #avail due to user
        self.assertIn(self.group2, groups) #avail due to group1
        self.assertNotIn(self.group3, groups) #not avail at all 
