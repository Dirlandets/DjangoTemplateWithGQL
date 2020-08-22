from typing import TYPE_CHECKING, Optional

from django.contrib.auth.models import BaseUserManager

if TYPE_CHECKING:
    from accounts.models import AppUser  # noqa: WPS433


class AppUserManager(BaseUserManager):
    """Менеджер реализует правильное сохранение юзера."""

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        date_of_birth: Optional[str] = None,
        password: Optional[str] = None,
    ) -> 'AppUser':
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        if date_of_birth:
            user.date_of_birth = date_of_birth
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: Optional[str] = None
    ) -> 'AppUser':
        """Creates and saves a superuser with the given email and password."""
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
