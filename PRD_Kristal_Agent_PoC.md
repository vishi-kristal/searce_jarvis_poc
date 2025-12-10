# Product Requirements Document (PRD)
## Kristal Agent PoC UI

**Version:** 1.0  
**Date:** January 2025  
**Status:** Draft  
**Owner:** Product Team

---

## 1. Executive Summary

### 1.1 Overview
This PRD outlines the requirements for a Proof of Concept (PoC) web interface for the Kristal Agent system. The agent is currently deployed and accessible at `https://google-portal.kristal.ai`. This PoC will enable internal power users to interact with the multi-agent financial advisory system through a simple, intuitive chat interface.

### 1.2 Objectives
- **Primary:** Enable internal power users to test and validate the Kristal Agent capabilities
- **Secondary:** Gather user feedback for future product iterations
- **Tertiary:** Demonstrate agent functionality to stakeholders

### 1.3 Success Criteria
- At least 10 internal power users successfully test the system
- 80% of test queries return accurate, validated responses
- Average response time < 30 seconds for complex queries
- Positive user feedback on UI/UX (≥4/5 rating)

---

## 2. User Personas

### 2.1 Primary Persona: Internal Power User
**Profile:**
- Role: Relationship Manager, Financial Advisor, or Product Manager
- Technical Level: Moderate to High
- Use Case: Testing agent capabilities, validating responses, exploring features
- Context: Internal testing environment, familiar with financial terminology

**Goals:**
- Quickly test agent responses for various query types
- Validate accuracy of financial data retrieval
- Understand agent capabilities and limitations
- Provide feedback for improvements

**Pain Points:**
- Need to test multiple query types efficiently
- Want to see source documents and validation results
- Require clear error messages when queries fail

---

## 3. Functional Requirements

### 3.1 Core Features

#### FR-1: Chat Interface
**Priority:** P0 (Must Have)

**Description:**
- Simple, clean chat interface similar to ChatGPT/Claude
- Message history visible in conversation thread
- Real-time streaming responses (if supported by backend)
- Clear distinction between user messages and agent responses

**Acceptance Criteria:**
- Users can type and send messages
- Messages appear immediately after sending
- Agent responses stream in real-time (if available) or appear when complete
- Conversation history persists during session
- Mobile-responsive design

#### FR-2: Session Management
**Priority:** P0 (Must Have)

**Description:**
- Each user session maintains client context (clientId, kristalId)
- Session state persists across page refreshes
- Ability to start new conversation/clear history
- Session ID visible for debugging

**Acceptance Criteria:**
- Client ID can be set/updated in UI
- Session persists in browser storage
- "New Chat" button clears conversation history
- Session ID displayed in UI (collapsible debug panel)

#### FR-3: Query Input
**Priority:** P0 (Must Have)

**Description:**
- Text input field for user queries
- Support for multi-line queries
- Character limit indicator (optional)
- Submit button or Enter key to send

**Acceptance Criteria:**
- Text area accepts multi-line input
- Enter key sends message (Shift+Enter for new line)
- Input clears after successful submission
- Loading state prevents duplicate submissions

#### FR-4: Response Display
**Priority:** P0 (Must Have)

**Description:**
- Display agent responses in readable format
- Support markdown rendering (tables, lists, formatting)
- Show source documents with clickable links
- Display validation results when available
- Show charts/images when generated

**Acceptance Criteria:**
- Markdown renders correctly (tables, lists, bold, italic)
- Source links are clickable and open in new tab
- Validation results displayed in collapsible section
- Charts/images display inline or as thumbnails
- Long responses are scrollable

#### FR-5: Source Attribution
**Priority:** P1 (Should Have)

**Description:**
- Display source documents/links for each response
- Show BigQuery table names when SQL queries are used
- Format: `[Document Name](URL)` for PDFs
- Show SQL queries used (in collapsible section)

**Acceptance Criteria:**
- All sources listed at end of response
- Links are properly formatted and clickable
- SQL queries shown in code block format
- Sources section is collapsible/expandable

#### FR-6: Validation Results
**Priority:** P1 (Should Have)

**Description:**
- Display validation status (PASS/FAIL)
- Show validation summary and discrepancies
- Indicate which agent was validated
- Separate validation section from main response

