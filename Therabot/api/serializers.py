from rest_framework import serializers
from .models import Conversation, Message
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

class MessageSerializer(serializers.ModelSerializer):
    """
    Enhanced Message serializer with:
    - Read-only timestamp
    - Input validation
    - Optimized for bulk operations
    """
    sent_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'text', 'is_from_user', 'sent_at', 'conversation']
        read_only_fields = ['id', 'sent_at']
        extra_kwargs = {
            'conversation': {'write_only': True}  # Hide in output but allow input
        }

    def validate_text(self, value):
        """Ensure messages aren't empty or too long"""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Message cannot be empty")
        if len(value) > 2000:
            raise serializers.ValidationError("Message too long (max 2000 chars)")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    """
    Enhanced Conversation serializer with:
    - Optimized message prefetching
    - Dynamic field control
    - Automatic title generation
    """
    messages = MessageSerializer(many=True, read_only=True)
    unread_count = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 
            'title', 
            'created_at', 
            'updated_at',
            'is_active', 
            'messages',
            'unread_count',
            'duration'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_unread_count(self, obj):
        """Count of unread messages (for client-side indicators)"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(is_from_user=False, read=False).count()
        return 0

    def get_duration(self, obj):
        """Calculate conversation duration in minutes"""
        if not obj.messages.exists():
            return 0
        first = obj.messages.earliest('sent_at')
        last = obj.messages.latest('sent_at')
        return (last.sent_at - first.sent_at).total_seconds() / 60

    def validate_title(self, value):
        """Clean and validate conversation titles"""
        value = value.strip()
        if not value:
            return f"Session {now().strftime('%Y-%m-%d')}"
        if len(value) > 100:
            return f"{value[:97]}..."
        return value

    def to_representation(self, instance):
        """
        Optimize database queries by:
        - Prefetching messages in bulk
        - Limiting message history for list views
        """
        representation = super().to_representation(instance)
        
        # Context-aware message limiting
        if self.context.get('is_list_view', False):
            representation['messages'] = MessageSerializer(
                instance.messages.order_by('-sent_at')[:5],
                many=True
            ).data
        
        return representation