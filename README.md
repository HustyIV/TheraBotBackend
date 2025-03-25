# **TheraBot API Documentation**  
**For Mobile Developers**  

This guide explains how to integrate with the TheraBot backend API, which provides AI-powered therapy conversations.  

---

## **📌 Base URL**  
```
https://therabothutsy.onrender.com/ 
```  

---

## **📝 API Endpoints**  

### **1. 💬 Send a Message & Get AI Response**  
**Endpoint:** `POST /chat/`  

**Request:**  
```json
{
    "message": "I've been feeling anxious lately"
}
```  

**Response (Success):**  
```json
{
    "response": "I'm sorry to hear that. Let's explore what might be causing this anxiety. Can you describe when these feelings typically occur?",
    "conversation_id": 5
}
```  

**Possible Errors:**  
| Code | Reason |  
|------|--------|  
| `400` | Empty message |  
| `401` | Invalid/missing Firebase token |  

---

### **2. 📜 Get Conversation History**  
**Endpoint:** `GET /conversations/`  

**Response:**  
```json
[
    {
        "id": 5,
        "title": "Anxiety Discussion",
        "created_at": "2023-11-20T14:30:00Z",
        "messages": [
            {
                "text": "I've been feeling anxious",
                "is_from_user": true,
                "sent_at": "2023-11-20T14:30:05Z"
            },
            {
                "text": "I'm sorry to hear that...",
                "is_from_user": false,
                "sent_at": "2023-11-20T14:30:07Z"
            }
        ]
    }
]
```  

**Notes:**  
- Returns conversations sorted by **newest first**  
- Each conversation includes all messages in chronological order  

---

## **🔧 Testing the API**  

### **1. Using Postman**  
For `POST /chat/`, include JSON body with `message`  

### **2. Using cURL**  
```bash

# Send a message
curl -X POST https://therabothutsy.onrender.com/api/chat/ \
-H "Content-Type: application/json" \
-d '{"message":"Hello"}'
```  

---

## **🛠️ Error Handling**  
- **401 Unauthorized**: Invalid/missing Firebase token  
- **400 Bad Request**: Missing/empty `message` in POST request  
- **500 Server Error**: Contact backend team  

---

## **📱 Mobile Implementation Tips**  

## **🚀 Next Steps**  
1. Integrate the `/chat/` endpoint for real-time messaging  
2. Use `/conversations/` to display chat history  
 

**Need Help?**  
Contact: [christineoyiera51@gmail.com]  

--- 

**Last Updated**: March 2025