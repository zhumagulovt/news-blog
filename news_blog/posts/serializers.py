from rest_framework import serializers

from news_blog.users.serializers import UserSerializer

from .models import Post, Category, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    # Поле для получения категории
    category = CategorySerializer(read_only=True)

    # Поле для создания или изменения категории по id
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        write_only=True,
        queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content',
                  'category', 'category_id', 'created_at', 'image']


class RecursiveField(serializers.Serializer):
    """
    Поле сериалайзер для ссылки на самого себя
    """
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для вложенных комментариев
    """
    author = UserSerializer(read_only=True)
    replies = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'replies']
