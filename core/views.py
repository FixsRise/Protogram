
import os
from uuid import uuid4

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from posts.models import Post


POSTS_PER_PAGE = 5  # количество постов за один запрос

def index(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_obj = paginator.get_page(1)

    context = {
        'posts': page_obj,
    }
    return render(request, 'main/index.html', context)


def load_more_posts(request):
    page = int(request.GET.get('page', 1))
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    try:
        posts = paginator.get_page(page)
    except:
        return JsonResponse({'posts_html': '', 'has_next': False})

    posts_html = render_to_string('posts/post_list.html', {'posts': posts}, request=request)
    return JsonResponse({
        'posts_html': posts_html,
        'has_next': posts.has_next()
    })
