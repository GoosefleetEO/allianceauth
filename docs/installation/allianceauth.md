# Alliance Auth

This document describes how to install **Alliance Auth** from scratch.

```eval_rst
.. note::
    There are additional installation steps for activating services and apps that come with **Alliance Auth**. Please see the page for the respective service or apps in chapter :doc:`/features/index` for details.
```

## Dependencies

### Operating Systems

Alliance Auth can be installed on any in-support *nix operating system.

Our install documentation targets the following operating systems.

- Ubuntu 18.04
- Ubuntu 20.04
- Ubuntu 22.04
- Centos 7
- CentOS Stream 8
- CentOS Stream 9

To install on your favorite flavour of Linux, identify and install equivalent packages to the ones listed here.

### OS Maintenance

It is recommended to ensure your OS is fully up to date before proceeding. We may also add Package Repositories here, used later in the documentation.

Ubuntu 1804, 2004, 2204:

```bash
sudo apt-get update
```

```bash
sudo apt-get upgrade
```

```bash
sudo do-dist-upgrade
```

CentOS 7:

```bash
yum install epel-release
```

```bash
sudo yum upgrade
```

CentOS Stream 8:

```bash
sudo dnf config-manager --set-enabled powertools
```

```bash
sudo dnf install epel-release epel-next-release
```

```bash
sudo yum upgrade
```

CentOS Stream 9:

```bash
sudo dnf config-manager --set-enabled crb
```

```bash
dnf install epel-release epel-next-release
```

```bash
sudo yum upgrade
```

### Python

Install Python 3.10 and related tools on your system.

Ubuntu 1804, 2004:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
```

```bash
sudo apt-get update
```

```bash
sudo apt-get install python3.10 python3.10-dev python3.10-venv
```

Ubuntu 2204:

```eval_rst
.. note::
    Ubuntu 2204 ships with Python 3.10 already, but some important tools are missing in the default installation.
```

```bash
sudo apt-get install python3.10-dev python3.10-venv
```

CentOS 7:
We need to build Python from source

Centos Stream 8/9:

```eval_rst
.. note::
    A Python 3.9 Package is available for Stream 8 and 9. You _may_ use this instead of building your own package. But our documentation will assume Python3.10 and you may need to substitute as necessary
    sudo dnf install python39 python39-devel
```

```bash
cd ~
```

```bash
sudo yum install gcc openssl-devel bzip2-devel libffi-devel wget
```

```bash
wget https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tgz
```

```bash
tar xvf Python-3.10.5.tgz
```

```bash
cd Python-3.10.5/
```

```bash
./configure --enable-optimizations --enable-shared
```

```bash
sudo make altinstall
```

### Database

It's recommended to use a database service instead of SQLite. Many options are available, but this guide will use MariaDB.

```eval_rst
.. note::
    Ubuntu distributions prior to 20.04 come with an older version of Maria DB, which is not compatible with **Alliance Auth**. You need Maria DB 10.3 or higher!
    For 20.04 we still recommend to install Maria DB from the link below in order to get the newest stable version.
    For 22.04 we recommend installing from the default Ubuntu distro, since it comes with the newest stable version.
```

Ubuntu 1804, 2004:

```eval_rst
.. warning::
    Please follow these steps to update MariaDB
    https://mariadb.org/download/?t=repo-config&d=20.04+%22focal%22&v=10.6&r_m=osuosl
```

Ubuntu 1804, 2004, 2204

```bash
sudo apt-get install mariadb-server mariadb-client libmysqlclient-dev
```

CentOS 7:

```eval_rst
.. warning::
    Please follow these steps to update MariaDB
    https://mariadb.org/download/?t=repo-config&d=CentOS+7+%28x86_64%29&v=10.6&r_m=osuosl
```

```bash
sudo yum install MariaDB-server MariaDB-client MariaDB-devel MariaDB-shared
```

CentOS Stream 8/9:

```eval_rst
.. note::
    We recommend using the built in AppStream, as they are maintained by CentOS. Currently an AppStream is not available for 10.6
```

```bash
sudo dnf module enable mariadb:10.5
```

```bash
sudo dnf install mariadb mariadb-server mariadb-devel
```

```bash
sudo systemctl enable mariadb
```

```bash
sudo systemctl start mariadb
```

```eval_rst
.. important::
    If you don't plan on running the database on the same server as auth you still need to install the ``libmysqlclient-dev`` package on Ubuntu or ``mariadb-devel`` package on CentOS.
