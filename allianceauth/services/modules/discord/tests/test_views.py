from django_webtest import WebTest
from unittest import mock

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from allianceauth.tests.auth_utils import AuthUtils

from ..models import DiscordUser
from ..manager import DiscordOAuthManager

from . import DEFAULT_AUTH_GROUP, add_permissions, MODULE_PATH


class DiscordViewsTestCase(WebTest):
    def setUp(self):
        self.member = AuthUtils.create_member('auth_member')
        AuthUtils.add_main_character(self.member, 'test character', '1234', '2345', 'test corp', 'testc')
        add_permissions()

    def login(self):
        self.app.set_user(self.member)

    @mock.patch(MODULE_PATH + '.views.DiscordOAuthManager')
    def test_activate(self, manager):
        self.login()
        manager.generate_oauth_redirect_url.return_value = '/example.com/oauth/'
        response = self.app.get('/discord/activate/', auto_follow=False)
        self.assertRedirects(
            response,
            expected_url="/example.com/oauth/",
            target_status_code=404,
            fetch_redirect_response=False,
        )

    @mock.patch(MODULE_PATH + '.tasks.DiscordOAuthManager')
    def test_callback(self, manager):
        self.login()
        manager.add_user.return_value = '1234'
        response = self.app.get('/discord/callback/', params={'code': '1234'})

        self.member = User.objects.get(pk=self.member.pk)

        self.assertTrue(manager.add_user.called)
        self.assertEqual(manager.update_nickname.called, settings.DISCORD_SYNC_NAMES)
        self.assertEqual(self.member.discord.uid, '1234')
        self.assertRedirects(response, expected_url='/services/', target_status_code=200)

    @mock.patch(MODULE_PATH + '.tasks.DiscordOAuthManager')
    def test_reset(self, manager):
        self.login()
        DiscordUser.objects.create(user=self.member, uid='12345')
        manager.delete_user.return_value = True

        response = self.app.get('/discord/reset/')

        self.assertRedirects(response, expected_url='/discord/activate/', target_status_code=302)

    @mock.patch(MODULE_PATH + '.tasks.DiscordOAuthManager')
    def test_deactivate(self, manager):
        self.login()
        DiscordUser.objects.create(user=self.member, uid='12345')
        manager.delete_user.return_value = True

        response = self.app.get('/discord/deactivate/')

        self.assertTrue(manager.delete_user.called)
        self.assertRedirects(response, expected_url='/services/', target_status_code=200)
        with self.assertRaises(ObjectDoesNotExist):
            discord_user = User.objects.get(pk=self.member.pk).discord
