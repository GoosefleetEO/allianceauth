from celery.signals import task_failure, task_retry, task_success, worker_ready

from django.conf import settings

from .event_series import FailedTaskSeries, RetriedTaskSeries, SucceededTaskSeries


def reset_counters():
    """Reset all counters for the celery status."""
    SucceededTaskSeries().clear()
    FailedTaskSeries().clear()
    RetriedTaskSeries().clear()


def is_enabled() -> bool:
    return not bool(
        getattr(settings, "ALLIANCEAUTH_DASHBOARD_TASK_STATISTICS_DISABLED", False)
    )


@worker_ready.connect
def reset_counters_when_celery_restarted(*args, **kwargs):
    if is_enabled():
        reset_counters()


@task_success.connect
def record_task_succeeded(*args, **kwargs):
    if is_enabled():
        SucceededTaskSeries().add()


@task_retry.connect
def record_task_retried(*args, **kwargs):
    if is_enabled():
        RetriedTaskSeries().add()


@task_failure.connect
def record_task_failed(*args, **kwargs):
    if is_enabled():
        FailedTaskSeries().add()
