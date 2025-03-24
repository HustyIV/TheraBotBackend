from django.urls import path
from .views import ChatHistoryListCreateView, ChatHistoryDetailView

urlpatterns = [
    path('chat-history/', ChatHistoryListCreateView.as_view(), name='chat-history-list-create'),
    path('chat-history/<int:pk>/', ChatHistoryDetailView.as_view(), name='chat-history-detail'),
]