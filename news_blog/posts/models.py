from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """Модель для постов"""
    title = models.CharField("Заголовок", max_length=150)
    content = models.TextField("Содержание")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts', verbose_name='Автор')
    image = models.ImageField("Фото", upload_to="post_images/", blank=True)
    created_at = models.DateTimeField("Дата создания: ", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        # Сортировка по дате
        ordering = ["-created_at"]

        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comment(models.Model):
    """Модель для вложенных комментариев"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')
    content = models.TextField("Комментарий")

    # Родительский комментарий
    parent = models.ForeignKey("self", on_delete=models.CASCADE,
                               related_name='replies', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
