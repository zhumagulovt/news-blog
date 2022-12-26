import pytest

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestProfile:
    url = '/api/v1/users/profile/'

    def test_get_profile(self, logged_in_client):

        api_client, user = logged_in_client
        response = api_client.get(self.url)

        assert response.status_code == 200

    def test_update(self, logged_in_client, user_factory):
        api_client, user = logged_in_client

        new_user_data = user_factory.build()

        data = {
            'username': new_user_data.username,
            'first_name': new_user_data.first_name,
            'last_name': new_user_data.last_name
        }

        response = api_client.patch(self.url, data=data)

        assert response.status_code == 200

    def test_delete_profile(self, logged_in_client):
        api_client, _ = logged_in_client

        assert User.objects.count() == 1

        response = api_client.delete(self.url)
        assert response.status_code == 204
        assert User.objects.count() == 0
