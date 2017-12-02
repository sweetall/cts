# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from core.models import UserProfile, UserMixin, DateMixin


STAT_CHOICES = (
    (1, u'发布'),
    (2, u'隐藏'),
    (3, u'存稿'),
)
MESSAGE_STATUS = (
    (1, u'评论'),
    (2, u'收藏'),
    (3, u'赞'),
)


# navigation
class Navigation(models.Model):
    value = models.CharField(max_length=200, verbose_name=u'导航')
    describe = models.CharField(max_length=200, verbose_name=u'说明')

    class Meta:
        verbose_name = u'导航表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.value


# category
class Category(models.Model):
    value = models.CharField(max_length=200, verbose_name=u'分类')
    describe = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'说明')
    navigation = models.ForeignKey('Navigation', related_name='categories', verbose_name=u'导航索引')

    class Meta:
        verbose_name = u'分类表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.value


# article
class Article(UserMixin, DateMixin):
    title = models.CharField(max_length=200, verbose_name=u'标题')
    label = models.CharField(null=True, blank=True, max_length=200, verbose_name=u'标签')
    content = models.TextField(verbose_name=u'正文')
    file_field = models.FileField(upload_to='document/%Y/%m', null=True, blank=True, verbose_name=u'附件')
    state = models.IntegerField(choices=STAT_CHOICES, default=1, verbose_name=u'状态')
    category = models.ForeignKey('Category', related_name='articles', verbose_name=u'分类', on_delete=models.SET(1))

    class Meta:
        verbose_name = u'博文表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
        # return '%d: %s' % (self.id, self.title)


# summary
class Summary(models.Model):
    article = models.OneToOneField(Article, unique=True, verbose_name=u'博文')
    click_count = models.IntegerField(default=0, verbose_name=u'点击量')
    comment_count = models.IntegerField(default=0, verbose_name=u'评论量')
    vote_count = models.IntegerField(default=0, verbose_name=u'点赞量')
    collect_count = models.IntegerField(default=0, verbose_name=u'收藏量')

    class Meta:
        verbose_name = u'汇总表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.article.title


def create_summary(sender, instance, created, **kwargs):
    if created:
        Summary.objects.get_or_create(article=instance)

post_save.connect(create_summary, sender=Article)


#  comment
class Comment(UserMixin, DateMixin):
    value = models.CharField(max_length=500, verbose_name=u'评论')
    article = models.ForeignKey('Article', related_name='comments', verbose_name=u'博文索引')

    class Meta:
        verbose_name = u'评论表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.value


# collect
class Collect(UserMixin, DateMixin):
    article = models.ForeignKey('Article', related_name='collectors', verbose_name=u'博文索引')

    class Meta:
        verbose_name = u'收藏表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.article.title


# vote
class Vote(UserMixin, DateMixin):
    article = models.ForeignKey('Article', related_name='voters',  verbose_name=u'博文索引')

    class Meta:
        verbose_name = u'点赞表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.article.title


# message
class Message(UserMixin, DateMixin):
    article = models.ForeignKey('Article', verbose_name=u'博文')
    author = models.ForeignKey(User, related_name='messages', verbose_name=u'作者')
    value = models.CharField(max_length=200, blank=True, null=True, verbose_name='内容')
    status = models.IntegerField(choices=MESSAGE_STATUS, default=1, verbose_name=u'消息类型')

    class Meta:
        verbose_name = u'消息表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.value


def create_message(sender, instance, created, **kwargs):
    if created:
        if instance.creator == instance.article.creator:
            return
        if sender == Comment:
            value = '评论了你：' + instance.value
            status = 1
        elif sender == Collect:
            value = '收藏了你'
            status = 2
        elif sender == Vote:
            value = '赞了你'
            status = 3
        else:
            value = ''
            status = 1
        Message.objects.create(article=instance.article, author=instance.article.creator,
                               value=value, status=status, creator=instance.creator)

post_save.connect(create_message, sender=Comment)
post_save.connect(create_message, sender=Collect)
post_save.connect(create_message, sender=Vote)
