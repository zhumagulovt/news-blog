from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly


@extend_schema_view(
    list=extend_schema(
        description='Получить все посты'
    ),
    create=extend_schema(
        description='Создать новый пост'
    ),
    retrieve=extend_schema(
        description='Получить данные о посте'
    ),
    partial_update=extend_schema(
        description='Частично изменить пост'
    ),
    update=extend_schema(
        description='Полностью изменить пост'
    ),
    destroy=extend_schema(
        description='Удалить пост'
    )
)
class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('category', 'author')
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        """При сохранении установить текущего пользователя как автора поста"""
        serializer.save(author=self.request.user)
