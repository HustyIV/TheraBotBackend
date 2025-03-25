from django.db import models
from django.utils import timezone

class Conversation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    
    mood_start = models.CharField(max_length=50, blank=True)
    mood_end = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['-created_at']

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    is_from_user = models.BooleanField(default=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    sentiment = models.FloatField(null=True, blank=True)
    keywords = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ['sent_at']