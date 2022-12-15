from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import RegistrationSerializer

User = get_user_model()


class RegistrationAPIView(GenericAPIView):
    """
    View for registration
    """
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)

        return Response(
            "Новый пользователь успешно создан",
            status=status.HTTP_201_CREATED
        )
