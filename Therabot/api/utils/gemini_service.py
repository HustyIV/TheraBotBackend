import os
import google.generativeai as genai
from django.apps import apps  # Use this for dynamic model import


def generate_therapist_response(user_message, conversation_id):
    """
    Generate a therapist response using Gemini AI
    """
    if not os.getenv('GEMINI_API_KEY'):
        return "Gemini API key not found. Please set the GEMINI_API_KEY environment variable."
    try:
        # Dynamic model import to avoid potential circular import
        Conversation = apps.get_model('api', 'Conversation')
        Message = apps.get_model('api', 'Message')

        # Configure the Gemini API
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_output_tokens": 300,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        # Retrieve the conversation and its messages
        conversation = Conversation.objects.get(id=conversation_id)
        
        # Get previous messages in the conversation
        previous_messages = Message.objects.filter(
            conversation=conversation
        ).order_by('sent_at')
        
        # Prepare conversation history for AI processing
        conversation_context = "\n".join([
            f"{'User' if msg.is_from_user else 'Therapist'}: {msg.text}" 
            for msg in previous_messages
        ])
        
        # Construct the full prompt
        full_prompt = f"""
        You are a compassionate AI therapist. Provide a supportive and empathetic response.
        
        Conversation Context:
        {conversation_context}
        
        Latest User Message:
        {user_message}
        
        Therapist Response:
        """
        
        # Initialize the model
        # model = genai.GenerativeModel(
        #     model_name="gemini-pro",
        #     generation_config=generation_config,
        #     safety_settings=safety_settings
        # )
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        # Generate response
        response = model.generate_content(full_prompt)
        
        # Extract and clean the response text
        ai_response = response.text.strip()
        
        return ai_response
    
    except Conversation.DoesNotExist:
        return "Sorry, I couldn't find the conversation."
    except Exception as e:
        error_msg = f"Gemini Error: {str(e)}"
        print(error_msg)
        return {
        "response": "I'm having technical difficulties. Please try again later.",
        "error": error_msg, 
        "conversation_id": conversation_id
    }