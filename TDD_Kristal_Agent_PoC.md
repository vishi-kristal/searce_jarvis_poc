# Technical Design Document (TDD)
## Kristal Agent PoC UI

**Version:** 1.0  
**Date:** January 2025  
**Status:** Draft  
**Owner:** Engineering Team

---

## 1. Document Overview

### 1.1 Purpose
This document provides detailed technical specifications for implementing the Kristal Agent PoC UI, including system architecture, API design, component structure, and deployment strategy.

### 1.2 Scope
- Frontend application (Next.js 15)
- Backend API (FastAPI)
- Integration with Kristal Agent API
- Deployment configuration
- Security and performance considerations

### 1.3 Audience
- Frontend developers
- Backend developers
- DevOps engineers
- Technical leads

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Next.js Frontend (Vercel)                    │  │
│  │  - React 19 Components                                │  │
│  │  - Vercel AI SDK (Streaming)                          │  │
│  │  - Tailwind CSS                                       │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS/REST API
                        │
┌───────────────────────▼─────────────────────────────────────┐
│         FastAPI Backend (Railways)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  - REST API Endpoints                                 │  │
│  │  - Session Management                                 │  │
│  │  - Request/Response Validation                        │  │
│  │  - Error Handling                                     │  │
│  └───────────────────────┬──────────────────────────────┘  │
└───────────────────────────┼────────────────────────────────┘
                            │ HTTPS/REST API
                            │
┌───────────────────────────▼────────────────────────────────┐
│      Kristal Agent API (Cloud Run)                          │
│  https://google-portal.kristal.ai                           │
│  - Multi-Agent System                                       │
│  - Query Processing                                         │
│  - Response Generation                                       │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Component Architecture

**Frontend (Next.js App Router):**
```
app/
├── layout.tsx                 # Root layout
├── page.tsx                   # Main chat page
├── api/                       # API routes (if needed)
│   └── proxy/                 # Proxy endpoints
├── components/
│   ├── chat/
│   │   ├── ChatContainer.tsx  # Main chat wrapper
│   │   ├── MessageList.tsx    # Message display
│   │   ├── MessageBubble.tsx  # Individual message
│   │   ├── ChatInput.tsx      # Input component
│   │   └── LoadingIndicator.tsx
│   ├── sources/
│   │   ├── SourceList.tsx     # Source links display
│   │   └── SourceLink.tsx     # Individual source
│   ├── validation/
│   │   ├── ValidationBadge.tsx
│   │   └── ValidationDetails.tsx
│   ├── session/
│   │   ├── SessionManager.tsx
│   │   └── ClientIdInput.tsx
│   └── ui/                    # Reusable UI components
│       ├── Button.tsx
│       ├── Input.tsx
│       └── Card.tsx
├── lib/
│   ├── api/
│   │   └── agent.ts          # API client
│   ├── hooks/
│   │   ├── useChat.ts        # Chat hook
│   │   └── useSession.ts    # Session hook
│   ├── utils/
│   │   ├── markdown.ts       # Markdown utilities
│   │   └── storage.ts       # Local storage utilities
│   └── types/
│       └── agent.ts          # TypeScript types
└── styles/
    └── globals.css           # Global styles
```

**Backend (FastAPI):**
```
backend/
├── main.py                   # FastAPI app entry
├── app/
│   ├── __init__.py
│   ├── config.py            # Configuration
│   ├── dependencies.py       # Dependency injection
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── chat.py      # Chat endpoints
│   │   │   ├── session.py   # Session endpoints
│   │   │   └── health.py    # Health check
│   │   └── schemas/
│   │       ├── chat.py      # Request/response models
│   │       └── session.py
│   ├── services/
│   │   ├── agent_service.py # Agent API integration
│   │   └── session_service.py # Session management
│   ├── middleware/
│   │   ├── cors.py          # CORS configuration
│   │   ├── rate_limit.py    # Rate limiting
│   │   └── error_handler.py # Error handling
│   └── utils/
│       ├── logger.py         # Logging utilities
│       └── exceptions.py    # Custom exceptions
├── requirements.txt
└── Dockerfile               # For containerization (optional)
```

---

## 3. API Design

### 3.1 Backend API Endpoints

#### 3.1.1 POST /api/chat
**Purpose:** Send query to agent and receive response

**Request:**
```typescript
{
  message: string;           // User query
  clientId: string;          // Client ID (e.g., "16325000" or "K16325000")
  kristalId?: string;        // Optional Kristal ID
  sessionId?: string;        // Optional session ID for continuation
}
```

