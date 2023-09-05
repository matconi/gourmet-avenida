from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, first_name, password, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def _create_superuser(self, email, first_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Um superusuário deve ser administrador.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Um superusuário deve possuir todas as permissões.")
            
        return self._create_user(email, first_name, password, **extra_fields)