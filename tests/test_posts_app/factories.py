from factory.django import DjangoModelFactory
from factory import Faker, SubFactory

from ..factories import UserFactory


class CategoryFactory(DjangoModelFactory):

    class Meta:
        model = 'posts.Category'

    name = Faker('word')


class PostFactory(DjangoModelFactory):

    class Meta:
        model = 'posts.Post'

    title = Faker('word')
    content = Faker('text')
    category = SubFactory(CategoryFactory)
    author = SubFactory(UserFactory)


class CommentFactory(DjangoModelFactory):
    """Factory для создания не вложенных комментариев"""

    class Meta:
        model = 'posts.Comment'

    post = SubFactory(PostFactory)
    author = SubFactory(UserFactory)
    content = Faker('text')
