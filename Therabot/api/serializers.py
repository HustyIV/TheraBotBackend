from rest_framework import serializers
from .models import chatHistory

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = chatHistory
        fields = '__all__'  # Include all fields in the model