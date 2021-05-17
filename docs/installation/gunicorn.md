# Gunicorn

[Gunicorn](http://gunicorn.org) is a Python WSGI HTTP Server for UNIX. The Gunicorn server is light on server resources, and fairly speedy.

If you find Apache's `mod_wsgi` to be a headache or want to use NGINX (or some other webserver), then Gunicorn could be for you. There are a number of other WSGI server options out there and this documentation should be enough for you to piece together how to get them working with your environment.

Check out the full [Gunicorn docs](http://docs.gunicorn.org/en/latest/index.html).

```eval_rst
.. note::
    The page contains additional steps on how to setup and configure Gunicorn that are not required for users who decide to stick with the default Gunicorn configuration as described in the main installation guide for AA.
```

## Setting up Gunicorn

```eval_rst
.. note::
    If you're using a virtual environment, activate it now. ``source /path/to/venv/bin/activate``.
```

Install Gunicorn using pip, `pip install gunicorn`.

In your `myauth` base directory, try running `gunicorn --bind 0.0.0.0:8000 myauth.wsgi`. You should be able to browse to `http://yourserver:8000` and see your Alliance Auth installation running. Images and styling will be missing, but don't worry, your web server will provide them.

Once you validate its running, you can kill the process with Ctrl+C and continue.

## Running Gunicorn with Supervisor

You should use [Supervisor](allianceauth.md#supervisor) to keep all of Alliance Auth components running (instead of using screen). You don't _have to_ but we will be using it to start and run Gunicorn so you might as well.

### Sample Supervisor config

You'll want to edit `/etc/supervisor/conf.d/myauth.conf` (or whatever you want to call the config file)

```text
[program:gunicorn]
user = allianceserver
directory=/home/allianceserver/myauth/
command=/home/allianceserver/venv/auth/bin/gunicorn myauth.wsgi --workers=3 --timeout 120
stdout_logfile=/home/allianceserver/myauth/log/gunicorn.log
stderr_logfile=/home/allianceserver/myauth/log/gunicorn.log
autostart=true
autorestart=true
stopsignal=INT
```

- `[program:gunicorn]` - Change `gunicorn` to whatever you wish to call your process in Supervisor.
- `user = allianceserver` - Change to whatever user you wish Gunicorn to run as. You could even set this as allianceserver if you wished. I'll leave the question security of that up to you.
- `directory=/home/allianceserver/myauth/` - Needs to be the path to your Alliance Auth project.
- `command=/home/allianceserver/venv/auth/bin/gunicorn myauth.wsgi --workers=3 --timeout 120` - Running Gunicorn and the options to launch with. This is where you have some decisions to make, we'll continue below.

#### Gunicorn Arguments

See the [Commonly Used Arguments](http://docs.gunicorn.org/en/latest/run.html#commonly-used-arguments) or [Full list of settings](http://docs.gunicorn.org/en/stable/settings.html) for more information.

##### Where to bind Gunicorn to

What address are you going to use to reference it? By default, without a bind parameter, Gunicorn will bind to `127.0.0.1:8000`. This might be fine for your application. If it clashes with another application running on that port you will need to change it. I would suggest using UNIX sockets too, if you can.

For UNIX sockets add `--bind=unix:/run/allianceauth.sock` (or to a path you wish to use). Remember that your web server will need to be able to access this socket file.

For a TCP address add `--bind=127.0.0.1:8001` (or to the address/port you wish to use, but I would strongly advise against binding it to an external address).

Whatever you decide to use, remember it because we'll need it when configuring your webserver.

##### Number of workers

By default Gunicorn will spawn only one worker. The number you set this to will depend on your own server environment, how many visitors you have etc. Gunicorn suggests `(2 x $num_cores) + 1` for the number of workers. So for example if you have 2 cores you want 2 x 2 + 1 = 5 workers. See [here](https://docs.gunicorn.org/en/stable/design.html#how-many-workers) for the official discussion on this topic.

Change it by adding `--workers=5` to the command.

##### Running with a virtual environment

If you're running with a virtual environment, you'll need to add the path to the `command=` config line.

e.g. `command=/path/to/venv/bin/gunicorn myauth.wsgi`

The example config is using the myauth venv from the main installation guide: `command=/home/allianceserver/venv/auth/bin/gunicorn myauth.wsgi`

### Starting via Supervisor

Once you have your configuration all sorted, you will need to reload your supervisor config `service supervisor reload` and then you can start the Gunicorn server via `supervisorctl start myauth:gunicorn` (or whatever you renamed it to). You should see something like the following `myauth-gunicorn: started`. If you get some other message, you'll need to consult the Supervisor log files, usually found in `/var/log/supervisor/`.

## Configuring your webserver

Any web server capable of proxy passing should be able to sit in front of Gunicorn. Consult their documentation armed with your `--bind=` address and you should be able to find how to do it relatively easy.

## Restarting Gunicorn

In the past when you made changes you restarted the entire Apache server. This is no longer required. When you update or make configuration changes that ask you to restart Apache, instead you can just restart Gunicorn:

`supervisorctl restart gunicorn`, or the service name you chose for it.
