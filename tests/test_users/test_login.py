import pytest

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_login(api_client, user_factory):
    user_factory.create()

    data = {
        'username': user_factory.username,
        'password': user_factory.password
    }

    response = api_client.post('/api/v1/users/login/', data=data)

    assert response.status_code == 200
    assert 'refresh' in response.data
    assert 'access' in response.data
