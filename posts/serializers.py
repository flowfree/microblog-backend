from django.contrib.auth import get_user_model
from rest_framework import serializers 

from .models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Post
        fields = ['id', 'text', 'user', 'created_at']
        read_only_fields = ['user']
