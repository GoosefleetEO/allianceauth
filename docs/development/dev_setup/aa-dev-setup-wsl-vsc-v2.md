# Development on Windows 10 with WSL and Visual Studio Code

This document describes step-by-step how to setup a complete development environment for Alliance Auth apps on Windows 10 with Windows Subsystem for Linux (WSL) and Visual Studio Code.

The main benefit of this setup is that it runs all services and code in the native Linux environment (WSL) and at the same time can be full controlled from within a comfortable Windows IDE (Visual Studio Code) including code debugging.

In addition all tools described in this guide are open source or free software.

```eval_rst
.. hint::
    This guide is meant for development purposes only and not for installing AA in a production environment. For production installation please see chapter **Installation**.
```

## Overview

The development environment consists of the following components:

- Visual Studio Code with Remote WSL and Python extension
- WSL with Ubuntu (18.04. LTS or higher)
- Python environment on WSL (3.8 or higher)
- MySQL server on WSL
- Redis on WSL
- Alliance Auth on WSL
- Celery on WSL

We will use the build-in Django development web server, so we don't need to setup a WSGI server or a web server.

```eval_rst
.. note::
    This setup works with both WSL 1 and WSL 2. However, due to the significantly better performance we recommend WSL 2.
```

## Requirement

The only requirement is a PC with Windows 10 and Internet connection in order to download the additional software components.

## Installing Windows apps

### Windows Subsystem for Linux

