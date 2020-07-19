from rest_framework.response import Response
from rest_framework import viewsets, status, permissions, filters

from django.shortcuts import get_object_or_404

from .models import User, Post, Follow, Group
from .serializers import (
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupSerializer
)

from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group', None)

        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        serializer.save(author=self.request.user,
                        post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        return post.comments.all()


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['=following__username', '=user__username']

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = self.request.data.get(
                'following'
            )
            if username is None:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            following = User.objects.get(username=username)
            if following is None:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not Follow.objects.filter(
                user=self.request.user,
                following=following
            ).exists():
                serializer.save(user=self.request.user, following=following)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
