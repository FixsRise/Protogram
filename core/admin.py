from django.contrib import admin

# Register your models here.

# В одном из файлов admin.py (лучше в основном, например в accounts/admin.py)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from accounts.models import UserProfile
from posts.models import Post



class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ('image', 'caption', 'created_at')
    readonly_fields = ('created_at',)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'


class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, PostInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


admin.site.register(UserProfile)
admin.site.register(Post)