"""sampleapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import json 

from django.contrib import admin
from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import ( 
    TokenObtainPairView,
    TokenRefreshView,
)

from account.views import RegisterView


@api_view()
def home(request):
    return Response({'message': 'API is up and running.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reverse(request):
    body = json.loads(request.body.decode('utf-8'))
    message = body.get('message')
    if not message:
        return Response({'message': 'Please specify the input string.'}, status=400)
    else:
        return Response({'message': message[::-1]})


urlpatterns = [
    path('', home),
    path('reverse', reverse),
    path('auth/token', TokenObtainPairView.as_view()),
    path('auth/token/refresh', TokenRefreshView.as_view()),
    path('account/signup', RegisterView.as_view()),
    path('admin/', admin.site.urls),
]