```

### Redis and Other Tools

A few extra utilities are also required for installation of packages.

Ubuntu 1804, 2004, 2204:

```bash
sudo apt-get install unzip git redis-server curl libssl-dev libbz2-dev libffi-dev build-essential pkg-config
```

CentOS 7:

```bash
sudo yum install gcc gcc-c++ unzip git redis curl bzip2-devel openssl-devel libffi-devel wget pkg-config
```

```bash
sudo systemctl enable redis.service
```

```bash
sudo systemctl start redis.service
```

CentOS Stream 8, Stream 9:

```bash
sudo dnf install gcc gcc-c++ unzip git redis curl bzip2-devel openssl-devel libffi-devel wget
```

```bash
sudo systemctl enable redis.service
```

```bash
sudo systemctl start redis.service
```

## Database Setup

Alliance Auth needs a MySQL user account and database. Open an SQL shell with

```bash
sudo mysql -u root
```

and create them as follows, replacing `PASSWORD` with an actual secure password:

```sql
CREATE USER 'allianceserver'@'localhost' IDENTIFIED BY 'PASSWORD';
CREATE DATABASE alliance_auth CHARACTER SET utf8mb4;
GRANT ALL PRIVILEGES ON alliance_auth . * TO 'allianceserver'@'localhost';
```

Once your database is set up, you can leave the SQL shell with `exit`.

Add timezone tables to your mysql installation:

```bash
mysql_tzinfo_to_sql /usr/share/zoneinfo | sudo mysql -u root mysql
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

Ubuntu 1804, 2004, 2204:

```bash
sudo adduser --disabled-login allianceserver
```

CentOS 7, Stream 8, Stream 9:

```bash
sudo useradd -s /bin/bash allianceserver
```

```bash
sudo passwd -l allianceserver
```

### Prepare Directories

```bash
sudo mkdir -p /var/www/myauth/static
```

```bash
sudo chown -R allianceserver:allianceserver /var/www/myauth/static/
```

```eval_rst
.. note::
    When installing and performing maintenance on Alliance Auth, using the allianceserver user will greatly simplify permission management::

      sudo su allianceserver
```

### Virtual Environment

Switch to the allianceserver user.

```bash
sudo su allianceserver
```

And switch to it's home directory:

```bash
cd
```

```eval_rst
.. note::
    In general using the allianceserver user will greatly simplify permission management, when installing and performing maintenance on Alliance Auth.
```

Create a Python virtual environment and put it somewhere convenient (e.g. `/home/allianceserver/venv/auth/`)

```eval_rst
.. note::
    Your python3.x command/version may vary depending on your installed python version.
```

```bash
python3.10 -m venv /home/allianceserver/venv/auth/
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

### Alliance Auth Project

```eval_rst
.. warning::
    Before installing any Python packages please double-check that you have activated in the virtual environment. This is usually indicated by your command line in the terminal starting with: `(auth)`.
```

#### Install Python packages

Update & install basic tools before installing further Python packages:

```bash
pip install -U pip setuptools wheel
```

You can install **Alliance Auth** with the following command. This will install AA, AA's Python dependencies, superlance for memory monitoring and gunicorn as a wsgi server

```bash
pip install allianceauth superlance gunicorn
```

#### Create Alliance Auth project

Now you need to create the Django project that will run **Alliance Auth**. Ensure you are in the allianceserver home directory by issuing:

```bash
cd /home/allianceserver
```

The following command bootstraps a Django project which will run your **Alliance Auth** instance. You can rename it from `myauth` to anything you'd like. Note that this name is shown by default as the site name but that can be changed later.

```bash
allianceauth start myauth
```

#### Update settings

Your settings file needs configuring:

```bash
nano myauth/myauth/settings/local.py
```

**Be sure to configure:**

- Your site URL as `SITE_URL`
- The database user account setup from earlier in [Database Setup](#database-setup)
- `ESI_SSO_CLIENT_ID`, `ESI_SSO_CLIENT_SECRET` from the EVE Online Developers Portal from earlier in [Eve Online SSO](#eve-online-sso)
- `ESI_USER_CONTACT_EMAIL` to an email address to ensure that CCP has reliable contact information for you
- Valid email server settings

#### Install database & static files

Django needs to setup the database before it can start.

```bash
python /home/allianceserver/myauth/manage.py migrate
```

Now we need to round up all the static files required to render templates. Make a directory to serve them from and populate it.

```bash
python /home/allianceserver/myauth/manage.py collectstatic --noinput
```

Check to ensure your settings are valid.

```bash
python /home/allianceserver/myauth/manage.py check
```

```eval_rst
.. hint::
    If you are using root, ensure the allianceserver user has read/write permissions to this directory before proceeding::

      chown -R allianceserver:allianceserver /home/allianceserver/myauth
