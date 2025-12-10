# Kristal Agent PoC - Backend

FastAPI backend application for the Kristal Agent Proof of Concept.

## Tech Stack

- **Python 3.11+**
- **FastAPI**
- **Pydantic** (Data validation)
- **httpx** (HTTP client)
- **Uvicorn** (ASGI server)

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Update `.env` with your configuration:
```env
AGENT_API_URL=https://google-portal.kristal.ai
AGENT_API_KEY=your-api-key-if-needed
CORS_ORIGINS=http://localhost:3000
```

### Development

Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000)

API documentation:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Production

Run with production settings:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Or using Docker:
```bash
docker build -t kristal-agent-backend .
docker run -p 8000:8000 kristal-agent-backend
```

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── app/
│   ├── config.py          # Configuration settings
│   ├── api/
│   │   ├── routes/        # API route handlers
│   │   └── schemas/       # Pydantic models
│   ├── services/          # Business logic
│   ├── middleware/        # Middleware (CORS, error handling)
│   └── utils/             # Utilities (logger, exceptions)
└── requirements.txt        # Python dependencies
```

## API Endpoints

### Chat
- `POST /api/chat` - Send message to agent

### Session
- `POST /api/session` - Create new session
- `GET /api/session/{session_id}` - Get session details
- `DELETE /api/session/{session_id}` - Delete session

### Health
- `GET /api/health` - Health check

## Environment Variables

- `AGENT_API_URL` - Agent API endpoint URL (required)
- `AGENT_API_KEY` - API key for agent API (optional)
- `CORS_ORIGINS` - Comma-separated list of allowed origins
- `ENVIRONMENT` - Environment (development/production)
- `LOG_LEVEL` - Logging level (INFO/DEBUG/ERROR)
- `SESSION_TIMEOUT_MINUTES` - Session timeout in minutes

## Configuration

The agent API endpoint and request format may need to be adjusted based on the actual API specification. Update `app/services/agent_service.py` to match your agent API:

1. Endpoint path
2. Request payload format
3. Response format mapping

## Deployment

### Railways

1. Connect your GitHub repository
2. Set environment variables in Railways dashboard
3. Deploy

Railways will automatically detect Python and install dependencies.

### Docker

Build and run:
```bash
docker build -t kristal-agent-backend .
docker run -p 8000:8000 --env-file .env kristal-agent-backend
```

## Testing

Run tests (when implemented):
```bash
pytest
```

## Notes

- Session storage is in-memory for PoC. Replace with Redis for production.
- Agent API integration needs to be configured based on actual API spec.
- Error handling is implemented but may need adjustment based on agent API errors.

## Next Steps

- [ ] Add unit tests
- [ ] Implement Redis for session storage
- [ ] Add rate limiting
- [ ] Configure agent API endpoint
- [ ] Add request/response logging
- [ ] Implement streaming support

