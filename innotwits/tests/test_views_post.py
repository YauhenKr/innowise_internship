import pytest

from innotwits.models import Post
from users.services_auth import AuthenticationServices


def test_add_post_to_page_successfully(
        client, token_user_1_pages, payload_create_post,
        payload_create_post_admin
):
    endpoint = 'http://127.0.0.1:8000/post/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'
    response = client.post(
        endpoint, payload_create_post, content_type='application/json'
    )
    response_not_owner = client.post(
        endpoint, payload_create_post_admin, content_type='application/json'
    )
    data = response.json()
    posts = Post.objects.all().count()

    assert response.status_code == 201
    assert response_not_owner.status_code == 403
    assert posts == 1
    assert data['page'] == payload_create_post['page']


def test_add_reply_to_some_post(
        client, token_user_1_pages, page_user_1_private,
        payload_create_post_user_1_reply_to, create_post_13
):
    post = create_post_13
    post.refresh_from_db()

    endpoint = 'http://127.0.0.1:8000/post/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'
    response = client.post(
        endpoint, payload_create_post_user_1_reply_to, content_type='application/json'
    )
    data = response.json()

    assert response.status_code == 201
    assert data['reply_to'] == payload_create_post_user_1_reply_to['reply_to']


def test_creating_like_unlike_on_post(client, create_post_13, token_user_1_pages):
    post = create_post_13
    post.refresh_from_db()

    endpoint = f'http://127.0.0.1:8000/post/{create_post_13.id}/like/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'
    response = client.post(endpoint, content_type='application/json')
    header = AuthenticationServices.check_jwt_token(token_user_1_pages)
    data = response.json()
    post.refresh_from_db()
    like_existing = post.like.filter(id=header['user_id']).exists()

    response_unlike = client.post(endpoint, content_type='application/json')
    post.refresh_from_db()
    like_not_existing = post.like.filter(id=header['user_id']).exists()

    assert response.status_code == 201
    assert data == 'Creating like'
    assert like_existing
    assert response_unlike.status_code == 204
    assert not like_not_existing


def test_getting_list_of_liked_posts(
        client, create_post_13, create_post_14, token_user_1_pages
):
    post_1, post_2 = create_post_13, create_post_14
    post_1.refresh_from_db()
    post_2.refresh_from_db()

    endpoint_1 = f'http://127.0.0.1:8000/post/{create_post_13.id}/like/'
    endpoint_2 = f'http://127.0.0.1:8000/post/{create_post_14.id}/like/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'
    client.post(endpoint_1, content_type='application/json')
    post_1.refresh_from_db()
    client.post(endpoint_2, content_type='application/json')
    post_2.refresh_from_db()

    endpoint_list_liked_posts = f'http://127.0.0.1:8000/post/list_liked_posts/'
    response = client.get(endpoint_list_liked_posts, content_type='application/json')
    data = response.json()

    assert len(data) == 2
    assert response.status_code == 200


def test_post_can_be_deleted_and_updated_by_owner(
        client, create_post_13, token_user_1_pages,
        create_post_14
):
    payload = {'content': 'changing the content'}

    endpoint = f'http://127.0.0.1:8000/post/{create_post_13.id}/'
    endpoint_not_owner = f'http://127.0.0.1:8000/post/{create_post_14.id}/'

    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_user_1_pages}'
    response_update = client.patch(endpoint, data=payload, content_type='application/json')
    response_update_not_owner = client.patch(endpoint_not_owner, data=payload, content_type='application/json')
    create_post_13.refresh_from_db()
    data_update = response_update.json()
    client.delete(endpoint, content_type='application/json')
    deleted_post_equal_one = Post.objects.filter(content='changing the content').count()

    assert data_update['content'] == payload['content']
    assert response_update_not_owner.status_code == 403
    assert deleted_post_equal_one == 0


def test_post_can_be_deleted_and_not_updated_by_admin(client, token_admin_pages, create_post_15):
    payload = {'content': 'changing the content'}

    endpoint = f'http://127.0.0.1:8000/post/{create_post_15.id}/'
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token_admin_pages}'
    response_update = client.patch(endpoint, data=payload, content_type='application/json')
    print(response_update)
    response_delete = client.delete(endpoint, content_type='application/json')
    deleted_post_equal_zero = Post.objects.filter(
        content='content create post 15'
    ).count()

    assert response_update.status_code == 403
    assert response_delete.status_code == 204
    assert deleted_post_equal_zero == 0
