# Authentication Setup Guide

## Issue
The agent API returns 401 Unauthorized because it requires Google Cloud Identity Tokens, not API keys.

## Solution
The backend has been updated to automatically try using `gcloud auth print-identity-token` first, then fall back to the API key.

## Setup Instructions

### Option 1: Use gcloud CLI (Recommended for Local Development)

1. **Install Google Cloud SDK** (if not already installed):
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   ```

3. **Set your project** (optional):
   ```bash
   gcloud config set project kristal-prod-service-project
   ```

4. **Test authentication**:
   ```bash
   gcloud auth print-identity-token
   ```
   This should output a token string.

5. **Restart your backend server**:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload
   ```

The backend will now automatically use the gcloud identity token for authentication.

### Option 2: Use API Key (If gcloud is not available)

If you can't use gcloud CLI, the backend will fall back to the API key. However, this might still result in 401 errors if the API requires identity tokens.

**Note:** The API key method may not work if the agent API strictly requires Google Cloud identity tokens.

## Testing

### Test Authentication

1. **Check if gcloud is available**:
   ```bash
   which gcloud
   gcloud auth print-identity-token
   ```

2. **Test the backend**:
   ```bash
   curl -X POST "http://localhost:8000/api/session" \
     -H "Content-Type: application/json" \
     -d '{"clientId": "19754000"}'
   ```

3. **Check backend logs**:
   Look for one of these messages:
   - `"Using gcloud identity token for authentication"` ✅
   - `"gcloud not available, using API key"` ⚠️

## For Production Deployment (Railways)

For production, you'll need to use service account authentication:

1. **Create a service account** in GCP Console
2. **Download the service account key** (JSON file)
3. **Set environment variable** in Railways:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
   ```
4. **Update the code** to use Google Auth Library instead of gcloud CLI

## Current Implementation

The backend now:
1. ✅ Tries to get gcloud identity token first
2. ✅ Falls back to API key if gcloud is not available
3. ✅ Logs which authentication method is being used

## Troubleshooting

### "gcloud: command not found"
- Install Google Cloud SDK
- Or ensure gcloud is in your PATH

### "gcloud auth print-identity-token" fails
- Run `gcloud auth login` first
- Check if you have the correct permissions

### Still getting 401 errors
- Verify you're authenticated: `gcloud auth list`
- Check if the token is valid: `gcloud auth print-identity-token`
- Verify the agent API endpoint is correct
- Contact the API team to confirm authentication requirements

