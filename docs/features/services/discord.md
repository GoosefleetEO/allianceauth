# Discord

## Overview

Discord is a web-based instant messaging client with voice. Kind of like TeamSpeak meets Slack meets Skype. It also has a standalone app for phones and desktop.

Discord is very popular amongst ad-hoc small groups and larger organizations seeking a modern technology. Alternative voice communications should be investigated for larger than small-medium groups for more advanced features.

## Setup

### Prepare Your Settings File

Make the following changes in your auth project's settings file (`local.py`):

- Add `'allianceauth.services.modules.discord',` to `INSTALLED_APPS`
- Append the following to the bottom of the settings file:

```python
# Discord Configuration
# Be sure to set the callback URLto https://example.com/discord/callback/
# substituting your domain for example.com in Discord's developer portal
# (Be sure to add the trailing slash)
DISCORD_GUILD_ID = ''
DISCORD_CALLBACK_URL = f"{SITE_URL}/discord/callback/"
DISCORD_APP_ID = ''
DISCORD_APP_SECRET = ''
DISCORD_BOT_TOKEN = ''
DISCORD_SYNC_NAMES = False

CELERYBEAT_SCHEDULE['discord.update_all_usernames'] = {
    'task': 'discord.update_all_usernames',
    'schedule': crontab(minute=0, hour='*/12'),
}
```

```eval_rst
.. note::
    You will have to add most the values for these settings, e.g. your Discord server ID (aka guild ID), later in the setup process.
```

### Creating a Server

