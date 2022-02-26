"""
Alliance Auth Test Suite Django settings

Testing all services and plug-in apps
"""

from allianceauth.project_template.project_name.settings.base import *

# Celery configuration
CELERY_ALWAYS_EAGER = True  # Forces celery to run locally for testing

INSTALLED_APPS += [
    'allianceauth.eveonline.autogroups',
    'allianceauth.hrapplications',
    'allianceauth.timerboard',
    'allianceauth.srp',
    'allianceauth.optimer',
    'allianceauth.corputils',
    'allianceauth.fleetactivitytracking',
    'allianceauth.permissions_tool',
    'allianceauth.services.modules.mumble',
    'allianceauth.services.modules.discord',
    'allianceauth.services.modules.discourse',
    'allianceauth.services.modules.ips4',
    'allianceauth.services.modules.openfire',
    'allianceauth.services.modules.smf',
    'allianceauth.services.modules.phpbb3',
    'allianceauth.services.modules.xenforo',
    'allianceauth.services.modules.teamspeak3',
]

ROOT_URLCONF = 'tests.urls'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1"
    }
}

########################
# XenForo Configuration
########################
XENFORO_ENDPOINT = 'example.com/api.php'
XENFORO_DEFAULT_GROUP = 0
XENFORO_APIKEY   = 'yourapikey'
#####################

######################
# Jabber Configuration
######################
# JABBER_URL - Jabber address url
# JABBER_PORT - Jabber service portal
# JABBER_SERVER - Jabber server url
# OPENFIRE_ADDRESS - Address of the openfire admin console including port
#                    Please use http with 9090 or https with 9091
# OPENFIRE_SECRET_KEY - Openfire REST API secret key
# BROADCAST_USER - Broadcast user JID
# BROADCAST_USER_PASSWORD - Broadcast user password
######################
JABBER_URL = "example.com"
JABBER_PORT = 5223
JABBER_SERVER = "example.com"
OPENFIRE_ADDRESS = "http://example.com:9090"
OPENFIRE_SECRET_KEY = "somekey"
BROADCAST_USER = "broadcast@" + JABBER_URL
BROADCAST_USER_PASSWORD = "somepassword"
BROADCAST_SERVICE_NAME = "broadcast"

######################################
# Mumble Configuration
######################################
# MUMBLE_URL - Mumble server url
# MUMBLE_SERVER_ID - Mumble server id
######################################
MUMBLE_URL = "example.com"
MUMBLE_SERVER_ID = 1

######################################
# PHPBB3 Configuration
######################################
PHPBB3_URL = ''

######################################
# Teamspeak3 Configuration
######################################
# TEAMSPEAK3_SERVER_IP - Teamspeak3 server ip
# TEAMSPEAK3_SERVER_PORT - Teamspeak3 server port
# TEAMSPEAK3_SERVERQUERY_USER - Teamspeak3 serverquery username
# TEAMSPEAK3_SERVERQUERY_PASSWORD - Teamspeak3 serverquery password
# TEAMSPEAK3_VIRTUAL_SERVER - Virtual server id
# TEAMSPEAK3_AUTHED_GROUP_ID - Default authed group id
# TEAMSPEAK3_PUBLIC_URL - teamspeak3 public url used for link creation
######################################
TEAMSPEAK3_SERVER_IP = '127.0.0.1'
TEAMSPEAK3_SERVER_PORT = 10011
TEAMSPEAK3_SERVERQUERY_USER = 'serveradmin'
TEAMSPEAK3_SERVERQUERY_PASSWORD = 'passwordhere'
TEAMSPEAK3_VIRTUAL_SERVER = 1
TEAMSPEAK3_PUBLIC_URL = 'example.com'

######################################
# Discord Configuration
######################################
# DISCORD_GUILD_ID - ID of the guild to manage
# DISCORD_BOT_TOKEN - oauth token of the app bot user
# DISCORD_INVITE_CODE - invite code to the server
# DISCORD_APP_ID - oauth app client ID
# DISCORD_APP_SECRET - oauth app secret
# DISCORD_CALLBACK_URL - oauth callback url
# DISCORD_SYNC_NAMES - enable to force discord nicknames to be set to eve char name (bot needs Manage Nicknames permission)
######################################
DISCORD_GUILD_ID = '0118999'
DISCORD_BOT_TOKEN = 'bottoken'
DISCORD_INVITE_CODE = 'invitecode'
DISCORD_APP_ID = 'appid'
DISCORD_APP_SECRET = 'secret'
DISCORD_CALLBACK_URL = 'http://example.com/discord/callback'
DISCORD_SYNC_NAMES = 'True' == 'False'

######################################
# Discourse Configuration
######################################
# DISCOURSE_URL - Web address of the forums (no trailing slash)
# DISCOURSE_API_USERNAME - API account username
# DISCOURSE_API_KEY - API Key
# DISCOURSE_SSO_SECRET - SSO secret key
######################################
DISCOURSE_URL = 'https://example.com'
DISCOURSE_API_USERNAME = ''
DISCOURSE_API_KEY = ''
DISCOURSE_SSO_SECRET = 'd836444a9e4084d5b224a60c208dce14'
# Example secret from https://meta.discourse.org/t/official-single-sign-on-for-discourse/13045

#####################################
# IPS4 Configuration
#####################################
# IPS4_URL - base url of the IPS4 install (no trailing slash)
# IPS4_API_KEY - API key provided by IPS4
#####################################
IPS4_URL = 'http://example.com/ips4'
IPS4_API_KEY = ''

######################################
# SMF Configuration
######################################
SMF_URL = ''

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

LOGGING = None  # Comment out to enable logging for debugging

ALLIANCEAUTH_DASHBOARD_TASK_STATISTICS_DISABLED = True  # disable for tests
