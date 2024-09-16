from django.contrib import admin

from .models import Post, Group, Comment, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'group')
    search_fields = ('text',)
    list_filter = ('author', 'pub_date', 'group')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created')
    search_fields = ('text',)
    list_filter = ('author', 'created', 'post')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    list_filter = ('user',)
