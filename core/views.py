
import os
from uuid import uuid4

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from posts.models import Post



def index(request):
    post_list = Post.objects.all().order_by('-created_at')
    last_news_id = request.session.get('last_news_id')


    context = {
        'posts': post_list,
        'last_news_id': last_news_id,
    }


    return render(request, 'main/index.html', context)