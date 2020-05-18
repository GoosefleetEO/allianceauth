from unittest.mock import patch, Mock

from requests.exceptions import HTTPError

from django.test import TestCase

from allianceauth.tests.auth_utils import AuthUtils

from . import TEST_USER_NAME, TEST_USER_ID, TEST_MAIN_NAME, TEST_MAIN_ID, MODULE_PATH
from ..discord_client import DiscordClient, DiscordApiBackoff
from ..models import DiscordUser
from ..utils import set_logger_to_file


logger = set_logger_to_file(MODULE_PATH + '.models', __file__)


class TestBasicsAndHelpers(TestCase):

    def test_str(self):
        user = AuthUtils.create_user(TEST_USER_NAME)
        discord_user = DiscordUser.objects.create(user=user, uid=TEST_USER_ID)
        expected = 'Peter Parker - 198765432012345678'
        self.assertEqual(str(discord_user), expected)

    def test_repr(self):
        user = AuthUtils.create_user(TEST_USER_NAME)
        discord_user = DiscordUser.objects.create(user=user, uid=TEST_USER_ID)
        expected = 'DiscordUser(user=\'Peter Parker\', uid=198765432012345678)'
        self.assertEqual(repr(discord_user), expected)
    
    def test_guild_get_or_create_role_ids(self):
        mock_client = Mock(spec=DiscordClient)
        mock_client.match_guild_roles_to_names.return_value = \
            [({'id': 1, 'name': 'alpha'}, True), ({'id': 2, 'name': 'bravo'}, True)]
        
        result = DiscordUser._guild_get_or_create_role_ids(mock_client, [])
        excepted = [1, 2]
        self.assertEqual(set(result), set(excepted))


@patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
class TestUpdateNick(TestCase):

    def setUp(self): 
        self.user = AuthUtils.create_user(TEST_USER_NAME)
        self.discord_user = DiscordUser.objects.create(
            user=self.user, uid=TEST_USER_ID
        )

    @staticmethod
    def user_info(nick):
        return {
            'user': {
                'id': TEST_USER_ID,
                'username': TEST_USER_NAME
            },
            'nick': nick,
            'roles': [1, 2, 3]
        }
   
    def test_can_update(self, mock_DiscordClient):
        AuthUtils.add_main_character_2(self.user, TEST_MAIN_NAME, TEST_MAIN_ID)        
        mock_DiscordClient.return_value.modify_guild_member.return_value = True
        
        result = self.discord_user.update_nickname()
        self.assertTrue(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)

    def test_dont_update_if_user_has_no_main(self, mock_DiscordClient):        
        mock_DiscordClient.return_value.modify_guild_member.return_value = False
        
        result = self.discord_user.update_nickname()
        self.assertFalse(result)
        self.assertFalse(mock_DiscordClient.return_value.modify_guild_member.called)
    
    def test_return_none_if_user_no_longer_a_member(
        self, mock_DiscordClient
    ):
        AuthUtils.add_main_character_2(self.user, TEST_MAIN_NAME, TEST_MAIN_ID)
        mock_DiscordClient.return_value.modify_guild_member.return_value = None
        
        result = self.discord_user.update_nickname()
        self.assertIsNone(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)        

    def test_return_false_if_api_returns_false(self, mock_DiscordClient):
        AuthUtils.add_main_character_2(self.user, TEST_MAIN_NAME, TEST_MAIN_ID)        
        mock_DiscordClient.return_value.modify_guild_member.return_value = False
        
        result = self.discord_user.update_nickname()
        self.assertFalse(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)


