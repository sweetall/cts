# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import *


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = u'用户详情'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'chinese_name', 'nickname')
    search_fields = ('chinese_name',)
    list_filter = ('chinese_name', )


class VersionRecordAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('number', 'value')}),)
    list_display = ('number', 'value')
    search_fields = ('number',)
    list_filter = ('number', )

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(VersionRecord, VersionRecordAdmin)
