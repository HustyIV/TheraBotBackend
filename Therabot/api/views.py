from rest_framework import generics
from .models import chatHistory
from .serializers import ChatHistorySerializer

# List all chat histories or create a new one
class ChatHistoryListCreateView(generics.ListCreateAPIView):
    queryset = chatHistory.objects.all()
    serializer_class = ChatHistorySerializer

# Retrieve, update, or delete a specific chat history
class ChatHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = chatHistory.objects.all()
    serializer_class = ChatHistorySerializer