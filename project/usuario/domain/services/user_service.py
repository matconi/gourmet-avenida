from usuario.domain.repositories import user_repository
from usuario.models import User
from django import forms

def block_user_by_password_err(email: str) -> None:
    try:
        user = user_repository.get_by_email(email)
        if user.attempts < 5:
            user.attempts += 1
            user.save()
        else:
            raise forms.ValidationError('Usuário bloqueado. Para acessar, use uma conta social ou redefina a sua senha.')
    except User.DoesNotExist:
        pass

def email_in_use(email: str) -> None:
    if user_repository.exists_by_email(email):
        raise forms.ValidationError('Um usuário já foi registrado com este endereço de e-mail.')