from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework_simplejwt.tokens import RefreshToken
import pytest

from posts.models import Post


@pytest.fixture
def user1():
    user = User.objects.create_user('user1', 'user1@example.com', 'password123')
    user.profile.name = 'First User'
    user.profile.bio = 'Full Stack Developer'
    user.profile.website = 'https://www.example.com'
    user.profile.save()

    refresh = RefreshToken.for_user(user)
    user.access_token = str(refresh.access_token)

    return user


@pytest.fixture
def user2():
    user = User.objects.create_user('user2', 'user2@example.com', 'password123')
    refresh = RefreshToken.for_user(user)
    user.access_token = str(refresh.access_token)

    return user


@pytest.fixture
def posts(user1, user2):
    return [
        Post.objects.create(text='First post', user=user1),
        Post.objects.create(text='Second post', user=user1),
        Post.objects.create(text='Third post', user=user2),
    ]