**Response (Streaming):**
```typescript
// SSE (Server-Sent Events) format
data: {"type": "chunk", "content": "partial response text"}
data: {"type": "sources", "sources": [...]}
data: {"type": "validation", "validation": {...}}
data: {"type": "done", "sessionId": "..."}
```

**Response (Non-Streaming):**
```typescript
{
  response: string;          // Full agent response
  sources: Source[];        // Array of source documents/links
  validation?: {
    status: "PASS" | "FAIL";
    summary: string;
    discrepancies: string[];
    agent: string;
  };
  sessionId: string;        // Session ID for continuation
  chart?: {
    url: string;
    title: string;
  };
  metadata?: {
    agentUsed: string;
    responseTime: number;
    timestamp: string;
  };
}
```

**Error Response:**
```typescript
{
  error: {
    code: string;            // Error code (e.g., "AGENT_ERROR", "NETWORK_ERROR")
    message: string;          // User-friendly message
    details?: string;        // Technical details (debug mode only)
  }
}
```

#### 3.1.2 POST /api/session
**Purpose:** Create new session

**Request:**
```typescript
{
  clientId: string;
  kristalId?: string;
}
```

**Response:**
```typescript
{
  sessionId: string;
  clientId: string;
  createdAt: string;        // ISO timestamp
}
```

#### 3.1.3 GET /api/session/:sessionId
**Purpose:** Get session details

**Response:**
```typescript
{
  sessionId: string;
  clientId: string;
  kristalId?: string;
  createdAt: string;
  messageCount: number;
}
```

#### 3.1.4 DELETE /api/session/:sessionId
**Purpose:** Delete session

**Response:**
```typescript
{
  success: boolean;
  message: string;
}
```

#### 3.1.5 GET /api/health
**Purpose:** Health check

**Response:**
```typescript
{
  status: "healthy" | "unhealthy";
  timestamp: string;
  agentApiStatus?: "available" | "unavailable";
}
```

### 3.2 Agent API Integration

**Base URL:** `https://google-portal.kristal.ai`

**Expected Agent API Structure:**
```python
# Based on the agent code, the API likely expects:
POST /query  # or similar endpoint
{
  "message": str,
  "clientId": str,
  "kristalId": str | None,
  "sessionId": str | None
}

# Response format (to be confirmed):
{
  "response": str,
  "sources": List[Dict],
  "validation": Dict | None,
  "sessionId": str
}
```

**Backend Service Implementation:**
```python
# app/services/agent_service.py
import httpx
from app.config import settings

class AgentService:
    def __init__(self):
        self.base_url = settings.AGENT_API_URL
        self.api_key = settings.AGENT_API_KEY
        self.timeout = 300  # 5 minutes for long queries
    
    async def send_query(
        self,
        message: str,
        client_id: str,
        kristal_id: str | None = None,
        session_id: str | None = None
    ) -> dict:
        """Send query to agent API"""
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        payload = {
            "message": message,
            "clientId": client_id,
            "kristalId": kristal_id,
            "sessionId": session_id,
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/query",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise AgentAPIError(f"Agent API error: {e.response.status_code}")
            except httpx.TimeoutException:
                raise AgentAPIError("Agent API timeout")
            except httpx.RequestError as e:
                raise AgentAPIError(f"Network error: {str(e)}")
```

---

## 4. Data Models

### 4.1 Frontend Types

```typescript
// lib/types/agent.ts

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  sources?: Source[];
  validation?: ValidationResult;
  chart?: ChartInfo;
  metadata?: MessageMetadata;
}

export interface Source {
  type: "document" | "table" | "url";
  name: string;
  url?: string;
  query?: string;  // SQL query if type is "table"
}

export interface ValidationResult {
  status: "PASS" | "FAIL";
  summary: string;
  discrepancies: string[];
  agent: string;
}

export interface ChartInfo {
  url: string;
  title: string;
}

export interface MessageMetadata {
  agentUsed: string;
  responseTime: number;
}

export interface Session {
  id: string;
  clientId: string;
  kristalId?: string;
  createdAt: Date;
  messages: ChatMessage[];
}

export interface ChatRequest {
  message: string;
  clientId: string;
  kristalId?: string;
  sessionId?: string;
}

export interface ChatResponse {
  response: string;
  sources: Source[];
  validation?: ValidationResult;
  sessionId: string;
  chart?: ChartInfo;
  metadata?: MessageMetadata;
}
```

### 4.2 Backend Schemas

