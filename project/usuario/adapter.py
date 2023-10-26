from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .domain.repositories import user_repository
from .models.User import User

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin): 
        user = sociallogin.user
        if user.id or not user.email:
            return

        try:
            local_user: User = user_repository.get_by_email(user)
            sociallogin.connect(request, local_user)
        except User.DoesNotExist:
            pass