from typing import Any, List, Optional, cast

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> 'User':
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return cast(User, user)

    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> 'User':  # type: ignore
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> 'User':  # type: ignore
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # type: ignore
    email = models.EmailField('email address', unique=True)
    is_admin = models.BooleanField(default=False, help_text='admins can manage products')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: List[str] = []

    objects = UserManager()
