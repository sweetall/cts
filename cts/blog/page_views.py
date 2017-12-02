from django.shortcuts import render

from .models import Comment, Vote, Collect, Article
from .serializers import ArticleRetrieveSerializer, ArticleListSerializer
from core.models import UserProfile
from core.serializers import UserProfileSerializer


def index(request):
    user = get_user(request)

    category = request.GET.get('category', 0)
    creator = request.GET.get('creator', 0)
    search = request.GET.get('search', 0)
    context = {'user': user, 'category': category, 'creator': creator, 'search': search}
    return render(request, 'blog/base/index.html', context=context)


def retrieve(request, pk):
    update_summary(pk=pk)

    user = get_user(request)

    article = Article.objects.get(id=pk)
    article_data = ArticleRetrieveSerializer(article).data

    article_query = Article.objects.filter(state=1).filter(creator=article.creator).order_by('-summary__click_count')[:5]
    click_top5 = ArticleListSerializer(article_query, many=True).data
    for n in range(len(click_top5)):
        if len(click_top5[n]['title']) > 9:
            click_top5[n]['title'] = click_top5[n]['title'][0:13] + '...'

    if Collect.objects.filter(creator=request.user, article=pk).exists():
        article_data['collect_state'] = True
    else:
        article_data['collect_state'] = False

    if Vote.objects.filter(creator=request.user, article=pk).exists():
        article_data['vote_state'] = True
    else:
        article_data['vote_state'] = False

    context = {'user': user, 'article_id': pk, 'article_data': article_data, 'click_top5': click_top5}
    return render(request, 'blog/base/retrieve.html', context=context)


def create(request):
    user = get_user(request)
    context = {'user': user, 'article_id': 0}
    return render(request, 'blog/base/edit.html', context=context)


def update(request, pk):
    user = get_user(request)
    context = {'user': user, 'article_id': pk}
    return render(request, 'blog/base/edit.html', context=context)


def center(request):
    user = get_user(request)

    profile_id = request.user.userprofile.id
    context = {'user': user, 'profile_id': profile_id}
    return render(request, 'blog/user/center.html', context=context)


def get_user(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return UserProfileSerializer(user_profile).data


def update_summary(pk):
    article = Article.objects.get(id=pk)

    article.summary.click_count = int(article.summary.click_count) + 1
    article.summary.comment_count = article.comments.count()
    article.summary.vote_count = article.voters.count()
    article.summary.collect_count = article.collectors.count()
    article.summary.save()
