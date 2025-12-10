# Kristal Agent PoC

Proof of Concept UI for the Kristal Agent multi-agent financial advisory system.

## Overview

This project provides a web interface for interacting with the Kristal Agent system, which is deployed at `https://google-portal.kristal.ai`. The PoC consists of a Next.js frontend and a FastAPI backend.

## Architecture

```
┌─────────────────┐
│  Next.js Frontend│  (Vercel)
│   (Port 3000)   │
└────────┬────────┘
         │
         │ REST API
         │
┌────────▼────────┐
│ FastAPI Backend │  (Railways)
│   (Port 8000)   │
└────────┬────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│ Kristal Agent   │
│  (Cloud Run)    │
└─────────────────┘
```

## Project Structure

```
gcp_jarvis_ui/
├── frontend/          # Next.js frontend application
├── backend/           # FastAPI backend application
├── colab_code/        # Original Colab notebook code
├── PRD_Kristal_Agent_PoC.md  # Product Requirements Document
└── TDD_Kristal_Agent_PoC.md  # Technical Design Document
```

## Quick Start

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
# Update .env with your backend URL
npm run dev
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Update .env with agent API URL
uvicorn main:app --reload
```

## Documentation

- [PRD](./PRD_Kristal_Agent_PoC.md) - Product Requirements Document
- [TDD](./TDD_Kristal_Agent_PoC.md) - Technical Design Document
- [Frontend README](./frontend/README.md) - Frontend setup and documentation
- [Backend README](./backend/README.md) - Backend setup and documentation

## Features

- ✅ Chat interface for querying the agent
- ✅ Session management
- ✅ Source attribution display
- ✅ Validation results
- ✅ Error handling
- ✅ Responsive design

## Development Status

**Current Phase:** MVP Development

- [x] Project scaffolding
- [x] Basic chat UI
- [x] Backend API structure
- [ ] Agent API integration (needs configuration)
- [ ] Testing
- [ ] Deployment

## Configuration Required

Before running, you need to:

1. **Configure Agent API endpoint** in `backend/app/services/agent_service.py`
   - Update endpoint path
   - Adjust request/response format mapping

2. **Set environment variables**:
   - Frontend: `NEXT_PUBLIC_API_URL`
   - Backend: `AGENT_API_URL`, `CORS_ORIGINS`

## Deployment

### Frontend (Vercel)
1. Connect GitHub repository
2. Set environment variables
3. Deploy

### Backend (Railways)
1. Connect GitHub repository
2. Set environment variables
3. Deploy

## Contributing

1. Create a feature branch
2. Make your changes
3. Test locally
4. Submit a pull request

## License

Internal use only - Kristal AI

