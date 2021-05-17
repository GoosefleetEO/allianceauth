# Celery

```eval_rst
.. hint::
    Most tunings will require a change to your supervisor configuration in your `supervisor.conf` file. Note that you need to restart the supervisor daemon in order for any changes to take effect. And before restarting the daemon you may want to make sure your supervisors stop gracefully:(Ubuntu):

    ::

      supervisor stop myauth:
      systemctl supervisor restart
```

## Task Logging

By default task logging is deactivated. Enabling task logging allows you to monitor what tasks are doing in addition to getting all warnings and error messages. To enable info logging for tasks add the following to the command configuration of your worker in the `supervisor.conf` file:

```text
-l info
```

Full example:

```text
command=/home/allianceserver/venv/auth/bin/celery -A myauth worker -l info
```

## Protection against memory leaks

Celery workers often have memory leaks and will therefore grow in size over time. While the Alliance Auth team is working hard to ensure Auth is free of memory leaks some may still be cause by bugs in different versions of libraries or community apps. It is therefore good practice to enable features that protect against potential memory leaks.

There are two ways to protect against memory leaks:

- Worker
- Supervisor

### Worker

Celery workers can be configured to automatically restart if they grow above a defined memory threshold. Restarts will be graceful, so current tasks will be allowed to complete before the restart happens.

To add protection against memory leaks add the following to the command configuration of your worker in the `supervisor.conf` file. This sets the upper limit to 256MB.

```text
--max-memory-per-child 262144
```

Full example:

```text
command=/home/allianceserver/venv/auth/bin/celery -A myauth worker --max-memory-per-child 262144
```

```eval_rst
.. hint::
    The 256 MB limit is just an example and should be adjusted to your system configuration. We would suggest to not go below 128MB though, since new workers start with around 80 MB already. Also take into consideration that this value is per worker and that you properly have more than one worker running in your system (if your workers run as processes, which is the default).
```

```eval_rst
.. warning::
    The ``max-memory-per-child`` parameter only works when workers run as processes (which is the default). It does not work for threads.
```

```eval_rst
.. note::
    Alternatively, you can also limit the number of runs per worker until a restart is performed with the worker parameter ``max-tasks-per-child``. This can also protect against memory leaks if you set the threshold is low enough. However, it is less precise since than using ``max-memory-per-child``.
```

See also the [official Celery documentation](https://docs.celeryproject.org/en/stable/userguide/workers.html#max-memory-per-child-setting) for more information about these two worker parameters.

### Supervisor

It is also possible to configure your supervisor to monitor and automatically restart programs that exceed a memory threshold.

This is not a built in feature and requires the 3rd party extension [superlance](https://superlance.readthedocs.io/en/latest/), which includes a set of plugin utilities for supervisor. The one that watches memory consumption is [memmon](https://superlance.readthedocs.io/en/latest/memmon.html).

To setup install superlance into your venv with:

```bash
pip install superlance
```

You can then add `memmon` to your `supervisor.conf`. Here is an example setup with a worker that runs with gevent:

```text
[eventlistener:memmon]
command=/home/allianceserver/venv/auth/bin/memmon -p worker=512MB
directory=/home/allianceserver/myauth
events=TICK_60
```

This setup will check the memory consumption of the program "worker" every 60 secs and automatically restart it if is goes above 512 MB. Note that it will use the stop signal configured in supervisor, which is `TERM` by default. `TERM` will cause a "warm shutdown" of your worker, so all currently running tasks are completed before the restart.

Again, the 512 MB is just an example and should be adjusted to fit your system configuration.

## Increasing task throughput

Celery tasks are designed to run concurrently, so one obvious way to increase task throughput is run more tasks in parallel.

### Concurrency

This can be achieved by the setting the concurrency parameter of the celery worker to a higher number. For example:

```text
--concurrency=4
```

However, there is a catch: In the default configuration each worker will spawn as it's own process. So increasing the number of workers will increase both CPU load and memory consumption in your system.

The recommended number of workers is one per core, which is what you get automatically with the default configuration. Going beyond that can quickly reduce you overall system performance. i.e. the response time for Alliance Auth or other apps running on the same system may take a hit while many tasks are running.

```eval_rst
.. hint::
    The optimal number will hugely depend on your individual system configuration and you may want to experiment with different settings to find the optimal. One way to generate task load and verify your configuration is to run a model update with the following command:

    ::

      celery -A myauth call allianceauth.eveonline.tasks.run_model_update

```

### Processes vs. Threads

A better way to increase concurrency without impacting is to switch from processes to threads for celery workers. In general celery workers perform better with processes when tasks are primarily CPU bound. And they perform better with threads when tasks that are primarily I/O bound.

Alliance Auth tasks are primarily I/O bound (most tasks are fetching data from ESI and/or updating the local database), so threads are clearly the better choice for Alliance Auth. However, there is a catch. Celery's out-of-the-box support for threads is limited and additional packages and configurations is required to make it work. Nonetheless, the performance gain - especially in smaller systems - is significant, so it may well be worth the additional configuration complexity.

```eval_rst
.. warning::
    One important feature that no longer works with threads is the worker parameter ``--max-memory-per-child`` that protects against memory leaks. But you can alternatively use supervisor_ to monitor and restart your workers.
```

See also the also [this guide](https://www.distributedpython.com/2018/10/26/celery-execution-pool/) on more information about how to configure the execution pool for workers.

### Setting up for threads

First, you need to install a threads packages. Celery supports both gevent and eventlet. We will go with gevent, since it's newer and better supported. Should you encounter any issues with gevent, you may want to try eventlet.

To install gevent make sure you are in your venv and install the following:

```bash
pip install gevent
```

Next we need to reconfigure the workers to use gevent threads. For that add the following parameters to your worker config:

```text
--pool=gevent --concurrency=10
```

Full example:

```text
command=/home/allianceserver/venv/auth/bin/celery -A myauth worker --pool=gevent --concurrency=10
```

Make sure to restart supervisor to activate the changes.

```eval_rst
.. hint::
    The optimal number of concurrent workers will be different for every system and we recommend experimenting with different figures to find the optimal for your system. Note, that the example of 10 threads is conservative and should work even with smaller systems.
```
