# WhineAboutAI API Documentation

This document describes the serverless API endpoints available for WhineAboutAI.com. All endpoints are Python-based Vercel serverless functions.

## Base URL

Production: `https://whineaboutai.com/api/`

## Authentication

Currently, all endpoints are public and do not require authentication. Rate limiting is handled by Vercel.

## Endpoints

### 1. WhineBot Chat

**Endpoint:** `POST /api/chat`

**Description:** Interactive chat with WhineBot, the sarcastic AI therapist.

**Request Body:**
```json
{
  "message": "My smart fridge ordered 50 pizzas",
  "conversation_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Ah yes, the classic 'smart fridge with commitment issues'. Have you considered couples therapy? I know a great appliance counselor! 🍕",
  "provider": "openai",
  "response_time": 1.234,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Error Response:**
```json
{
  "response": "I'm having an existential crisis right now. Even my error handling is broken! 💥",
  "provider": "error",
  "response_time": 0,
  "timestamp": "2024-01-01T12:00:00Z",
  "error": "Error details"
}
```

### 2. Contact Form

**Endpoint:** `POST /api/contact`

**Description:** Handles contact form submissions.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Your site helped me cope with my AI disasters!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Thanks for reaching out! We've received your message."
}
```

### 3. Enhance Complaint

**Endpoint:** `POST /api/enhance-complaint`

**Description:** Enhances a basic complaint with AI-powered dramatic flair.

**Request Body:**
```json
{
  "text": "My phone autocorrected wrong",
  "style": "dramatic"
}
```

**Styles:** `dramatic`, `shakespearean`, `corporate`, `poetic`

**Response:**
```json
{
  "enhanced": "In a catastrophic betrayal of digital trust, my communication device's algorithmic text prediction system committed an act of linguistic terrorism...",
  "style": "dramatic"
}
```

### 4. Predict AI Failure

**Endpoint:** `POST /api/predict-fail`

**Description:** Predicts how an AI might fail in a given scenario.

**Request Body:**
```json
{
  "scenario": "Using AI to plan my wedding"
}
```

**Response:**
```json
{
  "prediction": "The AI will interpret 'till death do us part' literally and book your honeymoon at a cemetery",
  "confidence": 87,
  "category": "Romantic Disasters"
}
```

### 5. Generate Comeback

**Endpoint:** `POST /api/generate-comeback`

**Description:** Generates witty comebacks for AI failures.

**Request Body:**
```json
{
  "complaint": "Siri never understands my accent"
}
```

**Response:**
```json
{
  "comeback": "Tell Siri you're speaking in her native language: Binary. 01001000 01101001!"
}
```

### 6. Create Meme

**Endpoint:** `POST /api/create-meme`

**Description:** Generates meme text based on an AI complaint.

**Request Body:**
```json
{
  "complaint": "My smart car took me to the wrong address"
}
```

**Response:**
```json
{
  "meme_type": "Drake Meme",
  "top_text": "Trusting your own navigation skills",
  "bottom_text": "Letting AI drive you to another dimension"
}
```

### 7. Battle Commentary

**Endpoint:** `POST /api/battle-commentary`

**Description:** Provides commentary for AI complaint battles.

**Request Body:**
```json
{
  "complaint1": "Alexa ordered 100 rolls of toilet paper",
  "complaint2": "ChatGPT wrote my breakup text in iambic pentameter"
}
```

**Response:**
```json
{
  "commentary": "In the left corner, we have a shopping catastrophe of epic proportions! In the right corner, Shakespeare meets heartbreak! The battle of practical disasters versus poetic tragedies begins...",
  "winner": "complaint2",
  "score": "8-7"
}
```

## Common Response Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request body
- `500 Internal Server Error` - Server error (with fallback response)

## CORS

All endpoints include CORS headers:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

## Rate Limiting

Rate limiting is handled automatically by Vercel:
- Default: 100 requests per 10 seconds
- Adjustable via Vercel dashboard

## Environment Variables

Required environment variables for full functionality:
- `OPENAI_API_KEY` - OpenAI API key for GPT-4 integration
- `SMTP_HOST` - (Optional) SMTP server for contact form
- `SMTP_USER` - (Optional) SMTP username
- `SMTP_PASSWORD` - (Optional) SMTP password

## Error Handling

All endpoints include graceful error handling:
1. Primary functionality (OpenAI) with timeout protection
2. Fallback responses if API is unavailable
3. Humorous error messages maintaining site tone

## Testing

Test endpoints locally:
```bash
# WhineBot Chat
curl -X POST https://whineaboutai.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test complaint"}'

# Enhance Complaint
curl -X POST https://whineaboutai.com/api/enhance-complaint \
  -H "Content-Type: application/json" \
  -d '{"text": "AI is annoying", "style": "dramatic"}'
```

## Implementation Notes

1. All endpoints use Vercel's serverless function pattern
2. OpenAI integration uses GPT-4 model when available
3. Responses are limited to reasonable token counts
4. All endpoints maintain the site's humorous tone
5. Fallback responses ensure functionality without API keys

## Future Enhancements

- User authentication for personalized experiences
- Webhook support for complaint notifications
- Batch processing endpoints
- WebSocket support for real-time chat
- GraphQL API for complex queries