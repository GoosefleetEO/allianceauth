from django.contrib import admin

from .models import DiscordUser
from ...admin import ServicesUserAdmin


@admin.register(DiscordUser)
class DiscordUserAdmin(ServicesUserAdmin):            
    list_display = ServicesUserAdmin.list_display + ('_uid',)
    search_fields = ServicesUserAdmin.search_fields + ('uid', )
   
    def _uid(self, obj):
        return obj.uid
    
    _uid.short_description = 'Discord ID (UID)'
    _uid.admin_order_field = 'uid'

