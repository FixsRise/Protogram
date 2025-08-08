
import os
from uuid import uuid4

from django.shortcuts import render

from posts.models import Post


def index(request):
    post = Post.objects.all().order_by('-created_at')
    last_news_id = request.session.get('last_news_id')
    context = {'posts': post, 'last_news_id': last_news_id}

    return render(request, 'main/index.html', context)
# Create your views here.

