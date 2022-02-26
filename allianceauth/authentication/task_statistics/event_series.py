import datetime as dt
from collections import namedtuple
from typing import Optional, List

from redis import Redis
from pytz import utc

from django.core.cache import cache

_TaskCounts = namedtuple(
    "_TaskCounts", ["succeeded", "retried", "failed", "total", "earliest_task", "hours"]
)


def dashboard_results(hours: int) -> _TaskCounts:
    """Counts of all task events within the given timeframe."""
    def earliest_if_exists(events: EventSeries, earliest: dt.datetime) -> list:
        my_earliest = events.first_event(earliest=earliest)
        return [my_earliest] if my_earliest else []

    earliest = dt.datetime.utcnow() - dt.timedelta(hours=hours)
    earliest_events = list()
    succeeded = SucceededTaskSeries()
    succeeded_count = succeeded.count(earliest=earliest)
    earliest_events += earliest_if_exists(succeeded, earliest)
    retried = RetriedTaskSeries()
    retried_count = retried.count(earliest=earliest)
    earliest_events += earliest_if_exists(retried, earliest)
    failed = FailedTaskSeries()
    failed_count = failed.count(earliest=earliest)
    earliest_events += earliest_if_exists(failed, earliest)
    return _TaskCounts(
        succeeded=succeeded_count,
        retried=retried_count,
        failed=failed_count,
        total=succeeded_count + retried_count + failed_count,
        earliest_task=min(earliest_events) if earliest_events else None,
        hours=hours,
    )


class EventSeries:
    """Base class for recording and analysing a series of events.

    This class must be inherited from and the child class must define KEY_ID.
    """

    _ROOT_KEY = "ALLIANCEAUTH_TASK_SERIES"

    def __init__(
        self,
        redis: Redis = None,
    ) -> None:
        if type(self) == EventSeries:
            raise TypeError("Can not instantiate base class.")
        if not hasattr(self, "KEY_ID"):
            raise ValueError("KEY_ID not defined")
        self._redis = cache.get_master_client() if not redis else redis
        if not isinstance(self._redis, Redis):
            raise TypeError(
                "This class requires a Redis client, but none was provided "
                "and the default Django cache backend is not Redis either."
            )

    @property
    def _key_counter(self):
        return f"{self._ROOT_KEY}_{self.KEY_ID}_COUNTER"

    @property
    def _key_sorted_set(self):
        return f"{self._ROOT_KEY}_{self.KEY_ID}_SORTED_SET"

    def add(self, event_time: dt.datetime = None) -> None:
        """Add event.

        Args:
        - event_time: timestamp of event. Will use current time if not specified.
        """
        if not event_time:
            event_time = dt.datetime.utcnow()
        id = self._redis.incr(self._key_counter)
        self._redis.zadd(self._key_sorted_set, {id: event_time.timestamp()})

    def all(self) -> List[dt.datetime]:
        """List of all known events."""
        return [
            event[1]
            for event in self._redis.zrangebyscore(
                self._key_sorted_set,
                "-inf",
                "+inf",
                withscores=True,
                score_cast_func=self._cast_scores_to_dt,
            )
        ]

    def clear(self) -> None:
        """Clear all events."""
        self._redis.delete(self._key_sorted_set)
        self._redis.delete(self._key_counter)

    def count(self, earliest: dt.datetime = None, latest: dt.datetime = None) -> int:
        """Count of events, can be restricted to given timeframe.

        Args:
        - earliest: Date of first events to count(inclusive), or -infinite if not specified
        - latest: Date of last events to count(inclusive), or +infinite if not specified
        """
        min = "-inf" if not earliest else earliest.timestamp()
        max = "+inf" if not latest else latest.timestamp()
        return self._redis.zcount(self._key_sorted_set, min=min, max=max)

    def first_event(self, earliest: dt.datetime = None) -> Optional[dt.datetime]:
        """Date/Time of first event. Returns `None` if series has no events.

        Args:
        - earliest: Date of first events to count(inclusive), or any if not specified
        """
        min = "-inf" if not earliest else earliest.timestamp()
        event = self._redis.zrangebyscore(
            self._key_sorted_set,
            min,
            "+inf",
            withscores=True,
            start=0,
            num=1,
            score_cast_func=self._cast_scores_to_dt,
        )
        if not event:
            return None
        return event[0][1]

    @staticmethod
    def _cast_scores_to_dt(score) -> dt.datetime:
        return dt.datetime.fromtimestamp(float(score), tz=utc)


class SucceededTaskSeries(EventSeries):
    """A task has succeeded."""

    KEY_ID = "SUCCEEDED"


class RetriedTaskSeries(EventSeries):
    """A task has been retried."""

    KEY_ID = "RETRIED"


class FailedTaskSeries(EventSeries):
    """A task has failed."""

    KEY_ID = "FAILED"
