# Quick Start Guide

## Prerequisites

### Frontend
- **Node.js** 18+ ([Download](https://nodejs.org/))
- **npm** (comes with Node.js) or **yarn**

### Backend
- **Python** 3.11+ ([Download](https://www.python.org/downloads/))
- **pip** (comes with Python)

## Step-by-Step Setup

### 1. Backend Setup (Terminal 1)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env file (optional - defaults are already set)
# The file should contain:
# AGENT_API_URL=https://kristal-agent-953081186136.asia-southeast1.run.app
# AGENT_API_KEY=AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4
# RELATIONSHIP_MANAGER_ID=001
# CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Run the backend server
uvicorn main:app --reload
```

The backend will start on **http://localhost:8000**

You can verify it's working by visiting:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

### 2. Frontend Setup (Terminal 2)

Open a **new terminal window**:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file from example
cp .env.example .env

# Edit .env file (if backend is not on default port)
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Run the development server
npm run dev
```

The frontend will start on **http://localhost:3000**

Open your browser and navigate to: **http://localhost:3000**

## Usage

1. **Set Client ID**: Enter a client ID in the header (e.g., `19754000` or `K19754000`)

2. **Create Session** (optional): Click "New Session" button to create a session via the agent API

3. **Ask Questions**: Type your question in the input field and press Enter or click Send

4. **View Results**: 
   - Agent response will appear in the chat
   - Sources will be displayed below the response
   - Validation results will show if available
   - Charts will display if generated

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

**Module not found errors:**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Agent API connection errors:**
- Check your internet connection
- Verify the API URL in `.env` file
- Check if the API key is correct

### Frontend Issues

**Port 3000 already in use:**
```bash
# Use a different port
PORT=3001 npm run dev
```

**Cannot connect to backend:**
- Make sure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env` file
- Verify CORS settings in backend

**Module not found errors:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Development Commands

### Backend

```bash
# Run with auto-reload (development)
uvicorn main:app --reload

# Run without reload (production-like)
uvicorn main:app --host 0.0.0.0 --port 8000

# Check code formatting (if using black)
black .

# Type checking (if using mypy)
mypy .
```

### Frontend

```bash
# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start

# Linting
npm run lint

# Type checking
npm run type-check
```

## Testing the API Directly

### Test Session Creation

```bash
curl -X POST "http://localhost:8000/api/session" \
  -H "Content-Type: application/json" \
  -d '{"clientId": "19754000"}'
```

### Test Chat Query

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is my portfolio value?",
    "clientId": "19754000",
    "sessionId": "your-session-id"
  }'
```

## Project Structure

```
gcp_jarvis_ui/
├── backend/           # FastAPI backend
│   ├── app/
│   ├── main.py
│   └── requirements.txt
├── frontend/          # Next.js frontend
│   ├── app/
│   ├── components/
│   └── package.json
└── README.md
```

## Next Steps

1. ✅ Backend and frontend are running
2. ✅ Test with a real client ID
3. ✅ Try different types of queries
4. ✅ Check source links and validation results
5. 🔄 Deploy to production (Vercel + Railways)

## Production Deployment

### Backend (Railways)

1. Push code to GitHub
2. Connect repository to Railways
3. Set environment variables in Railways dashboard
4. Deploy

### Frontend (Vercel)

1. Push code to GitHub
2. Import project in Vercel
3. Set `NEXT_PUBLIC_API_URL` to your backend URL
4. Deploy

## Support

If you encounter issues:
1. Check the console/terminal for error messages
2. Verify all environment variables are set correctly
3. Ensure both frontend and backend are running
4. Check network connectivity to the agent API

