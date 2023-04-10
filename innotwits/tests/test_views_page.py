import pytest

from innotwits.models import Page, Tag
from users.services_auth import AuthenticationServices


@pytest.mark.django_db
def test_get_page_which_does_not_exist(client, token_admin_pages):
    endpoint = f'http://127.0.0.1:8000/page/999/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_admin_pages}'
    response = client.get(endpoint, content_type='application/json')

    assert response.status_code == 404


@pytest.mark.django_db
def test_get_page_which_exists(client, token_admin_pages, page_user_1_private):
    endpoint = f'http://127.0.0.1:8000/page/{page_user_1_private.id}/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_admin_pages}'
    response = client.get(endpoint, content_type='application/json')
    data = response.json()

    assert response.status_code == 200
    assert 'detail' not in data.keys()


@pytest.mark.django_db
def test_create_page_with_correct_required_data(
        client, correct_payload_for_creating_page_required_fields, token_admin_pages
):
    endpoint = f'http://127.0.0.1:8000/page/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_admin_pages}'
    response = client.post(
        endpoint,
        correct_payload_for_creating_page_required_fields,
        content_type='application/json'
    )
    payload_owner = AuthenticationServices.check_jwt_token(token_admin_pages)
    data = response.json()

    assert Page.objects.filter(
        owner=payload_owner['user_id']).exclude(name='page_test_admin').count() == 1
    assert response.status_code == 201
    assert data['owner']['username'] == payload_owner['username']
    assert not data['is_private']


@pytest.mark.django_db
def test_create_page_with_correct_non_required_data(
        client, correct_payload_for_creating_page_all, token_admin_pages
):
    endpoint = f'http://127.0.0.1:8000/page/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_admin_pages}'
    response = client.post(
        endpoint,
        correct_payload_for_creating_page_all,
        content_type='application/json'
    )
    payload_owner = AuthenticationServices.check_jwt_token(token_admin_pages)
    data = response.json()

    assert Page.objects.filter(
        owner=payload_owner['user_id']).exclude(name='page_test_admin').count() == 1
    assert response.status_code == 201
    assert data['owner']['username'] == payload_owner['username']
    assert data['is_private']


@pytest.mark.django_db
def test_create_page_with_incorrect_data(
        client, incorrect_payload_for_creating_page, token_admin_pages
):
    endpoint = f'http://127.0.0.1:8000/page/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_admin_pages}'
    response = client.post(
        endpoint,
        incorrect_payload_for_creating_page,
        content_type='application/json'
    )
    data = response.json()

    assert response.status_code == 400
    assert data['name'][0] == 'This field may not be blank.'


@pytest.mark.django_db
def test_admin_can_update_only_is_blocked_unblock_date(
        client, page_user_1_private, token_admin_pages,
        correct_payload_for_creating_page_required_fields,
        admin_can_update
):
    endpoint = f'http://127.0.0.1:8000/page/{page_user_1_private.id}/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_admin_pages}'

    response = client.patch(
        endpoint,
        correct_payload_for_creating_page_required_fields,
        content_type='application/json'
    )

    response_admin_can = client.patch(
        endpoint,
        admin_can_update,
        content_type='application/json'
    )
    data = response.json()
    data_admin = response_admin_can.json()

    assert response.status_code == 403
    assert data['detail'] == 'You do not have permission to perform this action.'
    assert response_admin_can.status_code == 200
    assert data_admin['is_blocked']


@pytest.mark.django_db
def test_owner_can_update_only_is_blocked_unblock_date(
        client, token_user_1_pages, correct_payload_for_creating_page_required_fields,
        page_user_1_private, admin_can_update
):
    endpoint = f'http://127.0.0.1:8000/page/{page_user_1_private.id}/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'

    response = client.patch(
        endpoint,
        correct_payload_for_creating_page_required_fields,
        content_type='application/json'
    )

    response_admin_can = client.patch(
        endpoint,
        admin_can_update,
        content_type='application/json'
    )
    data_admin = response_admin_can.json()

    assert response.status_code == 200
    assert data_admin['detail'] == 'You do not have permission to perform this action.'
    assert response_admin_can.status_code == 403


def test_successful_tag_adding_or_getting_already_exists(
        client, token_user_1_pages, page_user_1_private
):
    endpoint = f'http://127.0.0.1:8000/page/{page_user_1_private.id}/tag/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'
    payload = {'name': 'Tests are the best thing!!!'}
    payload_2 = {'name': 'test_tag_2'}
    response = client.post(
        endpoint,
        payload,
        content_type='application/json'
    )
    data = response.json()
    response_2 = client.post(
        endpoint,
        payload_2,
        content_type='application/json'
    )
    data_2 = response_2.json()
    page_user_1_private.refresh_from_db()
    tags = page_user_1_private.tags.all()

    assert Tag.objects.filter(name=payload['name'].lower()).count() == 1
    assert tags.filter(name=payload['name'].lower()).exists()
    assert response.status_code == 200
    assert data == 'Tag was successfully added'
    assert data_2 == 'Tag is already exists'


def test_successful_tag_deleting(client, token_user_1_pages, page_user_1_private):
    endpoint = f'http://127.0.0.1:8000/page/{page_user_1_private.id}/tag/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'
    payload = {'name': 'test_tag_2'}
    payload_does_not_exist_tag = {'name': 'test_tag_3'}
    response = client.delete(
        endpoint,
        payload,
        content_type='application/json'
    )
    data = response.json()
    response_non_existing_tag = client.delete(
        endpoint,
        payload_does_not_exist_tag,
        content_type='application/json'
    )
    data_non_existing_tag = response_non_existing_tag.json()
    page_user_1_private.refresh_from_db()
    tags = page_user_1_private.tags.all()

    assert Tag.objects.filter(name=payload['name'].lower()).count() == 1
    assert not tags.filter(name=payload['name'].lower()).exists()
    assert response.status_code == 200
    assert data == 'Tag was deleted'
    assert data_non_existing_tag['detail'] == 'Not found.'


