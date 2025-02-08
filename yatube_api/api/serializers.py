# api/serializers.py
from rest_framework import serializers
from posts.models import Post, Group, Comment, Follow
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Post
        fields = '__all__'  # Исправлено: '__all__' вместо 'all'
        read_only_fields = ('id', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'  # Исправлено: '__all__' вместо 'all'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'  # Исправлено: '__all__' вместо 'all'
        read_only_fields = ('id', 'post', 'created')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = '__all__'  # Исправлено: '__all__' вместо 'all'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message="Вы уже подписаны."
            )
        ]

    def validate_following(self, value):
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError("Нельзя подписаться на себя!")
        return value
