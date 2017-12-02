# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.conf import settings
from urllib import unquote

from models import *
from core.models import UserProfile


class SummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Summary
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    portrait = serializers.StringRelatedField(source='creator.userprofile.portrait')
    nickname = serializers.StringRelatedField(source='creator.userprofile.nickname')
    username = serializers.StringRelatedField(source='creator.username')

    create_time = serializers.SerializerMethodField()
    modify_time = serializers.SerializerMethodField()

    def get_create_time(self, obj):
        return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_modify_time(self, obj):
        return obj.modify_time.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comment
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):
    portrait = serializers.StringRelatedField(source='creator.userprofile.portrait')
    nickname = serializers.StringRelatedField(source='creator.userprofile.nickname')
    username = serializers.StringRelatedField(source='creator.username')
    content = serializers.SerializerMethodField()
    category_value = serializers.StringRelatedField(source='category.value')
    summary = SummarySerializer(read_only=True)

    create_time = serializers.SerializerMethodField()
    modify_time = serializers.SerializerMethodField()

    def get_create_time(self, obj):
        return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_modify_time(self, obj):
        return obj.modify_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_content(self, obj):
        return strip_tags(obj.content)[:100].replace('\r\n', '').replace('\t', '') + '...'

    class Meta:
        model = Article
        fields = '__all__'


class ArticleRetrieveSerializer(serializers.ModelSerializer):
    portrait = serializers.StringRelatedField(source='creator.userprofile.portrait')
    nickname = serializers.StringRelatedField(source='creator.userprofile.nickname')
    username = serializers.StringRelatedField(source='creator.username')
    category_value = serializers.StringRelatedField(source='category.value')
    state_value = serializers.SerializerMethodField()
    summary = SummarySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    file_name = serializers.SerializerMethodField()

    def get_file_name(self, obj):
        if obj.file_field:
            return unquote(obj.file_field.url[(obj.file_field.url.rfind('/')+1):]).decode('utf-8')
        else:
            return ''

    create_time = serializers.SerializerMethodField()
    modify_time = serializers.SerializerMethodField()

    def get_state_value(self, obj):
        return STAT_CHOICES[obj.state-1][1]

    def get_create_time(self, obj):
        return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_modify_time(self, obj):
        return obj.modify_time.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Article
        fields = '__all__'


class CollectSerializer(serializers.ModelSerializer):
    article_title = serializers.StringRelatedField(source='article.title')
    article_author = serializers.StringRelatedField(source='article.creator.username')
    article_category = serializers.StringRelatedField(source='article.category.value')

    create_time = serializers.SerializerMethodField()
    modify_time = serializers.SerializerMethodField()

    def get_create_time(self, obj):
        return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_modify_time(self, obj):
        return obj.modify_time.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Collect
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()
    modify_time = serializers.SerializerMethodField()

    def get_create_time(self, obj):
        return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_modify_time(self, obj):
        return obj.modify_time.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Vote
        fields = '__all__'


class NavigationSerializer(serializers.ModelSerializer):

    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ('id', 'value')

    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Navigation
        fields = ('id', 'value', 'categories')


class CategorySerializer(serializers.ModelSerializer):
    articles = ArticleListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    portrait = serializers.StringRelatedField(source='creator.userprofile.portrait')
    username = serializers.StringRelatedField(source='creator.username')
    article_title = serializers.StringRelatedField(source='article.title')

    create_time = serializers.SerializerMethodField()
    modify_time = serializers.SerializerMethodField()

    def get_create_time(self, obj):
        return obj.create_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_modify_time(self, obj):
        return obj.modify_time.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Message
        fields = '__all__'
