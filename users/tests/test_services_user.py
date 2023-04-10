import pytest

from rest_framework.exceptions import AuthenticationFailed

from users.services_user import UsersServices


def test_get_user_by_email(user_1, user_2, email):
    user = UsersServices.get_user_by_email(email)

    assert type(user) == type(user_1)
    assert user == user_1
    assert user != user_2


def test_check_user_by_password_correct(user_1, right_pass):
    user = UsersServices.check_user(user_1.email, right_pass)

    assert user == user_1


def test_check_user_by_password_incorrect(user_1, wrong_pass):
    with pytest.raises(AuthenticationFailed) as err:
        UsersServices.check_user(user_1.email, wrong_pass)

    assert err.value.detail == 'Invalid password.'
