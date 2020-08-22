import graphene
from graphene_django.types import DjangoObjectType

from accounts.models import AppUser


class AppUserType(DjangoObjectType):
    """Тип для юзера AppUser."""

    class Meta:
        model = AppUser


class Query(object):
    """Объект Query для импорта в app.root_shema."""

    user = graphene.Field(
        AppUserType,
        id=graphene.Int(),
        first_name=graphene.String(),
        last_name=graphene.String(),
    )
    all_users = graphene.List(AppUserType)

    def resolve_user(self, info, **kwargs):
        """Возвращаем пользователя по id, email."""
        id_ = kwargs.get('id')
        email = kwargs.get('email')

        if id_ is not None:
            return AppUser.objects.get(pk=id_)

        if email is not None:
            return AppUser.objects.get(email=email)

        return None

    def resolve_all_users(self, info, **kwargs):
        """Возвращаем всех пользователей."""
        return AppUser.objects.all()
