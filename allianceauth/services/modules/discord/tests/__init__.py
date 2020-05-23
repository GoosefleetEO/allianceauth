from django.contrib.auth.models import Group
from allianceauth.tests.auth_utils import AuthUtils
from ..discord_client.tests import create_role

DEFAULT_AUTH_GROUP = 'Member'
MODULE_PATH = 'allianceauth.services.modules.discord'

TEST_GUILD_ID = 123456789012345678
TEST_USER_ID = 198765432012345678
TEST_USER_NAME = 'Peter Parker'
TEST_MAIN_NAME = 'Spiderman'
TEST_MAIN_ID = 1005

ROLE_ALPHA = create_role(1, 'alpha')
ROLE_BRAVO = create_role(2, 'bravo')
ROLE_CHARLIE = create_role(3, 'charlie')
ROLE_MIKE = create_role(13, 'mike', True)


def add_permissions_to_members():
    permission = AuthUtils.get_permission_by_name('discord.access_discord')
    members = Group.objects.get_or_create(name=DEFAULT_AUTH_GROUP)[0]
    AuthUtils.add_permissions_to_groups([permission], [members])
