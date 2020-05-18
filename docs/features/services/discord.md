# Discord

## Overview

Discord is a web-based instant messaging client with voice. Kind of like TeamSpeak meets Slack meets Skype. It also has a standalone app for phones and desktop.

Discord is very popular amongst ad-hoc small groups and larger organizations seeking a modern technology. Alternative voice communications should be investigated for larger than small-medium groups for more advanced features.

## Setup

### Prepare Your Settings File

Make the following changing in your auth project's settings file (`local.py`):

- Add `'allianceauth.services.modules.discord',` to `INSTALLED_APPS`
- Append the following to the bottom of the settings file:

```python
# Discord Configuration
DISCORD_GUILD_ID = ''
DISCORD_CALLBACK_URL = ''
DISCORD_APP_ID = ''
DISCORD_APP_SECRET = ''
DISCORD_BOT_TOKEN = ''
DISCORD_SYNC_NAMES = False

CELERYBEAT_SCHEDULE['discord.update_all_usernames'] = {
    'task': 'discord.update_all_usernames',
    'schedule': crontab(hour='*/12'),
}
```

```eval_rst
.. note::
   You will have to add most the values for these settings, e.g. your Discord server ID (aka guild ID), later in the setup process.
```

### Creating a Server

Navigate to the [Discord site](https://discordapp.com/) and register an account, or log in if you have one already.

On the left side of the screen you’ll see a circle with a plus sign. This is the button to create a new server. Go ahead and do that, naming it something obvious.

Now retrieve the server ID [following this procedure.](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

Update your auth project's settings file, inputting the server ID as `DISCORD_GUILD_ID`

```eval_rst
.. note::
   If you already have a Discord server skip the creation step, but be sure to retrieve the server ID
```

### Registering an Application

Navigate to the [Discord Developers site.](https://discordapp.com/developers/applications/me) Press the plus sign to create a new application.

Give it a name and description relating to your auth site. Add a redirect to `https://example.com/discord/callback/`, substituting your domain. Press Create Application.

Update your auth project's settings file, inputting this redirect address as `DISCORD_CALLBACK_URL`

On the application summary page, press Create a Bot User.

Update your auth project's settings file with these pieces of information from the summary page:

- From the App Details panel, `DISCORD_APP_ID` is the Client/Application ID
- From the App Details panel, `DISCORD_APP_SECRET` is the Secret
- From the App Bot Users panel, `DISCORD_BOT_TOKEN` is the Token

### Preparing Auth

Before continuing it is essential to run migrations and restart Gunicorn and Celery.

### Adding a Bot to the Server

Once created, navigate to the services page of your Alliance Auth install as the superuser account. At the top there is a big green button labelled Link Discord Server. Click it, then from the drop down select the server you created, and then Authorize.

This adds a new user to your Discord server with a `BOT` tag, and a new role with the same name as your Discord application. Don't touch either of these. If for some reason the bot loses permissions or is removed from the server, click this button again.

To manage roles, this bot role must be at the top of the hierarchy. Edit your Discord server, roles, and click and drag the role with the same name as your application to the top of the list. This role must stay at the top of the list for the bot to work.  Finally, the owner of the bot account must enable 2 Factor Authentication (this is required from Discord for kicking and modifying member roles).  If you are unsure what 2FA is or how to set it up, refer to [this support page](https://support.discordapp.com/hc/en-us/articles/219576828).  It is also recommended to force 2FA on your server (this forces any admins or moderators to have 2fa enabled to perform similar functions on discord).

Note that the bot will never appear online as it does not participate in chat channels.

### Linking Accounts

Instead of the usual account creation procedure, for Discord to work we need to link accounts to Alliance Auth. When attempting to enable the Discord service, users are redirected to the official Discord site to authenticate. They will need to create an account if they don't have one prior to continuing. Upon authorization, users are redirected back to Alliance Auth with an OAuth code which is used to join the Discord server.

### Syncing Nicknames

If you want users to have their Discord nickname changed to their in-game character name, set `DISCORD_SYNC_NAMES` to `True`.

## Managing Roles

Once users link their accounts you’ll notice Roles get populated on Discord. These are the equivalent to groups on every other service. The default permissions should be enough for members to use text and audio communications. Add more permissions to the roles as desired through the server management window.

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
============================== ============================================================================================= =======
Name                           Description                                                                                   Default
============================== ============================================================================================= =======
`DISCORD_APP_ID`               Oauth client ID for the Discord Auth app                                                      `''`
`DISCORD_APP_SECRET`           Oauth client secret for the Discord Auth app                                                  `''`
`DISCORD_BOT_TOKEN`            Generated bot token for the Discord Auth app                                                  `''`
`DISCORD_CALLBACK_URL`         Oauth callback URL                                                                            `''`
`DISCORD_GUILD_ID`             Discord ID of your Discord server                                                             `''`
`DISCORD_ROLES_CACHE_MAX_AGE`  How long roles retrieved from the Discord server are caches locally in milliseconds           `7200000`
`DISCORD_SYNC_NAMES`           When set to True the nicknames of Discord users will be set to the user's main character name `False`
`DISCORD_TASKS_RETRY_PAUSE`    Pause in seconds until next retry for tasks after an error occurred                           `60`
`DISCORD_TASKS_MAX_RETRIES`    max retries of tasks after an error occurred                                                  `3`
============================== ============================================================================================= =======
```

## Troubleshooting

### "Unknown Error" on Discord site when activating service

This indicates your callback URL doesn't match. Ensure the `DISCORD_CALLBACK_URL` setting exactly matches the URL entered on the Discord developers site. This includes http(s), trailing slash, etc.