**Acceptance Criteria:**
- Validation status clearly visible (green for PASS, red for FAIL)
- Discrepancies listed when validation fails
- Validation section collapsible
- Agent name displayed in validation results

#### FR-7: Error Handling
**Priority:** P0 (Must Have)

**Description:**
- Display user-friendly error messages
- Show technical error details in debug mode
- Handle network errors gracefully
- Indicate when agent is unavailable

**Acceptance Criteria:**
- Error messages are clear and actionable
- Network errors show retry option
- 500 errors show generic message with support contact
- Debug mode shows full error stack (toggle)

#### FR-8: Loading States
**Priority:** P0 (Must Have)

**Description:**
- Show loading indicator when query is processing
- Display "Agent is thinking..." message
- Indicate when multiple agents are being called
- Show progress for long-running queries

**Acceptance Criteria:**
- Spinner/loading animation during query processing
- Loading state prevents new queries
- Estimated time shown (if available)
- Can cancel long-running queries (optional)

### 3.2 Enhanced Features

#### FR-9: Query Examples
**Priority:** P2 (Nice to Have)

**Description:**
- Pre-populated example queries users can click
- Categorized by agent type (Portfolio, Product, Fees, etc.)
- Quick access to common query patterns

**Acceptance Criteria:**
- Example queries displayed as clickable chips/buttons
- Examples categorized by use case
- Clicking example populates input field
- Examples can be dismissed/hidden

#### FR-10: Query History
**Priority:** P2 (Nice to Have)

**Description:**
- Save query history locally
- Search/filter past queries
- Re-run previous queries
- Export conversation history

**Acceptance Criteria:**
- Past queries saved in browser storage
- Search bar to filter history
- Click to re-run query
- Export as JSON/text file

#### FR-11: Agent Selection (Advanced)
**Priority:** P3 (Future)

**Description:**
- Allow users to specify which agent to use
- Override automatic routing
- Show which agent was used for each response

**Acceptance Criteria:**
- Dropdown/selector for agent choice
- "Auto" option for automatic routing
- Agent name shown in response metadata
- Warning when overriding routing

---

## 4. Technical Requirements

### 4.1 Frontend Stack

**Framework:** Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS for styling
- Shadcn UI components (optional, for consistent design)

**Key Libraries:**
- `ai` SDK (Vercel AI SDK) for streaming responses
- `react-markdown` for markdown rendering
- `zustand` or React Context for state management
- `axios` or `fetch` for API calls

### 4.2 Backend Stack

**Framework:** Python FastAPI
- Python 3.11+
- FastAPI for REST API
- Pydantic for request/response validation
- `httpx` or `requests` for calling agent endpoint

**API Endpoints:**
```
POST /api/chat
  - Request: { message: string, clientId: string, kristalId?: string, sessionId?: string }
  - Response: Streaming response or { response: string, sources: [], validation: {}, sessionId: string }

GET /api/health
  - Health check endpoint

POST /api/session
  - Create new session: { clientId: string, kristalId?: string }
  - Response: { sessionId: string }
```

### 4.3 Integration

**Agent Endpoint:**
- Base URL: `https://google-portal.kristal.ai`
- Authentication: TBD (API key, OAuth, or service account)
- Request format: Match existing agent API structure
- Response format: Handle streaming or JSON responses

### 4.4 Deployment

**Frontend:**
- Platform: Vercel
- Environment: Production + Preview deployments
- Environment Variables:
  - `NEXT_PUBLIC_API_URL` - Backend API URL
  - `NEXT_PUBLIC_AGENT_URL` - Agent endpoint URL (if direct calls)

**Backend:**
- Platform: Railways
- Environment: Production
- Environment Variables:
  - `AGENT_API_URL` - Agent endpoint URL
  - `AGENT_API_KEY` - Authentication key (if required)
  - `CORS_ORIGINS` - Allowed frontend origins

---

## 5. UI/UX Requirements

### 5.1 Design Principles
- **Simplicity:** Clean, uncluttered interface
- **Clarity:** Clear visual hierarchy
- **Feedback:** Immediate visual feedback for all actions
- **Accessibility:** WCAG 2.1 AA compliance

### 5.2 Layout

