from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("email", "username", "first_name", "last_name")
    search_fields = ('email', 'last_name', 'username', 'first_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {
            "fields": ("username",
                       ('first_name', 'last_name'),
                       "email",
                       "is_staff",
                       "is_active",
                       'date_joined',
                       'last_login')
        }),
        ('Change password', {
            'classes': ('collapse',),
            "fields": ("password",)
        })
    )