from typing import Callable, List, Optional

import pytest
from mimesis import Person

from accounts.models import AppUser, Organization


@pytest.fixture
def app_user_factory(db) -> Callable[[], AppUser]:
    """Фабрика генератор юзеров с фейковыми даными."""

    def create_app_user(
        domains: Optional[List[str]] = None,
        organization: Optional[Organization] = None,
    ) -> AppUser:
        """Опционально можно передать домены, или инстанс организации.

        Тогда пользователи будут созданы с emails:
        * либо с переданными domains;
        * либо с organization.domains.
        """
        app_user = Person('ru')
        first_name = app_user.first_name()
        last_name = app_user.last_name()
        if organization:
            domains = organization.get_domains()
        email = app_user.email(domains=domains)

        user = AppUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        return user
    return create_app_user


@pytest.fixture
def superuser(db, app_user_factory) -> AppUser:
    """Генеририруем суперюзера юзера."""
    superu = app_user_factory()
    superu.is_superuser = True
    superu.is_staff = True
    superu.is_active = True
    superu.save()
    return superu


@pytest.fixture
def organization(db):
    def create_org(name: str = 'TestOrg', domains: List[str] = ['test.ru', 'test.com']):
        return Organization.objects.create(
            name=name,
            domains='\n'.join(domains),
        )
    return create_org


@pytest.fixture
def banch_of_managers(db, app_user_factory, organization):
    """Генерируем толпу юзеров."""
    def generate_managers(
        quantity: int = 10,
        domains: Optional[List[str]] = None,
        org: Optional[Organization] = None,
    ):  
        if not org:
            org = organization()
        managers = []
        for _ in range(quantity):
            managers.append(app_user_factory(domains=domains, organization=org))
        return managers
    return generate_managers


@pytest.fixture
def manager(db, banch_of_managers):
    """Генерирует менеджера."""
    return banch_of_managers(1)[0]
