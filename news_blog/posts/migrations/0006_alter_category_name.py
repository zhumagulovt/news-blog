# Generated by Django 4.1.3 on 2023-01-17 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0005_alter_post_likes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                max_length=150, unique=True, verbose_name="Название"
            ),
        ),
    ]
