from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    RegisterSerializer, 
    UserProfileSerializer,
    ChangePasswordSerializer,
)


class RegisterView(generics.CreateAPIView):
    """Signup view"""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def post(self, request, *args, **kwags):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.profile.name = serializer.validated_data['name']
        request.user.profile.bio = serializer.validated_data['bio']
        request.user.profile.website = serializer.validated_data['website']
        request.user.profile.save()

        return Response(serializer.validated_data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        return Response()
