from unittest import TestCase
from unittest.mock import patch

from redis import RedisError

from allianceauth.authentication.task_statistics.helpers import (
    ItemCounter, _RedisStub, get_redis_client_or_stub,
)

MODULE_PATH = "allianceauth.authentication.task_statistics.helpers"

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

    def test_can_not_decrement_counter_below_minimum(self):
        # given
        counter = ItemCounter(COUNTER_NAME, minimum=0)
        counter.reset(0)
        # when
        counter.decr(1)
        # then
        self.assertEqual(counter.value(), 0)

    def test_can_not_reset_counter_below_minimum(self):
        # given
        counter = ItemCounter(COUNTER_NAME, minimum=0)
        # when/then
        with self.assertRaises(ValueError):
            counter.reset(-1)

    def test_can_not_init_without_name(self):
        # when/then
        with self.assertRaises(ValueError):
            ItemCounter(name="")

    def test_can_ignore_invalid_values_when_incrementing(self):
        # given
        counter = ItemCounter(COUNTER_NAME)
        counter.reset(0)
        # when
        with patch(MODULE_PATH + ".cache.incr") as m:
            m.side_effect = ValueError
            counter.incr()
        # then
        self.assertEqual(counter.value(), 0)

    def test_can_ignore_invalid_values_when_decrementing(self):
        # given
        counter = ItemCounter(COUNTER_NAME)
        counter.reset(1)
        # when
        with patch(MODULE_PATH + ".cache.decr") as m:
            m.side_effect = ValueError
            counter.decr()
        # then
        self.assertEqual(counter.value(), 1)


class TestGetRedisClient(TestCase):
    def test_should_return_mock_if_redis_not_available_1(self):
        # when
        with patch(MODULE_PATH + ".get_redis_client") as mock_get_master_client:
            mock_get_master_client.return_value.ping.side_effect = RedisError
            result = get_redis_client_or_stub()
        # then
        self.assertIsInstance(result, _RedisStub)

    def test_should_return_mock_if_redis_not_available_2(self):
        # when
        with patch(MODULE_PATH + ".get_redis_client") as mock_get_master_client:
            mock_get_master_client.return_value.ping.return_value = False
            result = get_redis_client_or_stub()
        # then
        self.assertIsInstance(result, _RedisStub)
