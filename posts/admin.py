from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import *


class PostInline(admin.TabularInline):  # или admin.StackedInline
    model = Post
    extra = 0
    fields = ('image', 'caption', 'created_at')
    readonly_fields = ('created_at',)


class UserAdmin(BaseUserAdmin):
    inlines = (PostInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Post)