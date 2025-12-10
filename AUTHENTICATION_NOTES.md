# Authentication Notes

## Issue
The agent API is returning 401 Unauthorized when trying to create a session.

## Current Implementation
The backend is using the GEMINI API key as a Bearer token:
```python
headers = {
    "Authorization": f"Bearer {self.api_key}"
}
```

## API Documentation Reference
According to the API docs, authentication should use:
```bash
gcloud auth print-identity-token
```

This suggests the API might require Google Cloud Identity Token instead of an API key.

## Possible Solutions

### Option 1: Use Google Cloud Identity Token (Recommended for GCP)
If running from a GCP environment or with gcloud CLI:

```python
import subprocess

def get_gcloud_token():
    """Get Google Cloud identity token"""
    try:
        result = subprocess.run(
            ['gcloud', 'auth', 'print-identity-token'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        raise Exception("Failed to get gcloud identity token")
```

**Note:** This requires:
- gcloud CLI installed
- User authenticated: `gcloud auth login`
- Or service account configured

### Option 2: Use Service Account (For Production)
For production deployment on Railways or other platforms:

1. Create a service account in GCP
2. Download the service account key JSON
3. Set environment variable: `GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`
4. Use Google Auth Library:

```python
from google.auth import default
from google.auth.transport.requests import Request

def get_service_account_token():
    """Get service account token"""
    credentials, project = default()
    credentials.refresh(Request())
    return credentials.token
```

### Option 3: Verify API Key Format
The API key might need to be used differently. Check if:
- It should be in a different header (e.g., `X-API-Key`)
- It should be used without "Bearer" prefix
- It needs to be combined with other authentication

## Testing Authentication

### Test with gcloud token:
```bash
TOKEN=$(gcloud auth print-identity-token)
curl -X POST "https://kristal-agent-953081186136.asia-southeast1.run.app/get_session" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"relationship_manager_id": "001", "client_id": "19754000"}'
```

### Test with API key (current):
```bash
curl -X POST "https://kristal-agent-953081186136.asia-southeast1.run.app/get_session" \
  -H "Authorization: Bearer AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4" \
  -H "Content-Type: application/json" \
  -d '{"relationship_manager_id": "001", "client_id": "19754000"}'
```

## Recommended Next Steps

1. **Test locally with gcloud:**
   - Install gcloud CLI if not installed
   - Run `gcloud auth login`
   - Test the curl command above
   - If it works, update the backend to use gcloud token

2. **For Production (Railways):**
   - Set up service account authentication
   - Use Google Auth Library to get tokens
   - Update `agent_service.py` and `session_service.py`

3. **Alternative:**
   - Contact the agent API team to confirm:
     - Correct authentication method
     - If API key is valid for this endpoint
     - Required permissions/scopes

## Current Status
- ✅ Backend code is correct
- ✅ Network connectivity works
- ⚠️ Authentication method needs verification
- ⚠️ 401 error suggests auth format might be wrong

