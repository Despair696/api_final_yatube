from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework import mixins

from django.shortcuts import get_object_or_404

from .models import Post, Follow, Group
from .serializers import (
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupSerializer
)
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly,
    )
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user,
                        post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['=following__username', '=user__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
