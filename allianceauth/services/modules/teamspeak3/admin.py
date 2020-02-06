from django.contrib import admin
from .models import AuthTS, Teamspeak3User, StateGroup


class Teamspeak3UserAdmin(admin.ModelAdmin):    
    ordering = ('user__username', )
    list_select_related = True  
    
    list_display = (
        'user', 
        'uid',        
        '_corporation',
        '_alliance',        
        '_date_joined',
        'perm_key',
    )
    search_fields = (
        'user__username', 
        'uid',
        'perm_key'
    )
    list_filter = (
        'user__profile__main_character__corporation_name',
        'user__profile__main_character__alliance_name',
        'user__date_joined',
    )

    def _corporation(self, obj):
        if obj.user.profile.main_character:
            return obj.user.profile.main_character.corporation_name
        else:
            return ''
    
    _corporation.short_description = 'corporation (main)'
    _corporation.admin_order_field \
        = 'user__profile__main_character__corporation_name'


    def _alliance(self, obj):        
        if (obj.user.profile.main_character 
            and obj.user.profile.main_character.alliance_id
        ):
            return obj.user.profile.main_character.alliance_name
        else:
            return ''
    
    _alliance.short_description = 'alliance (main)'
    _alliance.admin_order_field \
        = 'user__profile__main_character__alliance_name'


    def _date_joined(self, obj):
        return obj.user.date_joined
    
    _date_joined.short_description = 'date joined'
    _date_joined.admin_order_field = 'user__date_joined'


class AuthTSgroupAdmin(admin.ModelAdmin):
    fields = ['auth_group', 'ts_group']
    filter_horizontal = ('ts_group',)


@admin.register(StateGroup)
class StateGroupAdmin(admin.ModelAdmin):
    list_display = ('state', 'ts_group')
    search_fields = ('state__name', 'ts_group__ts_group_name')


admin.site.register(AuthTS, AuthTSgroupAdmin)
admin.site.register(Teamspeak3User, Teamspeak3UserAdmin)
