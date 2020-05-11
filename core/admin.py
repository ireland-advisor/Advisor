from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models
from .models import MentoringTags, SeekingTags


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["id", "email", "first_name", "last_name", "okta_id"]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ("first_name", "last_name",)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(MentoringTags)
admin.site.register(SeekingTags)
