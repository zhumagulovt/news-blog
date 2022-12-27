import pytest

from pytest_factoryboy import register

from .factories import UserFactory

register(UserFactory)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def logged_in_client(api_client, user_factory):
    user = user_factory.create()
    api_client.force_authenticate(user=user)

    return api_client, user
