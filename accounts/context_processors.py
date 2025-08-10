def get_user_profile_data(request):
    if request.user.is_authenticated:
        return {
            'user_profile_url': f"/accounts/{request.user.username}",
            'user_avatar': request.user.userprofile.avatar.url,
        }
    return {}