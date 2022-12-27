import pytest

from news_blog.posts.models import Post


@pytest.mark.django_db
class TestPost:

    URL = '/api/v1/news/posts/'

    def test_get_post(self, api_client, post_factory):
        post = post_factory()

        url = self.URL + f'{post.id}/'
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data['id'] == post.id

    def test_update_post(self, logged_in_client, post_factory):
        api_client, user = logged_in_client

        post = post_factory(author=user)

        new_post_data = post_factory.build()

        data = {
            'title': new_post_data.title,
            'content': new_post_data.content
        }

        url = self.URL + f'{post.id}/'
        response = api_client.patch(url, data=data)

        assert response.status_code == 200
        assert response.data['title'] == new_post_data.title
        assert response.data['content'] == new_post_data.content

    def test_delete_post(self, logged_in_client, post_factory):
        api_client, user = logged_in_client

        post = post_factory(author=user)

        url = self.URL + f'{post.id}/'
        response = api_client.delete(url)

        assert response.status_code == 204
        assert Post.objects.count() == 0

    def test_like(self, logged_in_client, post_factory):
        api_client, user = logged_in_client

        post = post_factory()

        url = self.URL + f'{post.id}/like/'
        response = api_client.post(url)

        assert response.status_code == 200
        assert post.likes.count() == 1

    def test_unlike(self, logged_in_client, post_factory):

        api_client, user = logged_in_client

        post = post_factory()
        post.likes.add(user)

        url = self.URL + f'{post.id}/like/'
        response = api_client.post(url)

        assert response.status_code == 200
        assert post.likes.count() == 0

    def test_get_comments(self, api_client, post_factory, comment_factory):
        post = post_factory()

        comments_count = 10
        comment_factory.create_batch(comments_count, post=post)

        url = self.URL + f'{post.id}/comments/'
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == comments_count
