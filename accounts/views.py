import os
from uuid import uuid4

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from Protogram import settings
from accounts.models import LoginUserForm, RegisterUserForm, UserProfile
from posts.models import Post


# Create your views here.

def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginUserForm()
    return render(request, 'accounts/login_user.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()


            UserProfile.objects.create(
                user=user,
                avatar=os.path.join(settings.MEDIA_ROOT, 'avatars', 'default.jpg'),
                bio="Hi, I'm new here!"
            )


            login(request, user)
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'accounts/register_user.html', {'form': form})


@login_required
def profile(request, username):
    try:
        user = get_object_or_404(User, username=username)
        profile = user.userprofile
        post_list = Post.objects.all().filter(author=user).order_by('-created_at')

        context = {
            'profile_user': user,
            'profile': profile,
            'posts' : post_list,
        }

        return render(request, 'accounts/user_profile.html', context)
    except User.DoesNotExist:
        raise Http404("User not found")
    except AttributeError:

        profile = UserProfile.objects.create(user=user)
        post_list = Post.objects.all().filter(author=user).order_by('-created_at')
        context = {
            'profile_user': user,
            'profile': profile,
            'posts': post_list,
        }
        return render(request, 'accounts/user_profile.html', context)