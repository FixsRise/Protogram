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
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    avatar = models.ImageField(upload_to=edit_avatar_name, blank=True)
    bio = models.TextField(blank=True)

class RegisterUserForm(UserCreationForm):

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your bio here...',
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['avatar'].required = False
            self.fields['avatar'].widget = forms.FileInput(attrs={'class': 'form-control-file'})

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if not avatar and self.instance.avatar:
            return self.instance.avatar
        return avatar


