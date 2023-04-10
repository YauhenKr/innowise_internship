import pytest
from rest_framework import exceptions

from users.models import User
from users.services_auth import AuthenticationServices


def test_is_method_replace_bearer_or_not(bearer_token):
    clear_token = AuthenticationServices.get_the_token_from_header(bearer_token)

    assert len(clear_token) == len(bearer_token) - 7


def test_jwt_token_valid(token_user_admin):
    payload = AuthenticationServices.check_jwt_token(token_user_admin)

    assert payload['exp'] > 0
    assert payload['username'] == 'username_admin'


def test_jwt_token_does_not_valid(expired_token):
    with pytest.raises(exceptions.AuthenticationFailed) as err:
        AuthenticationServices.check_jwt_token(expired_token)

    assert err.value.detail == 'Token has expired'


def test_jwt_token_invalid_signature(invalid_token):
    with pytest.raises(exceptions.AuthenticationFailed) as err:
        AuthenticationServices.check_jwt_token(invalid_token)

    assert err.value.detail == 'Invalid signature'


def test_encode_token_when_user_is_got(user_2):
    token = AuthenticationServices.encode_token(user_2)
    payload = AuthenticationServices.check_jwt_token(token)

    assert type(token) == str
    assert payload['exp'] > 0
    assert payload['username'] == user_2.username


def test_get_user_through_payload_correct(token_user_1, user_1):
    payload = AuthenticationServices.check_jwt_token(token_user_1)
    user = AuthenticationServices.get_user_through_payload(payload)

    assert type(user) == User
    assert user.username == user_1.username
