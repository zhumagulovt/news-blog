from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views
from .viewsets import UserViewSet


user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

delete_profile_pic = UserViewSet.as_view({
    'delete': 'delete_profile_picture'
})

urlpatterns = [
    path("registration/", views.RegistrationAPIView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", user_detail),
    path("profile/picture/", delete_profile_pic)
]