```python
# app/api/schemas/chat.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SourceSchema(BaseModel):
    type: str  # "document" | "table" | "url"
    name: str
    url: Optional[str] = None
    query: Optional[str] = None

class ValidationSchema(BaseModel):
    status: str  # "PASS" | "FAIL"
    summary: str
    discrepancies: List[str]
    agent: str

class ChartSchema(BaseModel):
    url: str
    title: str

class ChatRequestSchema(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    clientId: str = Field(..., pattern=r'^K?\d+$')
    kristalId: Optional[str] = None
    sessionId: Optional[str] = None

class ChatResponseSchema(BaseModel):
    response: str
    sources: List[SourceSchema]
    validation: Optional[ValidationSchema] = None
    sessionId: str
    chart: Optional[ChartSchema] = None
    metadata: Optional[dict] = None

class ErrorResponseSchema(BaseModel):
    error: dict
```

```python
# app/api/schemas/session.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionCreateSchema(BaseModel):
    clientId: str = Field(..., pattern=r'^K?\d+$')
    kristalId: Optional[str] = None

class SessionResponseSchema(BaseModel):
    sessionId: str
    clientId: str
    kristalId: Optional[str]
    createdAt: datetime
    messageCount: int = 0
```

---

## 5. State Management

### 5.1 Frontend State

**Session State (Zustand or React Context):**
```typescript
// lib/store/chatStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface ChatState {
  sessionId: string | null;
  clientId: string;
  kristalId: string | null;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setClientId: (id: string) => void;
  setKristalId: (id: string | null) => void;
  addMessage: (message: ChatMessage) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearChat: () => void;
  createSession: () => Promise<void>;
}

export const useChatStore = create<ChatState>()(
  persist(
    (set) => ({
      sessionId: null,
      clientId: '',
      kristalId: null,
      messages: [],
      isLoading: false,
      error: null,
      
      setClientId: (id) => set({ clientId: id }),
      setKristalId: (id) => set({ kristalId: id }),
      addMessage: (message) => set((state) => ({
        messages: [...state.messages, message]
      })),
      setLoading: (loading) => set({ isLoading: loading }),
      setError: (error) => set({ error }),
      clearChat: () => set({ messages: [], sessionId: null }),
      createSession: async () => {
        // Implementation
      },
    }),
    {
      name: 'kristal-agent-chat',
      partialize: (state) => ({
        clientId: state.clientId,
        kristalId: state.kristalId,
        sessionId: state.sessionId,
        messages: state.messages,
      }),
    }
  )
);
```

### 5.2 Backend State

**Session Storage:**
- In-memory storage for PoC (Redis for production)
- Session data structure:
```python
{
  "session_id": str,
  "client_id": str,
  "kristal_id": str | None,
  "created_at": datetime,
  "messages": List[dict],
  "last_activity": datetime
}
```

---

## 6. Component Specifications

### 6.1 ChatContainer Component

```typescript
// components/chat/ChatContainer.tsx
'use client';

import { useChatStore } from '@/lib/store/chatStore';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';
import { SessionManager } from '../session/SessionManager';

export function ChatContainer() {
  const { messages, isLoading, error } = useChatStore();
  
  return (
    <div className="flex flex-col h-screen">
      <SessionManager />
      <div className="flex-1 overflow-y-auto">
        <MessageList messages={messages} />
        {isLoading && <LoadingIndicator />}
        {error && <ErrorMessage error={error} />}
      </div>
      <ChatInput />
    </div>
  );
}
```

### 6.2 MessageBubble Component

```typescript
// components/chat/MessageBubble.tsx
import { ChatMessage } from '@/lib/types/agent';
import { SourceList } from '../sources/SourceList';
import { ValidationBadge } from '../validation/ValidationBadge';
import { ReactMarkdown } from 'react-markdown';

interface MessageBubbleProps {
  message: ChatMessage;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-3xl ${isUser ? 'bg-blue-500 text-white' : 'bg-gray-100'}`}>
        <div className="p-4 rounded-lg">
          <ReactMarkdown>{message.content}</ReactMarkdown>
          
          {message.sources && message.sources.length > 0 && (
            <SourceList sources={message.sources} />
          )}
          
          {message.validation && (
            <ValidationBadge validation={message.validation} />
          )}
          
          {message.chart && (
            <img src={message.chart.url} alt={message.chart.title} />
          )}
          
          <span className="text-xs opacity-70">
            {message.timestamp.toLocaleTimeString()}
          </span>
        </div>
      </div>
    </div>
  );
}
```

### 6.3 ChatInput Component

```typescript
// components/chat/ChatInput.tsx
'use client';

import { useState } from 'react';
import { useChatStore } from '@/lib/store/chatStore';
import { sendMessage } from '@/lib/api/agent';

