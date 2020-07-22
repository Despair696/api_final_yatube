from rest_framework import serializers

from .models import User, Post, Comment, Follow, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    def validate(self, data):
        if data.get('user') == data.get('following'):
            raise serializers.ValidationError('You cannot follow yourself')
        return data

    class Meta:
        fields = ('user', 'following',)
        model = Follow
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]


class GroupSerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        fields = ('title', 'slug', 'id',)
        model = Group
