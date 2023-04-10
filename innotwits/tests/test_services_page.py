from innotwits.services import PageServices


def test_get_page_by_access_if_user_and_owner_because_private_page(
        user_for_page_1, user_for_page_2, page_user_1_private
):
    user_role = user_for_page_1.role
    staff_or_not = user_for_page_1.is_staff
    serializer = PageServices.get_page_by_access(
        user_role, staff_or_not, page_user_1_private.id, user_for_page_1
    )
    get_username = list(serializer['owner'].items())
    get_username = get_username[0][1]

    assert get_username == user_for_page_1.username
    assert serializer['description']
    assert serializer['is_private']


def test_get_page_by_access_if_user_and_not_owner(
        user_for_page_1, user_for_page_2, page_user_1_private
):
    user_role = user_for_page_2.role
    staff_or_not = user_for_page_2.is_staff
    serializer = PageServices.get_page_by_access(
        user_role, staff_or_not, page_user_1_private.id, user_for_page_2
    )

    assert len(serializer) == 1
    assert serializer['name']


def test_get_page_by_access_if_admin_and_moderator(
        admin_pages, moderator_pages, page_user_1_private
):
    user_role = admin_pages.role
    user_role_moderator = moderator_pages.role
    staff_or_not = admin_pages.is_staff
    staff_or_not_moderator = moderator_pages.is_staff
    serializer_admin = PageServices.get_page_by_access(
        user_role, staff_or_not, page_user_1_private.id, admin_pages
    )
    serializer_moderator = PageServices.get_page_by_access(
        user_role_moderator, staff_or_not_moderator, page_user_1_private.id, moderator_pages
    )

    assert serializer_moderator == serializer_admin
    assert len(serializer_admin) > 2
