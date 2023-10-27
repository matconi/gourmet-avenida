from usuario.models.User import User

def get_by_email(email: str) -> User:
    return User.objects.get(email=email)