from django.urls import path, include

from rest_framework.routers import SimpleRouter

from . import viewsets

router = SimpleRouter()
router.register('posts', viewsets.PostViewSet)
router.register('comments', viewsets.CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
