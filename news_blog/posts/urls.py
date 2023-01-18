from django.urls import path, include

from rest_framework.routers import SimpleRouter

from . import viewsets, views

router = SimpleRouter()
router.register('posts', viewsets.PostViewSet, 'post')
router.register('comments', viewsets.CommentViewSet)

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view()),
    path('posts/my_posts/', views.UserPostListAPIView.as_view()),
    path('posts/favorites/', views.FavoritePostListAPIView.as_view()),
    path('', include(router.urls))
]
