import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
from allianceauth.services.tasks import QueueOnce
from allianceauth.notifications import notify
from allianceauth.services.hooks import NameFormatter
from .manager import SmfManager
from .models import SmfUser

logger = logging.getLogger(__name__)


class SmfTasks:
    def __init__(self):
        pass

    @classmethod
    def delete_user(cls, user, notify_user=False):
        if cls.has_account(user):
            logger.debug(f"User {user} has a SMF account {user.smf.username}. Deleting.")
            SmfManager.disable_user(user.smf.username)
            user.smf.delete()
            if notify_user:
                notify(user, "SMF Account Disabled", level='danger')
            return True
        return False

    @staticmethod
    def has_account(user):
        try:
            return user.smf.username != ''
        except ObjectDoesNotExist:
            return False

    @classmethod
    def disable(cls):
        SmfUser.objects.all().delete()

    @staticmethod
    @shared_task(bind=True, name="smf.update_groups", base=QueueOnce)
    def update_groups(self, pk):
        user = User.objects.get(pk=pk)
        logger.debug("Updating smf groups for user %s" % user)
        if SmfTasks.has_account(user):
            groups = [user.profile.state.name]
            for group in user.groups.all():
                groups.append(str(group.name))
            logger.debug(f"Updating user {user} smf groups to {groups}")
            try:
                SmfManager.update_groups(user.smf.username, groups)
            except:
                logger.exception("smf group sync failed for %s, retrying in 10 mins" % user)
                raise self.retry(countdown=60 * 10)
            logger.debug("Updated user %s smf groups." % user)
        else:
            logger.debug("User does not have an smf account")

    @staticmethod
    @shared_task(bind=True, name="smf.update_display_name", base=QueueOnce)
    def update_display_name(self, pk):
        user = User.objects.get(pk=pk)
        logger.debug(f"Updating SMF displayed name user {user}")

        if SmfTasks.has_account(user):
            try:
                if not SmfManager.update_display_name(user):
                    raise Exception("SMF Displayed Name Sync failed")
                logger.debug(f"Updated user {user} SMF displayed name.")
                return True
            except SmfUser.DoesNotExist:
                logger.info(
                    f"SMF displayed name sync failed for {user}, "
                    "user does not have a SMF account"
                )
            except:
                logger.exception(
                    f"SMF displayed name sync failed for {user}, retrying in 10 mins"
                )
                raise self.retry(countdown=60 * 10)
        else:
            logger.debug(f"User {user} does not have a SMF account, skipping")

        return False

    @staticmethod
    @shared_task(name="smf.update_all_display_names")
    def update_all_display_names():
        logger.debug("Updating ALL SMF display names")
        for smf_user in SmfUser.objects.exclude(username__exact=''):
            SmfTasks.update_display_name.delay(smf_user)

    @staticmethod
    @shared_task(name="smf.update_all_groups")
    def update_all_groups():
        logger.debug("Updating ALL smf groups")
        for user in SmfUser.objects.exclude(username__exact=''):
            SmfTasks.update_groups.delay(user.user_id)

    @staticmethod
    def get_username(user):
        from .auth_hooks import SmfService
        return NameFormatter(SmfService(), user).format_name()
