from usuario.models.User import User

def get_by_email(email: str) -> User:
    return User.objects.get(email=email)

def exists_by_email(email: str) -> bool:
    return User.objects.filter(email=email).exists()

def get_by_email_and_status(email: str, is_active: bool=True) -> bool:
    return User.objects.get(email=email, is_active=is_active)

def get_by_id(id: int) -> User:
    return User.objects.get(id=id)