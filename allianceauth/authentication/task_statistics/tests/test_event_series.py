import datetime as dt

from pytz import utc
from django.test import TestCase
from django.utils.timezone import now

from allianceauth.authentication.task_statistics.event_series import (
    EventSeries,
    FailedTaskSeries,
    RetriedTaskSeries,
    SucceededTaskSeries,
    dashboard_results,
)


class TestEventSeries(TestCase):
    """Testing EventSeries class."""

    class IncompleteEvents(EventSeries):
        """Child class without KEY ID"""

    class MyEventSeries(EventSeries):
        KEY_ID = "TEST"

    def test_should_create_object(self):
        # when
        events = self.MyEventSeries()
        # then
        self.assertIsInstance(events, self.MyEventSeries)

    def test_should_abort_when_redis_client_invalid(self):
        with self.assertRaises(TypeError):
            self.MyEventSeries(redis="invalid")

    def test_should_not_allow_instantiation_of_base_class(self):
        with self.assertRaises(TypeError):
            EventSeries()

    def test_should_not_allow_creating_child_class_without_key_id(self):
        with self.assertRaises(ValueError):
            self.IncompleteEvents()

    def test_should_add_event(self):
        # given
        events = self.MyEventSeries()
        events.clear()
        # when
        events.add()
        # then
        result = events.all()
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[0], now(), delta=dt.timedelta(seconds=30))

    def test_should_add_event_with_specified_time(self):
        # given
        events = self.MyEventSeries()
        events.clear()
        my_time = dt.datetime(2021, 11, 1, 12, 15, tzinfo=utc)
        # when
        events.add(my_time)
        # then
        result = events.all()
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[0], my_time, delta=dt.timedelta(seconds=30))

    def test_should_count_events(self):
        # given
        events = self.MyEventSeries()
        events.clear()
        events.add()
        events.add()
        # when
        result = events.count()
        # then
        self.assertEqual(result, 2)

    def test_should_count_zero(self):
        # given
        events = self.MyEventSeries()
        events.clear()
        # when
        result = events.count()
        # then
        self.assertEqual(result, 0)

    def test_should_count_events_within_timeframe_1(self):
        # given
        events = self.MyEventSeries()
        events.clear()
        events.add(dt.datetime(2021, 12, 1, 12, 0, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 10, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 15, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 30, tzinfo=utc))
        # when
        result = events.count(
            earliest=dt.datetime(2021, 12, 1, 12, 8, tzinfo=utc),
            latest=dt.datetime(2021, 12, 1, 12, 17, tzinfo=utc),
        )
        # then
        self.assertEqual(result, 2)

    def test_should_count_events_within_timeframe_2(self):
        # given
        events = self.MyEventSeries()
        events.clear()
        events.add(dt.datetime(2021, 12, 1, 12, 0, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 10, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 15, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 30, tzinfo=utc))
        # when
        result = events.count(earliest=dt.datetime(2021, 12, 1, 12, 8))
        # then
        self.assertEqual(result, 3)

    def test_should_count_events_within_timeframe_3(self):
        # given
        events = self.MyEventSeries()
        events.clear()
        events.add(dt.datetime(2021, 12, 1, 12, 0, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 10, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 15, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 30, tzinfo=utc))
        # when
        result = events.count(latest=dt.datetime(2021, 12, 1, 12, 12))
        # then
        self.assertEqual(result, 2)

    def test_should_clear_events(self):
        # given
        events = self.MyEventSeries()
        events.clear()
        events.add()
        events.add()
        # when
        events.clear()
        # then
        self.assertEqual(events.count(), 0)

    def test_should_return_date_of_first_event(self):
        # given
        events = self.MyEventSeries()
        events.clear()
        events.add(dt.datetime(2021, 12, 1, 12, 0, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 10, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 15, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 30, tzinfo=utc))
        # when
        result = events.first_event()
        # then
        self.assertEqual(result, dt.datetime(2021, 12, 1, 12, 0, tzinfo=utc))

    def test_should_return_date_of_first_event_with_range(self):
        # given
        events = self.MyEventSeries()
        events.clear()
        events.add(dt.datetime(2021, 12, 1, 12, 0, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 10, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 15, tzinfo=utc))
        events.add(dt.datetime(2021, 12, 1, 12, 30, tzinfo=utc))
        # when
        result = events.first_event(
            earliest=dt.datetime(2021, 12, 1, 12, 8, tzinfo=utc)
        )
        # then
        self.assertEqual(result, dt.datetime(2021, 12, 1, 12, 10, tzinfo=utc))

    def test_should_return_all_events(self):
        # given
        events = self.MyEventSeries()
        events.clear()
        events.add()
        events.add()
        # when
        results = events.all()
        # then
        self.assertEqual(len(results), 2)


class TestDashboardResults(TestCase):
    def test_should_return_counts_for_given_timeframe_only(self):
        # given
        earliest_task = now() - dt.timedelta(minutes=15)
        succeeded = SucceededTaskSeries()
        succeeded.clear()
        succeeded.add(now() - dt.timedelta(hours=1, seconds=1))
        succeeded.add(earliest_task)
        succeeded.add()
        succeeded.add()
        retried = RetriedTaskSeries()
        retried.clear()
        retried.add(now() - dt.timedelta(hours=1, seconds=1))
        retried.add(now() - dt.timedelta(seconds=30))
        retried.add()
        failed = FailedTaskSeries()
        failed.clear()
        failed.add(now() - dt.timedelta(hours=1, seconds=1))
        failed.add()
        # when
        results = dashboard_results(hours=1)
        # then
        self.assertEqual(results.succeeded, 3)
        self.assertEqual(results.retried, 2)
        self.assertEqual(results.failed, 1)
        self.assertEqual(results.total, 6)
        self.assertEqual(results.earliest_task, earliest_task)

    def test_should_work_with_no_data(self):
        # given
        succeeded = SucceededTaskSeries()
        succeeded.clear()
        retried = RetriedTaskSeries()
        retried.clear()
        failed = FailedTaskSeries()
        failed.clear()
        # when
        results = dashboard_results(hours=1)
        # then
        self.assertEqual(results.succeeded, 0)
        self.assertEqual(results.retried, 0)
        self.assertEqual(results.failed, 0)
        self.assertEqual(results.total, 0)
        self.assertIsNone(results.earliest_task)
