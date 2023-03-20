from rest_framework import exceptions

from innotwits.models import Page
from innotwits import serializers


class PageServices:
    @classmethod
    def get_page_by_access(cls, request, page_id) -> serializers:
        user_role = request.user.role  # if admin or moderator -> True
        staff_or_not = request.user.is_staff    # True/False
        page = cls.get_page_by_id(page_id)

        # """It returns extended info page info"""
        if user_role == 'admin' or user_role == 'moderator' or staff_or_not or\
                (user_role == 'user' and page.is_private is False and page.owner.is_blocked is False):
            return serializers.PageSerializer(
                page,
                many=False
            ).data

        # """It returns just page name"""
        elif user_role == 'user' and page.owner.is_blocked is False:
            if page.is_private:
                return serializers.PrivatePageSerializer(
                    page,
                    many=False
                ).data

        else:
            raise exceptions.NotAcceptable

    @classmethod
    def get_page_by_id(cls, page_id) -> Page:
        return Page.objects.filter(id=page_id).first()


class PostServices:
    @classmethod
    def get_page_id(cls, page, request) -> [str or bool]:
        page_id = page.pk
        page_ids = Page.objects.filter(owner=request.user.pk).values_list('id')     # flat=True
        page_ids = [int(page_id[0]) for page_id in page_ids]
        if page_id not in page_ids:
            return False

        return page_id




