import pytest
from simple_email_confirmation.models import EmailAddress

from django.db.utils import IntegrityError

from accounts.models import AppUser


def test_new_user(manager):
    """Cвежесозданный пользователь не имеет никаких прав."""
    assert manager.is_superuser is False
    assert manager.is_active is False
    assert manager.is_staff is False
    assert manager.is_confirmed is False


def test_user_confirmation(manager):
    """Проверяем, что получится подтвердить email."""
    assert manager.is_confirmed is False
    AppUser.confirm_user_email(manager.email, manager.confirmation_key)

    manager.refresh_from_db()
    assert manager.is_confirmed is True


def test_user_confirmation_wrong_key(banch_of_managers):
    """Проверяем, что не получится подтвердить email чужим ключем."""
    managers = banch_of_managers(2)
    assert managers[0].is_confirmed is False
    assert managers[1].is_confirmed is False

    with pytest.raises(EmailAddress.DoesNotExist):
        AppUser.confirm_user_email(managers[0].email, managers[1].confirmation_key)

    managers[0].refresh_from_db()
    managers[1].refresh_from_db()

    assert managers[0].is_confirmed is False
    assert managers[1].is_confirmed is False


def test_new_user_required_fields(manager):
    """Cвежесозданный пользователь имеет все обязательные поля."""
    assert manager.first_name is not None
    assert manager.last_name is not None
    assert manager.email is not None


def test_email_is_unique(banch_of_managers):
    """Email пользоваетеля должен быть уникальным."""
    users = banch_of_managers(2)
    with pytest.raises(IntegrityError):
        users[0].email = users[1].email
        users[0].save()


def test_personnel_number_is_unique(banch_of_managers):
    """Табельный номер пользоваетеля должен быть уникальным."""
    users = banch_of_managers(2)
    with pytest.raises(IntegrityError):
        for user in users:
            user.personnel_number = 'FX1234567'
            user.save()


def test_supervisor_can_add_managers(banch_of_managers):
    """Пользователь может быть супервайзером."""
    users = banch_of_managers(10)

    supervisor = users[0]

    for manager in users[1:]:
        manager.supervisors.add(supervisor)
        assert supervisor in manager.supervisors.all()
        assert manager in supervisor.managers.all()
