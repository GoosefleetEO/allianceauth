from django.conf import settings

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as BaseUser, \
    Permission as BasePermission
from django.db.models import Q, F
from allianceauth.services.hooks import ServicesHook
from django.db.models.signals import pre_save, post_save, pre_delete, \
    post_delete, m2m_changed
from django.dispatch import receiver
from django.forms import ModelForm
from django.utils.html import format_html
from django.utils.text import slugify

from allianceauth.authentication.models import State, get_guest_state,\
    CharacterOwnership, UserProfile, OwnershipRecord
from allianceauth.hooks import get_hooks
from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo

if 'allianceauth.eveonline.autogroups' in settings.INSTALLED_APPS:
    _has_auto_groups = True
    from allianceauth.eveonline.autogroups.models import *
else:
    _has_auto_groups = False


def make_service_hooks_update_groups_action(service):
    """
    Make a admin action for the given service
    :param service: services.hooks.ServicesHook
    :return: fn to update services groups for the selected users
    """
    def update_service_groups(modeladmin, request, queryset):
        for user in queryset:  # queryset filtering doesn't work here?
            service.update_groups(user)

    update_service_groups.__name__ = str('update_{}_groups'.format(slugify(service.name)))
    update_service_groups.short_description = "Sync groups for selected {} accounts".format(service.title)
    return update_service_groups


def make_service_hooks_sync_nickname_action(service):
    """
    Make a sync_nickname admin action for the given service
    :param service: services.hooks.ServicesHook
    :return: fn to sync nickname for the selected users
    """
    def sync_nickname(modeladmin, request, queryset):
        for user in queryset:  # queryset filtering doesn't work here?
            service.sync_nickname(user)

    sync_nickname.__name__ = str('sync_{}_nickname'.format(slugify(service.name)))
    sync_nickname.short_description = "Sync nicknames for selected {} accounts".format(service.title)
    return sync_nickname


class QuerysetModelForm(ModelForm):
    # allows specifying FK querysets through kwarg
    def __init__(self, querysets=None, *args, **kwargs):
        querysets = querysets or {}
        super().__init__(*args, **kwargs)
        for field, qs in querysets.items():
            self.fields[field].queryset = qs


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    readonly_fields = ('state',)
    form = QuerysetModelForm
    verbose_name = ''
    verbose_name_plural = 'Profile'

    def get_formset(self, request, obj=None, **kwargs):
        # main_character field can only show current value or unclaimed alts
        # if superuser, allow selecting from any unclaimed main
        query = Q()
        if obj and obj.profile.main_character:
            query |= Q(pk=obj.profile.main_character_id)
            if request.user.is_superuser:
                query |= Q(userprofile__isnull=True)
            else:
                query |= Q(character_ownership__user=obj)
        qs = EveCharacter.objects.filter(query)
        formset = super().get_formset(request, obj=obj, **kwargs)

        def get_kwargs(self, index):
            return {'querysets': {'main_character': EveCharacter.objects.filter(query)}}
        formset.get_form_kwargs = get_kwargs
        return formset

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class RealGroupsFilter(admin.SimpleListFilter):
    """Custom filter to get groups w/o Autogroups"""
    title = 'group'
    parameter_name = 'real_groups'

    def lookups(self, request, model_admin):
        qs = Group.objects.all().order_by('name')
        if _has_auto_groups:
            qs = qs\
                .filter(managedalliancegroup__exact=None)\
                .filter(managedcorpgroup__exact=None)
        return tuple([(x.pk, x.name) for x in qs])

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        else:    
            return queryset.filter(groups__pk=self.value())


class MainCorporationsFilter(admin.SimpleListFilter):
    """Custom filter to show corporations from mains only"""
    title = 'corporation'
    parameter_name = 'main_corporations'

    def lookups(self, request, model_admin):
        qs = EveCharacter.objects\
            .exclude(userprofile=None)\
            .values('corporation_id', 'corporation_name')\
            .distinct()
        return tuple([
           (x['corporation_id'], x['corporation_name']) for x in qs
        ])

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        else:    
            return queryset\
                .filter(profile__main_character__corporation_id=self.value())


