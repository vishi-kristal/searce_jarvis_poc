# CORS and 404 Error Fix

## Issues Found
1. **CORS Error**: Backend not allowing requests from `https://searce-jarvis-poc.vercel.app`
2. **404 Error**: Backend route might not be accessible

## Solution

### Step 1: Update CORS Environment Variable in Railways

1. Go to **Railways Dashboard** → Your Backend Service → **Variables**
2. Find or add `CORS_ORIGINS`
3. Update it to include your Vercel URL:

```bash
CORS_ORIGINS=https://searce-jarvis-poc.vercel.app,http://localhost:3000
```

**Important**: 
- No spaces after commas
- Include `https://` protocol
- No trailing slashes

### Step 2: Redeploy Backend

After updating the environment variable:
1. Go to **Railways** → Your Service → **Deployments**
2. Click **"Redeploy"** (or it may auto-redeploy)
3. Wait for deployment to complete

### Step 3: Verify Backend is Running

Test the health endpoint:
```bash
curl https://kristal-backend.up.railway.app/api/health
```

Should return:
```json
{"status": "healthy"}
```

### Step 4: Test CORS

Test from browser console on your Vercel site:
```javascript
fetch('https://kristal-backend.up.railway.app/api/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

If CORS is fixed, this should work without errors.

## Troubleshooting

### If Still Getting 404:
1. Check backend logs in Railways
2. Verify the route exists: `POST /api/chat`
3. Check if backend is actually running

### If Still Getting CORS Error:
1. Double-check `CORS_ORIGINS` has exact Vercel URL (no typos)
2. Make sure backend was redeployed after changing env var
3. Clear browser cache and try again
4. Check backend logs for CORS-related errors

### Check Backend Logs:
In Railways → Your Service → **Logs**, look for:
- CORS errors
- Route not found errors
- Startup messages

## Quick Fix Command

If you have Railway CLI:
```bash
railway variables set CORS_ORIGINS="https://searce-jarvis-poc.vercel.app,http://localhost:3000"
railway up
```

