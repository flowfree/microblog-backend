from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,
                                     validators=[UniqueValidator(
                                        queryset=User.objects.all(),
                                        message='This username is already taken'
                                     )])
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(
                                        queryset=User.objects.all(),
                                        message='This email address is already taken'
                                    )])
    password = serializers.CharField(write_only=True, 
                                     required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, 
                                      required=True)
    agreement = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'agreement')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': "Password confirmation does not match."
            })
        if attrs['agreement'] is not True:
            raise serializers.ValidationError({
                'agreement': 'You need to agree with our Terms of Service to continue'
            })

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


class AppTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'website']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField(write_only=True, 
                                     required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, 
                                      required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user or not user.check_password(value):
            raise serializers.ValidationError('Wrong password.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': "Password confirmation does not match."
            })

        return attrs
