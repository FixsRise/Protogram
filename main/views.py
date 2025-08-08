
import os
from uuid import uuid4

from django.shortcuts import render

from posts.models import Post


def index(request):
    post = Post.objects.all().order_by('-created_at')
    context = {'posts': post}

    return render(request, 'main/index.html', context)
# Create your views here.

