import os
from django.conf import settings
from huggingface_hub import InferenceClient
import logging

logger = logging.getLogger(__name__)

# Initialize client at module level (reuses connection)
client = InferenceClient(token=os.getenv("HF_API_KEY"))

def generate_therapist_response(user_message, conversation_id):
    """
    Generate response using Hugging Face's cloud Inference API
    """
    try:
        # Structured prompt for therapy context
        prompt = f"""<|system|>
        You are an empathetic AI therapist. Provide supportive, concise responses.
        Focus on active listening and guiding self-reflection.
        </s>
        <|user|>
        {user_message}
        </s>
        <|assistant|>"""
        
        # API call with optimized parameters
        response = client.text_generation(
            prompt,
            model="HuggingFaceH4/zephyr-7b-beta",
            max_new_tokens=150,  # Keeps responses focused
            temperature=0.7,     # Balances creativity/consistency
            repetition_penalty=1.1  # Reduces looping
        )
        
        # Clean output by removing prompt remnants
        return response.split("<|assistant|>")[-1].strip()
        
    except Exception as e:
        logger.error(f"Inference API error: {str(e)}")
        return {
            "response": "I'm currently experiencing high demand. Please try again in a moment.",
            "error": str(e),
            "conversation_id": conversation_id
        }