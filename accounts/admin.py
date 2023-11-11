from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["email", "is_superuser", "is_staff", "is_active"]
    ordering = ["email"]
    list_filter = ["is_superuser", "is_staff", "is_active"]
    search_fields = ["email"]
    fieldsets = (
        ("Genaral", {"fields": ("email", "password")}),
        (
            "Permissions",
            {"fields": ("is_superuser", "is_staff", "is_active", "is_verified")},
        ),
        ("Group Permissions", {"fields": ("groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        ("Genaral", {"fields": ("email", "password1", "password2")}),
        (
            "Permissions",
            {"fields": ("is_superuser", "is_staff", "is_active", "is_verified")},
        ),
        ("Group Permissions", {"fields": ("groups", "user_permissions")}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name"]
    search_fields = ["user", "first_name", "last_name"]
    ordering = ["user"]
    list_filter = ["user", "first_name", "last_name"]
