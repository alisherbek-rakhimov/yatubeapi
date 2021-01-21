import time

from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer


class OwnResourcePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return request.user == obj.author
        return super().has_object_permission(request, view, obj)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [OwnResourcePermission]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    author = None
    owner = True

    # def create(self, request, *args, **kwargs):
    #     self.author = request.user
    #     return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.author)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        response = super().update(request, *args, **kwargs)
        if post.author != request.user:
            self.owner = False
            response.status_code = status.HTTP_403_FORBIDDEN

        return response

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        response = super().destroy(request, *args, **kwargs)

        if post.author != request.user:
            self.owner = False
            response.status_code = status.HTTP_403_FORBIDDEN

        return response

    def perform_update(self, serializer):
        if self.owner:
            serializer.save()

    def perform_destroy(self, instance):
        if self.owner:
            instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    # queryset = Comment.objects.filter(post=post_id)
    serializer_class = CommentSerializer
    author = None
    owner = True

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        return Comment.objects.filter(post=post)
        # return super().get_queryset()

    def create(self, request, *args, **kwargs):
        self.author = request.user
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.author)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        response = super().update(request, *args, **kwargs)
        if comment.author != request.user:
            self.owner = False
            response.status_code = status.HTTP_403_FORBIDDEN
        return response

    def perform_update(self, serializer):
        if self.owner:
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)

        response = Response(status=status.HTTP_204_NO_CONTENT)

        if comment.author != request.user:
            self.owner = False
            response.status_code = status.HTTP_403_FORBIDDEN
            return response

        if comment.post != post:
            self.owner = False
            response.status_code = status.HTTP_403_FORBIDDEN
            return response

        comment.delete()
        return response

    def perform_destroy(self, instance):
        pass