export function ChatInput() {
  const [input, setInput] = useState('');
  const { clientId, sessionId, isLoading, setLoading, addMessage } = useChatStore();
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    const userMessage = {
      id: crypto.randomUUID(),
      role: 'user' as const,
      content: input,
      timestamp: new Date(),
    };
    
    addMessage(userMessage);
    setInput('');
    setLoading(true);
    
    try {
      const response = await sendMessage({
        message: input,
        clientId,
        sessionId: sessionId || undefined,
      });
      
      const assistantMessage = {
        id: crypto.randomUUID(),
        role: 'assistant' as const,
        content: response.response,
        timestamp: new Date(),
        sources: response.sources,
        validation: response.validation,
        chart: response.chart,
      };
      
      addMessage(assistantMessage);
    } catch (error) {
      // Handle error
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="p-4 border-t">
      <div className="flex gap-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
          className="flex-1 p-2 border rounded"
          placeholder="Ask a question..."
          rows={3}
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </form>
  );
}
```

---

## 7. API Client Implementation

### 7.1 Frontend API Client

```typescript
// lib/api/agent.ts
import { ChatRequest, ChatResponse } from '@/lib/types/agent';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error?.message || 'Failed to send message');
  }
  
  return response.json();
}

export async function createSession(clientId: string, kristalId?: string) {
  const response = await fetch(`${API_BASE_URL}/api/session`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ clientId, kristalId }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to create session');
  }
  
  return response.json();
}
```

### 7.2 Streaming Support (Optional)

```typescript
// lib/api/agent.ts (streaming version)
export async function* sendMessageStream(request: ChatRequest) {
  const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });
  
  if (!response.ok) {
    throw new Error('Failed to stream message');
  }
  
  const reader = response.body?.getReader();
  const decoder = new TextDecoder();
  
  if (!reader) {
    throw new Error('No response body');
  }
  
  let buffer = '';
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        yield data;
      }
    }
  }
}
```

---

## 8. Security Considerations

### 8.1 Input Validation

**Frontend:**
- Sanitize user input before sending
- Validate client ID format (numeric or K-prefixed)
- Limit message length (5000 characters)
- Prevent XSS in markdown rendering

**Backend:**
- Pydantic schema validation
- Rate limiting (100 requests/hour per IP)
- Input sanitization
- SQL injection prevention (if applicable)

### 8.2 Authentication & Authorization

**PoC Phase:**
- No authentication required (internal use only)
- IP whitelisting (optional)
- Simple API key for agent API (if required)

**Production Phase:**
- OAuth 2.0 / SSO integration
- JWT tokens
- Role-based access control

### 8.3 Data Protection

- No sensitive data in client-side logs
- HTTPS only
- Secure session storage
- CORS configuration
- Rate limiting

---

## 9. Error Handling

### 9.1 Error Types

```typescript
// lib/utils/errors.ts
export class AgentError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: string
  ) {
    super(message);
    this.name = 'AgentError';
  }
}

export class NetworkError extends AgentError {
  constructor(message: string, details?: string) {
    super(message, 'NETWORK_ERROR', details);
  }
}

export class AgentAPIError extends AgentError {
  constructor(message: string, details?: string) {
    super(message, 'AGENT_API_ERROR', details);
  }
}
```

### 9.2 Error Handling Strategy

**Frontend:**
- Try-catch blocks around API calls
- User-friendly error messages
- Retry logic for network errors
- Error boundary for React errors

**Backend:**
- Global exception handler
- Structured error responses
- Logging for debugging
- Graceful degradation

---

## 10. Performance Optimization

### 10.1 Frontend Optimizations

- Code splitting with Next.js dynamic imports
- Lazy loading for heavy components
- Virtual scrolling for long message lists
- Debouncing for input
- Memoization for expensive computations
- Image optimization for charts

### 10.2 Backend Optimizations

- Connection pooling for HTTP client
- Request timeout configuration
- Response caching (if applicable)
- Async/await for non-blocking operations
- Efficient session storage

### 10.3 Caching Strategy

- Session data: In-memory (PoC), Redis (production)
- Agent responses: No caching (always fresh)
- Static assets: CDN caching via Vercel

---

## 11. Testing Strategy

### 11.1 Frontend Testing

**Unit Tests:**
- Component rendering
- State management
- Utility functions
- API client functions

**Integration Tests:**
- User flows
- API integration
- Error handling

**E2E Tests:**
- Complete chat flow
- Session management
- Error scenarios

**Tools:**
- Jest + React Testing Library
- Playwright for E2E

### 11.2 Backend Testing

**Unit Tests:**
- Service functions
- API endpoints
- Validation logic

**Integration Tests:**
- Agent API integration
- Session management
- Error handling

**Tools:**
- pytest
- httpx for async testing
- pytest-asyncio

---

## 12. Deployment Configuration

### 12.1 Frontend (Vercel)

**vercel.json:**
```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url"
  }
}
```

**Environment Variables:**
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_AGENT_URL`: Agent API URL (if direct calls)