@patch(MODULE_PATH + '.models.notify')
@patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
class TestDeleteUser(TestCase):

    def setUp(self): 
        self.user = AuthUtils.create_user(TEST_USER_NAME)        
        self.discord_user = DiscordUser.objects.create(
            user=self.user, uid=TEST_USER_ID
        )

    def test_can_delete_user(self, mock_DiscordClient, mock_notify):        
        mock_DiscordClient.return_value.remove_guild_member.return_value = True
        result = self.discord_user.delete_user()
        self.assertTrue(result)
        self.assertFalse(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.remove_guild_member.called)
        self.assertFalse(mock_notify.called)

    def test_can_delete_user_and_notify_user(self, mock_DiscordClient, mock_notify):
        mock_DiscordClient.return_value.remove_guild_member.return_value = True
        result = self.discord_user.delete_user(notify_user=True)
        self.assertTrue(result)
        self.assertTrue(mock_notify.called)

    def test_can_delete_user_when_member_is_unknown(
        self, mock_DiscordClient, mock_notify
    ): 
        mock_DiscordClient.return_value.remove_guild_member.return_value = None
        result = self.discord_user.delete_user()
        self.assertTrue(result)
        self.assertFalse(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.remove_guild_member.called)
        self.assertFalse(mock_notify.called)

    def test_return_false_when_api_fails(self, mock_DiscordClient, mock_notify):
        mock_DiscordClient.return_value.remove_guild_member.return_value = False
        result = self.discord_user.delete_user()
        self.assertFalse(result)

    def test_dont_notify_if_user_was_already_deleted_and_return_none(
        self, mock_DiscordClient, mock_notify
    ):
        mock_DiscordClient.return_value.remove_guild_member.return_value = None
        DiscordUser.objects.get(pk=self.discord_user.pk).delete()
        result = self.discord_user.delete_user()
        self.assertIsNone(result)
        self.assertFalse(
            DiscordUser.objects.filter(user=self.user, uid=TEST_USER_ID).exists()
        )
        self.assertTrue(mock_DiscordClient.return_value.remove_guild_member.called)
        self.assertFalse(mock_notify.called)

    def test_return_false_on_api_backoff(self, mock_DiscordClient, mock_notify):
        mock_DiscordClient.return_value.remove_guild_member.side_effect = \
            DiscordApiBackoff(999)
        result = self.discord_user.delete_user()
        self.assertFalse(result)

    def test_return_false_on_http_error(self, mock_DiscordClient, mock_notify):
        mock_exception = HTTPError('error')
        mock_exception.response = Mock()
        mock_exception.response.status_code = 500
        mock_DiscordClient.return_value.remove_guild_member.side_effect = \
            mock_exception
        result = self.discord_user.delete_user()
        self.assertFalse(result)


@patch(MODULE_PATH + '.managers.DiscordClient', spec=DiscordClient)
@patch(MODULE_PATH + '.models.DiscordUser._guild_get_or_create_role_ids')
@patch(MODULE_PATH + '.models.DiscordUser.objects.user_group_names')
class TestUpdateGroups(TestCase):

    def setUp(self): 
        self.user = AuthUtils.create_user(TEST_USER_NAME)
        self.discord_user = DiscordUser.objects.create(
            user=self.user, uid=TEST_USER_ID
        )
        
    def test_can_update(
        self, 
        mock_user_group_names, 
        mock_guild_get_or_create_role_ids, 
        mock_DiscordClient
    ):        
        roles_requested = [1, 2, 3]
        mock_user_group_names.return_value = []
        mock_guild_get_or_create_role_ids.return_value = roles_requested
        mock_DiscordClient.return_value.modify_guild_member.return_value = True
        
        result = self.discord_user.update_groups()
        self.assertTrue(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)
    
    def test_return_none_if_user_no_longer_a_member(
        self,
        mock_user_group_names, 
        mock_guild_get_or_create_role_ids, 
        mock_DiscordClient
    ):        
        roles_requested = [1, 2, 3]
        mock_user_group_names.return_value = []
        mock_guild_get_or_create_role_ids.return_value = roles_requested
        mock_DiscordClient.return_value.modify_guild_member.return_value = None
                
        result = self.discord_user.update_groups()
        self.assertIsNone(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)

    def test_return_false_if_api_returns_false(
        self, 
        mock_user_group_names, 
        mock_guild_get_or_create_role_ids, 
        mock_DiscordClient
    ):
        roles_requested = [1, 2, 3]
        mock_user_group_names.return_value = []
        mock_guild_get_or_create_role_ids.return_value = roles_requested
        mock_DiscordClient.return_value.modify_guild_member.return_value = False      
        
        result = self.discord_user.update_groups()
        self.assertFalse(result)
        self.assertTrue(mock_DiscordClient.return_value.modify_guild_member.called)
