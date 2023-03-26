from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = User

admin.site.register(User, CustomUserAdmin)
