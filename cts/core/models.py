# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserMixin(models.Model):
    creator = models.ForeignKey(User, blank=True, null=True, related_name='creator_%(class)s',
                                on_delete=models.SET_NULL, editable=False)
    modifier = models.ForeignKey(User, blank=True, null=True, related_name='modifier_%(class)s',
                                 on_delete=models.SET_NULL, editable=False)

    class Meta:
        abstract = True


class DateMixin(models.Model):
    create_time = models.DateTimeField(editable=False, auto_now_add=True)
    modify_time = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    chinese_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='中文名')
    nickname = models.CharField(max_length=20, blank=True, null=True, verbose_name='昵称')
    portrait = models.CharField(max_length=200, blank=True, null=True, default='http://up.qqjia.com/z/23/tu29190_2.jpg',
                                verbose_name='头像链接')
    signature = models.CharField(max_length=200, blank=True, null=True, verbose_name='签名')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)


class VersionRecord(models.Model):
    number = models.CharField(max_length=20, verbose_name='版本号')
    value = models.TextField(verbose_name='版本更新记录')

    class Meta:
        verbose_name = '更新记录表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.number
