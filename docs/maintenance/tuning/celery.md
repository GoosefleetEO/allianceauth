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

```eval_rst
.. hint::
    The 256 MB limit is just an example and should be adjusted to your system configuration. We would suggest to not go below 128MB though, since new workers start with around 80 MB already. Also take into consideration that this value is per worker and that you may have more than one worker running in your system.
```


### Supervisor

It is also possible to configure your supervisor to monitor and automatically restart programs that exceed a memory threshold.

This is not a built in feature and requires the 3rd party extension [superlance](https://superlance.readthedocs.io/en/latest/), which includes a set of plugin utilities for supervisor. The one that watches memory consumption is [memmon](https://superlance.readthedocs.io/en/latest/memmon.html).

To setup install superlance into your venv with:

```bash
pip install superlance
```

You can then add `memmon` to your `supervisor.conf`:

```text
[eventlistener:memmon]
command=/home/allianceserver/venv/auth/bin/memmon -p worker=256MB
directory=/home/allianceserver/myauth
events=TICK_60
```

This setup will check the memory consumption of the program "worker" every 60 secs and automatically restart it if is goes above 256 MB. Note that it will use the stop signal configured in supervisor, which is `TERM` by default. `TERM` will cause a "warm shutdown" of your worker, so all currently running tasks are completed before the restart.

Again, the 256 MB is just an example and should be adjusted to fit your system configuration.

## Increasing task throughput

Celery tasks are designed to run concurrently, so one obvious way to increase task throughput is run more tasks in parallel. The default celery worker configuration will allow either of these options to be configured out of the box.

### Extra Worker Threads

The easiest way to increate throughput can be achieved by increasing the `numprocs` parameter of the suprvisor process. For example:

```text
[program:worker]
...
numprocs=2
process_name=%(program_name)s_%(process_num)02d
...
```

This number will be multiplied by your concurrency setting,

```
numprocs * concurency = workers
```

increasing this number will require a modification to the memmon settings as each `numproc` worker will get a unique name for example with `numproc=3`

```text
[eventlistener:memmon]
...
command=... -p worker_00=256MB -p worker_01=256MB -p worker_02=256MB
...
```

```eval_rst
.. hint::
    You will want to experiment with different settings to find the optimal. One way to generate task load and verify your configuration is to run a model update with the following command:

    ::

      celery -A myauth call allianceauth.eveonline.tasks.run_model_update

```

### Concurrency

This can be achieved by the setting the concurrency parameter of the celery worker to a higher number. For example:

```text
--concurrency=10
```

```eval_rst
.. hint::
    The optimal number will hugely depend on your individual system configuration and you may want to experiment with different settings to find the optimal. One way to generate task load and verify your configuration is to run a model update with the following command:

    ::

      celery -A myauth call allianceauth.eveonline.tasks.run_model_update

```

```eval_rst
.. hint::
    The optimal number of concurrent workers will be different for every system and we recommend experimenting with different figures to find the optimal for your system. Note, that the example of 10 threads is conservative and should work even with smaller systems.
```
