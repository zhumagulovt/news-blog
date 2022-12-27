from pytest_factoryboy import register

from .factories import PostFactory, CategoryFactory, CommentFactory

register(PostFactory)
register(CategoryFactory)
register(CommentFactory)
