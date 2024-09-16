from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from api import serializers
from api import permissions
from posts.models import Comment, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          permissions.IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        post = self.get_post()
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [permissions.IsAuthorOrReadOnly]
        return super().get_permissions()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        return self.request.user.following.all()
