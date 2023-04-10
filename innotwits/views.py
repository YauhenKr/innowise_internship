from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, status
from rest_framework.response import Response

from innotwits.models import Page, Post
from innotwits.services import PageServices, PostServices
from innotwits.permissions import IsOwnerAdminModeratorCanEdit,\
    IsAdminModeratorDeleteIsOwnerDeleteUpdate
from innotwits import serializers
from users import serializers as user_serializers
from users.models import User


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Page.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'tags__name', 'uuid', 'owner__username']

    action_to_serializer = {
        "list": serializers.PageSerializer,
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
        user_role = request.user.role
        staff_or_not = request.user.is_staff
        page_id = kwargs['pk']
        page = PageServices.get_page_by_access(
            user_role, staff_or_not, page_id=page_id, user=request.user
        )
        return Response(page, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create page for user
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=request.user.pk)
        name = serializer.validated_data.get('name'),
        description = serializer.validated_data.get('description'),
        is_private = serializer.validated_data.get('is_private', False)
        create_page = PageServices.create_page(name, description, user, is_private)
        return Response(
            serializers.CreatePageSerializer(create_page).data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['post', 'delete'], detail=True)
    def tag(self, request, pk=None):
        """
        Creating a new tag and adding to the page/Unpinning from the page
        """
        data = request.data
        page = self.get_object()
        tag = data.get("name").lower()
        method = request.method
        response = PageServices.create_delete_tag(method, tag, page)
        return Response(response, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def send_following_unfollowing_request(self, request, pk=None):
        """
        Sending follow/unfollow request
        """
        page = self.get_object()
        page_id = page.pk
        user_id = request.user.pk
        unfollow = request.data.get('unfollow')
        if unfollow:
            subscribe_bool, text = PageServices.unfollow_page(user_id, page, unfollow)
            return Response(text)
        else:
            subscribe_bool, text = PageServices.subscribe_to_page(user_id, page_id)
            return Response(text)

    @action(methods=['get'], detail=True)
    def list_followers_requests(self, request, pk=None):
        """
        Getting a list with follower's requests
        """
        page = self.get_object()
        user = User.objects.get(id=request.user.pk)
        page = Page.objects.get(id=page.pk)
        if page.owner == user:
            if page.is_private:
                all_requests = page.follow_requests.all()
                return Response(
                    user_serializers.UserSerializer(all_requests, many=True).data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response('You have no requests. Page is not private')
        else:
            return Response('Forbidden. It is not your page!')

    @action(methods=['post'], detail=True)
    def approve_disapprove_request(self, request, pk=None):
        """
        Approving/disapproving one or list of requests
        """
        page = self.get_object()
        user = User.objects.get(id=request.user.pk)
        page = Page.objects.get(id=page.pk)
        accept = request.data.get('accept')
        request_user_ids = request.data.get('request_user_ids')
        response_text = PageServices.approve_disapprove_request(page, user, request_user_ids, accept)
        return Response(response_text, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE'] and self.action != 'like':
            return [IsAdminModeratorDeleteIsOwnerDeleteUpdate(), ]

        return [IsAuthenticatedOrReadOnly(), ]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.RetrievePostSerializer

        return serializers.PostSerializer

    def list(self, request, *args, **kwargs):
        """
        Getting a list of user's and followings' posts
        """
        user = request.user
        posts = self.get_queryset()
        posts = PostServices.get_posts_list(user, posts)
        return Response(
            serializers.RetrievePostSerializer(posts, many=True).data,
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        """
        Creating a new post or creating a reply to it
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = serializer.validated_data.get('page')
        reply_to = serializer.validated_data.get('reply_to')
        page_id = PostServices.get_page_id(page, request)
        if not page_id:
            return Response(
                'It is not your page. Posting is forbidden',
                status=status.HTTP_403_FORBIDDEN
            )

        create_post = PostServices.create_new_post(page_id, serializer, reply_to)
        return Response(
            serializers.PostSerializer(create_post).data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['post'], detail=True)
    def like(self, request, pk=None):
        """
        Liking/unliking posts
        """
        post = self.get_object()
        if not post.like.filter(id=request.user.pk).exists():
            post.like.add(request.user)
            return Response('Creating like', status=status.HTTP_201_CREATED)

        post.like.remove(request.user)
        return Response('Unlike', status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def list_liked_posts(self, request, *args, **kwargs):
        """
        Getting a list of liked posts
        """
        posts = self.get_queryset()
        liked_posts = PostServices.get_liked_posts(posts, request)
        return Response(
            serializers.PostSerializer(liked_posts, many=True).data,
            status=status.HTTP_200_OK
        )
