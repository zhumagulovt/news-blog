from django.urls import path, include

from rest_framework.routers import SimpleRouter

from . import viewsets

router = SimpleRouter()
router.register('', viewsets.PostViewSet)

urlpatterns = [
    path('', include(router.urls))
]
