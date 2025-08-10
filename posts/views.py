import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from posts.models import PostForm, Post, edit_image_name


# Create your views here.


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    request.session['last_news_id'] = post_id
    return render(request, 'posts/post_details.html', {'post': post})


@require_POST
@login_required(login_url='/accounts/login/')
def like_post(request, post_id):

    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Authentication required'},
            status=401
        )


    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(
            {'status': 'error', 'message': 'AJAX requests only'},
            status=400
        )


    if not request.content_type == 'application/json':
        return JsonResponse(
            {'status': 'error', 'message': 'Content-Type must be application/json'},
            status=400
        )

    try:
        try:
            data = json.loads(request.body.decode('utf-8'))
            action = data.get('action')
        except (json.JSONDecodeError, UnicodeDecodeError, AttributeError) as e:
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid JSON format'},
                status=400
            )

        if action not in ['like', 'unlike']:
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid action parameter'},
                status=400
            )

        with transaction.atomic():
            post = Post.objects.select_for_update().get(id=post_id)

            # if not request.user.is_authenticated:
            #     raise PermissionDenied("You can't like this post")
            #
            # if not request.user.has_perm('posts.can_like', post):
            #     raise PermissionDenied("You can't like this post")

            if action == 'like':
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)

            likes_count = post.likes.count()


        return JsonResponse({
            'status': 'ok',
            'likes_count': likes_count,
            'is_liked': action == 'like'
        })

    except Post.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Post not found'},
            status=404
        )
    except PermissionDenied as e:
        return JsonResponse(
            {'status': 'error', 'message': str(e)},
            status=403
        )
    except Exception as e:

        return JsonResponse(
            {'status': 'error', 'message': 'Internal server error'},
            status=500
        )
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect('home')

    return render(request, 'posts/includes/confirm_delete.html', {'post': post})
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():

            if 'image' in request.FILES:
                new_image = request.FILES['image']

                post.image.save(
                    edit_image_name(post, new_image.name),
                    new_image
                )

                try:
                    old_image = Post.objects.get(id=post.id).image
                    if old_image and old_image != post.image:
                        old_image.delete(save=False)
                except Post.DoesNotExist:
                    pass

            post.caption = form.cleaned_data['caption']
            post.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})