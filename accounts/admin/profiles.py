from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name"]
    search_fields = ["user", "first_name", "last_name"]
    ordering = ["user"]
    list_filter = ["user", "first_name", "last_name"]
