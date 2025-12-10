# CORS Troubleshooting Guide

## Issue: Still Getting CORS Errors After Setting CORS_ORIGINS

### Step 1: Verify CORS_ORIGINS in Railways

1. Go to **Railways** → Your Backend Service → **Variables**
2. Check `CORS_ORIGINS` value. It should be exactly:
   ```
   https://searce-jarvis-poc.vercel.app,http://localhost:3000
   ```
3. **Common mistakes:**
   - ❌ Extra spaces: `https://searce-jarvis-poc.vercel.app , http://localhost:3000`
   - ❌ Trailing slash: `https://searce-jarvis-poc.vercel.app/`
   - ❌ Missing https: `searce-jarvis-poc.vercel.app`
   - ❌ Wrong domain: `https://searce-jarvis-poc.vercel.com` (wrong TLD)

### Step 2: Check Backend Logs

After redeploying, check Railways logs for:
```
CORS Origins: ['https://searce-jarvis-poc.vercel.app', 'http://localhost:3000']
CORS Origins count: 2
```

If you see empty list or wrong origins, the environment variable isn't being read correctly.

### Step 3: Test Health Endpoint

```bash
curl https://kristal-backend.up.railway.app/api/health
```

Should return:
```json
{
  "status": "healthy",
  "cors_origins": ["https://searce-jarvis-poc.vercel.app", "http://localhost:3000"],
  "cors_origins_count": 2
}
```

This confirms:
- Backend is running
- CORS_ORIGINS is being read correctly
- The origins are parsed properly

### Step 4: Test CORS from Browser

On your Vercel site (`https://searce-jarvis-poc.vercel.app`), open browser console and run:

```javascript
fetch('https://kristal-backend.up.railway.app/api/health', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(r => r.json())
.then(console.log)
.catch(console.error)
```

**If this works:** CORS is fixed! The chat endpoint should work too.

**If this fails:** Check the error message:
- "No 'Access-Control-Allow-Origin' header" → CORS_ORIGINS not set correctly
- "CORS policy" → Origin not in allowed list
- Network error → Backend might be down

### Step 5: Force Redeploy Backend

Sometimes environment variables don't take effect until redeploy:

1. Go to **Railways** → Your Service → **Deployments**
2. Click **"Redeploy"**
3. Wait for deployment to complete
4. Check logs for CORS origins

### Step 6: Verify Exact Origin Match

The browser sends the exact origin. Check what origin is being sent:

```javascript
console.log('Origin:', window.location.origin);
```

This should match exactly what's in `CORS_ORIGINS`:
- ✅ `https://searce-jarvis-poc.vercel.app`
- ❌ `https://searce-jarvis-poc.vercel.app/` (trailing slash)
- ❌ `http://searce-jarvis-poc.vercel.app` (wrong protocol)

---

## Common Fixes

### Fix 1: Remove Spaces
If your CORS_ORIGINS has spaces:
```
https://searce-jarvis-poc.vercel.app , http://localhost:3000
```

Change to (no spaces):
```
https://searce-jarvis-poc.vercel.app,http://localhost:3000
```

### Fix 2: Use Wildcard (Temporary)
For testing, you can temporarily allow all origins:
```
*
```

**⚠️ Warning:** Only use this for testing! Change back to specific origins for production.

### Fix 3: Check Backend is Running
If backend returns 404 or connection errors:
1. Check Railways service status (should be green)
2. Check backend logs for errors
3. Test health endpoint: `curl https://kristal-backend.up.railway.app/api/health`

---

## Updated Code

The backend code has been updated to:
1. Strip whitespace from CORS origins
2. Log CORS origins on startup
3. Show CORS origins in health endpoint

After redeploying with the updated code, check the logs to verify CORS_ORIGINS is being read correctly.

