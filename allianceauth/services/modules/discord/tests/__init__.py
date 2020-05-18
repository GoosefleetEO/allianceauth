from django.contrib.auth.models import Group, Permission
from allianceauth.tests.auth_utils import AuthUtils

DEFAULT_AUTH_GROUP = 'Member'
MODULE_PATH = 'allianceauth.services.modules.discord'

TEST_GUILD_ID = 123456789012345678
TEST_USER_ID = 198765432012345678
TEST_USER_NAME = 'Peter Parker'
TEST_MAIN_NAME = 'Spiderman'
TEST_MAIN_ID = 1005


def add_permissions_to_members():
    permission = Permission.objects.get(codename='access_discord')
    members = Group.objects.get_or_create(name=DEFAULT_AUTH_GROUP)[0]
    AuthUtils.add_permissions_to_groups([permission], [members])
