from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone_number', 'profile_image', 'is_verified_provider')
        }),
    )

    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_verified_provider',
        'is_staff',
        'is_active',
    )
