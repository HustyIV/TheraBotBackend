from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Conversation, Message
from .serializers import ConversationSerializer
from api.utils.gemini_service import generate_therapist_response

class ChatAPIView(APIView):
    def post(self, request):
        user_message = request.data.get('message', '').strip()
        if not user_message:
            return Response({"error": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new conversation for each interaction
        conversation = Conversation.objects.create(
            title="New Session",
            is_active=True
        )
        
        # Save user message
        Message.objects.create(
            conversation=conversation,
            text=user_message,
            is_from_user=True
        )
        
        # Generate AI response
        ai_response = generate_therapist_response(
            user_message=user_message,
            conversation_id=conversation.id
        )
        
        # Save AI message
        Message.objects.create(
            conversation=conversation,
            text=ai_response,
            is_from_user=False
        )
        
        return Response({
            "response": ai_response,
            "conversation_id": conversation.id
        })

class ConversationHistoryView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Retrieve all conversations, ordered by most recent
        conversations = Conversation.objects.order_by('-created_at')
        
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)