def test_successful_sending_following_request(
        client, page_user_1_private, page_user_2_public, page_admin_public,
        token_admin_pages
):
    endpoint_private = f'http://127.0.0.1:8000/page/{page_user_1_private.id}/send_following_unfollowing_request/'
    endpoint_public = f'http://127.0.0.1:8000/page/{page_user_2_public.id}/send_following_unfollowing_request/'
    endpoint_not_exist = f'http://127.0.0.1:8000/page/667/send_following_unfollowing_request/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_admin_pages}'

    response_from_private_page = client.post(endpoint_private, content_type='application/json')
    response_from_public_page = client.post(endpoint_public, content_type='application/json')
    response_from_not_existing_page = client.post(endpoint_not_exist, content_type='application/json')

    data_private = response_from_private_page.json()
    data_public = response_from_public_page.json()
    data_not_exist = response_from_not_existing_page.json()

    admin_id = AuthenticationServices.check_jwt_token(token_admin_pages)['user_id']
    page_added = page_user_2_public.followers.all().count()
    page_requests = page_user_1_private.follow_requests.filter(id=admin_id).count()

    assert data_not_exist['detail'] == 'Not found.'
    assert data_private == 'Follow request has been sent'
    assert data_public == 'You have subscribed to the page'
    assert page_added == 1
    assert page_requests == 1


def test_sending_following_request_to_themselves(client, page_user_1_private, token_user_1_pages):
    endpoint_myself = f'http://127.0.0.1:8000/page/{page_user_1_private.id}/send_following_unfollowing_request/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'
    response_from_myself = client.post(endpoint_myself, content_type='application/json')
    data_myself = response_from_myself.json()

    assert data_myself == 'You cannot subscribe to yourself'


def test_successful_unfollowing_or_get_that_you_are_not_friends(
        client, page_user_1_private, token_admin_pages,
        page_admin_public
):
    endpoint_myself = f'http://127.0.0.1:8000/page/{page_user_1_private.id}/send_following_unfollowing_request/'
    endpoint_friend = f'http://127.0.0.1:8000/page/{page_admin_public.id}/send_following_unfollowing_request/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_admin_pages}'
    payload = {'unfollow': True}
    response_not_friends = client.post(endpoint_myself, data=payload, content_type='application/json')
    response_for_friend = client.post(endpoint_friend, data=payload, content_type='application/json')
    data_not_friends = response_not_friends.json()
    data_for_friend = response_for_friend.json()
    amount_friends = page_admin_public.followers.all().count()

    assert amount_friends == 0
    assert data_not_friends == 'You are not friends'
    assert data_for_friend == 'You have just unfollowed that user'


def test_getting_list_of_followers_requests(
        client, page_user_1_private, token_user_1_pages, page_admin_public,
        page_user_2_public
):
    endpoint = f'http://127.0.0.1:8000/page/{page_user_1_private.id}/list_followers_requests/'
    endpoint_not_owner = f'http://127.0.0.1:8000/page/{page_admin_public.id}/list_followers_requests/'
    endpoint_public_page = f'http://127.0.0.1:8000/page/{page_user_2_public.id}/list_followers_requests/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'
    response = client.get(endpoint, content_type='application/json')
    response_not_owner = client.get(
        endpoint_not_owner, content_type='application/json'
    )
    response_public_page = client.get(
        endpoint_public_page, content_type='application/json'
    )
    data_not_owner = response_not_owner.json()
    data_public_page = response_public_page.json()
    data = response.json()

    assert len(data) == 3
    assert response.status_code == 200
    assert data_not_owner == 'Forbidden. It is not your page!'
    assert data_public_page == 'You have no requests. Page is not private'


def test_approve_requests_one_or_list(
        client, page_user_1_private, token_user_1_pages,
        payload_accept_requests, payload_deny_requests
):
    endpoint = f'http://127.0.0.1:8000/page/{page_user_1_private.id}/approve_disapprove_request/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'
    response_accept = client.post(
        endpoint, payload_accept_requests, content_type='application/json'
    )
    page_user_1_private.refresh_from_db()
    data = response_accept.json()
    requests = page_user_1_private.follow_requests.filter(
        id__in=payload_accept_requests['request_user_ids']).count()
    followers = page_user_1_private.followers.all().count()

    assert response_accept.status_code == 200
    assert data == "User's requests were approved successfully"
    assert requests == 0
    assert followers == 2


def test_disapprove_requests_one_or_list(
        client, page_user_1_private, token_user_1_pages,
        payload_deny_requests, page_admin_public
):
    endpoint = f'http://127.0.0.1:8000/page/{page_user_1_private.id}/approve_disapprove_request/'
    endpoint_not_owner = f'http://127.0.0.1:8000/page/{page_admin_public.id}/approve_disapprove_request/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'
    response_deny = client.post(
        endpoint, payload_deny_requests, content_type='application/json'
    )
    response_not_owner = client.post(
        endpoint_not_owner, payload_deny_requests, content_type='application/json'
    )
    page_user_1_private.refresh_from_db()
    data = response_deny.json()
    data_not_owner = response_not_owner.json()
    requests = page_user_1_private.follow_requests.filter(
        id__in=payload_deny_requests['request_user_ids']).count()

    assert response_deny.status_code == 200
    assert data == 'All requests were disapproved successfully'
    assert data_not_owner == 'Forbidden. It is not your page!'
    assert requests == 0
