import pytest
from django.urls import reverse


def test_successful_registration(client, registration_success_payload):
    endpoint = reverse('auth-register')
    response = client.post(endpoint, registration_success_payload)

    assert response.status_code == 201


def test_failed_registration(client, registration_fail_payload):
    endpoint = reverse('auth-register')
    response = client.post(endpoint, registration_fail_payload)

    assert response.status_code == 400


def test_successful_login(client, user_1):
    endpoint = reverse('auth-login')
    payload = {
        'email': 'email111@email.com',
        'password': '1234567890'
    }
    response = client.post(endpoint, payload)
    data = response.json()

    assert response.status_code == 200
    assert data['token'] != ''


def test_failed_login(client):
    endpoint = reverse('auth-login')
    payload = {
        'email': 'аа',
        'password': '1234567890'
    }
    response = client.post(endpoint, payload)
    data = response.json()

    assert data['error'] == 'Check you credentials'
    assert response.status_code == 404


def test_just_admin_can_patch_but_user_trying(client, user_2, token_user_1):
    endpoint = f'http://127.0.0.1:8000/auth/{user_2.id}/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1}'
    payload = {
        'is_blocked': True
    }
    response = client.patch(endpoint, payload, content_type='application/json')

    assert response.status_code == 403


@pytest.mark.django_db
def test_just_admin_can_patch_and_admin_trying(client, token_user_admin, user_for_blocking):
    endpoint = f'http://127.0.0.1:8000/auth/{user_for_blocking.id}/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_admin}'
    payload = {
        'is_blocked': True
    }
    response = client.patch(endpoint, payload, content_type='application/json')
    user_for_blocking.refresh_from_db()

    assert response.status_code == 200
    assert user_for_blocking.is_blocked
