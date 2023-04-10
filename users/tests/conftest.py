import jwt
import pytest

from django.urls import reverse

from core import settings
from users.models import User


@pytest.fixture(autouse=True)
def wrong_pass():
    return "Str#410-P@55"


@pytest.fixture(autouse=True)
def right_pass():
    return "1234567890"


@pytest.fixture(autouse=True)
def email():
    return "email111@email.com"


@pytest.fixture(scope='session', autouse=False)
def user_1(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_1 = User.objects.create(
            id=17,
            username='username_111',
            email='email111@email.com',
            password='1234567890',
            role='user',
            is_staff=False
        )
        user_1.set_password('1234567890')
        user_1.save()

        yield user_1


@pytest.fixture(scope='session', autouse=False)
def user_2(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_2 = User.objects.create(
            id=33,
            username='username_222',
            email='user_222@email.com',
            password='12345678333',
            is_blocked=False
        )

        yield user_2


@pytest.fixture(scope='session', autouse=False)
def user_admin(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_admin = User.objects.create(
            id=38,
            username='username_admin',
            email='admin@email.com',
            password='admin12345678333',
            role='admin',
            is_staff=True
        )
        user_admin.set_password('admin12345678333')
        user_admin.save()

        yield user_admin


@pytest.fixture
def registration_success_payload():
    return {
        'username': 'username_1yaaay',
        'email': 'registrationyaaay@mail.com',
        'password': 'registrationyaaaay1234'
    }


@pytest.fixture
def registration_fail_payload():
    return {
        'username': 'username_1',
        'email': '',
        'password': 'registration1234'
    }


@pytest.fixture
def token_user_1(client, user_1):
    endpoint = reverse('auth-login')
    payload = {
        'email': 'email111@email.com',
        'password': '1234567890'
    }
    response = client.post(endpoint, payload)
    data = response.json()
    return data['token']


@pytest.fixture
def token_user_admin(client, user_admin):
    endpoint = reverse('auth-login')
    payload = {
        'email': 'admin@email.com',
        'password': 'admin12345678333',
    }
    response = client.post(endpoint, payload)
    data = response.json()
    return data['token']


@pytest.fixture
def bearer_token():
    return 'Bearer fghiuth54896uhUHFGPLD5676"L"FGHPK%(I'


@pytest.fixture
def expired_token(user_2):
    payload = {
        'user_id': user_2.id,
        'username': user_2.username,
        'exp': 0.0
    }

    exp_token = jwt.encode(
        payload=payload,
        key=settings.JWT_AUTH.get('SIGNING_KEY'),
        algorithm=settings.JWT_AUTH.get('ALGORITHM')
    )

    return exp_token


@pytest.fixture
def invalid_token(user_2):
    payload = {
        'user_id': user_2.id,
        'username': user_2.username,
        'exp': 0.0
    }

    exp_token = jwt.encode(
        payload=payload,
        key=settings.JWT_AUTH.get('SIGNING_KEY'),
        algorithm=settings.JWT_AUTH.get('ALGORITHM')
    )

    return f"{exp_token}dfhfghjdfid"


@pytest.fixture(scope='session', autouse=False)
def user_for_blocking(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        block_user = User.objects.create(
            id=778,
            username='userblock',
            email='blockban@email.com',
            password='777banbanban',
            role='user',
            is_blocked=False
        )

        return block_user
