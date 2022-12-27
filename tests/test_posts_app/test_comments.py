import pytest

from news_blog.posts.models import Post, Comment


@pytest.mark.django_db
class TestComments:
    URL = '/api/v1/news/comments/'

    def test_create_comment(self, logged_in_client, post_factory, comment_factory):
        api_client, user = logged_in_client

        post = post_factory()
        comment = comment_factory.build()

        data = {
            'content': comment.content,
            'post': post.pk
        }
        response = api_client.post(self.URL, data=data)

        assert response.status_code == 201

    def test_update_comment(self, logged_in_client, comment_factory):
        api_client, user = logged_in_client

        comment = comment_factory(author=user)
        new_comment_data = comment_factory.build()

        data = {
            'content': new_comment_data.content
        }

        url = self.URL + f'{comment.pk}/'
        response = api_client.patch(url, data=data)

        assert response.status_code == 200

    def test_delete_comment(self, logged_in_client, comment_factory):
        api_client, user = logged_in_client

        comment = comment_factory(author=user)
        url = self.URL + f'{comment.pk}/'
        response = api_client.delete(url)

        assert response.status_code == 204
        assert Comment.objects.count() == 0
