from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import serializers
from users.models import Subscription, User
from users.pagination import CustomPagination


class UserSerializer(serializers.ModelSerializer):
    """Basic User Serializer"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        if self.context:
            user = self.context['request'].user
            return (
                user.is_authenticated and obj.subs.filter(user=user).exists()
            )
        else:
            return False


class CreateUserSerializer(serializers.ModelSerializer):
    """Create user Serializer"""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
        extra_kwargs = {

            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = (
            make_password(validated_data.pop('password'))
        )
        return super().create(validated_data)


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=UserSerializer(read_only=True))
    author = UserSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ('author', 'user')

    def validate(self, data):
        id_author = self.context['view'].kwargs['pk']
        author = get_object_or_404(
            User,
            pk=id_author
        )
        user = self.context['request'].user
        if author == user:
            raise serializers.ValidationError(
                {'errors': ['Нельзя подписаться на самого себя']})
        if user.subscriptions.filter(author=author):
            raise serializers.ValidationError(
                {'errors': ['вы уже подписаны']})
        return data

    def create(self, validated_data):
        id_author = self.context['view'].kwargs['pk']
        author = get_object_or_404(
            User,
            pk=id_author
        )
        user = self.context['request'].user
        return Subscription.objects.create(user=user, author=author)


class RecipeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionSerializer(UserSerializer):
    recipes = RecipeShortSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count',)

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class PasswordChangeSerializer(serializers.Serializer):
    model = User
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, new_password):
        password_validation.validate_password(new_password, self.instance)
        return new_password
