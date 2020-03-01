from django.contrib import admin
from .models import Subject, Post, MyComment, Content


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created', 'publish', 'status']
    list_filter = ['status', 'created', 'subject', 'owner', 'publish']
    search_fields = ['title',]
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('owner',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(MyComment)
class MyCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')



@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('post', 'content_type', 'object_id', 'item', 'order')
