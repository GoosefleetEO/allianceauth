# Mumble

Mumble is a free voice chat server. While not as flashy as TeamSpeak, it has all the functionality and is easier to customize. And is better. I may be slightly biased.

```eval_rst
.. note::
   Note that this guide assumes that you have installed Auth with the official :doc:`/installation/allianceauth` guide under ``/home/allianceserver`` and that it is called ``myauth``. Accordingly it assumes that you have a service user called ``allianceserver`` that is used to run all Auth services under supervisor.
```

```eval_rst
.. note::
   Same as the official installation guide this guide is assuming you are performing all steps as ``root`` user.
```

```eval_rst
.. warning::
   This guide is currently for Ubuntu only.
```

## Installations

### Installing Mumble Server

The mumble server package can be retrieved from a repository, which we need to add:

```bash
apt-add-repository ppa:mumble/release
```

```bash
apt-get update
```

Now three packages need to be installed:

```bash
apt-get install python-software-properties mumble-server libqt5sql5-mysql
```

### Installing Mumble Authenticator

Next, we need to download the latest authenticator release from the [authenticator repository](https://gitlab.com/allianceauth/mumble-authenticator).

```bash
git clone https://gitlab.com/allianceauth/mumble-authenticator /home/allianceserver/mumble-authenticator
```

We will now install the authenticator into your Auth virtual environment. Please make sure to activate it first:

```bash
source /home/allianceserver/venv/auth/bin/activate
```

Install the python dependencies for the mumble authenticator. Note that this process can take a couple minutes to complete.

```bash
pip install -r requirements.txt
```

## Configuring Mumble Server

The mumble server needs it's own database. Open an SQL shell with `mysql -u root -p` and execute the SQL commands to create it:

```sql
CREATE DATABASE alliance_mumble CHARACTER SET utf8mb4;
```

```sql
GRANT ALL PRIVILEGES ON alliance_mumble . * TO 'allianceserver'@'localhost';
```

Mumble ships with a configuration file that needs customization. By default it’s located at `/etc/mumble-server.ini`. Open it with your favorite text editor:

```bash
nano /etc/mumble-server.ini
```

We need to enable the ICE authenticator. Edit the following:

- `icesecretwrite=MY_CLEVER_PASSWORD`, obviously choosing a secure password
- ensure the line containing `Ice="tcp -h 127.0.0.1 -p 6502"` is uncommented

We also want to enable Mumble to use the previously created MySQL / MariaDB database, edit the following:

- uncomment the database line, and change it to `database=alliance_mumble`
- `dbDriver=QMYSQL`
- `dbUsername=allianceserver` or whatever you called the Alliance Auth MySQL user
- `dbPassword=` that user’s password
- `dbPort=3306`
- `dbPrefix=murmur_`

To name your root channel, uncomment and set `registerName=` to whatever cool name you want

Save and close the file.

To get Mumble superuser account credentials, run the following:

```bash
dpkg-reconfigure mumble-server
```

Set the password to something you’ll remember and write it down. This is your superuser password and later needed to manage ACLs.

Now restart the server to see the changes reflected.

```bash
service mumble-server restart
```

That’s it! Your server is ready to be connected to at example.com:64738

## Configuring Mumble Authenticator

The ICE authenticator lives in the mumble-authenticator repository, cd to the directory where you cloned it.

Make a copy of the default config:

```bash
cp authenticator.ini.example authenticator.ini
```

Edit `authenticator.ini` and change these values:

- `[database]`
  - `user =` your allianceserver MySQL user
  - `password =` your allianceserver MySQL user's password
- `[ice]`
  - `secret =` the `icewritesecret` password set earlier

Test your configuration by starting it:

```bash
python /home/allianceserver/mumble-authenticator/authenticator.py
```

And finally ensure the allianceserver user has read/write permissions to the mumble authenticator files before proceeding:

```bash
chown -R allianceserver:allianceserver /home/allianceserver/mumble-authenticator
```

The authenticator needs to be running 24/7 to validate users on Mumble. This can be achieved by adding a section to your auth project's supervisor config file like the following example:

```text
[program:authenticator]
command=/home/allianceserver/venv/auth/bin/python authenticator.py
directory=/home/allianceserver/mumble-authenticator
user=allianceserver
stdout_logfile=/home/allianceserver/myauth/log/authenticator.log
stderr_logfile=/home/allianceserver/myauth/log/authenticator.log
autostart=true
autorestart=true
startsecs=10
priority=996
```

In addition we'd recommend to add the authenticator to Auth's restart group in your supervisor conf. For that you need to add it to the group line as shown in the following example:

```text
[group:myauth]
programs=beat,worker,gunicorn,authenticator
priority=999
```

To enable the changes in your supervisor configuration you need to restart the supervisor process itself. And before we do that we are shutting down the current Auth supervisors gracefully:

```bash
supervisor stop myauth:
systemctl restart supervisor
```

## Configuring Auth

In your auth project's settings file (`myauth/settings/local.py`), do the following:

- Add `'allianceauth.services.modules.mumble',` to your `INSTALLED_APPS` list
- set `MUMBLE_URL` to the public address of your mumble server. Do not include any leading `http://` or `mumble://`.

Example config:

```python
# Installed apps
INSTALLED_APPS += [
  # ...
  'allianceauth.services.modules.mumble'
  # ...
]

# Mumble Configuration
MUMBLE_URL = "mumble.example.com"
```

Finally, run migrations and restart your supervisor to complete the setup:

```bash
python /home/allianceserver/myauth/manage.py migrate
```

```bash
supervisorctl restart myauth:
```

## Permissions

To use this service, users will require some of the following.

```eval_rst
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| Permission                            | Admin Site       | Auth Site                                                                |
+=======================================+==================+==========================================================================+
| mumble.access_mumble                  | None             | Can Access the Mumble Service                                            |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
```

## ACL configuration

On a freshly installed mumble server only your superuser has the right to configure ACLs and create channels. The credentials for logging in with your superuser are:

- user: `SuperUser`
- password: *what you defined when configuring your mumble server*

## Optimizing a Mumble Server

The needs and available resources will vary between Alliance Auth installations. Consider yours when applying these settings.

### Bandwidth

<https://wiki.mumble.info/wiki/Murmur.ini#bandwidth>
This is likely the most important setting for scaling a Mumble install, The default maximum Bandwidth is 72000bps Per User. Reducing this value will cause your clients to automatically scale back their bandwidth transmitted, while causing a reduction in voice quality. A value thats still high may cause robotic voices or users with bad connections to drop due entirely due to network load.

Please tune this value to your individual needs, the below scale may provide a rough starting point.
72000 - Superior voice quality - Less than 50 users.
54000 - No noticeable reduction in quality - 50+ Users or many channels with active audio.
36000 - Mild reduction in quality - 100+ Users
30000 - Noticeable reduction in quality but not function - 250+ Users

### Forcing Opus

<https://wiki.mumble.info/wiki/Murmur.ini#opusthreshold>
A Mumble server by default, will fall back to the older CELT codec as soon as a single user connects with an old client. This will significantly reduce your audio quality and likely place higher load on your server. We _highly_ reccommend setting this to Zero, to force OPUS to be used at all times. Be aware any users with Mumble clients prior to 1.2.4 (From 2013...) Will not hear any audio.

`opusthreshold=0`

### AutoBan and Rate Limiting

<https://wiki.mumble.info/wiki/Murmur.ini#autobanAttempts.2C_autobanTimeframe_and_autobanTime>
The AutoBan feature has some sensible settings by default, You may wish to tune these if your users keep locking themselves out by opening two clients by mistake, or if you are receiving unwanted attention

<https://wiki.mumble.info/wiki/Murmur.ini#messagelimit_and_messageburst>
This too, is set to a sensible configuration by default. Take note on upgrading older installs, as this may actually be set too restrictively and will rate-limit your admins accidentally, take note of the configuration in <https://github.com/mumble-voip/mumble/blob/master/scripts/murmur.ini#L156>

### "Suggest" Options

There is no way to force your users to update their clients or use Push to Talk, but these options will throw an error into their Mumble Client.

<https://wiki.mumble.info/wiki/Murmur.ini#Miscellany>

We suggest using Mumble 1.3.0+ for your server and Clients, you can tune this to the latest Patch version.
`suggestVersion=1.3.0`

If Push to Talk is to your tastes, configure the suggestion as follows
`suggestPushToTalk=true`

## General notes

### Setting a server password

With the default configuration your mumble server is public. Meaning that everyone who has the address can at least connect to it and might also be able join all channels that don't have any permissions set (Depending on your ACL configured for the root channel). If you want only registered member being able to join your mumble, you have to set a server password. To do so open your mumble server configuration which is by default located at `/etc/mumble-server.ini`.

```bash
nano /etc/mumble-server.ini
```

Now search for `serverpassword=` and set your password here. If there is no such line, simply add it.

```text
serverpassword=YourSuperSecretServerPassword
```

Save the file and restart your mumble server afterwards.

```bash
service mumble-server restart
```

From now on, only registered member can join your mumble server. Now if you still want to allow guests to join you have 2 options.

- Allow the "Guest" state to activate the Mumble service in your Auth instance
- Use [Mumble temporary links](https://github.com/pvyParts/allianceauth-mumble-temp)

### Enabling Avatars in Overlay (V1.0.0+)

Ensure you have an up to date Mumble-Authenticator, this feature was added in V1.0.0

Edit `authenticator.ini` and change (or add for older installs) This code block.

```ini
;If enabled, textures are automatically set as player's EvE avatar for use on overlay.
avatar_enable = True
;Get EvE avatar images from this location. {charid} will be filled in.
ccp_avatar_url = https://images.evetech.net/characters/{charid}/portrait?size=32
```
