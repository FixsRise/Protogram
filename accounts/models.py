import os
from uuid import uuid4

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

