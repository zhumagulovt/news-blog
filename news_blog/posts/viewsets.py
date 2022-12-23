from rest_framework import status, mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
)

from .models import Post, Comment
from .serializers import (
    PostSerializer,
    CommentSerializer,
    CommentRepliesSerializer
)
from .permissions import IsOwnerOrReadOnly


@extend_schema_view(
    list=extend_schema(description="Получить все посты"),
    create=extend_schema(description="Создать новый пост"),
    retrieve=extend_schema(description="Получить данные о посте"),
    partial_update=extend_schema(description="Частично изменить пост"),
    update=extend_schema(description="Полностью изменить пост"),
    destroy=extend_schema(description="Удалить пост"),
)
class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related("category", "author")
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        """При сохранении установить текущего пользователя как автора поста"""
        serializer.save(author=self.request.user)

    @extend_schema(request=None)
    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def my_posts(self, request):
        """Вернуть все посты пользователя"""
        user = request.user
        user_posts = user.posts.all()

        serializer = self.get_serializer(user_posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=None)
    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def favorites(self, request):
        """Вернуть все посты которые пользователь лайкнул"""

        user = request.user
        favorite_posts = user.likes.all()

        serializer = self.get_serializer(favorite_posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=None, responses=None)
    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticated]
    )
    def like(self, request, pk):
        """Поставить или отменить лайк"""

        post = self.get_object()
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)

        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        responses=CommentSerializer,
        examples=[OpenApiExample(
            name="Example",
            value=[{"id": 1, "post": 1, "author": 1,
                    "content": "This is comment",
                    "created_at": "2022-12-21T16:00",
                    "replies":
                        [{"id": 2, "post": 1, "author": 1,
                          "content": "This is reply for comment",
                          "created_at": "2022-12-21T17:44",
                          "replies": []}]}])]
    )
    @action(detail=True, methods=["get"])
    def comments(self, request, pk):
        """Получить все комментарии поста"""
        post = self.get_object()

        # Получить только корневые комментарии
        # Вложенные комментарии будут получены в сериалайзере
        root_comments = post.comments.filter(parent=None) \
            .select_related('author', 'post')

        serializer = CommentRepliesSerializer(root_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):

    queryset = Comment.objects.select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        """
        При сохранении установить текущего пользователя как автора комментария
        """
        serializer.save(author=self.request.user)