**Desktop:**
```
┌─────────────────────────────────────────┐
│ Header: Kristal Agent PoC              │
│ [Client ID: K16325000] [New Chat]      │
├─────────────────────────────────────────┤
│                                         │
│  Chat Messages Area (scrollable)        │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ User: What is my portfolio...   │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Agent: Your portfolio value...  │   │
│  │ Sources: [link] [link]          │   │
│  │ Validation: ✓ PASS              │   │
│  └─────────────────────────────────┘   │
│                                         │
├─────────────────────────────────────────┤
│ [Query input field...] [Send]          │
│ Example queries: [Chip] [Chip] [Chip]  │
└─────────────────────────────────────────┘
```

**Mobile:**
- Full-width layout
- Bottom-fixed input area
- Collapsible header
- Swipe gestures for navigation (optional)

### 5.3 Components

**Message Bubbles:**
- User messages: Right-aligned, blue background
- Agent messages: Left-aligned, gray/white background
- Timestamp: Small, muted text
- Avatar: User icon for user, bot icon for agent

**Source Links:**
- Displayed as list below response
- Format: `📄 Document Name` (clickable)
- External links open in new tab
- PDF links show preview option (if available)

**Validation Badge:**
- Green checkmark + "PASS" for successful validation
- Red X + "FAIL" for failed validation
- Collapsible details section
- Discrepancies listed in expandable section

**Loading Indicator:**
- Typing indicator animation
- "Agent is thinking..." message
- Progress dots or spinner

### 5.4 Color Scheme

