from django.contrib import admin
from blog.models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    fieldsets = (
        (
            'Genaral',{
                'fields':('name',)
            }
        ),
    )
    add_fieldsets = (
        (
            'Genaral',{
                'fields':('name',)
            }
        ),
    )
    
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_time']
    list_filter = ['status', 'created_time']
    fieldsets = (
        (
            'Genaral',{
                'fields':('author', 'category', 'title', 'content', 'status')
            }
        ),
        (
            'Important Times',{
                'fields':('published_time',)
            }
        )
    )
    add_fieldsets = (
        (
            'Genaral',{
                'fields':('author', 'category', 'title', 'content', 'status')
            }
        ),
        (
            'Important Times',{
                'fields':('published_time',)
            }
        )
    )