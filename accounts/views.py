import os
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from Protogram import settings
from accounts.models import LoginUserForm, RegisterUserForm, UserProfile, ProfileForm
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

def logout_user(request):
    logout(request)
    return redirect('home')




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


@login_required
def edit_profile(request, username):
    if request.user.username != username:
        messages.error(request, "You can only edit your own profile.")
        return redirect('profile', username=request.user.username)

    user = get_object_or_404(User, username=username)

    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=username)
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile_user': user,
    }

    return render(request, 'accounts/edit_profile.html', context)