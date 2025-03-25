# **API Endpoint Guide: Conversation History**  
**Endpoint:** `GET /api/conversations/`  
**Authentication:** None (`AllowAny`)  

This endpoint retrieves all conversations sorted by most recent first.  

---

## **📌 Quick Start**
### **1. Base URL**  
```
https://your-api-domain.com/api/conversations/
```

### **2. Request Example**
```bash
curl -X GET "https://your-api-domain.com/api/conversations/" \
-H "Content-Type: application/json"
```

### **3. Expected Response (200 OK)**
```json
[
    {
        "id": 1,
        "title": "Stress Management",
        "created_at": "2025-03-25T10:00:00Z",
        "is_active": true,
        "messages": [
            {
                "text": "I've been feeling anxious",
                "is_from_user": true,
                "sent_at": "2025-03-25T10:05:00Z"
            },
            {
                "text": "Let's explore what might be causing this.",
                "is_from_user": false,
                "sent_at": "2025-03-25T10:05:30Z"
            }
        ]
    }
]
```

---

## **🔍 Response Fields**
| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Unique conversation ID |
| `title` | String | Auto-generated conversation title |
| `created_at` | ISO-8601 | Conversation start time |
| `is_active` | Boolean | `true` if ongoing |
| `messages[]` | Array | List of messages |
| → `text` | String | Message content |
| → `is_from_user` | Boolean | `true` if sent by the user |
| → `sent_at` | ISO-8601 | Timestamp |

---

## **⚠️ Error Cases**
| Status Code | Response Body | Reason |
|------------|---------------|--------|
| `500 Server Error` | `{"detail": "Internal server error"}` | Database/backend issue |

---

## **🛠️ Integration Guide (Mobile)**
### **Android (Kotlin)**
```kotlin
val retrofit = Retrofit.Builder()
    .baseUrl("https://your-api-domain.com/")
    .build()

val api = retrofit.create(ApiService::class.java)
val call = api.getConversations()

call.enqueue(object : Callback<List<Conversation>> {
    override fun onResponse(call: Call<List<Conversation>>, response: Response<List<Conversation>>) {
        if (response.isSuccessful) {
            val conversations = response.body()
            // Update UI
        }
    }
    override fun onFailure(call: Call<List<Conversation>>, t: Throwable) {
        // Handle error
    }
})
```

---

## **🧪 Testing in Development**
1. **Mock Data Response**  
   If the backend is unavailable, mock the response:
   ```json
   [{"id": 1, "title": "Test", "is_active": true, "messages": []}]
   ```

2. **Error Simulation**  
   Test error handling by temporarily changing the endpoint URL to an invalid path.

---

## **📝 Notes for Developers**
- **Pagination**: Currently returns all conversations. Contact backend if pagination is needed.
- **Auto-Refresh**: Poll this endpoint every 60s if real-time updates are required.
- **Filtering**: Use `?is_active=true` to fetch only ongoing conversations (if implemented).

**Last Updated:** March 2025  

---

**🔗 Backend Contact:** [christineoyiera51@gmail.com](mailto:your-email@domain.com)  

Let me know what you'd like to add:
