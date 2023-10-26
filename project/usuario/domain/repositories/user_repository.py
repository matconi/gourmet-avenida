from usuario.models.User import User

def get_by_email(user: User) -> User:
    return User.objects.get(email=user.email)