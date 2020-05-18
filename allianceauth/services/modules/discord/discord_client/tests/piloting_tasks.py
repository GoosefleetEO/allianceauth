"""Load testing Discord services tasks

This script will load test the Discord service tasks.
Note that his will run against your production Auth.
To run this test start a bunch of celery workers and then run this script directly.

This script requires a user with a Discord account setup through Auth. 
Please provide the respective Discord user ID by setting it as environment variable:

export DISCORD_USER_ID="123456789"
"""

import os
import sys

myauth_dir = '/home/erik997/dev/python/aa/allianceauth-dev/myauth'
sys.path.insert(0, myauth_dir)

import django   # noqa: E402

# init and setup django project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myauth.settings.local")
django.setup()

from uuid import uuid1  # noqa: E402

from django.contrib.auth.models import User     # noqa: E402
# from allianceauth.services.modules.discord.tasks import update_groups  # noqa: E402

if 'DISCORD_USER_ID' not in os.environ:
    print('Please set DISCORD_USER_ID')
    exit()

DISCORD_USER_ID = os.environ['DISCORD_USER_ID']


def run_many_updates(runs):        
    user = User.objects.get(discord__uid=DISCORD_USER_ID)
    for _ in range(runs):                
        new_nick = f'Testnick {uuid1().hex}'[:32]
        user.profile.main_character.character_name = new_nick
        user.profile.main_character.save()
        # update_groups.delay(user_pk=user.pk)
        

if __name__ == "__main__":
    run_many_updates(20)
