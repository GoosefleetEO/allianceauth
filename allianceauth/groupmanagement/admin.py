from django.conf import settings

from django.contrib import admin
from django.contrib.auth.models import Group as BaseGroup
from django.db.models import Count
from django.db.models.signals import pre_save, post_save, pre_delete, \
    post_delete, m2m_changed
from django.dispatch import receiver

from .models import AuthGroup
from .models import GroupRequest
from . import signals

if 'allianceauth.eveonline.autogroups' in settings.INSTALLED_APPS:
    _has_auto_groups = True
    from allianceauth.eveonline.autogroups.models import *
else:
    _has_auto_groups = False


class AuthGroupInlineAdmin(admin.StackedInline):
    model = AuthGroup
    filter_horizontal = ('group_leaders', 'group_leader_groups', 'states',)
    fields = ('description', 'group_leaders', 'group_leader_groups', 'states', 'internal', 'hidden', 'open', 'public')
    verbose_name_plural = 'Auth Settings'
    verbose_name = ''

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('auth.change_group')


if _has_auto_groups:
    class IsAutoGroupFilter(admin.SimpleListFilter):
        title = 'auto group'
        parameter_name = 'auto_group'

        def lookups(self, request, model_admin):
            return (
                ('Yes', 'Yes'),
                ('No', 'No'),
            )

        def queryset(self, request, queryset):
            value = self.value()
            if value == 'Yes':
                return queryset.exclude(
                    managedalliancegroup__exact=None, 
                    managedcorpgroup__exact=None
                )
            elif value == 'No':
                return queryset.filter(managedalliancegroup__exact=None).filter(managedcorpgroup__exact=None)
            else:
                return queryset


class GroupAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'name', 
        'description', 
        'member_count', 
        'has_leader', 
        '_attributes'
    )

    list_filter = (
        'authgroup__internal', 
        'authgroup__hidden', 
        'authgroup__open', 
        'authgroup__public',
        IsAutoGroupFilter
    )
    
    filter_horizontal = ('permissions',)
    inlines = (AuthGroupInlineAdmin,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _member_count=Count('user', distinct=True),            
        )        
        return queryset

    def description(self, obj):
        return obj.authgroup.description

    def member_count(self, obj):
        return obj._member_count

    member_count.admin_order_field = '_member_count'
    
    def has_leader(self, obj):
        return obj.authgroup.group_leaders.exists()
    
    has_leader.boolean = True

    def _attributes(self, obj):
        attributes = list()
        if _has_auto_groups and (obj.managedalliancegroup_set.exists() 
                or obj.managedcorpgroup_set.exists()
            ):
            attributes.append('Auto Group')
        elif obj.authgroup.internal:
            attributes.append('Internal')
        else:
            if obj.authgroup.hidden:
                attributes.append('Hidden')
            if obj.authgroup.open:
                attributes.append('Open')
            if obj.authgroup.public:
                attributes.append('Public')
        if not attributes:
            attributes.append('Default')
        
        return ', '.join(attributes)

    _attributes.short_description = "Attributes"

class Group(BaseGroup):
    class Meta:
        proxy = True
        verbose_name = BaseGroup._meta.verbose_name
        verbose_name_plural = BaseGroup._meta.verbose_name_plural

try:
    admin.site.unregister(BaseGroup)
finally:
    admin.site.register(Group, GroupAdmin)


admin.site.register(GroupRequest)


@receiver(pre_save, sender=Group)
def redirect_pre_save(sender, signal=None, *args, **kwargs):
    pre_save.send(BaseGroup, *args, **kwargs)


@receiver(post_save, sender=Group)
def redirect_post_save(sender, signal=None, *args, **kwargs):
    post_save.send(BaseGroup, *args, **kwargs)


@receiver(pre_delete, sender=Group)
def redirect_pre_delete(sender, signal=None, *args, **kwargs):
    pre_delete.send(BaseGroup, *args, **kwargs)


@receiver(post_delete, sender=Group)
def redirect_post_delete(sender, signal=None, *args, **kwargs):
    post_delete.send(BaseGroup, *args, **kwargs)


@receiver(m2m_changed, sender=Group.permissions.through)
def redirect_m2m_changed_permissions(sender, signal=None, *args, **kwargs):
    m2m_changed.send(BaseGroup, *args, **kwargs)