- Install from here: [Microsoft docs](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

- Choose Ubuntu 18.04. LTS or higher

### Visual Studio Code

- Install from here: [VSC Download](https://code.visualstudio.com/Download)

- Open the app and install the following VSC extensions:

- Remote WSL

- Connect to WSL. This will automatically install the VSC server on the VSC server for WSL

- Once connected to WSL install the Python extension on the WSL side

## Setting up WSL / Linux

Open a WSL bash and update all software packets:

```bash
sudo apt update && sudo apt upgrade -y
```

### Install Tools

```bash
sudo apt-get install build-essential
sudo apt-get install gettext
```

### Install Python

Next we need to install Python and related development tools.

```eval_rst
.. hint::
    To check your system's Python 3 version you can enter: ``python3 --version``
```

```eval_rst
.. note::
    Should your Ubuntu come with a newer version of Python we recommend to still setup your dev environment with the oldest Python 3 version currently supported by AA (e.g Python 3.8 at this time of writing) to ensure your apps are compatible with all current AA installations
    You an check out this `page <https://askubuntu.com/questions/682869/how-do-i-install-a-different-python-version-using-apt-get/1195153>`_ on how to install additional Python versions on Ubuntu.
```

Use the following command to install Python 3 with all required libraries with the default version:

```bash
sudo apt-get install python3 python3-dev python3-venv python3-setuptools python3-pip python-pip
```

### Install redis and other tools

```bash
sudo apt-get install unzip git redis-server curl libssl-dev libbz2-dev libffi-dev
```

Start redis

```bash
sudo redis-server --daemonize yes
```

## Installing the DBMS

Install MySQL and required libraries with the following command:

```bash
sudo apt-get install mysql-server mysql-client libmysqlclient-dev
```

```eval_rst
.. note::
    We chose to use MySQL instead of MariaDB, because the standard version of MariaDB that comes with this Ubuntu distribution will not work with AA.
```

We need to apply a permission fix to mysql or you will get a warning with every startup:

```bash
sudo usermod -d /var/lib/mysql/ mysql
```

Start the mysql server

```bash
sudo service mysql start
```

Create database and user for AA

```bash
sudo mysql -u root
```

```sql
CREATE DATABASE aa_dev CHARACTER SET utf8mb4;
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'YOUR-PASSWORD';
GRANT ALL PRIVILEGES ON * . * TO 'admin'@'localhost';
FLUSH PRIVILEGES;
exit;
```

Add timezone info to mysql:

```bash
sudo mysql_tzinfo_to_sql /usr/share/zoneinfo | sudo mysql -u root mysql
```

```eval_rst
.. note::
    If your WSL does not have an init.d service, it will not automatically start your services such as MySQL and Redis when you boot your Windows machine and you have to manually start them. For convenience we recommend putting these commands in a bash script. Here is an example:

    ::

        #/bin/bash
        # start services for AA dev
        sudo service mysql start
        sudo redis-server --daemonize yes

```

### Setup dev folder on WSL

Setup your folders on WSL bash for your dev project. Our approach will setup one AA project with one venv and multiple apps running under the same AA project, but each in their own folder and git.

A good location for setting up this folder structure is your home folder or a subfolder of your home:

```text
~/aa-dev
|- venv
|- myauth
|- my_app_1
|- my_app_2
|- ...
```

Following this approach you can also setup additional AA projects, e.g. aa-dev-2, aa-dev-3 if needed.

Create the root folder `aa-dev`.

```eval_rst
.. hint::
    The folders `venv` and `myauth` will be created automatically in later steps. Please do not create them manually as this would lead to errors.
```

### Setup virtual Python environment for aa-dev

Create the virtual environment. Run this in your aa-dev folder:

```bash
python3 -m venv venv
```

And activate your venv:

```bash
source venv/bin/activate
```

### Install and update basic Python packages

```bash
pip install -U pip setuptools wheel
```

## Installing Alliance Auth

### Install and create AA instance

```bash
pip install allianceauth
```

Now we are ready to setup our AA instance. Make sure to run this command in your aa-dev folder:

```bash
allianceauth start myauth
```

Next we will setup our VSC project for aa-dev by starting it directly from the WSL bash:

```bash
code .
```

First you want to make sure exclude the venv folder from VSC as follows:
Open settings and go to Files:Exclude
Add pattern: `**/venv`

### Create EVE Online SSO App

For the Eve Online related setup you need to create a SSO app on the developer site:

- Create your Eve Online SSO App on the [Eve Online developer site](https://developers.eveonline.com/)
- Add all ESI scopes
- Set callback URL to: `http://127.0.0.1:8000/sso/callback`

### Update Django settings

Open your local Django settings with VSC. The file is under `myauth/myauth/settings/local.py`

```eval_rst
.. hint::
    There are two Django settings files: ``base.py`` and ``local.py``. The base settings file is controlled by the AA project and may change at any time. It is therefore recommended to only change the local settings file.
```

```python
DEBUG = True
```

Define URL and name of your site:

```python
SITE_URL = "http://127.0.0.1:8000"
...
SITE_NAME = "AA Dev"
```

Update name, user and password of your DATABASE configuration.

```python
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'aa_dev',
    'USER': 'admin',
    'PASSWORD': 'YOUR-PASSWORD',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'OPTIONS': {'charset': 'utf8mb4'},
    "TEST": {"CHARSET": "utf8mb4"},
}
```

Add the credentials for your Eve Online SSO app as defined above:

```python
ESI_SSO_CLIENT_ID = 'YOUR-ID'
ESI_SSO_CLIENT_SECRET = 'YOUR_SECRET'
```

Disable email registration:

```python
REGISTRATION_VERIFY_EMAIL = False
```

### Migrations and superuser

Before we can start AA we need to run migrations:

```bash
cd myauth
python manage.py migrate
```

We also need to create a superuser for our AA installation:

```bash
python manage.py createsuperuser
```

## Running Alliance Auth

## AA instance

We are now ready to run out AA instance with the following command:

```bash
python manage.py runserver
```

Once running you can access your auth site on the browser under `http://localhost:8000`. Or the admin site under `http://localhost:8000/admin`

```eval_rst
.. hint::
    You can start your AA server directly from a terminal window in VSC or with a VSC debug config (see chapter about debugging for details).
```

```eval_rst
.. note::
    **Debug vs. Non-Debug mode**
    Usually it is best to run your dev AA instance in debug mode, so you get all the detailed error messages that helps a lot for finding errors. But there might be cases where you want to test features that do not exist in debug mode (e.g. error pages) or just want to see how your app behaves in non-debug / production mode.

    When you turn off debug mode you will see a problem though: Your pages will not render correctly. The reason is that Django will stop serving your static files in production mode and expect you to serve them from a real web server. Luckily, there is an option that forces Django to continue serving your static files directly even when not in debug mode. Just start your server with the following option: ``python manage.py runserver --insecure``
```

### Celery

In addition you can start a celery worker instance for myauth. For development purposed it makes sense to only start one instance and add some additional logging.

This can be done from the command line with the following command in the myauth folder (where manage.py is located):

```bash
celery -A myauth worker -l info -P solo
```

Same as AA itself you can start Celery from any terminal session, from a terminal window within VSC or as a debug config in VSC (see chapter about debugging for details). For convenience we recommend starting Celery as debug config.

## Debugging setup

To be able to debug your code you need to add debugging configuration to VSC. At least one for AA and one for celery.

### Breakpoints

By default VSC will break on any uncaught exception. Since every error raised by your tests will cause an uncaught exception we recommend to deactivate this feature.

To deactivate open click on the debug icon to switch to the debug view. Then un-check "Uncaught Exceptions" on the breakpoints window.

### AA debug config

In VSC click on Debug / Add Configuration and choose "Django". Should Django not appear as option make sure to first open a Django file (e.g. the local.py settings) to help VSC detect that you are using Django.

The result should look something like this:

```json
{
    "name": "Python: Django",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/myauth/manage.py",
    "cwd": "${workspaceFolder}/myauth",
    "args": [
        "runserver",
        "--noreload"
    ],
    "django": true,
    "justMyCode": true,
}
```

### Debug celery

For celery we need another debug config, so that we can run it in parallel to our AA instance.

Here is an example debug config for Celery:

```json
{
    "name": "Python: Celery",
    "type": "python",
    "request": "launch",
    "module": "celery",
    "cwd": "${workspaceFolder}/myauth",
    "console": "integratedTerminal",
    "args": [
        "-A",
        "myauth",
        "worker",
        "-l",
        "info",
        "-P",
        "solo",
    ],
    "django": true,
    "justMyCode": true,
},
```

### Debug config for unit tests

Finally it makes sense to have a dedicated debug config for running unit tests. Here is an example config for running all tests of the app `example`.

```json
{
    "name": "Python: myauth unit tests",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/myauth/manage.py",
    "cwd": "${workspaceFolder}/myauth",
    "args": [
        "test",
        "--keepdb",
        "--failfast",
        "example",
    ],
    "django": true,
    "justMyCode": true
},
```

You can also specify to run just a part of your test suite down to a test method. Just give the full path to the test you want to run, e.g. `example.test.test_models.TestDemoModel.test_this_method`

### Debugging normal python scripts

Finally you may also want to have a debug config to debug a non-Django Python script:

```json
{
    "name": "Python: Current File",
    "type": "python",
    "request": "launch",
    "program": "${file}",
    "console": "integratedTerminal"
},
```

## Additional tools

The following additional tools are very helpful when developing for AA with VS Code:

### VS Code extensions

#### Django Template

This extension adds language colorization support and user snippets for the Django template language to VS Code: [Django Template](https://marketplace.visualstudio.com/items?itemName=bibhasdn.django-html)

#### Code Spell Checker

Typos in your user facing comments can be quite embarrassing. This spell checker helps you avoid them: [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)

#### Git History

Very helpful to visualize the change history and compare different branches. [Git History](https://marketplace.visualstudio.com/items?itemName=donjayamanne.githistory)

#### markdownlint

Extension for Visual Studio Code - Markdown linting and style checking for Visual Studio Code: [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)

#### Live Server

Live Server allows you to start a mini webserver for any file quickly. This can e.g. be useful for looking at changes to to Sphinx docs.: [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)

### Django apps

#### Django Extensions

[django-extensions](https://django-extensions.readthedocs.io/en/latest/) is a swiss army knife for django developers with adds a lot of very useful features to your Django site. Here are a few highlights:

- shell_plus - An enhanced version of the Django shell. It will auto-load all your models at startup so you don't have to import anything and can use them right away.
- graph_models - Creates a dependency graph of Django models. Visualizing a model dependency structure can be very useful for trying to understand how an existing Django app works, or e.g. how all the AA models work together.
- runserver_plus - The standard runserver stuff but with the Werkzeug debugger baked in. This is a must have for any serious debugging.

#### Django Debug Toolbar

The [Django Debug Toolbar](https://github.com/jazzband/django-debug-toolbar) is a configurable set of panels that display various debug information about the current request/response and when clicked, display more details about the panel's content.

E.g. this tool is invaluable to debug and fix performance issues with Django queries.

### Windows applications

#### DBeaver

DBeaver is a free universal database tool and works with many different kinds of databases include MySQL. It can be installed on Windows 10 and will be able to help manage your MySQL databases running on WSL.

Install from here. [DBeaver](https://dbeaver.io/)

## Adding apps for development

The idea behind the particular folder structure of aa-dev is to have each and every app in its own folder and git repo. To integrate them with the AA instance they need to be installed once using the -e option that enabled editing of the package. And then added to the INSTALLED_APPS settings.

To demonstrate let's add the example plugin to our environment.

Open a WSL bash and navigate to the aa-dev folder. Make sure you have activate your virtual environment. (`source venv/bin/activate`)

Run these commands:

```bash
git clone https://gitlab.com/ErikKalkoken/allianceauth-example-plugin.git
pip install -e allianceauth-example-plugin
```

Add `'example'` to INSTALLED_APPS in your `local.py` settings.

Run migrations and restart your AA server, e.g.:

```bash
cd myauth
python manage.py migrate
```
