from django.utils import timezone
from api.models import User

def get_user_from_token(token):
    """Temporary stub for development"""
    try:
        user, _ = User.objects.get_or_create(
            firebase_uid="dev_"+token[:10],  # Mock UID
            defaults={'last_active': timezone.now()}
        )
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None