**Primary Colors:**
- Primary: Kristal brand color (to be confirmed)
- Success: Green (#10B981)
- Error: Red (#EF4444)
- Warning: Amber (#F59E0B)
- Info: Blue (#3B82F6)

**Neutral Colors:**
- Background: White/Light Gray
- Text: Dark Gray (#1F2937)
- Borders: Light Gray (#E5E7EB)

---

## 6. Non-Functional Requirements

### 6.1 Performance
- Initial page load: < 2 seconds
- Query response time: < 30 seconds (95th percentile)
- Streaming response: Start within 2 seconds
- Support concurrent users: 50+ simultaneous users

### 6.2 Security
- Input sanitization for XSS prevention
- CORS configuration for API access
- Rate limiting on backend (100 requests/hour per user)
- Secure storage of session data
- No sensitive data in client-side logs

### 6.3 Reliability
- Backend uptime: 99% availability
- Graceful degradation when agent is unavailable
- Retry logic for failed API calls
- Error recovery mechanisms

### 6.4 Browser Support
- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: iOS Safari, Chrome Mobile

---

## 7. User Flows

### 7.1 First-Time User Flow
1. User opens application
2. Sees welcome message with instructions
3. Enters Client ID (or uses default)
4. Views example queries
5. Clicks example query or types own query
6. Sees loading indicator
7. Receives response with sources and validation
8. Can continue conversation or start new chat

### 7.2 Query Flow
1. User types query in input field
2. Clicks Send or presses Enter
3. Input field shows loading state
4. Query appears in chat as user message
5. Loading indicator shows "Agent is thinking..."
6. Response streams in (or appears when complete)
7. Sources and validation results appear
8. User can click sources or ask follow-up question

### 7.3 Error Flow
1. User submits query
2. Network error occurs
3. Error message displayed: "Unable to connect. Please try again."
4. Retry button appears
5. User clicks retry
6. Query resubmitted

---

## 8. Success Metrics

### 8.1 Usage Metrics
- Number of unique users
- Number of queries per user
- Average queries per session
- Session duration
- Most used agent types

### 8.2 Performance Metrics
- Average response time
- P95/P99 response times
- Error rate
- Success rate (validated responses)

### 8.3 User Satisfaction
- User feedback rating (1-5 scale)
- Qualitative feedback comments
- Feature requests
- Bug reports

---

## 9. Risks & Mitigations

### 9.1 Technical Risks

**Risk:** Agent API rate limits or downtime  
**Mitigation:** Implement retry logic, show clear error messages, cache responses when possible

**Risk:** Large response payloads causing performance issues  
**Mitigation:** Implement pagination, lazy loading, optimize rendering

**Risk:** Streaming responses not working correctly  
**Mitigation:** Fallback to non-streaming mode, test thoroughly

### 9.2 User Experience Risks

**Risk:** Users don't understand how to use the system  
**Mitigation:** Clear onboarding, example queries, help documentation

**Risk:** Validation failures confuse users  
**Mitigation:** Clear explanation of validation, educational tooltips

---

## 10. Timeline & Phases

### Phase 1: MVP (Week 1-2)
**Deliverables:**
- Basic chat interface
- Query input and response display
- Integration with agent API
- Source attribution
- Basic error handling

**Success Criteria:**
- Users can send queries and receive responses
- Sources are displayed
- Basic errors are handled

### Phase 2: Enhanced Features (Week 3)
**Deliverables:**
- Validation results display
- Session management
- Query examples
- Improved UI/UX
- Loading states

**Success Criteria:**
- Validation results visible
- Sessions persist correctly
- UI is polished and responsive

### Phase 3: Testing & Refinement (Week 4)
**Deliverables:**
- User testing with 5-10 power users
- Bug fixes
- Performance optimization
- Documentation

**Success Criteria:**
- All critical bugs fixed
- Performance meets requirements
- User feedback incorporated

### Phase 4: Launch (Week 5)
**Deliverables:**
- Production deployment
- User onboarding materials
- Monitoring and analytics
- Support documentation

**Success Criteria:**
- System deployed and accessible
- Users can successfully use the system
- Monitoring is active

---

## 11. Future Enhancements (Post-PoC)

- Multi-agent conversation visualization
- Query templates and saved queries
- Export conversation history
- Advanced filtering and search
- User authentication and authorization
- Analytics dashboard
- Custom agent routing preferences
- Voice input/output
- Mobile app

---

## 12. Dependencies

### 12.1 External Dependencies
- Agent API availability (`https://google-portal.kristal.ai`)
- Agent API documentation
- Authentication mechanism for agent API
- Client ID and Kristal ID data sources

### 12.2 Internal Dependencies
- Design system/brand guidelines
- DevOps support for deployment
- User access management
- Monitoring and logging infrastructure

---

## 13. Open Questions

1. **Authentication:** How do we authenticate users? Internal SSO? API keys?
2. **Client ID:** How do users get their Client IDs? Pre-populated list? Manual entry?
3. **Rate Limiting:** What are the rate limits for the agent API?
4. **Streaming:** Does the agent API support streaming responses?
5. **Charts:** How are charts/images returned? URLs? Base64? Need to handle display.
6. **Session Management:** Should sessions be server-side or client-side only?
7. **Error Messages:** What level of detail should error messages show to users?
8. **Analytics:** What analytics tools should we integrate? Google Analytics? Custom?

---

## 14. Appendix

### 14.1 Example Queries by Agent Type

**User Agent:**
- "What is my portfolio value as of October 31, 2025?"
- "Show me my current holdings and their unrealized returns"
- "What was my portfolio return last month?"

**Portfolio Analysis Agent:**
- "What are the investment recommendations for my portfolio?"
- "How does my portfolio compare to the recommended allocation?"
- "What is the correlation of my recommended portfolio with SPY?"

**Product Agent:**
- "Tell me about the ARGA Global Equity Fund"
- "What are the fees for QIO Class C USD shares?"
- "Plot the monthly returns of Peregrine"

**Fees Agent:**
- "What are my transaction fees?"
- "How much did I pay in fees for January 2025?"
- "What is the fee for withdrawing USD?"

**Customer Cash Agent:**
- "What is the status of my recent deposit?"
- "Have you received my withdrawal request?"

**Recent Orders Agent:**
- "What is the status of my most recent order?"
- "Did my order for Ginko fund go through?"

### 14.2 API Response Structure (Expected)

```json
{
  "response": "Agent response text with markdown",
  "sources": [
    {
      "type": "document",
      "name": "Consolidated Monthly Report",
      "url": "https://signed-url-to-pdf"
    },
    {
      "type": "table",
      "name": "kristal_prod_jarvis.IO_DB",
      "query": "SELECT ..."
    }
  ],
  "validation": {
    "status": "PASS",
    "summary": "All facts verified",
    "discrepancies": [],
    "agent": "user_agent"
  },
  "sessionId": "session-123",
  "chart": {
    "url": "https://storage-url/chart.png",
    "title": "Monthly Returns"
  }
}
```

---

## Document Approval

**Prepared by:** [Name]  
**Reviewed by:** [Name]  
**Approved by:** [Name]  
**Date:** [Date]

---

**Next Steps:**
1. Review and approve PRD
2. Resolve open questions
3. Create technical design document
4. Begin development (Phase 1: MVP)

