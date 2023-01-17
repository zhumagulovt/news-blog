from rest_framework import serializers

from news_blog.users.serializers import UserSerializer

from .models import Post, Category, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    is_liked = serializers.BooleanField(read_only=True, default=None)
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content', 'is_liked',
                  'category', 'created_at', 'image']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        write_only=True,
        required=False,
        queryset=Comment.objects.all()
    )

    class Meta:
        model = Comment
        fields = ['id', 'post', 'parent', 'author',
                  'content', 'created_at']

    def validate(self, data):
        """Если комментарий вложенный т.е имеет поле parent,
        проверить к одному ли посту относятся создаваемый
        комментарий и родительский комментарий"""

        parent_comment = data.get('parent', None)

        if parent_comment:
            post_of_new_comment = data.get('post', None)

            post_of_parent_comment = parent_comment.post

            if post_of_parent_comment != post_of_new_comment:
                raise serializers.ValidationError(
                    {'post': 'Неверный post_id, '
                             'родительский комментарий относится к другому посту'}
                )

        return data

    def get_extra_kwargs(self):
        """
        При методе UPDATE или PATCH сделать поле post не записываемым.
        Чтобы нельзя было поменять пост комментария.
        """
        extra_kwargs = super(CommentSerializer, self).get_extra_kwargs()

        if self.instance:
            post_kwarg = extra_kwargs.get('post', {})
            post_kwarg['read_only'] = True
            extra_kwargs['post'] = post_kwarg

        return extra_kwargs


class RecursiveField(serializers.Serializer):
    """
    Поле сериалайзер для ссылки на самого себя
    """
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentRepliesSerializer(CommentSerializer):
    """
    Сериалайзер для вложенных комментариев
    """
    replies = RecursiveField(read_only=True, many=True)

    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields + ['replies']
