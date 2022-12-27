import pytest

from news_blog.posts.models import Post


@pytest.mark.django_db
class TestPosts:
    URL = '/api/v1/news/posts/'

    def test_get_posts(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == 200

    def test_get_posts_with_category(self, api_client, post_factory):
        post = post_factory()

        url = self.URL + f'?category={post.category_id}'
        response = api_client.get(url)

        assert response.status_code == 200

    def test_search_post(self, api_client, post_factory):
        post = post_factory()

        url = self.URL + f'?search={post.title}'
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data[0]['id'] == post.id

    def test_create_post(self, logged_in_client, post_factory, category_factory):
        api_client, user = logged_in_client

        post = post_factory.build()
        category = category_factory()

        data = {
            'title': post.title,
            'content': post.content,
            'category_id': category.id
        }

        response = api_client.post(self.URL, data=data)

        assert response.status_code == 201
        assert Post.objects.count() == 1

    def test_get_favorites(self, logged_in_client, post_factory):

        api_client, user = logged_in_client

        favorite_posts_count = 10
        posts = post_factory.create_batch(favorite_posts_count)

        for post in posts:
            post.likes.add(user)

        url = self.URL + 'favorites/'
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == favorite_posts_count

    def test_get_my_posts(self, logged_in_client, post_factory):
        api_client, user = logged_in_client

        my_posts_posts_count = 10
        post_factory.create_batch(my_posts_posts_count, author=user)

        url = self.URL + 'my_posts/'
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == my_posts_posts_count
