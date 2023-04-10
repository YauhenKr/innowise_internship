import pytest

from innotwits.models import Page, Tag, Post
from users.models import User


@pytest.fixture(scope='session', autouse=False)
def user_for_page_1(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_1 = User.objects.create(
            id=90,
            username='user_for_page_1',
            email='page_1_user@email.com',
            password='page_1_user1234567890',
            role='user',
            is_staff=False,
            is_blocked=False
        )
        user_1.set_password('page_1_user1234567890')
        user_1.save()

        yield user_1


@pytest.fixture(scope='session', autouse=False)
def user_for_page_2(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_2 = User.objects.create(
            id=13,
            username='username_page',
            email='user_222page@email.com',
            password='12345678333page',
            role='user',
            is_staff=False,
            is_blocked=False
        )

        yield user_2


@pytest.fixture(scope='session', autouse=False)
def admin_pages(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_admin = User.objects.create(
            id=6,
            username='username_page_admin',
            email='admin222page@email.com',
            password='123456adminpage',
            role='admin',
            is_staff=True,
            is_blocked=False
        )

        yield user_admin


@pytest.fixture(scope='session', autouse=False)
def moderator_pages(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_moderator = User.objects.create(
            id=9,
            username='username_page_moderator',
            email='moderator222page@email.com',
            password='123456moderatorpage',
            role='moderator',
            is_staff=False,
            is_blocked=False
        )

        user_moderator.set_password('123456moderatorpage')
        user_moderator.save()

        return user_moderator


@pytest.fixture(scope='session', autouse=False)
def moderator_pages_2(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_moderator_2 = User.objects.create(
            id=37,
            username='username_page37_moderator',
            email='moderator222pa37ge@email.com',
            password='123456modera37torpage',
            role='moderator',
            is_staff=False,
            is_blocked=False
        )

        user_moderator_2.set_password('123456modera37torpage')
        user_moderator_2.save()

        return user_moderator_2


@pytest.fixture(scope='session', autouse=False)
def page_user_1_private(
        django_db_setup, django_db_blocker, user_for_page_1, tag_one,
        tag_two, moderator_pages_2, moderator_pages
):
    with django_db_blocker.unblock():
        page_1 = Page.objects.create(
            id=12,
            name='page_test_1',
            description='some page description',
            owner=user_for_page_1,
            is_private=True,
            is_blocked=False
        )
        page_1.tags.add(tag_one.pk, tag_two.pk)
        page_1.follow_requests.add(moderator_pages_2.id, moderator_pages.id)

        return page_1


@pytest.fixture(scope='session', autouse=False)
def page_user_2_public(django_db_setup, django_db_blocker, user_for_page_1, tag_one, tag_two):
    with django_db_blocker.unblock():
        page_2 = Page.objects.create(
            id=14,
            name='page_test_2',
            description='some page description 2',
            owner=user_for_page_1,
            is_private=False,
            is_blocked=False
        )
        page_2.tags.add(tag_one.pk, tag_two.pk)

        return page_2


@pytest.fixture(scope='session', autouse=False)
def page_admin_public(
        django_db_setup, django_db_blocker, admin_pages,
        tag_one, tag_two, user_for_page_1
):
    with django_db_blocker.unblock():
        page_admin = Page.objects.create(
            id=83,
            name='page_test_admin',
            description='some page description admin',
            owner=admin_pages,
            is_private=False,
            is_blocked=False
        )
        page_admin.tags.add(tag_one.pk, tag_two.pk)

        return page_admin


@pytest.fixture(scope='session')
def tag_one(django_db_blocker):
    with django_db_blocker.unblock():
        return Tag.objects.create(name='dogs')


@pytest.fixture(scope='session')
def tag_two(django_db_blocker):
    with django_db_blocker.unblock():
        return Tag.objects.create(name='test_tag_2')


@pytest.fixture()
def token_admin_pages(client, page_admin_public, admin_pages):
    admin_pages.set_password('123456adminpage')
    admin_pages.save()

    page_admin_public.followers.add(admin_pages.id)

    endpoint = 'http://127.0.0.1:8000/auth/login/'
    payload = {
        'email': 'admin222page@email.com',
        'password': '123456adminpage',
    }
    response = client.post(endpoint, payload)
    data = response.json()
    return data['token']


@pytest.fixture
def token_user_1_pages(client, user_for_page_1):
    endpoint = 'http://127.0.0.1:8000/auth/login/'
    payload = {
        'email': 'page_1_user@email.com',
        'password': 'page_1_user1234567890',
    }

    response = client.post(endpoint, payload)
    data = response.json()
    return data['token']


@pytest.fixture
def correct_payload_for_creating_page_required_fields():
    return {
        'name': 'Yauhen',
        'description': 'Yauheeeeeen',
    }


@pytest.fixture
def correct_payload_for_creating_page_all():
    return {
        'name': 'Yauhen',
        'description': 'yauheeeeeeen',
        'is_private': True
    }


@pytest.fixture
def incorrect_payload_for_creating_page():
    return {
        'name': '',
        'description': 'yauheeeeeeen',
        'is_private': True
    }


@pytest.fixture
def admin_can_update():
    return {
        'is_blocked': True,
        'unblock_date': '2023-04-06'
    }


@pytest.fixture
def payload_accept_requests():
    return {
        'accept': True,
        "request_user_ids": [9, 37]
    }


@pytest.fixture
def payload_deny_requests():
    return {
        'accept': False,
        "request_user_ids": [9, 37]
    }


@pytest.fixture
def payload_create_post(page_user_1_private):
    return {
        'page': page_user_1_private.id,
        'content': 'some content for post'
    }


@pytest.fixture
def payload_create_post_admin(page_admin_public):
    return {
        'page': page_admin_public.id,
        'content': 'some content for post admiiiiin',
    }


@pytest.fixture
def payload_create_post_user_1_reply_to(page_user_1_private):
    return {
        'page': page_user_1_private.id,
        'content': 'some content for post admiiiiin',
        'reply_to': 13
    }


@pytest.fixture(scope='session')
def create_post_13(django_db_blocker, page_user_1_private):
    with django_db_blocker.unblock():
        return Post.objects.create(
            id=13,
            page=page_user_1_private,
            content='content create post 1'
        )


@pytest.fixture(scope='session')
def create_post_14(django_db_blocker, page_admin_public):
    with django_db_blocker.unblock():
        return Post.objects.create(
            id=14,
            page=page_admin_public,
            content='content create post 1'
        )


@pytest.fixture(scope='session')
def create_post_15(django_db_blocker, page_user_1_private):
    with django_db_blocker.unblock():
        return Post.objects.create(
            id=15,
            page=page_user_1_private,
            content='content create post 15'
        )
