from django.db import models 
from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
