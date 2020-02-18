from django.contrib.auth.models import User, Group, Permission
from allianceauth.tests.auth_utils import AuthUtils

DEFAULT_AUTH_GROUP = 'Member'
MODULE_PATH = 'allianceauth.services.modules.discord'

def add_permissions():
    permission = Permission.objects.get(codename='access_discord')
    members = Group.objects.get_or_create(name=DEFAULT_AUTH_GROUP)[0]
    AuthUtils.add_permissions_to_groups([permission], [members])
