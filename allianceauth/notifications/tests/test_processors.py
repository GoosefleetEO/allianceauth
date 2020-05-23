from unittest import mock
from django.test import TestCase
from allianceauth.notifications.context_processors import user_notification_count
from allianceauth.tests.auth_utils import AuthUtils
from django.core.cache import cache
from allianceauth.notifications.models import Notification

class TestNotificationCount(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = AuthUtils.create_user('magic_mike')
        AuthUtils.add_main_character(cls.user, 'Magic Mike', '1', corp_id='2', corp_name='Pole Riders', corp_ticker='PRIDE', alliance_id='3', alliance_name='RIDERS')
        cls.user.profile.refresh_from_db()

        ### test notifications for mike
        Notification.objects.all().delete()
        Notification.objects.create(user=cls.user,
                                    level="INFO",
                                    title="Job 1 Failed",
                                    message="Because it was broken",
                                    viewed=True)
        Notification.objects.create(user=cls.user,
                                    level="INFO",
                                    title="Job 2 Failed",
                                    message="Because it was broken")
        Notification.objects.create(user=cls.user,
                                    level="INFO",
                                    title="Job 3 Failed",
                                    message="Because it was broken")
        Notification.objects.create(user=cls.user,
                                    level="INFO",
                                    title="Job 4 Failed",
                                    message="Because it was broken")
        Notification.objects.create(user=cls.user,
                                    level="INFO",
                                    title="Job 5 Failed",
                                    message="Because it was broken")
        Notification.objects.create(user=cls.user,
                                    level="INFO",
                                    title="Job 6 Failed",
                                    message="Because it was broken")

        cls.user2 = AuthUtils.create_user('teh_kid')
        AuthUtils.add_main_character(cls.user, 'The Kid', '2', corp_id='2', corp_name='Pole Riders', corp_ticker='PRIDE', alliance_id='3', alliance_name='RIDERS')
        cls.user2.profile.refresh_from_db()

        # Noitification for kid
        Notification.objects.create(user=cls.user2,
                                    level="INFO",
                                    title="Job 6 Failed",
                                    message="Because it was broken")


    def test_no_cache(self):
        mock_req = mock.MagicMock()
        mock_req.user.id = self.user.id

        cache.delete("u-note:{}".format(self.user.id)) # force the db to be hit
        context_dict = user_notification_count(mock_req)
        self.assertIsInstance(context_dict, dict)
        self.assertEqual(context_dict.get('notifications'), 5)  # 5 only


    @mock.patch('allianceauth.notifications.models.Notification.objects')
    def test_cache(self, mock_foo):
        mock_foo.filter.return_value = mock_foo
        mock_foo.count.return_value = 5
        mock_req = mock.MagicMock()
        mock_req.user.id = self.user.id

        cache.set("u-note:{}".format(self.user.id),10,5)
        context_dict = user_notification_count(mock_req)
        self.assertIsInstance(context_dict, dict)
        self.assertEqual(context_dict.get('notifications'), 10) # cached value
        self.assertEqual(mock_foo.called, 0)  # ensure the DB was not hit
