from django.contrib import admin

from .models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'created_at')
    list_filter = ('title', 'category', 'created_at')
    search_fields = ('title',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        self.exclude = ('likes',)

        form = super(PostAdmin, self).get_form(request, obj, **kwargs)
        return form


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
