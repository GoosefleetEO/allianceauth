"""Integration tests

Testing all components of the service, with the exception of the Discord API.

Please note that these tests require Redis and will flush it
"""
from collections import namedtuple
import logging
from unittest.mock import patch
from uuid import uuid1

from django_webtest import WebTest
import requests_mock

from django.contrib.auth.models import Group, User
from django.core.cache import caches
from django.shortcuts import reverse
from django.test import TransactionTestCase
from django.test.utils import override_settings

from allianceauth.tests.auth_utils import AuthUtils

from . import (
    TEST_GUILD_ID,
    TEST_USER_NAME, 
    TEST_USER_ID, 
    TEST_MAIN_NAME, 
    TEST_MAIN_ID, 
    MODULE_PATH,
    add_permissions_to_members,
    ROLE_ALPHA,
    ROLE_BRAVO,
    ROLE_CHARLIE,
    ROLE_MIKE,
    create_role
)
from ..discord_client.app_settings import DISCORD_API_BASE_URL
from ..models import DiscordUser

logger = logging.getLogger('allianceauth')

ROLE_MEMBER = create_role(99, 'Member')

# Putting all requests to Discord into objects so we can compare them better
DiscordRequest = namedtuple('DiscordRequest', ['method', 'url'])
guild_roles_request = DiscordRequest(
    method='GET',
    url=f'{DISCORD_API_BASE_URL}guilds/{TEST_GUILD_ID}/roles'
)
create_guild_role_request = DiscordRequest(
    method='POST',
    url=f'{DISCORD_API_BASE_URL}guilds/{TEST_GUILD_ID}/roles'
)
guild_member_request = DiscordRequest(
    method='GET',
    url=f'{DISCORD_API_BASE_URL}guilds/{TEST_GUILD_ID}/members/{TEST_USER_ID}'
)
modify_guild_member_request = DiscordRequest(
    method='PATCH',
    url=f'{DISCORD_API_BASE_URL}guilds/{TEST_GUILD_ID}/members/{TEST_USER_ID}'
)            
remove_guild_member_request = DiscordRequest(
    method='DELETE',
    url=f'{DISCORD_API_BASE_URL}guilds/{TEST_GUILD_ID}/members/{TEST_USER_ID}'
)


def clear_cache():
    default_cache = caches['default']
    redis = default_cache.get_master_client()
    redis.flushall()
    logger.info('Cache flushed')


