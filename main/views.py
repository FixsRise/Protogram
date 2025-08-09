
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
    paginator = Paginator(post_list, 5)  # 5 постов на страницу
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('posts/post_list_partial.html', {'posts': page_obj.object_list})
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next()
        })

    context = {
        'posts': page_obj.object_list,
        'has_next': page_obj.has_next(),
        'last_news_id': last_news_id,
    }
    return render(request, 'main/index.html', context)
