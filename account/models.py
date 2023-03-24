from django.db import models 
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserManager(BaseUserManager):
    """
    Custom model manager for our custom User model. 
    """
    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(username, email, password, **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Please specify the email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        try:
            UserProfile.objects.create(user=user)
        except Exception: 
            pass

        return user


class User(AbstractUser):
    """
    Custom user model 
    """
    objects = UserManager()


class UserProfile(models.Model):
    name = models.CharField(max_length=125, blank=True, null=True)
    user = models.OneToOneField(User, 
                                related_name='profile', 
                                on_delete=models.CASCADE)
