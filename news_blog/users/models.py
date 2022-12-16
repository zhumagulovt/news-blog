from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    Добавил поле для фото профиля.
    Сделал имя и фамилию обязательными полями.
    """

    profile_picture = models.ImageField(
        "Фото профиля", upload_to="profile_pictures/", blank=True
    )
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)
    objects = UserManager()

    def __str__(self):
        return self.username
