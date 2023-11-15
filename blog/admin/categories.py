from django.contrib import admin
from blog.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]
    fieldsets = (("Genaral", {"fields": ("name",)}),)
    add_fieldsets = (("Genaral", {"fields": ("name",)}),)
