from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema_view, extend_schema

from .serializers import UserSerializer


@extend_schema_view(
    retrieve=extend_schema(description='Получить данные о текущем пользователе'),
    partial_update=extend_schema(description='Частично изменить текущего пользователя'),
    update=extend_schema(description='Полностью изменить текущего пользователя'),
    destroy=extend_schema(description='Удалить текущего пользователя')
)
class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    """
    ViewSet для получения, изменения и удаления профиля
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        return user

    @action(detail=False)
    def delete_profile_picture(self, request):
        user = self.get_object()
        if user.profile_picture:
            user.profile_picture = None
            user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
