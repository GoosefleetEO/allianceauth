# Celery FAQ

**Alliance Auth** uses Celery for asynchronous task management. This page aims to give developers some guidance on how to use Celery when developing apps for Alliance Auth.

For a complete documentation of Celery please refer to the [official Celery documentation](http://docs.celeryproject.org/en/latest/index.html).

## When should I use Celery in my app?

There are two main cases for using celery. Long duration of a process and recurrence of a process.

### Duration

Alliance Auth is an online web application and as such the user expects fast and immediate responses to any of his clicks or actions. Same as with any other good web site. Good response times are measures in ms and a user will perceive everything that takes longer than 1 sec as an interruption of his flow of thought (see also [Response Times: The 3 Important Limits](https://www.nngroup.com/articles/response-times-3-important-limits/)).

As a rule of thumb we therefore recommend to use celery tasks for every process that can take longer than 1 sec to complete (also think about how long your process might take with large amounts of data).

```eval_rst
.. note::
   Another solution for dealing with long response time in particular when loading pages is to load parts of a page asynchronously, for example with AJAX.
```

### Recurrence

Another case for using celery tasks is when you need recurring execution of tasks. For example you may want to update the list of characters in a corporation from ESI every hour.

These are called periodic tasks and Alliance Auth uses [celery beat](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html) to implement them.

## What is a celery task?

For the most part a celery task is a Python functions that is configured to be executed asynchronously and controlled by Celery. Celery tasks can be automatically retried, executed periodically, executed in work flows and much more. See the [celery docs](https://docs.celeryproject.org/en/latest/userguide/tasks.html) for a more detailed description.

## How should I use Celery in my app?

Please use the following approach to ensure your tasks are working properly with Alliance Auth:

- All tasks should be defined in a module of your app's package called `tasks.py`
- Every task is a Python function with has the `@shared_task` decorator.
- Task functions and the tasks module should be kept slim, just like views by mostly utilizing business logic defined in your models/managers.
- Tasks should always have logging, so their function and potential errors can be monitored properly

Here is an example implementation of a task:

```Python
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def example():
    logger.info('example task started')
```

This task can then be started from any another Python module like so:

```Python
from .tasks import example

example.delay()
```

## How should I use celery tasks in the UI?

There is a well established pattern for integrating asynchronous processes in the UI, for example when the user asks your app to perform a longer running action:

1. Notify the user immediately (with a Django message) that the process for completing the action has been started and that he will receive a report once completed.

2. Start the celery task

3. Once the celery task is completed it should send a notification containing the result of the action to the user. It's important to send that notification also in case of errors.

## Can I use long running tasks?

Long running tasks are possible, but in general Celery works best with short running tasks. Therefore we strongly recommend to try and break down long running tasks into smaller tasks if possible.

If contextually possible try to break down your long running task in shorter tasks that can run in parallel.

However, many long running tasks consist of several smaller processes that need to run one after the other. For example you may have a loop where you perform the same action on hundreds of objects. In those cases you can define each of the smaller processes as it's own task and then link them together, so that they are run one after the other. That is called chaining in Celery and is the preferred approach for implementing long running processes.

Example implementation for a celery chain:

```Python
import logging
from celery import shared_task, chain

logger = logging.getLogger(__name__)


@shared_task
def example():
    logger.info('example task')

@shared_task
def long_runner():
    logger.info('started long runner')
    my_tasks = list()
    for _ in range(10):
        task_signature = example.si()
        my_task.append(task_signature)

    chain(my_tasks).delay()
```

In this example we fist add 10 example tasks that need to run one after the other to a list. This can be done by creating a so called signature for a task. Those signature are a kind of wrapper for tasks and can be used in various ways to compose work flow for tasks.

The list of task signatures is then converted to a chain and started asynchronously.

```eval_rst
.. hint::
   In our example we use ``si()``, which is a shortcut for "immutable signatures" and prevents us from having to deal with result sharing between tasks.

   For more information on signature and work flows see the official documentation on `Canvas <https://docs.celeryproject.org/en/latest/userguide/canvas.html>`_.

   In this context please note that Alliance Auth currently only supports chaining, because all other variants require a so called results back, which Alliance Auth does not have.
```

## How can I define periodic tasks for my app?

Periodic tasks are normal celery tasks which are added the scheduler for periodic execution. The convention for defining periodic tasks for an app is to define them in the local settings. So user will need to add those settings manually to his local settings during the installation process.

Example setting:

```Python
CELERYBEAT_SCHEDULE['structures_update_all_structures'] = {
    'task': 'structures.tasks.update_all_structures',
    'schedule': crontab(minute='*/30'),
}
```

- `structures_update_all_structures` is the name of the scheduling entry. You can chose any name, but the convention is name of your app plus name of the task.

- `'task'`: Name of your task (full path)
- `'schedule'`: Schedule definition (see Celery documentation on [Periodic Tasks](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html) for details)

## How can I use priorities for tasks?

In Alliance Auth we have defined task priorities from 0 - 9 as follows:

```eval_rst
    ====== ========= ===========
    Number Priority  Description
    ====== ========= ===========
    0      Reserved  Reserved for Auth and may not be used by apps
    1, 2   Highest   Needs to run right now
    3, 4   High      needs to run as soon as practical
    5      Normal    default priority for most tasks
    6, 7   Low       needs to run soonish, but is less urgent than most tasks
    8, 9   Lowest    not urgent, can be run whenever there is time
    ====== ========= ===========
```

```eval_rst
.. warning::
   Please make sure to use task priorities with care and especially do not use higher priorities without a good reason. All apps including Alliance Auth share the same task queues, so using higher task priorities excessively can potentially prevent more important tasks (of other apps) from completing on time.

   You also want to make sure to run use lower priorities if you have a large amount of tasks or long running tasks, which are not super urgent. (e.g. the regular update of all Eve characters from ESI runs with priority 7)
```

```eval_rst
.. hint::
   If no priority is specified all tasks will be started with the default priority, which is 5.
```

To run a task with a different priority you need to specify it when starting it.

Example for starting a task with priority 3:

```Python
example.apply_async(priority=3)
```

```eval_rst
.. hint::
   For defining a priority to tasks you can not use the convenient shortcut ``delay()``, but instead need to start a task with ``apply_async()``, which also requires you to pass parameters to your task function differently. Please check out the `official docs <https://docs.celeryproject.org/en/stable/reference/celery.app.task.html#celery.app.task.Task.apply_async>`_ for details.
```

## What special features should I be aware of?

Every Alliance Auth installation will come with a couple of special celery related features "out-of-the-box" that you can make use of in your apps.

### celery-once

Celery-once is a celery extension "that allows you to prevent multiple execution and queuing of celery tasks". What that means is that you can ensure that only one instance of a celery task runs at any given time. This can be useful for example if you do not want multiple instances of you task to talk to the same external service at the same time.

We use a custom backend for celery_once in Alliance Auth defined [here](https://gitlab.com/allianceauth/allianceauth/-/blob/master/allianceauth/services/tasks.py#L14)
You can import it for use like so:

```Python
from allianceauth.services.tasks import QueueOnce
```

An example of AllianceAuth's use within the `@sharedtask` decorator, can be seen [here](https://gitlab.com/allianceauth/allianceauth/-/blob/master/allianceauth/services/modules/discord/tasks.py#L62) in the discord module
You can use it like so:

```Python
@shared_task(bind=True, name='your_modules.update_task', base=QueueOnce)
```

Please see the [official documentation](hhttps://pypi.org/project/celery_once/) of celery-once for details.

### task priorities

Alliance Auth is using task priorities to enable priority based scheduling of task execution. Please see [How can I use priorities for tasks?](#how-can-i-use-priorities-for-tasks) for details.
