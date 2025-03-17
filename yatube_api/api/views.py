from rest_framework import viewsets, exceptions
from django.shortcuts import get_object_or_404
from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise exceptions.PermissionDenied(
                'Изменение чужого контента запрещено!')
        serializer.save(author=self.request.user)

    def perform_destroy(self, serializer):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise exceptions.PermissionDenied(
                'Удаление чужого контента запрещено!')
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post

    def get_queryset(self):
        post = self.get_post()
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        post = self.get_post()
        if serializer.instance.author != self.request.user:
            raise exceptions.PermissionDenied(
                'Изменение чужого контента запрещено!')
        serializer.save(author=self.request.user, post=post)

    def perform_destroy(self, serializer):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise exceptions.PermissionDenied(
                'Удаление чужого контента запрещено!')
        instance.delete()
