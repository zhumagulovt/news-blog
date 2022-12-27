import pytest

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_data():
    data = {
        'first_name': 'Name',
        'last_name': 'Lastname',
        'username': 'username',
        'password': 'Testpassword',
        'password_confirm': 'Testpassword'
    }
    return data


@pytest.mark.django_db
class TestRegistration:

    def test_registration(self, api_client, user_data):

        response = api_client.post('/api/v1/users/registration/', data=user_data)

        assert response.status_code == 201
        assert User.objects.count() == 1

    def test_registration_with_existing_username(self, api_client, user_factory, user_data):
        user_factory.create()

        # Копируем юзернейм существующего пользователя
        user_data['username'] = user_factory.username
        response = api_client.post('/api/v1/users/registration/', data=user_data)

        assert response.status_code == 400
