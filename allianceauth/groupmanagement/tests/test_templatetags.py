from unittest.mock import patch

from django.test import TestCase
from allianceauth.tests.auth_utils import AuthUtils

from ..templatetags.groupmanagement import can_manage_groups

MODULE_PATH = 'allianceauth.groupmanagement.templatetags.groupmanagement'


@patch(MODULE_PATH + '.GroupManager.can_manage_groups')
class TestCanManageGroups(TestCase):
        
    def setUp(self):        
        self.user = AuthUtils.create_user('Bruce Wayne')

    def test_return_normal_result(self, mock_can_manage_groups):
        mock_can_manage_groups.return_value = True

        self.assertTrue(can_manage_groups(self.user))
        self.assertTrue(mock_can_manage_groups.called)
        
    def test_return_false_if_not_user(self, mock_can_manage_groups):
        mock_can_manage_groups.return_value = True

        self.assertFalse(can_manage_groups('invalid'))
        self.assertFalse(mock_can_manage_groups.called)
