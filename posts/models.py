from django import forms
from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4
import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver


def edit_image_name(instance, filename):
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid4()}{ext}"
    return f"posts/{new_filename}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to=edit_image_name, blank=False)
    caption = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def was_edited(self):
        return (self.updated_at - self.created_at).total_seconds() > 1


@receiver(pre_delete, sender=Post)
def delete_post_images(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your post here...',
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
            self.fields['image'].widget = forms.FileInput(attrs={'class': 'form-control-file'})

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not self.instance.pk and not image:
            raise forms.ValidationError("Image is required")
        return image