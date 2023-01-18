from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Category
from .serializers import CategorySerializer, PostSerializer
from . import services


class CategoryListAPIView(ListAPIView):
    """Получить все категории"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserPostListAPIView(ListAPIView):
    """Получить все посты текущего пользователя"""

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = services.get_user_posts(user)

        return queryset


class FavoritePostListAPIView(ListAPIView):
    """Вернуть все посты которые пользователь лайкнул"""

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = services.get_user_liked_posts(user)

        return queryset
