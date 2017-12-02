# -*-coding: utf-8 -*-
from django.contrib import admin
from models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('title', 'label', 'content', 'file_field', 'category', 'state')}), )
    list_display = ('title', 'label', 'file_field', 'category', 'state', 'creator', 'create_time')
    list_editable = ('category', 'state')
    list_display_links = ('title',)
    search_fields = ('state', )
    list_filter = ('creator', 'create_time')
    list_per_page = 15


class SummaryAdmin(admin.ModelAdmin):
    list_display = ('article', 'click_count', 'comment_count', 'vote_count', 'collect_count')
    search_fields = ('article',)


class CommentAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('value', 'article')}),)
    list_display = ('value', 'article', 'creator', 'create_time')
    search_fields = ('article',)
    list_filter = ('creator', )


class CollectAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('article', )}),)
    list_display = ('article', 'creator', 'create_time')
    search_fields = ('creator', )
    list_filter = ('creator', )


class VoteAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('article', )}),)
    list_display = ('article', 'creator', 'create_time')
    search_fields = ('creator',)
    list_filter = ('creator',)


class NavigationAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('value', 'describe')}),)
    list_display = ('value', 'describe')


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('value', 'describe', 'navigation')}),)
    list_display = ('value', 'describe', 'navigation')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Summary, SummaryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Collect, CollectAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Navigation, NavigationAdmin)
admin.site.register(Category, CategoryAdmin)


