from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from django.core.cache import cache
from .models import Conversation, Message
from .serializers import ConversationSerializer
from .utils.huggingface_service import generate_therapist_response
import logging

logger = logging.getLogger(__name__)

class ChatAPIView(APIView):
    """
    Handles therapy chat interactions with rate limiting and enhanced error handling.
    """
    throttle_classes = [UserRateThrottle]  # 100 requests/hour/user by default
    
    def get(self, request):
        return Response(
            {"message": "This endpoint only supports POST requests for chatting."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def post(self, request):
        # Input validation
        user_message = request.data.get('message', '').strip()
        if not user_message:
            return Response(
                {"error": "Message cannot be empty"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create conversation with context-based title
            conversation = self._create_conversation(user_message)
            
            # Generate and cache AI response
            ai_response = self._generate_and_cache_response(user_message, conversation.id)
            
            # Save messages transactionally
            self._save_messages(conversation, user_message, ai_response)

            return Response({
                "response": ai_response,
                "conversation_id": conversation.id,
                "status": "success"
            })

        except Exception as e:
            logger.error(f"Chat error: {str(e)}", exc_info=True)
            return Response(
                {
                    "error": "Unable to process your request",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _create_conversation(self, first_message):
        """Creates conversation with smart title generation"""
        title = f"Session: {first_message[:30]}..." if first_message else "New Session"
        return Conversation.objects.create(
            title=title,
            is_active=True
        )

    def _generate_and_cache_response(self, user_message, conversation_id):
        """Handles response generation with caching"""
        cache_key = f"therapy_response_{hash(user_message)}"
        
        # Check cache first
        if cached := cache.get(cache_key):
            return cached
            
        # Generate fresh response
        response = generate_therapist_response(
            user_message=user_message,
            conversation_id=conversation_id
        )
        
        # Cache for 1 hour (3600 seconds)
        cache.set(cache_key, response, timeout=3600)
        return response

    def _save_messages(self, conversation, user_message, ai_response):
        """Atomic message saving"""
        Message.objects.bulk_create([
            Message(
                conversation=conversation,
                text=user_message,
                is_from_user=True
            ),
            Message(
                conversation=conversation,
                text=ai_response,
                is_from_user=False
            )
        ])

class ConversationHistoryView(APIView):
    """
    Retrieves conversation history with pagination and optional filtering.
    """
    permission_classes = [IsAuthenticated]  # Changed from AllowAny for security
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        try:
            # Get pagination parameters
            page_size = int(request.query_params.get('page_size', 10))
            page = int(request.query_params.get('page', 1))
            
            # Filter conversations for current user only
            conversations = Conversation.objects.filter(
                is_active=True
            ).order_by('-created_at')
            
            # Paginate results
            paginated = self.paginate_queryset(conversations, request)
            serializer = ConversationSerializer(paginated, many=True)
            
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            logger.error(f"History error: {str(e)}", exc_info=True)
            return Response(
                {"error": "Unable to fetch history"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )