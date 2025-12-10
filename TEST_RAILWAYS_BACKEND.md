# Testing Your Railways Backend

## Your Backend URL

```
https://searcejarvispoc-production.up.railway.app
```

## Important: It's an API, Not a Website!

When you visit the root URL (`https://searcejarvispoc-production.up.railway.app`), you'll see nothing because it's an API backend, not a website.

You need to test the **API endpoints** instead.

---

## Step 1: Test Health Endpoint

Open this URL in your browser or use curl:

```
https://searcejarvispoc-production.up.railway.app/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-10T...",
  "agentApiStatus": "available",
  "cors_origins": [...],
  "cors_origins_count": 2
}
```

---

## Step 2: Test Debug Endpoint

Test the debug endpoint to see environment variables:

```
https://searcejarvispoc-production.up.railway.app/api/debug/env
```

**Expected response:**
```json
{
  "raw_cors_origins_env": "https://searce-jarvis-poc.vercel.app,http://localhost:3000",
  "parsed_cors_origins": ["https://searce-jarvis-poc.vercel.app", "http://localhost:3000"],
  "cors_origins_count": 2,
  ...
}
```

---

## Step 3: Test API Documentation

FastAPI automatically generates API docs:

**Swagger UI:**
```
https://searcejarvispoc-production.up.railway.app/docs
```

**ReDoc:**
```
https://searcejarvispoc-production.up.railway.app/redoc
```

These will show all available endpoints and let you test them.

---

## Step 4: Update Vercel Environment Variable

1. Go to **Vercel** → Your Project → **Settings** → **Environment Variables**
2. Update `NEXT_PUBLIC_API_URL` to:
   ```
   https://searcejarvispoc-production.up.railway.app
   ```
3. **Redeploy** frontend on Vercel

---

## Step 5: Update CORS_ORIGINS in Railways

1. Go to **Railways** → Your Service → **Variables**
2. Make sure `CORS_ORIGINS` includes your Vercel URL:
   ```
   https://searce-jarvis-poc.vercel.app,http://localhost:3000
   ```
3. **Redeploy** backend on Railways

---

## Step 6: Test from Browser Console

On your Vercel site (`https://searce-jarvis-poc.vercel.app`), open browser console and run:

```javascript
// Test health endpoint
fetch('https://searcejarvispoc-production.up.railway.app/api/health')
  .then(r => r.json())
  .then(data => {
    console.log('✅ Backend is working!', data);
    console.log('CORS Origins:', data.cors_origins);
  })
  .catch(err => {
    console.error('❌ Error:', err);
  });
```

If this works without CORS errors, you're all set!

---

## Troubleshooting

### If health endpoint doesn't work:

1. **Check backend logs** in Railways → Logs tab
2. **Verify backend is running** (should show "Deployment successful")
3. **Check for errors** in the logs

### If you get CORS errors:

1. **Verify CORS_ORIGINS** in Railways Variables includes your Vercel URL
2. **Redeploy backend** after changing CORS_ORIGINS
3. **Check debug endpoint** to see what CORS origins are being read

### If backend returns 404:

1. **Check the route** - make sure you're using `/api/health` not just `/health`
2. **Check backend logs** for route registration
3. **Test with `/docs`** to see all available endpoints

---

## Quick Test Commands

```bash
# Test health
curl https://searcejarvispoc-production.up.railway.app/api/health

# Test debug
curl https://searcejarvispoc-production.up.railway.app/api/debug/env

# Test CORS (from browser console on Vercel site)
fetch('https://searcejarvispoc-production.up.railway.app/api/health')
  .then(r => r.json())
  .then(console.log)
```

---

## Next Steps

1. ✅ Test health endpoint - should return JSON
2. ✅ Test debug endpoint - verify CORS_ORIGINS
3. ✅ Update Vercel `NEXT_PUBLIC_API_URL`
4. ✅ Update Railways `CORS_ORIGINS`
5. ✅ Redeploy both services
6. ✅ Test from browser console

Once these steps are complete, your frontend should be able to connect to the backend!