```

#### Setup superuser

Before using your auth site, it is essential to create a superuser account. This account will have all permissions in Alliance Auth. It's OK to use this as your personal auth account.

```bash
python /home/allianceserver/myauth/manage.py createsuperuser
```

Once your install is complete, the superuser account is accessed by logging in via the admin site at `https://example.com/admin`.

If you intend to use this account as your personal auth account you need to add a main character. Navigate to the normal user dashboard (at `https://example.com`) after logging in via the admin site and select `Change Main`. Once a main character has been added, it is possible to use SSO to login to this account.

## Services

Alliance Auth needs some additional services to run, which we will set up and configure next.

### Gunicorn

To run the **Alliance Auth** website a [WSGI Server](https://www.fullstackpython.com/wsgi-servers.html) is required. For this [Gunicorn](http://gunicorn.org/) is highly recommended for its ease of configuring. It can be manually run from within your `myauth` base directory with `gunicorn --bind 0.0.0.0 myauth.wsgi` or automatically run using Supervisor.

The default configuration is good enough for most installations. Additional information is available in the [gunicorn](gunicorn.md) doc.

### Supervisor

[Supervisor](http://supervisord.org/) is a process watchdog service: it makes sure other processes are started automatically and kept running. It can be used to automatically start the WSGI server and Celery workers for background tasks.

```eval_rst
.. note::
    You will need to exit the allianceserver user back to a user with sudo capabilities to install supervisor::

      exit
```

Ubuntu 1804, 2004, 2204:

```bash
sudo apt-get install supervisor
```

CentOS 7:

```bash
sudo dnf install supervisor
```

```bash
sudo systemctl enable supervisord.service
```

```bash
sudo systemctl start supervisord.service
```

CentOS Stream 8, Stream 9:

```bash
sudo dnf install supervisor
```

```bash
sudo systemctl enable supervisord.service
```

```bash
sudo systemctl start supervisord.service
```

Once installed, it needs a configuration file to know which processes to watch. Your Alliance Auth project comes with a ready-to-use template which will ensure the Celery workers, Celery task scheduler and Gunicorn are all running.

Ubuntu 1804, 2004:

```bash
ln -s /home/allianceserver/myauth/supervisor.conf /etc/supervisor/conf.d/myauth.conf
```

CentOS:

```bash
sudo ln -s /home/allianceserver/myauth/supervisor.conf /etc/supervisord.d/myauth.ini
```

Activate it with `sudo supervisorctl reload`.

You can check the status of the processes with `sudo supervisorctl status`. Logs from these processes are available in `/home/allianceserver/myauth/log` named by process.

```eval_rst
.. note::
    Any time the code or your settings change you'll need to restart Gunicorn and Celery. ::

      sudo supervisorctl restart myauth:
```

## Web server

Once installed, decide on whether you're going to use [NGINX](nginx.md) or [Apache](apache.md) and follow the respective guide.

Note that Alliance Auth is designed to run with web servers on HTTPS. While running on HTTP is technically possible, it is not recommended for production use, and some functions (e.g. Email confirmation links) will not work properly.

## Updating

Periodically [new releases](https://gitlab.com/allianceauth/allianceauth/tags) are issued with bug fixes and new features. Be sure to read the [release notes](https://gitlab.com/allianceauth/allianceauth/-/releases) which will highlight changes.

To update your install, swap to your allianceserver user

```bash
sudo su allianceserver
```

Activate your virtual environment

```bash
source /home/allianceserver/venv/auth/bin/activate
```

and update with:

```bash
pip install -U allianceauth
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
python /home/allianceserver/myauth/manage.py collectstatic --noinput
```

Always restart AA, Celery and Gunicorn after updating:

```bash
supervisorctl restart myauth:
```
