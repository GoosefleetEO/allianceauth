from ..utils import clean_setting


# Base URL for all API calls. Must end with /.
DISCORD_API_BASE_URL = clean_setting(
    'DISCORD_API_BASE_URL', 'https://discordapp.com/api/'
)

# Low level timeout for requests to the Discord API in ms
DISCORD_API_TIMEOUT = clean_setting(
    'DISCORD_API_TIMEOUT', 5000
)

# Base authorization URL for Discord Oauth
DISCORD_OAUTH_BASE_URL = clean_setting(
    'DISCORD_OAUTH_BASE_URL', 'https://discordapp.com/api/oauth2/authorize'
)

# Base authorization URL for Discord Oauth
DISCORD_OAUTH_TOKEN_URL = clean_setting(
    'DISCORD_OAUTH_TOKEN_URL', 'https://discordapp.com/api/oauth2/token'
)

# How long the Discord guild names retrieved from the server are 
# caches locally in milliseconds.
DISCORD_GUILD_NAME_CACHE_MAX_AGE = clean_setting(
    'DISCORD_GUILD_NAME_CACHE_MAX_AGE', 3600 * 1 * 1000
)

# How long Discord roles retrieved from the server are caches locally in milliseconds.
DISCORD_ROLES_CACHE_MAX_AGE = clean_setting(
    'DISCORD_ROLES_CACHE_MAX_AGE', 3600 * 1 * 1000
)

# Turns off creation of new roles. In case the rate limit for creating roles is
# exhausted, this setting allows the Discord service to continue to function 
# and wait out the reset. Rate limit is about 250 per 48 hrs.
DISCORD_DISABLE_ROLE_CREATION = clean_setting(
    'DISCORD_DISABLE_ROLE_CREATION', False
)