### 12.2 Backend (Railways)

**railways.json:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT"
  }
}
```

**Environment Variables:**
- `AGENT_API_URL`: https://google-portal.kristal.ai
- `AGENT_API_KEY`: API key (if required)
- `CORS_ORIGINS`: Comma-separated allowed origins
- `ENVIRONMENT`: production/development
- `LOG_LEVEL`: info/debug/error

**requirements.txt:**
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
httpx==0.26.0
python-dotenv==1.0.0
```

### 12.3 Docker Configuration (Optional)

**Dockerfile (Backend):**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 13. Monitoring & Logging

### 13.1 Frontend Logging

- Console logging (development only)
- Error tracking (Sentry or similar)
- Analytics (optional)

### 13.2 Backend Logging

```python
# app/utils/logger.py
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
```

**Log Levels:**
- INFO: Normal operations
- WARNING: Recoverable errors
- ERROR: Unrecoverable errors
- DEBUG: Detailed debugging (development only)

### 13.3 Monitoring Metrics

- Request count
- Response times
- Error rates
- Agent API availability
- Session count

---

## 14. Development Workflow

### 14.1 Local Development Setup

**Frontend:**
```bash
cd frontend
npm install
npm run dev  # Runs on http://localhost:3000
```

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload  # Runs on http://localhost:8000
```

### 14.2 Git Workflow

- Main branch: Production-ready code
- Develop branch: Integration branch
- Feature branches: Feature development
- PR reviews required before merge

### 14.3 CI/CD Pipeline

**Frontend (Vercel):**
- Automatic deployment on push to main
- Preview deployments for PRs
- Build checks

**Backend (Railways):**
- Automatic deployment on push to main
- Health checks
- Rollback capability

---

## 15. Open Technical Questions

1. **Agent API Specification:**
   - Exact endpoint path and method?
   - Request/response format?
   - Authentication mechanism?
   - Streaming support?

2. **Session Management:**
   - Server-side or client-side only?
   - Session expiration time?
   - Maximum session size?

3. **Streaming:**
   - Does agent API support streaming?
   - SSE or WebSocket?
   - Chunk format?

4. **Charts:**
   - Chart URL format?
   - CORS configuration?
   - Image format (PNG/SVG)?

5. **Rate Limiting:**
   - Per-user or per-IP?
   - Rate limit values?
   - Rate limit headers?

---

## 16. Implementation Checklist

### Phase 1: MVP
- [ ] Set up Next.js project
- [ ] Set up FastAPI backend
- [ ] Implement basic chat UI
- [ ] Implement API client
- [ ] Integrate with agent API
- [ ] Basic error handling
- [ ] Deploy to Vercel and Railways

### Phase 2: Enhanced Features
- [ ] Session management
- [ ] Source attribution display
- [ ] Validation results display
- [ ] Loading states
- [ ] Improved error handling
- [ ] Markdown rendering

### Phase 3: Polish
- [ ] Query examples
- [ ] UI/UX improvements
- [ ] Performance optimization
- [ ] Testing
- [ ] Documentation

---

## 17. Appendix

### 17.1 Technology Versions

**Frontend:**
- Next.js: 15.0.0
- React: 19.0.0
- TypeScript: 5.3.0
- Tailwind CSS: 3.4.0

**Backend:**
- Python: 3.11+
- FastAPI: 0.109.0
- Pydantic: 2.5.3
- httpx: 0.26.0

### 17.2 Useful Commands

**Frontend:**
```bash
npm run dev          # Development server
npm run build        # Production build
npm run start        # Production server
npm run lint         # Linting
npm run test         # Tests
```

**Backend:**
```bash
uvicorn main:app --reload           # Development server
pytest                               # Run tests
black .                              # Code formatting
mypy .                               # Type checking
```

---

## Document Approval

**Prepared by:** [Engineering Team]  
**Reviewed by:** [Technical Lead]  
**Approved by:** [Engineering Manager]  
**Date:** [Date]

---

**Next Steps:**
1. Resolve open technical questions
2. Set up development environments
3. Begin Phase 1 implementation
4. Schedule technical review meetings

