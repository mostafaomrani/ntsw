from django.contrib import admin
from .models import CustomUser, VerificationCode


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'mobile',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'is_mobile_verified',
    )

    search_fields = [
        'username',
        'mobile',
        'first_name',
        'last_name',
    ]


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'uuid',
        'created_at',
        'verification_code',
        'is_valid',
    )
