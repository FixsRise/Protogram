import os
from uuid import uuid4

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import models
from django.contrib.auth.models import User


def edit_avatar_name(instance, filename):
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid4()}{ext}"
    return f"avatars/{new_filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=edit_avatar_name, blank=True)
    bio = models.TextField(blank=True)

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            return username.lower()
        return username

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            return username.lower()
        return username

