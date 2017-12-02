# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from serializers import *
from models import *
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.filters import SearchFilter
from rest_framework import status, mixins
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django.core import serializers
from rest_framework import permissions, generics, renderers, parsers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import detail_route

from core.libs.pagination import StandardResultsSetPagination


class ArticleListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Article.objects.select_related('category',).filter(state=1).order_by('-create_time')
    serializer_class = ArticleListSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title', 'content', 'label')
    filter_fields = ('category', 'creator')
    pagination_class = StandardResultsSetPagination


class ArticleRetrieveViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('category',).order_by('-create_time')
    serializer_class = ArticleRetrieveSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ('category', 'creator')
    pagination_class = StandardResultsSetPagination

    # 重写retrieve
    def retrieve(self, request, *args, **kwargs):
        article = self.get_object()
        pk = article.id

        comment_query = Comment.objects.filter(article=pk)
        comment_count = comment_query.count()
        vote_count = Vote.objects.filter(article=pk).count()
        collect_count = Collect.objects.filter(article=pk).count()

        article.summary.click_count = int(article.summary.click_count) + 1
        article.summary.comment_count = comment_count
        article.summary.vote_count = vote_count
        article.summary.collect_count = collect_count
        article.summary.save()
        serializer = self.get_serializer(article)

        data = serializer.data

        if Collect.objects.filter(creator=request.user, article=pk).exists():
            data['collect_state'] = True
        else:
            data['collect_state'] = False

        if Vote.objects.filter(creator=request.user, article=pk).exists():
            data['vote_state'] = True
        else:
            data['vote_state'] = False

        return Response(data)

    @detail_route()
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @detail_route()
    def perform_update(self, serializer):
        serializer.save(update_by=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ('article', )

    @detail_route()
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @detail_route()
    def perform_update(self, serializer):
        serializer.save(update_by=self.request.user)


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ('creator', 'article')
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        if Collect.objects.filter(creator=self.request.user).filter(article=request.data['article']).exists():
            return Response({'status': False, 'message': 'already exist!'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @detail_route()
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @detail_route()
    def perform_update(self, serializer):
        serializer.save(update_by=self.request.user)


# cancel collect
class CancelCollect(APIView):
    def get(self, request, pk):
        collect_query = Collect.objects.filter(creator=request.user).filter(article=pk)
        if collect_query.exists():
            collect_query.delete()
            return Response({'status': True, 'message': 'Done'})
        else:
            return Response({'status': False, 'message': 'Not exist!'})


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        if Vote.objects.filter(creator=self.request.user).filter(article=request.data['article']).exists():
            return Response({'status': False, 'message': 'already exist!'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @detail_route()
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @detail_route()
    def perform_update(self, serializer):
        serializer.save(update_by=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('article',).order_by('-create_time')
    serializer_class = MessageSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ('author',)
    pagination_class = StandardResultsSetPagination

    @detail_route()
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @detail_route()
    def perform_update(self, serializer):
        serializer.save(update_by=self.request.user)


class MessageListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('author',)


# cancel vote
class CancelVote(APIView):
    def get(self, request, pk):
        collect_query = Vote.objects.filter(creator=request.user).filter(article=pk)
        if collect_query.exists():
            collect_query.delete()
            return Response({'status': True, 'message': 'Done'})
        else:
            return Response({'status': False, 'message': 'Not exist!'})


class NavigationViewSet(viewsets.ModelViewSet):
    queryset = Navigation.objects.all().order_by('-id')
    serializer_class = NavigationSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if int(instance.id) == 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if int(instance.id) == 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class VoteTop5(APIView):

    def get(self, request):
        article_query = Article.objects.filter(state=1).order_by('-summary__vote_count')[:5]
        data = ArticleListSerializer(article_query, many=True).data
        for n in range(len(data)):
            if len(data[n]['title']) > 9:
                data[n]['title'] = data[n]['title'][0:13] + '...'
        return Response(data=data)


class ClickTop5(APIView):

    def get(self, request):
        author = request.GET.get('creator', 0)
        if author:
            article_query = Article.objects.filter(state=1).filter(creator=author).order_by('-summary__click_count')[:5]
            data = ArticleListSerializer(article_query, many=True).data
        else:
            article_query = Article.objects.filter(state=1).order_by('-summary__click_count')[:5]
            data = ArticleListSerializer(article_query, many=True).data
        for n in range(len(data)):
            if len(data[n]['title']) > 9:
                data[n]['title'] = data[n]['title'][0:13] + '...'
        return Response(data=data)


class CommentTop5(APIView):

    def get(self, request):
        article_query = Article.objects.filter(state=1).order_by('-summary__comment_count')[:5]
        data = ArticleListSerializer(article_query, many=True).data
        for n in range(len(data)):
            if len(data[n]['title']) > 9:
                data[n]['title'] = data[n]['title'][0:13] + '...'
        return Response(data=data)


class CollectTop5(APIView):

    def get(self, request):
        article_query = Article.objects.filter(state=1).order_by('-summary__collect_count')[:5]
        data = ArticleListSerializer(article_query, many=True).data
        for n in range(len(data)):
            if len(data[n]['title']) > 9:
                data[n]['title'] = data[n]['title'][0:13] + '...'
        return Response(data=data)



