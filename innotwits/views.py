from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from innotwits.models import Page, Post, Tag
from innotwits.permissions import IsOwnerAdminModeratorCanEdit, IsAdminModeratorDeleteIsOwnerDeleteUpdate
from innotwits import serializers
from innotwits.services import PageServices, PostServices
from users.models import User


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Page.objects.all()

    action_to_serializer = {
        "retrieve": serializers.PageSerializer,
        "create": serializers.CreatePageSerializer,
        "partial_update": serializers.UpdatePageSerializer,
        "tag": serializers.TagSerializer
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsOwnerAdminModeratorCanEdit(), ]
        return [IsAuthenticatedOrReadOnly(), ]

    def retrieve(self, request, *args, **kwargs):
        """
        Get a definite page;
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        page_id = kwargs['pk']
        page = PageServices.get_page_by_access(request=self.request, page_id=page_id)
        if not page:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(page, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create another page for user
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=request.user.pk)     #
        create_page = Page.objects.create(
            name=serializer.validated_data.get('name'),
            description=serializer.validated_data.get('description'),
            owner_id=user.pk,
        )
        return Response(
            serializers.CreatePageSerializer(create_page).data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['post', 'delete'], detail=True)
    def tag(self, request, pk=None):
        data = request.data
        page = self.get_object()
        tag = data.get("name").lower()
        if request.method == 'POST':
            tag, created = Tag.objects.get_or_create(name=tag)
            page.tags.add(tag)

        elif request.method == 'DELETE':
            try:
                tag_to_delete = page.tags.get(name__exact=tag)
            except Tag.DoesNotExist:
                raise Http404
            page.tags.remove(tag_to_delete)
            return Response('Tag was deleted')
        return Response('Tag was successfully added')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE'] and self.action != 'like':
            return [IsAdminModeratorDeleteIsOwnerDeleteUpdate(), ]

        return [IsAuthenticatedOrReadOnly(), ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = serializer.validated_data.get('page')
        page_id = PostServices.get_page_id(page, request)
        if not page_id:
            return Response(
                'It is not your page. Posting is forbidden',
                status=status.HTTP_403_FORBIDDEN
            )

        create_post = Post.objects.create(
            page_id=page_id,
            content=serializer.validated_data.get('content'),
        )
        return Response(
            serializers.PostSerializer(create_post).data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['post'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        if not post.like.filter(id=request.user.pk).exists():
            post.like.add(request.user)
            return Response('Creating like', status=status.HTTP_201_CREATED)

        post.like.remove(request.user)
        return Response('Unlike', status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        pass
