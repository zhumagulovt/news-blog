from django.db.models import Exists, OuterRef, Value, QuerySet
from django.contrib.auth import get_user_model

from .models import Post

User = get_user_model()


def get_posts() -> QuerySet:
    queryset = Post.objects.select_related("category", "author")
    return queryset


def get_posts_with_is_liked(user: User) -> QuerySet:
    """Получить все посты с дополнительным полем is_liked"""
    queryset = (
        Post.objects
        # Лайкал ли текущий пользователь пост
        .annotate(
            is_liked=Exists(
                Post.likes.through.objects.filter(
                    customuser_id=user.id,
                    post_id=OuterRef('pk')
                )
            )
        )
        .select_related("category", "author")
    )

    return queryset


def get_user_liked_posts(user: User) -> QuerySet:
    """Вернуть все посты которые лайкнул пользователь"""

    return user.likes.annotate(is_liked=Value(True)).select_related('category', 'author')


def get_user_posts(user: User) -> QuerySet:
    """Вернуть все посты пользователя"""
    return user.posts.select_related('category')


def set_or_remove_like(user: User, post: Post) -> None:
    """Создать лайк или удалить"""

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)


def get_root_comments(post: Post) -> QuerySet:
    """Вернуть корневые комментарии поста"""

    root_comments = post.comments.filter(parent=None)\
        .prefetch_related('author', 'replies')

    return root_comments
