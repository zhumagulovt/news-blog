from rest_framework import status, mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
)

from django_filters.rest_framework import DjangoFilterBackend

from .models import Comment
from .serializers import (
    PostSerializer,
    CommentSerializer
)
from .permissions import IsOwnerOrReadOnly
from . import services


class PostViewSet(ModelViewSet):

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category',)
    search_fields = ('title',)

    def perform_create(self, serializer):
        """При сохранении установить текущего пользователя как автора поста"""
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Если авторизован, то с полем is_liked
        if self.request.user.is_authenticated:
            return services.get_posts_with_is_liked(self.request.user)
        return services.get_posts()

    @extend_schema(request=None, responses=None)
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        """Поставить или отменить лайк"""

        post = self.get_object()
        user = request.user
        services.set_or_remove_like(user, post)

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def comments(self, request, pk):
        """Получить все комментарии поста"""

        post = self.get_object()

        # Получить только корневые комментарии
        # Вложенные комментарии будут получены в сериалайзере
        root_comments = services.get_root_comments(post)

        serializer = CommentSerializer(root_comments, many=True)
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
