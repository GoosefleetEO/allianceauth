from unittest import mock

from django.test import TestCase
from django.contrib.auth.models import User, Group

from allianceauth.eveonline.models import EveCorporationInfo, EveAllianceInfo
from allianceauth.tests.auth_utils import AuthUtils

from ..signals import check_groups_on_state_change


class GroupManagementStateTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = AuthUtils.create_user('test')
        AuthUtils.add_main_character(
            cls.user, 'test character', '1', corp_id='2', corp_name='test_corp', corp_ticker='TEST', alliance_id='3', alliance_name='TEST'
        )
        cls.user.profile.refresh_from_db()
        cls.alliance = EveAllianceInfo.objects.create(
            alliance_id='3', alliance_name='test alliance', alliance_ticker='TEST', executor_corp_id='2'
        )
        cls.corp = EveCorporationInfo.objects.create(
            corporation_id='2', corporation_name='test corp', corporation_ticker='TEST', alliance=cls.alliance, member_count=1
        )
        cls.state_group = Group.objects.create(name='state_group')
        cls.open_group = Group.objects.create(name='open_group')
        cls.state = AuthUtils.create_state('test state', 500)
        cls.state_group.authgroup.states.add(cls.state)
        cls.state_group.authgroup.internal = False
        cls.state_group.save()

    def setUp(self):
        self.user.refresh_from_db()
        self.state.refresh_from_db()

    def _refresh_user(self):
        self.user = User.objects.get(pk=self.user.pk)

    def _refresh_test_group(self):
        self.state_group = Group.objects.get(pk=self.state_group.pk)

    def test_drop_state_group(self):
        self.user.groups.add(self.open_group)
        self.user.groups.add(self.state_group)     
        self.assertEqual(self.user.profile.state.name, "Guest")

        self.state.member_corporations.add(self.corp)
        self._refresh_user()
        self.assertEqual(self.user.profile.state, self.state)
        groups = self.user.groups.all()
        self.assertIn(self.state_group, groups) #keeps group
        self.assertIn(self.open_group, groups) #public group unafected

        self.state.member_corporations.clear()
        self._refresh_user()
        self.assertEqual(self.user.profile.state.name, "Guest")
        groups = self.user.groups.all()
        self.assertNotIn(self.state_group, groups) #looses group
        self.assertIn(self.open_group, groups) #public group unafected
