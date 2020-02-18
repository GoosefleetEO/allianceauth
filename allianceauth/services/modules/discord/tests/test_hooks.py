from unittest import mock

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from allianceauth.tests.auth_utils import AuthUtils

from ..auth_hooks import DiscordService
from ..models import DiscordUser
from ..tasks import DiscordTasks
from ..manager import DiscordOAuthManager

from . import DEFAULT_AUTH_GROUP, add_permissions, MODULE_PATH


class DiscordHooksTestCase(TestCase):
    def setUp(self):
        self.member = 'member_user'
        member = AuthUtils.create_member(self.member)
        DiscordUser.objects.create(user=member, uid='12345')
        self.none_user = 'none_user'
        none_user = AuthUtils.create_user(self.none_user)
        self.service = DiscordService
        add_permissions()

    def test_has_account(self):
        member = User.objects.get(username=self.member)
        none_user = User.objects.get(username=self.none_user)
        self.assertTrue(DiscordTasks.has_account(member))
        self.assertFalse(DiscordTasks.has_account(none_user))

    def test_service_enabled(self):
        service = self.service()
        member = User.objects.get(username=self.member)
        none_user = User.objects.get(username=self.none_user)

        self.assertTrue(service.service_active_for_user(member))
        self.assertFalse(service.service_active_for_user(none_user))

    @mock.patch(MODULE_PATH + '.tasks.DiscordOAuthManager')
    def test_update_all_groups(self, manager):
        service = self.service()
        service.update_all_groups()
        # Check member and blue user have groups updated
        self.assertTrue(manager.update_groups.called)
        self.assertEqual(manager.update_groups.call_count, 1)

    def test_update_groups(self):
        # Check member has Member group updated
        with mock.patch(MODULE_PATH + '.tasks.DiscordOAuthManager') as manager:
            service = self.service()
            member = User.objects.get(username=self.member)
            AuthUtils.disconnect_signals()
            service.update_groups(member)
            self.assertTrue(manager.update_groups.called)
            args, kwargs = manager.update_groups.call_args
            user_id, groups = args
            self.assertIn(DEFAULT_AUTH_GROUP, groups)
            self.assertEqual(user_id, member.discord.uid)

        # Check none user does not have groups updated
        with mock.patch(MODULE_PATH + '.tasks.DiscordOAuthManager') as manager:
            service = self.service()
            none_user = User.objects.get(username=self.none_user)
            service.update_groups(none_user)
            self.assertFalse(manager.update_groups.called)

    @mock.patch(MODULE_PATH + '.tasks.DiscordOAuthManager')
    def test_validate_user(self, manager):
        service = self.service()
        # Test member is not deleted
        member = User.objects.get(username=self.member)
        service.validate_user(member)
        self.assertTrue(member.discord)

        # Test none user is deleted
        none_user = User.objects.get(username=self.none_user)
        DiscordUser.objects.create(user=none_user, uid='abc123')
        service.validate_user(none_user)
        self.assertTrue(manager.delete_user.called)
        with self.assertRaises(ObjectDoesNotExist):
            none_discord = User.objects.get(username=self.none_user).discord

    @mock.patch(MODULE_PATH + '.tasks.DiscordOAuthManager')
    def test_sync_nickname(self, manager):
        service = self.service()
        member = User.objects.get(username=self.member)
        AuthUtils.add_main_character(member, 'test user', '12345', corp_ticker='AAUTH')

        service.sync_nickname(member)

        self.assertTrue(manager.update_nickname.called)
        args, kwargs = manager.update_nickname.call_args
        self.assertEqual(args[0], member.discord.uid)
        self.assertEqual(args[1], 'test user')

    @mock.patch(MODULE_PATH + '.tasks.DiscordOAuthManager')
    def test_delete_user(self, manager):
        member = User.objects.get(username=self.member)

        service = self.service()
        result = service.delete_user(member)

        self.assertTrue(result)
        self.assertTrue(manager.delete_user.called)
        with self.assertRaises(ObjectDoesNotExist):
            discord_user = User.objects.get(username=self.member).discord

    def test_render_services_ctrl(self):
        service = self.service()
        member = User.objects.get(username=self.member)
        request = RequestFactory().get('/services/')
        request.user = member

        response = service.render_services_ctrl(request)
        self.assertTemplateUsed(service.service_ctrl_template)
        self.assertIn('/discord/reset/', response)
        self.assertIn('/discord/deactivate/', response)

        # Test register becomes available
        member.discord.delete()
        member = User.objects.get(username=self.member)
        request.user = member
        response = service.render_services_ctrl(request)
        self.assertIn('/discord/activate/', response)

    # TODO: Test update nicknames
