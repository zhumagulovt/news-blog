from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'created_at')
    list_filter = ('title', 'category', 'created_at')
    search_fields = ('title',)
