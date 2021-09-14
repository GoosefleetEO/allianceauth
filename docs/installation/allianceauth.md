# Alliance Auth

This document describes how to install **Alliance Auth** from scratch.

```eval_rst
.. tip::
    If you are uncomfortable with Linux permissions follow the steps below as the root user.
```

```eval_rst
.. note::
    There are additional installation steps for activating services and apps that come with **Alliance Auth**. Please see the page for the respective service or apps in chapter :doc:`/features/index` for details.
```

## Dependencies

### Operating System

Alliance Auth can be installed on any Unix like operating system. Dependencies are provided below for two of the most popular Linux platforms: Ubuntu and CentOS. To install on your favorite flavour of Linux, identify and install equivalent packages to the ones listed here.

### Python

Alliance Auth requires Python 3.7 or higher. Ensure it is installed on your server before proceeding.

Ubuntu 1604 1804:

```eval_rst
.. note::
    Ubuntu 2004 ships with Python 3.8, No updates required.
```

```bash
add-apt-repository ppa:deadsnakes/ppa
```

```bash
apt-get update
```

```bash
apt-get install python3.7 python3.7-dev python3.7-venv
```

CentOS 7/8:

```bash
cd ~
```

```bash
sudo yum install gcc openssl-devel bzip2-devel libffi-devel wget
```

```bash
wget https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz
```

```bash
tar xvf Python-3.7.11.tgz
```

```bash
cd Python-3.7.11/
```

```bash
./configure --enable-optimizations --enable-shared
```

```bash
make altinstall
```

### Database

It's recommended to use a database service instead of SQLite. Many options are available, but this guide will use MariaDB.

```eval_rst
.. warning::
    Many Ubuntu distributions come with an older version of Maria DB, which is not compatible with **Alliance Auth**. You need Maria DB 10.3 or higher!

    For instructions on how To install a newer version of Maria DB on Ubuntu visit this page: `MariaDB Repositories <https://downloads.mariadb.org/mariadb/repositories/#distro=Ubuntu&mirror=osuosl>`_.
```

Ubuntu:

```bash
apt-get install mariadb-server mariadb-client libmysqlclient-dev
```

CentOS:

```bash
yum install mariadb-server mariadb-devel mariadb-shared mariadb
```

```eval_rst
.. note::
    If you don't plan on running the database on the same server as auth you still need to install the libmysqlclient-dev package on Ubuntu or mariadb-devel package on CentOS.
```

### Redis and Other Tools

A few extra utilities are also required for installation of packages.

Ubuntu:

```bash
apt-get install unzip git redis-server curl libssl-dev libbz2-dev libffi-dev
```

CentOS:

```bash
yum install gcc gcc-c++ unzip git redis curl bzip2-devel
```

```eval_rst
.. important::
    CentOS: Make sure Redis is running before continuing. ::

      systemctl enable redis.service
      systemctl start redis.service
```

## Database Setup

Alliance Auth needs a MySQL user account and database. Open an SQL shell with `mysql -u root -p` and create them as follows, replacing `PASSWORD` with an actual secure password:

```sql
CREATE USER 'allianceserver'@'localhost' IDENTIFIED BY 'PASSWORD';
CREATE DATABASE alliance_auth CHARACTER SET utf8mb4;
GRANT ALL PRIVILEGES ON alliance_auth . * TO 'allianceserver'@'localhost';
```

Once your database is set up, you can leave the SQL shell with `exit`.

Add timezone tables to your mysql installation:

```bash
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
```

```eval_rst
.. note::
    You may see errors when you add the timezone tables. To make sure that they were correctly added run the following commands and check for the ``time_zone`` tables::

      mysql -u root -p
      use mysql;
      show tables;
```

Close the SQL shell and secure your database server with this command:

```bash
mysql_secure_installation
```

## Auth Install

### User Account

For security and permissions, it’s highly recommended you create a separate user to install auth under. Do not log in as this account.

Ubuntu:

```bash
adduser --disabled-login allianceserver
```

CentOS:

```bash
useradd -s /bin/nologin allianceserver
```

### Virtual Environment

Create a Python virtual environment and put it somewhere convenient (e.g. `/home/allianceserver/venv/auth/`)

```bash
python3 -m venv /home/allianceserver/venv/auth/
```

```eval_rst
.. warning::
    The python3 command may not be available on all installations. Try a specific version such as ``python3.7`` if this is the case.
```

```eval_rst
.. tip::
    A virtual environment provides support for creating a lightweight "copy" of Python with their own site directories. Each virtual environment has its own Python binary (allowing creation of environments with various Python versions) and can have its own independent set of installed Python packages in its site directories. You can read more about virtual environments on the Python_ docs.
.. _Python: https://docs.python.org/3/library/venv.html
```

Activate the virtual environment with (Note the `/bin/activate` on the end of the path):

```bash
source /home/allianceserver/venv/auth/bin/activate
```

```eval_rst
.. hint::
    Each time you come to do maintenance on your Alliance Auth installation, you should activate your virtual environment first. When finished, deactivate it with the ``deactivate`` command.
```

### Eve Online SSO

You need to have a dedicated Eve SSO app for Alliance auth. Please go to [EVE Developer](https://developers.eveonline.com/applications) to create one.

For **scopes** your SSO app needs to have at least `publicData`. Additional scopes depends on which Alliance Auth apps you will be using. For convenience, we recommend adding all available ESO scopes to your SSO app. Note that Alliance Auth will always ask the users to approve specific scopes before they are used.

As **callback URL** you want to define the URL of your Alliance Auth site plus the route: `/sso/callback`. Example for a valid callback URL: `https://auth.example.com/sso/callback`

