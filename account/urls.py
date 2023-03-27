from django.urls import path
from .views import UserProfileView, ChangePasswordView

urlpatterns = [
    path('profile', UserProfileView.as_view()),
    path('change_password', ChangePasswordView.as_view()),
]
