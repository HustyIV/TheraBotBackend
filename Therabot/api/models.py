from django.db import models
from django.contrib.auth.models import User

class user(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

# Create your models here.
class chatHistory(models.Model):
    user = models.CharField(User)
    message = models.TextField()
    is_user_message = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.user.username} at {self.timestamp}"
    