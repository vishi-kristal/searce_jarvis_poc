# Railways Deployment Fix

## Issue
Railways was analyzing the root directory instead of the `backend` directory, causing build failures.

## Solution

### Option 1: Set Root Directory in Railways UI (Recommended)

1. Go to your Railways project
2. Click on **Settings** → **Service**
3. Set **Root Directory** to: `backend`
4. Set **Start Command** to: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Redeploy

### Option 2: Use railway.json (Already Created)

A `railway.json` file has been created at the root that tells Railways to:
- Use Dockerfile from `backend/Dockerfile`
- Use the correct start command

If Option 1 doesn't work, Railways should automatically detect `railway.json`.

## Updated Dockerfile

The Dockerfile has been updated to:
- Use `$PORT` environment variable (Railways provides this)
- Default to port 8000 if PORT is not set

## Verification

After deployment:
1. Check that the service is running
2. Copy the public domain URL
3. Test the health endpoint: `https://your-service.up.railway.app/api/health`

## Environment Variables

Make sure these are set in Railways:

```bash
AGENT_API_URL=https://kristal-agent-953081186136.asia-southeast1.run.app
RELATIONSHIP_MANAGER_ID=001
CORS_ORIGINS=http://localhost:3000
```

After Vercel deployment, update CORS_ORIGINS with your Vercel URL.

