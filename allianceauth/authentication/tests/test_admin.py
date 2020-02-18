from unittest.mock import patch

from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User as BaseUser, Group

from allianceauth.authentication.models import CharacterOwnership, State
from allianceauth.eveonline.autogroups.models import AutogroupsConfig
from allianceauth.eveonline.models import (
    EveCharacter, EveCorporationInfo, EveAllianceInfo
)

from ..admin import (
    BaseUserAdmin, 
    MainCorporationsFilter,
    MainAllianceFilter,
    User,
    UserAdmin,     
    user_main_organization,
    user_profile_pic, 
    user_username,     
)


MODULE_PATH = 'allianceauth.authentication.admin'


class MockRequest(object):
    
    def __init__(self, user=None):
        self.user = user


class TestUserAdmin(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # groups
        cls.group_1 = Group.objects.create(
            name='Group 1'
        )
        cls.group_2 = Group.objects.create(
            name='Group 2'
        )
        
        # user 1 - corp and alliance, normal user
        cls.character_1 = EveCharacter.objects.create(
            character_id='1001',
            character_name='Bruce Wayne',
            corporation_id='2001',
            corporation_name='Wayne Technologies',
            corporation_ticker='WT',
            alliance_id='3001',
            alliance_name='Wayne Enterprises',
            alliance_ticker='WE',
        )
        cls.character_1a = EveCharacter.objects.create(
            character_id='1002',
            character_name='Batman',
            corporation_id='2001',
            corporation_name='Wayne Technologies',
            corporation_ticker='WT',
            alliance_id='3001',
            alliance_name='Wayne Enterprises',
            alliance_ticker='WE',
        )
        alliance = EveAllianceInfo.objects.create(
            alliance_id='3001',
            alliance_name='Wayne Enterprises',
            alliance_ticker='WE',            
            executor_corp_id='2001'
        )
        EveCorporationInfo.objects.create(
            corporation_id='2001',
            corporation_name='Wayne Technologies',
            corporation_ticker='WT',            
            member_count=42,
            alliance=alliance
        )        
        cls.user_1 = User.objects.create_user(
            cls.character_1.character_name.replace(' ', '_'),
            'abc@example.com',
            'password'
        )
        CharacterOwnership.objects.create(
            character=cls.character_1,
            owner_hash='x1' + cls.character_1.character_name,
            user=cls.user_1
        )
        CharacterOwnership.objects.create(
            character=cls.character_1a,
            owner_hash='x1' + cls.character_1a.character_name,
            user=cls.user_1
        )
        cls.user_1.profile.main_character = cls.character_1
        cls.user_1.profile.save()
        cls.user_1.groups.add(cls.group_1)        

        # user 2 - corp only, staff
        cls.character_2 = EveCharacter.objects.create(
            character_id=1003,
            character_name='Clark Kent',
            corporation_id=2002,
            corporation_name='Daily Planet',
            corporation_ticker='DP',
            alliance_id=None
        )
        EveCorporationInfo.objects.create(
            corporation_id=2002,
            corporation_name='Daily Plane',
            corporation_ticker='DP',            
            member_count=99,
            alliance=None
        )
        cls.user_2 = User.objects.create_user(
            cls.character_2.character_name.replace(' ', '_'),
            'abc@example.com',
            'password'
        )
        CharacterOwnership.objects.create(
            character=cls.character_2,
            owner_hash='x1' + cls.character_2.character_name,
            user=cls.user_2
        )
        cls.user_2.profile.main_character = cls.character_2
        cls.user_2.profile.save()
        cls.user_2.groups.add(cls.group_2)
        cls.user_2.is_staff = True
        cls.user_2.save()
        
        # user 3 - no main, no group, superuser
        cls.character_3 = EveCharacter.objects.create(
            character_id=1101,
            character_name='Lex Luthor',
            corporation_id=2101,
            corporation_name='Lex Corp',
            corporation_ticker='LC',
            alliance_id=None
        )
        EveCorporationInfo.objects.create(
            corporation_id=2101,
            corporation_name='Lex Corp',
            corporation_ticker='LC',            
            member_count=666,
            alliance=None
        )
        EveAllianceInfo.objects.create(
            alliance_id='3101',
            alliance_name='Lex World Domination',
            alliance_ticker='LWD',
            executor_corp_id=''
        )
        cls.user_3 = User.objects.create_user(
            cls.character_3.character_name.replace(' ', '_'),
            'abc@example.com',
            'password'
        )
        CharacterOwnership.objects.create(
            character=cls.character_3,
            owner_hash='x1' + cls.character_3.character_name,
            user=cls.user_3
        )
        cls.user_3.is_superuser = True
        cls.user_3.save()

    def setUp(self):
        self.factory = RequestFactory()
        self.modeladmin = UserAdmin(
            model=User, admin_site=AdminSite()
        )

    def _create_autogroups(self):
        """create autogroups for corps and alliances"""
        autogroups_config = AutogroupsConfig(
            corp_groups = True,
            alliance_groups = True
        )
        autogroups_config.save()
        for state in State.objects.all():
            autogroups_config.states.add(state)        
        autogroups_config.update_corp_group_membership(self.user_1)        
    
    # column rendering

    def test_user_profile_pic_u1(self):
        expected = ('<img src="https://images.evetech.net/characters/1001/'
            'portrait?size=32" class="img-circle">')        
        self.assertEqual(user_profile_pic(self.user_1), expected)

    def test_user_profile_pic_u3(self):
        self.assertIsNone(user_profile_pic(self.user_3))

    def test_user_username_u1(self):
        expected = (
            '<strong><a href="/admin/authentication/user/{}/change/">'
            'Bruce_Wayne</a></strong><br>Bruce Wayne'.format(self.user_1.pk)
        )
        self.assertEqual(user_username(self.user_1), expected)

    def test_user_username_u3(self):
        expected = (
            '<strong><a href="/admin/authentication/user/{}/change/">'
            'Lex_Luthor</a></strong>'.format(self.user_3.pk)
        )
        self.assertEqual(user_username(self.user_3), expected)

    def test_user_main_organization_u1(self):
        expected = 'Wayne Technologies<br>Wayne Enterprises'
        self.assertEqual(user_main_organization(self.user_1), expected)

    def test_user_main_organization_u2(self):
        expected = 'Daily Planet'
        self.assertEqual(user_main_organization(self.user_2), expected)

    def test_user_main_organization_u3(self):
        expected = None
        self.assertEqual(user_main_organization(self.user_3), expected)

    def test_characters_u1(self):
        expected = 'Batman, Bruce Wayne'
        result = self.modeladmin._characters(self.user_1)
        self.assertEqual(result, expected)

    def test_characters_u2(self):
        expected = 'Clark Kent'
        result = self.modeladmin._characters(self.user_2)
        self.assertEqual(result, expected)

    def test_characters_u3(self):
        expected = 'Lex Luthor'
        result = self.modeladmin._characters(self.user_3)
        self.assertEqual(result, expected)
    
    def test_groups_u1(self):
        self._create_autogroups()
        expected = 'Group 1'
        result = self.modeladmin._groups(self.user_1)
        self.assertEqual(result, expected)

    def test_groups_u2(self):
        self._create_autogroups()
        expected = 'Group 2'
        result = self.modeladmin._groups(self.user_2)
        self.assertEqual(result, expected)
    
    def test_groups_u3(self):        
        self._create_autogroups()
        result = self.modeladmin._groups(self.user_3)
        self.assertIsNone(result)

    @patch(MODULE_PATH + '._has_auto_groups', False)
    def test_groups_u1_no_autogroups(self):        
        expected = 'Group 1'
        result = self.modeladmin._groups(self.user_1)
        self.assertEqual(result, expected)

    @patch(MODULE_PATH + '._has_auto_groups', False)
    def test_groups_u2_no_autogroups(self):        
        expected = 'Group 2'
        result = self.modeladmin._groups(self.user_2)
        self.assertEqual(result, expected)
    
    @patch(MODULE_PATH + '._has_auto_groups', False)
    def test_groups_u3_no_autogroups(self):                
        result = self.modeladmin._groups(self.user_3)
        self.assertIsNone(result)

    def test_state(self):
        expected = 'Guest'
        result = self.modeladmin._state(self.user_1)
        self.assertEqual(result, expected)

    def test_role_u1(self):
        expected = 'User'
        result = self.modeladmin._role(self.user_1)
        self.assertEqual(result, expected)

    def test_role_u2(self):
        expected = 'Staff'
        result = self.modeladmin._role(self.user_2)
        self.assertEqual(result, expected)

    def test_role_u3(self):
        expected = 'Superuser'
        result = self.modeladmin._role(self.user_3)
        self.assertEqual(result, expected)

    def test_list_2_html_w_tooltips_no_cutoff(self):
        items = ['one', 'two', 'three']
        expected = 'one, two, three'
        result = self.modeladmin._list_2_html_w_tooltips(items, 5)
        self.assertEqual(expected, result)

    def test_list_2_html_w_tooltips_w_cutoff(self):
        items = ['one', 'two', 'three']
        expected = ('<span data-tooltip="one, two, three" '
            'class="tooltip">one, two, (...)</span>')
        result = self.modeladmin._list_2_html_w_tooltips(items, 2)
        self.assertEqual(expected, result)

    def test_list_2_html_w_tooltips_empty_list(self):
        items = []
        expected = None
        result = self.modeladmin._list_2_html_w_tooltips(items, 5)
        self.assertEqual(expected, result)
    
    # actions

    @patch(MODULE_PATH + '.UserAdmin.message_user', auto_spec=True)
    @patch(MODULE_PATH + '.update_character')
    def test_action_update_main_character_model(
        self, mock_task, mock_message_user
    ):
        users_qs = User.objects.filter(pk__in=[self.user_1.pk, self.user_2.pk])
        self.modeladmin.update_main_character_model(
            MockRequest(self.user_1), users_qs
        )
        self.assertEqual(mock_task.delay.call_count, 2)
        self.assertTrue(mock_message_user.called)
    
    # filters

    def test_filter_real_groups_with_autogroups(self):
        
        class UserAdminTest(BaseUserAdmin): 
            list_filter = (UserAdmin.RealGroupsFilter,)
                
        self._create_autogroups()        
        my_modeladmin = UserAdminTest(User, AdminSite())

        # Make sure the lookups are correct
        request = self.factory.get('/')
        request.user = self.user_1
        changelist = my_modeladmin.get_changelist_instance(request)
        filters = changelist.get_filters(request)
        filterspec = filters[0][0]
        expected = [
            (self.group_1.pk, self.group_1.name), 
            (self.group_2.pk, self.group_2.name),
        ]
        self.assertEqual(filterspec.lookup_choices, expected)

        # Make sure the correct queryset is returned
        request = self.factory.get('/', {'group_id__exact': self.group_1.pk})
        request.user = self.user_1                
        changelist = my_modeladmin.get_changelist_instance(request)
        queryset = changelist.get_queryset(request)
        expected = User.objects.filter(groups__in=[self.group_1])
        self.assertSetEqual(set(queryset), set(expected))

    @patch(MODULE_PATH + '._has_auto_groups', False)
    def test_filter_real_groups_no_autogroups(self):
        
        class UserAdminTest(BaseUserAdmin): 
            list_filter = (UserAdmin.RealGroupsFilter,)
                        
        my_modeladmin = UserAdminTest(User, AdminSite())

        # Make sure the lookups are correct
        request = self.factory.get('/')
        request.user = self.user_1
        changelist = my_modeladmin.get_changelist_instance(request)
        filters = changelist.get_filters(request)
        filterspec = filters[0][0]
        expected = [
            (self.group_1.pk, self.group_1.name), 
            (self.group_2.pk, self.group_2.name),
        ]
        self.assertEqual(filterspec.lookup_choices, expected)

        # Make sure the correct queryset is returned
        request = self.factory.get('/', {'group_id__exact': self.group_1.pk})
        request.user = self.user_1                
        changelist = my_modeladmin.get_changelist_instance(request)
        queryset = changelist.get_queryset(request)
        expected = User.objects.filter(groups__in=[self.group_1])
        self.assertSetEqual(set(queryset), set(expected))

    def test_filter_main_corporations(self):
        
        class UserAdminTest(BaseUserAdmin): 
            list_filter = (MainCorporationsFilter,)
                
        my_modeladmin = UserAdminTest(User, AdminSite())

        # Make sure the lookups are correct
        request = self.factory.get('/')
        request.user = self.user_1
        changelist = my_modeladmin.get_changelist_instance(request)
        filters = changelist.get_filters(request)
        filterspec = filters[0][0]
        expected = [            
            ('2002', 'Daily Planet'),
            ('2001', 'Wayne Technologies'),
        ]
        self.assertEqual(filterspec.lookup_choices, expected)

        # Make sure the correct queryset is returned
        request = self.factory.get(
            '/', 
            {'main_corporation_id__exact': self.character_1.corporation_id}
        )
        request.user = self.user_1                
        changelist = my_modeladmin.get_changelist_instance(request)
        queryset = changelist.get_queryset(request)
        expected = [self.user_1]
        self.assertSetEqual(set(queryset), set(expected))

    def test_filter_main_alliances(self):
        
        class UserAdminTest(BaseUserAdmin): 
            list_filter = (MainAllianceFilter,)
                
        my_modeladmin = UserAdminTest(User, AdminSite())

        # Make sure the lookups are correct
        request = self.factory.get('/')
        request.user = self.user_1
        changelist = my_modeladmin.get_changelist_instance(request)
        filters = changelist.get_filters(request)
        filterspec = filters[0][0]
        expected = [            
            ('3001', 'Wayne Enterprises'),            
        ]
        self.assertEqual(filterspec.lookup_choices, expected)

        # Make sure the correct queryset is returned
        request = self.factory.get(
            '/', 
            {'main_alliance_id__exact': self.character_1.alliance_id}
        )
        request.user = self.user_1                
        changelist = my_modeladmin.get_changelist_instance(request)
        queryset = changelist.get_queryset(request)
        expected = [self.user_1]
        self.assertSetEqual(set(queryset), set(expected))