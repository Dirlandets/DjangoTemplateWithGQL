from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from accounts.managers import AppUserManager
from app.constants import TextLen


class AppUser(AbstractBaseUser, PermissionsMixin):
    """Базовый класс пользователя для приложения."""

    email = models.EmailField(
        verbose_name='email address',
        max_length=TextLen.MEDIUM,
        blank=False,
        null=False,
        unique=True,
    )

    first_name = models.CharField(
        verbose_name='first name',
        max_length=TextLen.MEDIUM,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_length=TextLen.MEDIUM,
        blank=False,
        null=False,
    )
    date_of_birth = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )

    USERNAME_FIELD = 'email'
    MAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = AppUserManager()  # noqa: WPS110

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """String representation of an instance."""
        return self.email
