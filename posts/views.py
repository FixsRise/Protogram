from django.shortcuts import render, redirect, get_object_or_404

from posts.models import PostForm, Post, edit_image_name


# Create your views here.


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # request.session['last_seen_post_id'] = news_id
    return render(request, 'posts/post_details.html', {'post': post})

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