# Gunicorn

## Number of workers

The default installation will have 3 workers configured for Gunicorn. This will be fine on most system, but if your system as more than one core than you might want to increase the number of workers to get better response times. Note that more workers will also need more RAM though.

The number you set this to will depend on your own server environment, how many visitors you have etc. Gunicorn suggests `(2 x $num_cores) + 1` for the number of workers. So for example if you have 2 cores you want 2 x 2 + 1 = 5 workers. See [here](https://docs.gunicorn.org/en/stable/design.html#how-many-workers) for the official discussion on this topic.

For example to get 5 workers change the setting `--workers=5` in your `supervisor.conf` file and then reload the supervisor with the following command to activate the change (Ubuntu):

```bash
systemctl restart supervisor
```
