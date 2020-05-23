from unittest import mock
from django.test import TestCase
from allianceauth.notifications.context_processors import user_notification_count
from allianceauth.tests.auth_utils import AuthUtils
from django.core.cache import cache
from allianceauth.notifications.models import Notification

class TestNotificationCount(TestCase):
    def setUp(self):
        self.user = AuthUtils.create_user('magic_mike')
        AuthUtils.add_main_character(self.user, 'Magic Mike', '1', corp_id='2', corp_name='Pole Riders', corp_ticker='PRIDE', alliance_id='3', alliance_name='RIDERS')
        self.user.profile.refresh_from_db()

        ### test notifications for mike

        Notification.objects.create(user_id=1,
                                    level="INFO",
                                    title="Job 1 Failed",
                                    message="Because it was broken",
                                    viewed=True)
        Notification.objects.create(user_id=1,
                                    level="INFO",
                                    title="Job 2 Failed",
                                    message="Because it was broken")
        Notification.objects.create(user_id=1,
                                    level="INFO",
                                    title="Job 3 Failed",
                                    message="Because it was broken")
        Notification.objects.create(user_id=1,
                                    level="INFO",
                                    title="Job 4 Failed",
                                    message="Because it was broken")
        Notification.objects.create(user_id=1,
                                    level="INFO",
                                    title="Job 5 Failed",
                                    message="Because it was broken")
        Notification.objects.create(user_id=1,
                                    level="INFO",
                                    title="Job 6 Failed",
                                    message="Because it was broken")

        self.user2 = AuthUtils.create_user('teh_kid')
        AuthUtils.add_main_character(self.user, 'The Kid', '2', corp_id='2', corp_name='Pole Riders', corp_ticker='PRIDE', alliance_id='3', alliance_name='RIDERS')
        self.user2.profile.refresh_from_db()

        # Noitification for kid

        Notification.objects.create(user_id=2,
                                    level="INFO",
                                    title="Job 6 Failed",
                                    message="Because it was broken")

        mock_req = mock.MagicMock()
        mock_req.user.id = 1
        self.req_mock = mock_req

    def test_no_cache(self):
        context_dict = user_notification_count(self.req_mock)
        self.assertIsInstance(context_dict, dict)
        self.assertEqual(context_dict.get('notifications'), 5)  # 5 only


    @mock.patch('allianceauth.notifications.models.Notification.objects')
    def test_cache(self, mock_foo):
        mock_foo.filter.return_value = mock_foo
        mock_foo.count.return_value = 5

        cache.set("u-note:{}".format(1),10,5)
        context_dict = user_notification_count(self.req_mock)
        self.assertIsInstance(context_dict, dict)
        self.assertEqual(context_dict.get('notifications'), 10) # cached value
        self.assertEqual(mock_foo.called, 0)  # ensure the DB was not hit
