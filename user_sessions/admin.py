from django.contrib import admin
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from user_sessions.templatetags.user_sessions import device, location

from .models import Session


class ExpiredFilter(admin.SimpleListFilter):
    title = _('Is Valid')
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Active')),
            ('0', _('Expired'))
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(expire_date__gt=now())
        elif self.value() == '0':
            return queryset.filter(expire_date__lte=now())


class OwnerFilter(admin.SimpleListFilter):
    title = _('Owner')
    parameter_name = 'owner'

    def lookups(self, request, model_admin):
        return (
            ('my', _('Self')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'my':
            return queryset.filter(user=request.user)


class SessionAdmin(admin.ModelAdmin):
    list_display = 'ip', 'user', 'is_valid', 'location', 'device',
    search_fields = 'user__username',
    list_filter = ExpiredFilter, OwnerFilter

    def is_valid(self, obj):
        return obj.expire_date > now()
    is_valid.boolean = True

    def location(self, obj):
        return location(obj.ip)

    def device(self, obj):
        return device(obj.user_agent)
admin.site.register(Session, SessionAdmin)