@patch(MODULE_PATH + '.models.DISCORD_GUILD_ID', TEST_GUILD_ID)
@override_settings(CELERY_ALWAYS_EAGER=True)
@requests_mock.Mocker()
class TestServiceFeatures(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.maxDiff = None
        
    def setUp(self):
        clear_cache()
        AuthUtils.disconnect_signals()
        Group.objects.all().delete()
        User.objects.all().delete()
        AuthUtils.connect_signals()
        self.group_3 = Group.objects.create(name='charlie')        
        self.user = AuthUtils.create_member(TEST_USER_NAME)
        AuthUtils.add_main_character_2(
            self.user, 
            TEST_MAIN_NAME, 
            TEST_MAIN_ID, 
            corp_id='2', 
            corp_name='test_corp', 
            corp_ticker='TEST',
            disconnect_signals=True
        )
        self.discord_user = DiscordUser.objects.create(user=self.user, uid=TEST_USER_ID)
        add_permissions_to_members()
        
    def test_name_of_main_changes(self, requests_mocker):      
        # modify_guild_member()        
        requests_mocker.patch(modify_guild_member_request.url, status_code=204)
        
        # changing nick to trigger signals
        new_nick = f'Testnick {uuid1().hex}'[:32]
        self.user.profile.main_character.character_name = new_nick
        self.user.profile.main_character.save()

        # Need to have called modify_guild_member two times only
        # Once for sync nickname
        # Once for change of main character        
        requests_made = list()
        for r in requests_mocker.request_history:            
            requests_made.append(DiscordRequest(r.method, r.url))

        expected = [modify_guild_member_request, modify_guild_member_request]        
        self.assertListEqual(requests_made, expected)

    def test_user_demoted_to_guest(self, requests_mocker):        
        # remove_guild_member()        
        requests_mocker.delete(remove_guild_member_request.url, status_code=204)
        self.user.groups.clear()

        requests_made = list()
        for r in requests_mocker.request_history:            
            requests_made.append(DiscordRequest(r.method, r.url))
        
        # compare the list of made requests with expected
        expected = [remove_guild_member_request]
        self.assertListEqual(requests_made, expected)

    def test_adding_group_to_user_role_exists(self, requests_mocker):
        # guild_member()                
        requests_mocker.get(
            guild_member_request.url,
            json={
                'user': {'id': str(TEST_USER_ID), 'username': TEST_MAIN_NAME},
                'roles': ['1', '13', '99']
            }
        )        
        # guild_roles()        
        requests_mocker.get(
            guild_roles_request.url, 
            json=[ROLE_ALPHA, ROLE_BRAVO, ROLE_CHARLIE, ROLE_MIKE, ROLE_MEMBER]
        )        
        # create_guild_role()        
        requests_mocker.post(create_guild_role_request.url, json=ROLE_CHARLIE)
        # modify_guild_member()                
        requests_mocker.patch(modify_guild_member_request.url, status_code=204)
                
        # adding new group to trigger signals
        self.user.groups.add(self.group_3)        
        self.user.refresh_from_db()
        
        # compare the list of made requests with expected
        requests_made = list()
        for r in requests_mocker.request_history:            
            requests_made.append(DiscordRequest(r.method, r.url))

        expected = [
            guild_member_request,
            guild_roles_request,            
            modify_guild_member_request
        ]        
        self.assertListEqual(requests_made, expected)

    def test_adding_group_to_user_role_does_not_exist(self, requests_mocker):    
        # guild_member()                
        requests_mocker.get(
            guild_member_request.url,
            json={
                'user': {'id': str(TEST_USER_ID), 'username': TEST_MAIN_NAME},
                'roles': ['1', '13', '99']
            }
        )        
        # guild_roles()        
        requests_mocker.get(
            guild_roles_request.url, 
            json=[ROLE_ALPHA, ROLE_BRAVO, ROLE_MIKE, ROLE_MEMBER]
        )        
        # create_guild_role()        
        requests_mocker.post(create_guild_role_request.url, json=ROLE_CHARLIE)
        # modify_guild_member()                
        requests_mocker.patch(modify_guild_member_request.url, status_code=204)
                
        # adding new group to trigger signals
        self.user.groups.add(self.group_3)        
        self.user.refresh_from_db()
        
        # compare the list of made requests with expected
        requests_made = list()
        for r in requests_mocker.request_history:            
            requests_made.append(DiscordRequest(r.method, r.url))

        expected = [
            guild_member_request,
            guild_roles_request,
            create_guild_role_request,
            modify_guild_member_request
        ]        
        self.assertListEqual(requests_made, expected)
    

class TestServiceUserActivation(WebTest):
    
    def setUp(self):
        self.member = AuthUtils.create_member(TEST_USER_NAME)
        AuthUtils.add_main_character_2(
            self.member, 
            TEST_MAIN_NAME, 
            TEST_MAIN_ID,
            disconnect_signals=True
        )
        add_permissions_to_members()
    
    @patch(MODULE_PATH + '.views.messages')
    @patch(MODULE_PATH + '.models.DiscordUser.objects.add_user')
    @patch(MODULE_PATH + '.managers.OAuth2Session')
    def test_user_activation(
        self, mock_OAuth2Session, mock_add_user, mock_messages
    ): 
        authentication_code = 'auth_code'
        mock_add_user.return_value = True
        oauth_url = 'https://www.example.com/oauth'
        state = ''
        mock_OAuth2Session.return_value.authorization_url.return_value = \
            oauth_url, state
        
        # login
        self.app.set_user(self.member)
        
        # click activate on the service page
        response = self.app.get(reverse('discord:activate'))
        
        # check we got a redirect to Discord OAuth        
        self.assertRedirects(
            response, expected_url=oauth_url, fetch_redirect_response=False
        )

        # simulate Discord callback
        response = self.app.get(
            reverse('discord:callback'), params={'code': authentication_code}
        )

        # user was added to Discord
        self.assertTrue(mock_add_user.called)

        # user got a success message
        self.assertTrue(mock_messages.success.called)
