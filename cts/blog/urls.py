"""contentsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from .page_views import index, retrieve, create, center, update
from .views import *

router = routers.DefaultRouter()
router.register(r'article-list', ArticleListViewSet, base_name='article-list')
router.register(r'article-retrieve', ArticleRetrieveViewSet, base_name='article-retrieve')
router.register(r'comment', CommentViewSet, base_name='comment')
router.register(r'collect', CollectViewSet, base_name='collect')
router.register(r'vote', VoteViewSet, base_name='vote')
router.register(r'navigation', NavigationViewSet, base_name='navigation')
router.register(r'category', CategoryViewSet, base_name='category')
router.register(r'message', MessageViewSet, base_name='message')
router.register(r'message-list', MessageListViewSet, base_name='message-list')

urlpatterns = [

    url(r'^$', index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', retrieve, name='retrieve'),
    url(r'^create/$', create, name='create'),
    url(r'^(?P<pk>[0-9]+)/update/$', update, name='update'),
    url(r'^center/$', center, name='center'),

    url(r'^api/', include(router.urls)),

    url(r'^api/vote_top5/$', VoteTop5.as_view()),
    url(r'^api/click_top5/$', ClickTop5.as_view()),
    url(r'^api/comment_top5/$', CommentTop5.as_view()),
    url(r'^api/collect_top5/$', CollectTop5.as_view()),

    url(r'^api/cancel_collect/$', CancelCollect.as_view()),
    url(r'^api/cancel_vote/$', CancelVote.as_view()),
]