In `local.py` you will need to set `ESI_USER_CONTACT_EMAIL` to an email address to ensure that CCP has reliable contact information for you.

### Alliance Auth Project

Ensure wheel is available before continuing:

```bash
pip install wheel
```

You can install **Alliance Auth** with the following command. This will install AA and all its Python dependencies.

```bash
pip install allianceauth
```

You should also install Gunicorn now unless you want to use another WSGI server (see [Gunicorn](#gunicorn) for details):

```bash
pip install gunicorn
```

Now you need to create the application that will run the **Alliance Auth** install. Ensure you are in the allianceserver home directory by issuing:

```bash
cd /home/allianceserver
```

The following command bootstraps a Django project which will run your **Alliance Auth** instance. You can rename it from `myauth` to anything you'd like. Note that this name is shown by default as the site name but that can be changed later.

```bash
allianceauth start myauth
```

The settings file needs configuring. Edit the template at `myauth/myauth/settings/local.py`. Be sure to configure the EVE SSO and Email settings.

Django needs to install models to the database before it can start.

```bash
python /home/allianceserver/myauth/manage.py migrate
```

Now we need to round up all the static files required to render templates. Make a directory to serve them from and populate it.

```bash
mkdir -p /var/www/myauth/static
python /home/allianceserver/myauth/manage.py collectstatic
```

Check to ensure your settings are valid.

```bash
python /home/allianceserver/myauth/manage.py check
```

Finally, ensure the allianceserver user has read/write permissions to this directory before proceeding.

```bash
chown -R allianceserver:allianceserver /home/allianceserver/myauth
```

## Services

Alliance Auth needs some additional services to run, which we will set up and configure next.

### Gunicorn

To run the **Alliance Auth** website a [WSGI Server](https://www.fullstackpython.com/wsgi-servers.html) is required. For this [Gunicorn](http://gunicorn.org/) is highly recommended for its ease of configuring. It can be manually run from within your `myauth` base directory with `gunicorn --bind 0.0.0.0 myauth.wsgi` or automatically run using Supervisor.

The default configuration is good enough for most installations. Additional information is available in the [gunicorn](gunicorn.md) doc.

### Supervisor

[Supervisor](http://supervisord.org/) is a process watchdog service: it makes sure other processes are started automatically and kept running. It can be used to automatically start the WSGI server and Celery workers for background tasks. Installation varies by OS:

```eval_rst
.. note::
    Many package managers will install Supervisor 3 by default, which requires Python 2.
```

Ubuntu:

```bash
apt-get install supervisor
```

CentOS:

```bash
yum install supervisor
systemctl enable supervisord.service
systemctl start supervisord.service
```

Once installed, it needs a configuration file to know which processes to watch. Your Alliance Auth project comes with a ready-to-use template which will ensure the Celery workers, Celery task scheduler and Gunicorn are all running.

Ubuntu:

```bash
ln -s /home/allianceserver/myauth/supervisor.conf /etc/supervisor/conf.d/myauth.conf
```

CentOS:

```bash
ln -s /home/allianceserver/myauth/supervisor.conf /etc/supervisord.d/myauth.ini
```

Activate it with `supervisorctl reload`.

You can check the status of the processes with `supervisorctl status`. Logs from these processes are available in `/home/allianceserver/myauth/log` named by process.

```eval_rst
.. note::
    Any time the code or your settings change you'll need to restart Gunicorn and Celery. ::

      supervisorctl restart myauth:
```

## Webserver

Once installed, decide on whether you're going to use [NGINX](nginx.md) or [Apache](apache.md) and follow the respective guide.

Note that Alliance Auth is designed to run with web servers on HTTPS. While running on HTTP is technically possible, it is not recommended for production use, and some functions (e.g. Email confirmation links) will not work properly.

## Superuser

Before using your auth site, it is essential to create a superuser account. This account will have all permissions in Alliance Auth. It's OK to use this as your personal auth account.

```bash
python /home/allianceserver/myauth/manage.py createsuperuser
```

The superuser account is accessed by logging in via the admin site at `https://example.com/admin`.

If you intend to use this account as your personal auth account you need to add a main character. Navigate to the normal user dashboard (at `https://example.com`) after logging in via the admin site and select `Change Main`. Once a main character has been added, it is possible to use SSO to login to this account.

## Updating

Periodically [new releases](https://gitlab.com/allianceauth/allianceauth/tags) are issued with bug fixes and new features. Be sure to read the [release notes](https://gitlab.com/allianceauth/allianceauth/-/releases) which will highlight changes.

To update your install, simply activate your virtual environment and update with:

```bash
pip install --upgrade allianceauth
```

Some releases come with changes to the base settings. Update your project's settings with:

```bash
allianceauth update /home/allianceserver/myauth
```

Some releases come with new or changed models. Update your database to reflect this with:

```bash
python /home/allianceserver/myauth/manage.py migrate
```

Finally, some releases come with new or changed static files. Run the following command to update your static files folder:

```bash
python /home/allianceserver/myauth/manage.py collectstatic
```

Always restart AA, Celery and Gunicorn after updating:

```bash
supervisorctl restart myauth:
```
