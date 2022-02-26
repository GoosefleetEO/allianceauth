from unittest.mock import patch

from celery.exceptions import Retry

from django.test import TestCase, override_settings

from allianceauth.authentication.task_statistics.event_series import (
    FailedTaskSeries,
    RetriedTaskSeries,
    SucceededTaskSeries,
)
from allianceauth.authentication.task_statistics.signals import (
    reset_counters,
    is_enabled,
)
from allianceauth.eveonline.tasks import update_character


@override_settings(
    CELERY_ALWAYS_EAGER=True, ALLIANCEAUTH_DASHBOARD_TASK_STATISTICS_DISABLED=False
)
class TestTaskSignals(TestCase):
    fixtures = ["disable_analytics"]

    def test_should_record_successful_task(self):
        # given
        events = SucceededTaskSeries()
        events.clear()
        # when
        with patch(
            "allianceauth.eveonline.tasks.EveCharacter.objects.update_character"
        ) as mock_update:
            mock_update.return_value = None
            update_character.delay(1)
        # then
        self.assertEqual(events.count(), 1)

    def test_should_record_retried_task(self):
        # given
        events = RetriedTaskSeries()
        events.clear()
        # when
        with patch(
            "allianceauth.eveonline.tasks.EveCharacter.objects.update_character"
        ) as mock_update:
            mock_update.side_effect = Retry
            update_character.delay(1)
        # then
        self.assertEqual(events.count(), 1)

    def test_should_record_failed_task(self):
        # given
        events = FailedTaskSeries()
        events.clear()
        # when
        with patch(
            "allianceauth.eveonline.tasks.EveCharacter.objects.update_character"
        ) as mock_update:
            mock_update.side_effect = RuntimeError
            update_character.delay(1)
        # then
        self.assertEqual(events.count(), 1)


@override_settings(ALLIANCEAUTH_DASHBOARD_TASK_STATISTICS_DISABLED=False)
class TestResetCounters(TestCase):
    def test_should_reset_counters(self):
        # given
        succeeded = SucceededTaskSeries()
        succeeded.clear()
        succeeded.add()
        retried = RetriedTaskSeries()
        retried.clear()
        retried.add()
        failed = FailedTaskSeries()
        failed.clear()
        failed.add()
        # when
        reset_counters()
        # then
        self.assertEqual(succeeded.count(), 0)
        self.assertEqual(retried.count(), 0)
        self.assertEqual(failed.count(), 0)


class TestIsEnabled(TestCase):
    @override_settings(ALLIANCEAUTH_DASHBOARD_TASK_STATISTICS_DISABLED=False)
    def test_enabled(self):
        self.assertTrue(is_enabled())

    @override_settings(ALLIANCEAUTH_DASHBOARD_TASK_STATISTICS_DISABLED=True)
    def test_disabled(self):
        self.assertFalse(is_enabled())
