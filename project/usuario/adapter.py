from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models.User import User

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin): 
        user = sociallogin.user
        if user.id or not user.email:  
            return

        try:
            local_user: User = User.objects.get(email=user.email)
            sociallogin.connect(request, local_user)
        except User.DoesNotExist:
            pass