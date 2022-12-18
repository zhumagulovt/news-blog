from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """Модель для постов"""
    title = models.CharField("Заголовок", max_length=150)
    content = models.TextField("Содержание")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts', verbose_name='Автор')
    created_at = models.DateTimeField("Дата создания: ", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        # Сортировка по дате
        ordering = ["-created_at"]
