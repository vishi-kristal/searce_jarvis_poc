# How to Check Environment Variables

## Step 1: Check What Backend is Reading

After redeploying the backend, test the debug endpoint:

```bash
curl https://kristal-backend.up.railway.app/api/debug/env
```

This will show you:
- Raw `CORS_ORIGINS` value from environment
- Parsed CORS origins (what FastAPI is using)
- All environment variables

**Expected output:**
```json
{
  "raw_cors_origins_env": "https://searce-jarvis-poc.vercel.app,http://localhost:3000",
  "parsed_cors_origins": ["https://searce-jarvis-poc.vercel.app", "http://localhost:3000"],
  "cors_origins_count": 2,
  ...
}
```

---

## Step 2: Check Railways Environment Variables

### In Railways Dashboard:

1. Go to **Railways** → Your Backend Service
2. Click **Variables** tab
3. Check these variables:

**Required Variables:**

| Variable | Expected Value | Notes |
|----------|---------------|-------|
| `CORS_ORIGINS` | `https://searce-jarvis-poc.vercel.app,http://localhost:3000` | No spaces, no trailing slashes |
| `AGENT_API_URL` | `https://kristal-agent-953081186136.asia-southeast1.run.app` | Agent API endpoint |
| `RELATIONSHIP_MANAGER_ID` | `001` | Relationship Manager ID |

### Common Issues:

❌ **Wrong:**
```
CORS_ORIGINS = https://searce-jarvis-poc.vercel.app , http://localhost:3000
```
(Spaces after comma)

❌ **Wrong:**
```
CORS_ORIGINS = https://searce-jarvis-poc.vercel.app/
```
(Trailing slash)

❌ **Wrong:**
```
CORS_ORIGINS = searce-jarvis-poc.vercel.app
```
(Missing https://)

✅ **Correct:**
```
CORS_ORIGINS = https://searce-jarvis-poc.vercel.app,http://localhost:3000
```

---

## Step 3: Check Vercel Environment Variables

### In Vercel Dashboard:

1. Go to **Vercel** → Your Project (`searce-jarvis-poc`)
2. Click **Settings** → **Environment Variables**
3. Check this variable:

**Required Variable:**

| Variable | Expected Value | Notes |
|----------|---------------|-------|
| `NEXT_PUBLIC_API_URL` | `https://kristal-backend.up.railway.app` | Your Railways backend URL |

### Verify:

- Variable name is exactly: `NEXT_PUBLIC_API_URL` (case-sensitive)
- Value is your Railways backend URL
- Applied to all environments (Production, Preview, Development)

---

## Step 4: Test After Changes

### 1. Test Backend Debug Endpoint:
```bash
curl https://kristal-backend.up.railway.app/api/debug/env
```

Check `parsed_cors_origins` includes your Vercel URL.

### 2. Test Health Endpoint:
```bash
curl https://kristal-backend.up.railway.app/api/health
```

Should show CORS origins in response.

### 3. Test from Browser:
On your Vercel site (`https://searce-jarvis-poc.vercel.app`), open browser console:

```javascript
// Check what API URL frontend is using
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL || 'NOT SET');

// Test CORS
fetch('https://kristal-backend.up.railway.app/api/health')
  .then(r => r.json())
  .then(data => {
    console.log('✅ CORS works!', data);
  })
  .catch(err => {
    console.error('❌ CORS error:', err);
  });
```

---

## Step 5: Common Fixes

### If CORS_ORIGINS is empty or wrong:

1. **Double-check the variable in Railways:**
   - Go to Variables tab
   - Click on `CORS_ORIGINS`
   - Copy the exact value
   - Verify no extra spaces or characters

2. **Redeploy backend:**
   - Environment variables require redeploy to take effect
   - Go to Deployments → Redeploy

3. **Check backend logs:**
   - Look for startup log: `CORS Origins: [...]`
   - Verify it shows your Vercel URL

### If NEXT_PUBLIC_API_URL is wrong:

1. **Check Vercel environment variables:**
   - Settings → Environment Variables
   - Verify `NEXT_PUBLIC_API_URL` exists
   - Verify value is correct Railways URL

2. **Redeploy frontend:**
   - Frontend must be redeployed after changing env vars
   - Go to Deployments → Redeploy

---

## Quick Diagnostic Checklist

- [ ] Backend debug endpoint shows correct CORS_ORIGINS
- [ ] Railways Variables tab shows correct CORS_ORIGINS
- [ ] Vercel Environment Variables shows NEXT_PUBLIC_API_URL
- [ ] Both services redeployed after setting variables
- [ ] Backend logs show CORS origins on startup
- [ ] Health endpoint returns CORS info
- [ ] Browser test works without CORS errors

---

## Still Not Working?

If you've checked everything and it's still not working:

1. **Share the debug endpoint output:**
   ```bash
   curl https://kristal-backend.up.railway.app/api/debug/env
   ```

2. **Share backend startup logs** from Railways (look for CORS Origins line)

3. **Share browser console errors** (exact error message)

4. **Verify exact URLs:**
   - Frontend URL: `https://searce-jarvis-poc.vercel.app`
   - Backend URL: `https://kristal-backend.up.railway.app`

These details will help diagnose the issue.

