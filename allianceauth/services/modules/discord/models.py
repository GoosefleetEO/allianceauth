import logging

from requests.exceptions import HTTPError

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy

from allianceauth.notifications import notify

from . import __title__
from .app_settings import DISCORD_GUILD_ID
from .discord_client import DiscordClient, DiscordApiBackoff
from .managers import DiscordUserManager
from .utils import LoggerAddTag


logger = LoggerAddTag(logging.getLogger(__name__), __title__)


class DiscordUser(models.Model):

    USER_RELATED_NAME = 'discord'
    
    user = models.OneToOneField(
        User, 
        primary_key=True, 
        on_delete=models.CASCADE, 
        related_name=USER_RELATED_NAME,
        help_text='Auth user owning this Discord account'
    )
    uid = models.BigIntegerField(
        db_index=True,
        help_text='user\'s ID on Discord'
    )
    username = models.CharField(
        max_length=32, 
        default='', 
        blank=True,
        db_index=True,
        help_text='user\'s username on Discord'
    )
    discriminator = models.CharField(
        max_length=4, 
        default='', 
        blank=True, 
        help_text='user\'s discriminator on Discord'
    )
    activated = models.DateTimeField(
        default=None, 
        null=True, 
        blank=True,
        help_text='Date & time this service account was activated'
    )

    objects = DiscordUserManager()

    class Meta:
        permissions = (
            ("access_discord", "Can access the Discord service"),
        )

    def __str__(self):
        return f'{self.user.username} - {self.uid}'

    def __repr__(self):
        return f'{type(self).__name__}(user=\'{self.user}\', uid={self.uid})'

    def update_nickname(self) -> bool:
        """Update nickname with formatted name of main character
                
        Returns:
        - True on success
        - None if user is no longer a member of the Discord server
        - False on error or raises exception
        """        
        requested_nick = DiscordUser.objects.user_formatted_nick(self.user)
        if requested_nick:            
            client = DiscordUser.objects._bot_client()            
            success = client.modify_guild_member(
                guild_id=DISCORD_GUILD_ID,
                user_id=self.uid,
                nick=requested_nick
            )
            if success:
                logger.info('Nickname for %s has been updated', self.user)
            else:
                logger.warning('Failed to update nickname for %s', self.user)
            return success
         
        else:
            return False

    def update_groups(self) -> bool:
        """update groups for a user based on his current group memberships. 
        Will add or remove roles of a user as needed.
        
        Returns:
        - True on success
        - None if user is no longer a member of the Discord server
        - False on error or raises exception
        """
        role_names = DiscordUser.objects.user_group_names(self.user)        
        client = DiscordUser.objects._bot_client()
        requested_role_ids = self._guild_get_or_create_role_ids(client, role_names)
        logger.debug(
            'Requested to update groups for user %s: %s', self.user, requested_role_ids
        )        
        success = client.modify_guild_member(
            guild_id=DISCORD_GUILD_ID,
            user_id=self.uid,
            role_ids=requested_role_ids
        )
        if success:
            logger.info('Groups for %s have been updated', self.user)
        else:
            logger.warning('Failed to update groups for %s', self.user)
        return success

    def update_username(self) -> bool:
        """Updates the username incl. the discriminator 
        from the Discord server and saves it
                
        Returns:
        - True on success
        - None if user is no longer a member of the Discord server
        - False on error or raises exception
        """        
    
        client = DiscordUser.objects._bot_client()            
        user_info = client.guild_member(guild_id=DISCORD_GUILD_ID, user_id=self.uid)
        if user_info is None:
            success = None
        elif (
            user_info 
            and 'user' in user_info 
            and 'username' in user_info['user'] 
            and 'discriminator' in user_info['user']
        ):            
            self.username = user_info['user']['username']
            self.discriminator = user_info['user']['discriminator']
            self.save()
            logger.info('Username for %s has been updated', self.user)
            success = True
        else:
            logger.warning('Failed to update username for %s', self.user)
            success = False
        return success
                
    def delete_user(
        self, notify_user: bool = False, is_rate_limited: bool = True
    ) -> bool:
        """Deletes the Discount user both on the server and locally

        Params:
        - notify_user: When True will sent a notification to the user 
        informing him about the deleting of his account
        - is_rate_limited: When False will disable default rate limiting (use with care)
        
        Returns True when successful, otherwise False or raises exceptions
        Return None if user does no longer exist
        """
        try:
            client = DiscordUser.objects._bot_client(is_rate_limited=is_rate_limited)
            success = client.remove_guild_member(
                guild_id=DISCORD_GUILD_ID, user_id=self.uid
            )
            if success is not False:
                deleted_count, _ = self.delete()
                if deleted_count > 0:
                    if notify_user:
                        notify(
                            user=self.user, 
                            title=gettext_lazy('Discord Account Disabled'), 
                            message=gettext_lazy(
                                'Your Discord account was disabeled automatically '
                                'by Auth. If you think this was a mistake, '
                                'please contact an admin.'
                            ),
                            level='warning'
                        )
                    logger.info('Account for user %s was deleted.', self.user)
                    return True
                else:
                    logger.debug('Account for user %s was already deleted.', self.user)
                    return None
            
            else:
                logger.warning(
                    'Failed to remove user %s from the Discord server', self.user
                )
                return False
        
        except (HTTPError, ConnectionError, DiscordApiBackoff) as ex:
            logger.exception(
                'Failed to remove user %s from Discord server: %s', self.user, ex
            )
            return False        

    @staticmethod
    def _guild_get_or_create_role_ids(client: DiscordClient, role_names: list) -> list:
        """wrapper for DiscordClient.match_guild_roles_to_names()
        that only returns the list of IDs
        """
        return [
            x[0]['id'] for x in client.match_guild_roles_to_names(
                guild_id=DISCORD_GUILD_ID, role_names=role_names
            )
        ]
