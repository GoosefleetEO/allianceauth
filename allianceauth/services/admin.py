from django import forms
from django.contrib import admin
from django.db.models.functions import Lower
from django.utils.html import format_html

from allianceauth import hooks
from allianceauth.eveonline.models import EveCharacter

from .models import NameFormatConfig


class MainCorporationsFilter(admin.SimpleListFilter):
    """Custom filter to show corporations from service users only
    To be used together with ServicesUserAdmin class
    """
    title = 'corporation'
    parameter_name = 'main_corporations'

    def lookups(self, request, model_admin):        
        qs = EveCharacter.objects\
            .exclude(userprofile=None)\
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
    """Custom filter to show alliances from service users only
    To be used together with ServicesUserAdmin class
    """
    title = 'alliance'
    parameter_name = 'main_alliances'

    def lookups(self, request, model_admin):
        qs = EveCharacter.objects\
            .exclude(alliance_id=None)\
            .exclude(userprofile=None)\
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


class ServicesUserAdmin(admin.ModelAdmin):
    """Parent class for UserAdmin classes for all services"""
    class Media:
        css = {
            "all": ("services/admin.css",)
        }

    search_fields = (
        'user__username', 
        'uid'
    )
    ordering = ('user__username', )
    list_select_related = True              
    list_display = (
        '_profile_pic',
        '_user',                         
        '_main_organization',        
        '_date_joined'
    )
    list_filter = (        
        MainCorporationsFilter,        
        MainAllianceFilter,
        'user__date_joined'
    )

    def _profile_pic(self, obj):
        if obj.user.profile.main_character:
            return format_html(
                '<img src="{}" class="img-circle">',
                obj.user.profile.main_character.portrait_url(size=32)
            )
        else:
            return ''
    _profile_pic.short_description = ''


    def _user(self, obj):
        link = '/admin/{}/{}/{}/change/'.format(            
            __package__.rsplit('.', 1)[-1],
            type(obj).__name__.lower(),
            obj.pk
        )
        return format_html(
            '<strong><a href="{}">{}</a></strong><br>{}',
            link, 
            obj.user.username,
            obj.user.profile.main_character.character_name \
                if obj.user.profile.main_character else ''
        )
    
    _user.short_description = 'user / main'
    _user.admin_order_field = 'user__username'

    
    def _main_organization(self, obj):
        if obj.user.profile.main_character:
            corporation = obj.user.profile.main_character.corporation_name
        else:
            corporation = ''
        if (obj.user.profile.main_character 
            and obj.user.profile.main_character.alliance_id
        ):
            alliance = obj.user.profile.main_character.alliance_name
        else:
            alliance = ''
        return format_html('{}<br>{}',
            corporation, 
            alliance
        )

    _main_organization.short_description = 'Corporation / Alliance (Main)'
    _main_organization.admin_order_field = \
        'profile__main_character__corporation_name'


    def _date_joined(self, obj):
        return obj.user.date_joined
    
    _date_joined.short_description = 'date joined'
    _date_joined.admin_order_field = 'user__date_joined'


class NameFormatConfigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NameFormatConfigForm, self).__init__(*args, **kwargs)
        SERVICE_CHOICES = [(s.name, s.name) for h in hooks.get_hooks('services_hook') for s in [h()]]
        if self.instance.id:
            current_choice = (self.instance.service_name, self.instance.service_name)
            if current_choice not in SERVICE_CHOICES:
                SERVICE_CHOICES.append(current_choice)
        self.fields['service_name'] = forms.ChoiceField(choices=SERVICE_CHOICES)


class NameFormatConfigAdmin(admin.ModelAdmin):
    form = NameFormatConfigForm
    list_display = ('service_name', 'get_state_display_string')

    def get_state_display_string(self, obj):
        return ', '.join([state.name for state in obj.states.all()])
    get_state_display_string.short_description = 'States'


admin.site.register(NameFormatConfig, NameFormatConfigAdmin)
