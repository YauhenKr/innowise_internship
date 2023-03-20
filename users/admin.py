from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional info',
            {
                'fields': (
                    'mobile_phone',
                )
            }
        )
    )


admin.site.register(User, CustomUserAdmin)
