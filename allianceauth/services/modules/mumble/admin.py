from django.contrib import admin
from django.db.models.functions import Lower
from allianceauth.eveonline.models import EveCharacter

from .models import MumbleUser


class MainCorporationsFilter(admin.SimpleListFilter):
    """Custom filter to show corporations from service users only"""
    title = 'corporation'
    parameter_name = 'main_corporations'

    def lookups(self, request, model_admin):
        qs = EveCharacter.objects\
            .exclude(userprofile=None)\
            .exclude(userprofile__user__mumble=None)\
            .values('corporation_id', 'corporation_name')\
            .distinct()\
            .order_by(Lower('corporation_name'))
        return tuple(
            [(x['corporation_id'], x['corporation_name']) for x in qs]
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        else:    
            return queryset\
                .filter(user__profile__main_character__corporation_id=self.value())


class MainAllianceFilter(admin.SimpleListFilter):
    """Custom filter to show alliances from service users only"""
    title = 'alliance'
    parameter_name = 'main_alliances'

    def lookups(self, request, model_admin):
        qs = EveCharacter.objects\
            .exclude(alliance_id=None)\
            .exclude(userprofile=None)\
            .exclude(userprofile__user__mumble=None)\
            .values('alliance_id', 'alliance_name')\
            .distinct()\
            .order_by(Lower('alliance_name'))
        return tuple(
            [(x['alliance_id'], x['alliance_name']) for x in qs]
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        else:    
            return queryset\
                .filter(user__profile__main_character__alliance_id=self.value())


class MumbleUserAdmin(admin.ModelAdmin):            
    ordering = ('user__username', )
    list_select_related = True  
    
    list_display = (
        'user',         
        'username',
        'groups', 
        '_corporation',
        '_alliance',        
        '_date_joined'
    )
    search_fields = (
        'user__username',
        'username',
        'groups'
    )

    list_filter = (        
        MainCorporationsFilter,        
        MainAllianceFilter,
        'user__date_joined',
    )

    fields = ('user', 'username', 'groups')  # pwhash is hidden from admin panel

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


admin.site.register(MumbleUser, MumbleUserAdmin)
