from unittest import TestCase

from allianceauth.authentication.task_statistics.helpers import ItemCounter

COUNTER_NAME = "test-counter"


class TestItemCounter(TestCase):
    def test_can_create_counter(self):
        # when
        counter = ItemCounter(COUNTER_NAME)
        # then
        self.assertIsInstance(counter, ItemCounter)

    def test_can_reset_counter_to_default(self):
        # given
        counter = ItemCounter(COUNTER_NAME)
        # when
        counter.reset()
        # then
        self.assertEqual(counter.value(), 0)

    def test_can_reset_counter_to_custom_value(self):
        # given
        counter = ItemCounter(COUNTER_NAME)
        # when
        counter.reset(42)
        # then
        self.assertEqual(counter.value(), 42)

    def test_can_increment_counter_by_default(self):
        # given
        counter = ItemCounter(COUNTER_NAME)
        counter.reset(0)
        # when
        counter.incr()
        # then
        self.assertEqual(counter.value(), 1)

    def test_can_increment_counter_by_custom_value(self):
        # given
        counter = ItemCounter(COUNTER_NAME)
        counter.reset(0)
        # when
        counter.incr(8)
        # then
        self.assertEqual(counter.value(), 8)

    def test_can_decrement_counter_by_default(self):
        # given
        counter = ItemCounter(COUNTER_NAME)
        counter.reset(9)
        # when
        counter.decr()
        # then
        self.assertEqual(counter.value(), 8)

    def test_can_decrement_counter_by_custom_value(self):
        # given
        counter = ItemCounter(COUNTER_NAME)
        counter.reset(9)
        # when
        counter.decr(8)
        # then
        self.assertEqual(counter.value(), 1)

    def test_can_decrement_counter_below_zero(self):
        # given
        counter = ItemCounter(COUNTER_NAME)
        counter.reset(0)
        # when
        counter.decr(1)
        # then
        self.assertEqual(counter.value(), -1)