class MainAllianceFilter(admin.SimpleListFilter):
    """Custom filter to show alliances from mains only"""
    title = 'alliance'
    parameter_name = 'main_alliances'

    def lookups(self, request, model_admin):
        qs = EveCharacter.objects\
            .exclude(alliance_id=None)\
            .exclude(userprofile=None)\
            .values('alliance_id', 'alliance_name')\
            .distinct()
        return tuple([
            (x['alliance_id'], x['alliance_name']) for x in qs
        ])

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        else:    
            return queryset\
                .filter(profile__main_character__alliance_id=self.value())


class UserAdmin(BaseUserAdmin):
    """
    Extending Django's UserAdmin model
    """
    def get_actions(self, request):
        actions = super(BaseUserAdmin, self).get_actions(request)

        for hook in get_hooks('services_hook'):
            svc = hook()
            # Check update_groups is redefined/overloaded
            if svc.update_groups.__module__ != ServicesHook.update_groups.__module__:
                action = make_service_hooks_update_groups_action(svc)
                actions[action.__name__] = (action,
                                            action.__name__,
                                            action.short_description)
            # Create sync nickname action if service implements it
            if svc.sync_nickname.__module__ != ServicesHook.sync_nickname.__module__:
                action = make_service_hooks_sync_nickname_action(svc)
                actions[action.__name__] = (action,
                                            action.__name__,
                                            action.short_description)

        return actions
    
    inlines = BaseUserAdmin.inlines + [UserProfileInline]

    ordering = ('username', )
    list_select_related = True    
    show_full_result_count = True 
    
    list_display = (
        '_profile_pic',
        '_user',                 
        '_state', 
        '_groups',
        '_main_organization',        
        '_characters',
        'is_active',
        'date_joined',
        '_role'
    )    
    list_display_links = None

    list_filter = ( 
        'profile__state',
        RealGroupsFilter,
        #'profile__main_character__corporation_name', 
        MainCorporationsFilter,
        #'profile__main_character__alliance_name',
        MainAllianceFilter,
        'is_active',
        'date_joined',
        'is_staff',
        'is_superuser'
    )
    search_fields = (
        'username', 
        'character_ownerships__character__character_name',
        'groups__name'
    )

    def _profile_pic(self, obj):
        if obj.profile.main_character:
            return format_html(
                '<img src="{}" style="border-radius: 50%;">',
                obj.profile.main_character.portrait_url(size=32)
            )
        else:
            return ''
    _profile_pic.short_description = ''


    def _user(self, obj):
        #/admin/<app>/<model>/<pk>/change/
        link = '/admin/authentication/{}/{}/change/'.format(            
            type(obj).__name__.lower(),
            obj.pk
        )
        return format_html(
            '<strong><a href="{}">{}</a></strong><br>{}',
            link, 
            obj.username,
            obj.profile.main_character.character_name \
                if obj.profile.main_character else ''
        )
    
    _user.short_description = 'user / main'
    _user.admin_order_field = 'username'

    def _main_organization(self, obj):
        if obj.profile.main_character:
            corporation = obj.profile.main_character.corporation_name
        else:
            corporation = ''
        if (obj.profile.main_character 
            and obj.profile.main_character.alliance_id
        ):
            alliance = obj.profile.main_character.alliance_name
        else:
            alliance = ''
        return format_html('{}<br>{}',
            corporation, 
            alliance
        )

    _main_organization.short_description = 'Corporation / Alliance (Main)'
    _main_organization.admin_order_field = \
        'profile__main_character__corporation_name'


    def _characters(self, obj):
        return [
            x.character.character_name 
            for x in CharacterOwnership.objects\
                .filter(user=obj)\
                .order_by('character__character_name')
        ]        
          
    _characters.short_description = 'characters'
    

    def _state(self, obj):
        return obj.profile.state
    
    _state.short_description = 'state'
    _state.admin_order_field = 'profile__state'


    def _groups(self, obj):
        if not _has_auto_groups:
            my_groups = [x.name for x in obj.groups.order_by('name')]
        else:
            my_groups = [
                x.name for x in obj.groups\
                    .filter(managedalliancegroup=None)\
                    .filter(managedcorpgroup=None)\
                    .order_by('name')
            ]
        
        return ', '.join(my_groups)

    _groups.short_description = 'groups'


    def _role(self, obj):
        if obj.is_superuser:
            role = 'Superuser'
        elif obj.is_staff:
            role = 'Staff'
        else:
            role = 'User'
        
        return role
    
    _role.short_description = 'role'
    

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('auth.change_user')

    def has_add_permission(self, request, obj=None):
        return request.user.has_perm('auth.add_user')

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('auth.delete_user')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'permissions', 'priority'),
        }),
        ('Membership', {
            'fields': ('public', 'member_characters', 'member_corporations', 'member_alliances'),
        })
    )
    filter_horizontal = ['member_characters', 'member_corporations', 'member_alliances', 'permissions']
    list_display = ('name', 'priority', 'user_count')

    def has_delete_permission(self, request, obj=None):
        if obj == get_guest_state():
            return False
        return super(StateAdmin, self).has_delete_permission(request, obj=obj)

    def get_fieldsets(self, request, obj=None):
        if obj == get_guest_state():
            return (
                (None, {
                    'fields': ('permissions', 'priority'),
                }),
            )
        return super(StateAdmin, self).get_fieldsets(request, obj=obj)

    @staticmethod
    def user_count(obj):
        return obj.userprofile_set.all().count()


class BaseOwnershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'character')
    search_fields = ('user__user', 'character__character_name', 'character__corporation_name', 'character__alliance_name')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.pk:
            return 'owner_hash', 'character'
        return tuple()


@admin.register(OwnershipRecord)
class OwnershipRecordAdmin(BaseOwnershipAdmin):
    list_display = BaseOwnershipAdmin.list_display + ('created',)


@admin.register(CharacterOwnership)
class CharacterOwnershipAdmin(BaseOwnershipAdmin):
    def has_add_permission(self, request):
        return False


class PermissionAdmin(admin.ModelAdmin):
    actions = None
    readonly_fields = [field.name for field in BasePermission._meta.fields]
    list_display = ('admin_name', 'name', 'codename', 'content_type')
    list_filter = ('content_type__app_label',)

    @staticmethod
    def admin_name(obj):
        return str(obj)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        # can see list but not edit it
        return not obj


# Hack to allow registration of django.contrib.auth models in our authentication app
class User(BaseUser):
    class Meta:
        proxy = True
        verbose_name = BaseUser._meta.verbose_name
        verbose_name_plural = BaseUser._meta.verbose_name_plural


class Permission(BasePermission):
    class Meta:
        proxy = True
        verbose_name = BasePermission._meta.verbose_name
        verbose_name_plural = BasePermission._meta.verbose_name_plural


try:
    admin.site.unregister(BaseUser)
finally:
    admin.site.register(User, UserAdmin)
    admin.site.register(Permission, PermissionAdmin)


@receiver(pre_save, sender=User)
def redirect_pre_save(sender, signal=None, *args, **kwargs):
    pre_save.send(BaseUser, *args, **kwargs)


@receiver(post_save, sender=User)
def redirect_post_save(sender, signal=None, *args, **kwargs):
    post_save.send(BaseUser, *args, **kwargs)


@receiver(pre_delete, sender=User)
def redirect_pre_delete(sender, signal=None, *args, **kwargs):
    pre_delete.send(BaseUser, *args, **kwargs)


@receiver(post_delete, sender=User)
def redirect_post_delete(sender, signal=None, *args, **kwargs):
    post_delete.send(BaseUser, *args, **kwargs)


@receiver(m2m_changed, sender=User.groups.through)
def redirect_m2m_changed_groups(sender, signal=None, *args, **kwargs):
    m2m_changed.send(BaseUser, *args, **kwargs)


@receiver(m2m_changed, sender=User.user_permissions.through)
def redirect_m2m_changed_permissions(sender, signal=None, *args, **kwargs):
    m2m_changed.send(BaseUser, *args, **kwargs)
