from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CashbackUserManager(BaseUserManager):
    """
        A custom user manager to deal with emails as unique identifiers for auth
        instead of usernames. The default that's used is "UserManager"
        """

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CashBackUser(AbstractUser):
    email = models.EmailField(
        _('email address'),
        error_messages={
            'unique': _('A user with that e-mail already exists.'),
        },
        blank=False,
        unique=True)
    username = models.CharField('Username', max_length=60, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CashbackUserManager()

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Usuário'

    def __str__(self):
        return self.email
