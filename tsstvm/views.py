from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from django.contrib.auth.models import User

from tsstvm.feeds.models import Feed
from tsstvm.articles.models import Article
import datetime

def home(request):
    """
    Home page view
    """
    users = len(User.objects.filter(is_active=True))
    articles = len(Article.objects.all())
    feeds_no = len(Feed.get_feeds())
    events_upcoming = 10
    events_old = 100
    today = timezone.now()
    past = today + datetime.timedelta(days=-30)
    print past, today
    posts = Feed.objects.filter(date__range=[past, today])[:4]#.order_by('-likes')[:4]
    print 'psots', posts
    return render(request, 'home.html', {
        'users_no':users,
        'articles_no':articles,
        'feeds_no':feeds_no,
        'events_up':events_upcoming,
        'events_old':events_old,
        'posts': posts,
        })