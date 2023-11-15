from django.contrib import admin
from blog.models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "created_at"]
    list_filter = ["status", "created_at"]
    fieldsets = (
        ("Genaral", {"fields": ("author", "category", "title", "content", "status")}),
        ("Important Times", {"fields": ("published_at",)}),
    )
    add_fieldsets = (
        ("Genaral", {"fields": ("author", "category", "title", "content", "status")}),
        ("Important Times", {"fields": ("published_at",)}),
    )
