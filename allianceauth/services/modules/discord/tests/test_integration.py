from django_webtest import WebTest
from unittest.mock import patch

from django.shortcuts import reverse

from allianceauth.tests.auth_utils import AuthUtils

from . import (
    add_permissions_to_members, 
    MODULE_PATH, 
    TEST_USER_NAME,    
    TEST_MAIN_NAME,
    TEST_MAIN_ID
)


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