Navigate to the [Discord site](https://discord.com/) and register an account, or log in if you have one already.

On the left side of the screen you’ll see a circle with a plus sign. This is the button to create a new server. Go ahead and do that, naming it something obvious.

Now retrieve the server ID [following this procedure.](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

Update your auth project's settings file, inputting the server ID as `DISCORD_GUILD_ID`

```eval_rst
.. note::
    If you already have a Discord server skip the creation step, but be sure to retrieve the server ID
```

### Registering an Application

Navigate to the [Discord Developers site.](https://discord.com/developers/applications/me) Press the plus sign to create a new application.

Give it a name and description relating to your auth site. Add a redirect to `https://example.com/discord/callback/`, substituting your domain. Press Create Application.

Update your auth project's settings file, inputting this redirect address as `DISCORD_CALLBACK_URL`

On the application summary page, press Create a Bot User.

Update your auth project's settings file with these pieces of information from the summary page:

- From the General Information panel, `DISCORD_APP_ID` is the Client/Application ID
- From the OAuth2 > General panel, `DISCORD_APP_SECRET` is the Client Secret
- From the Bot panel, `DISCORD_BOT_TOKEN` is the Token

### Preparing Auth

Before continuing it is essential to run migrations and restart Gunicorn and Celery.

### Adding a Bot to the Server

Once created, navigate to the services page of your Alliance Auth install as the superuser account. At the top there is a big green button labelled Link Discord Server. Click it, then from the drop down select the server you created, and then Authorize.

This adds a new user to your Discord server with a `BOT` tag, and a new role with the same name as your Discord application. Don't touch either of these. If for some reason the bot loses permissions or is removed from the server, click this button again.

To manage roles, this bot role must be at the top of the hierarchy. Edit your Discord server, roles, and click and drag the role with the same name as your application to the top of the list. This role must stay at the top of the list for the bot to work.  Finally, the owner of the bot account must enable 2 Factor Authentication (this is required from Discord for kicking and modifying member roles).  If you are unsure what 2FA is or how to set it up, refer to [this support page](https://support.discord.com/hc/en-us/articles/219576828).  It is also recommended to force 2FA on your server (this forces any admins or moderators to have 2fa enabled to perform similar functions on discord).

Note that the bot will never appear online as it does not participate in chat channels.

### Linking Accounts

Instead of the usual account creation procedure, for Discord to work we need to link accounts to Alliance Auth. When attempting to enable the Discord service, users are redirected to the official Discord site to authenticate. They will need to create an account if they don't have one prior to continuing. Upon authorization, users are redirected back to Alliance Auth with an OAuth code which is used to join the Discord server.

### Syncing Nicknames

If you want users to have their Discord nickname changed to their in-game character name, set `DISCORD_SYNC_NAMES` to `True`.

## Managing Roles

Once users link their accounts you’ll notice Roles get populated on Discord. These are the equivalent to groups on every other service. The default permissions should be enough for members to use text and audio communications. Add more permissions to the roles as desired through the server management window.

By default Alliance Auth is taking over full control of role assignments on Discord. This means that users on Discord can in general only have roles that correlate to groups on Auth. However, there are two exceptions to this rule.

### Internal Discord roles

First, users will keep their so called "Discord managed roles". Those are internal roles created by Discord e.g. for Nitro.

### Excluding roles from being managed by Auth

Second, it is possible to exclude Discord roles from being managed by Auth at all. This can be useful if you have other bots on your Discord server that are using their own roles and which would otherwise conflict with Auth. This would also allow you to manage a role manually on Discord if you so chose.

To exclude roles from being managed by Auth you only have to add them to the list of reserved group names in Group Management.

```eval_rst
.. note::
    Role names on Discord are case sensitive, while reserved group names on Auth are not. Therefore reserved group names will cover all roles regardless of their case. For example if you have reserved the group name "alpha", then the Discord roles "alpha" and "Alpha" will both be persisted.
```

```eval_rst
.. seealso::
    For more information see :ref:`ref-reserved-group-names`.
```

## Tasks

The Discord service contains a number of tasks that can be run to manually perform updates to all users.

You can run any of these tasks from the command line. Please make sure that you are in your venv and then you can run this command from the same folder that your manage.py is located:

```bash
celery -A myauth call discord.update_all_groups
```

```eval_rst
======================== ====================================================
Name                     Description
======================== ====================================================
`update_all_groups`      Updates groups of all users
`update_all_nicknames`   Update nicknames of all users (also needs setting)
`update_all_usernames`   Update locally stored Discord usernames of all users
`update_all`             Update groups, nicknames, usernames of all users
======================== ====================================================
```

```eval_rst
.. note::
    Depending on how many users you have, running these tasks can take considerable time to finish. You can calculate roughly 1 sec per user for all tasks, except update_all, which needs roughly 3 secs per user.
```

## Settings

You can configure your Discord services with the following settings:

```eval_rst
=================================== ============================================================================================= =======
Name                                Description                                                                                   Default
=================================== ============================================================================================= =======
`DISCORD_APP_ID`                    Oauth client ID for the Discord Auth app                                                      `''`
`DISCORD_APP_SECRET`                Oauth client secret for the Discord Auth app                                                  `''`
`DISCORD_BOT_TOKEN`                 Generated bot token for the Discord Auth app                                                  `''`
`DISCORD_CALLBACK_URL`              Oauth callback URL                                                                            `''`
`DISCORD_GUILD_ID`                  Discord ID of your Discord server                                                             `''`
`DISCORD_GUILD_NAME_CACHE_MAX_AGE`  How long the Discord server name is cached locally in seconds                                 `86400`
`DISCORD_ROLES_CACHE_MAX_AGE`       How long roles retrieved from the Discord server are cached locally in seconds                `3600`
`DISCORD_SYNC_NAMES`                When set to True the nicknames of Discord users will be set to the user's main character name `False`
`DISCORD_TASKS_RETRY_PAUSE`         Pause in seconds until next retry for tasks after an error occurred                           `60`
`DISCORD_TASKS_MAX_RETRIES`         max retries of tasks after an error occurred                                                  `3`
=================================== ============================================================================================= =======
```

## Permissions

To use this service, users will require some of the following.

```eval_rst
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| Permission                            | Admin Site       | Auth Site                                                                |
+=======================================+==================+==========================================================================+
| discord.access_discord                | None             | Can Access the Discord Service                                           |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
```

## Troubleshooting

### "Unknown Error" on Discord site when activating service

This indicates your callback URL doesn't match. Ensure the `DISCORD_CALLBACK_URL` setting exactly matches the URL entered on the Discord developers site. This includes http(s), trailing slash, etc.

### "Add/Remove" Errors in Discord Service

If you are receiving errors in your Notifications after verifying that your settings are all correct try the following:

- Ensure that the bot's role in Discord is at the top of the roles list. Each time you add it to your server you will need to do this again.
- Make sure that the bot is not trying to modify the Owner of the discord, as it will fail. A holding discord account added with invite link will mitigate this.
- Make sure that the bot role on discord has all needed permissions, Admin etc., remembering that these will need to be set every time you add the bot to the Discord server.
