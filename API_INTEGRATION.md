# API Integration Guide

## Agent API Configuration

The backend has been updated to integrate with the actual Kristal Agent API.

### Base URL
```
https://kristal-agent-953081186136.asia-southeast1.run.app
```

### Endpoints

#### 1. Create Session
**Endpoint:** `POST /get_session`

**Request Body:**
```json
{
  "relationship_manager_id": "001",
  "client_id": "19754000",
  "kristal_id": "optional"
}
```

**Response:**
```json
{
  "session_id": "session-uuid"
}
```

#### 2. Send Query
**Endpoint:** `POST /query`

**Request Body:**
```json
{
  "session_id": "session-uuid",
  "relationship_manager_id": "001",
  "client_id": "19754000",
  "kristal_id": "optional",
  "query": "What is my portfolio value?",
  "source": "optional"
}
```

**Response:**
```json
{
  "agent_response": "Response text with markdown...",
  "chart": "chart-url-or-object"
}
```

### Authentication

The API uses Bearer token authentication. The token is configured in the backend:
- **API Key:** `AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4` (GEMINI API Key)
- **Relationship Manager ID:** `001` (default)

### Configuration

Update `backend/.env`:
```env
AGENT_API_URL=https://kristal-agent-953081186136.asia-southeast1.run.app
AGENT_API_KEY=AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4
RELATIONSHIP_MANAGER_ID=001
```

### Response Parsing

The backend automatically parses the `agent_response` text to extract:
- **Sources:** Extracted from markdown links `[name](url)`
- **Validation:** Parsed from validation sections in the response
- **Chart:** Directly from the `chart` field in the API response

### Testing

Test the API directly:
```bash
# Create session
curl -X POST "https://kristal-agent-953081186136.asia-southeast1.run.app/get_session" \
  -H "Authorization: Bearer AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4" \
  -H "Content-Type: application/json" \
  -d '{"relationship_manager_id": "001", "client_id": "19754000"}'

# Send query
curl -X POST "https://kristal-agent-953081186136.asia-southeast1.run.app/query" \
  -H "Authorization: Bearer AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "relationship_manager_id": "001",
    "client_id": "19754000",
    "query": "What is my portfolio value?"
  }'
```

### Notes

1. **Client ID Format:** The backend normalizes client IDs by removing the "K" prefix if present
2. **Session Management:** Sessions are created via the agent API and cached locally
3. **Error Handling:** Network errors and API errors are properly handled and logged
4. **Response Format:** The agent_response is parsed to extract sources and validation information

### Next Steps

1. Test the integration with actual queries
2. Adjust source/validation parsing if the response format differs
3. Handle chart URLs appropriately (may need CORS configuration)
4. Add retry logic for transient failures
5. Implement rate limiting if needed

