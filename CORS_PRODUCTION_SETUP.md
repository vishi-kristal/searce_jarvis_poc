# CORS Configuration for Production Deployment

## Important: CORS_ORIGINS Must Be Set in Production

The code defaults to `localhost` **only for local development**. For production deployment, you **MUST** set `CORS_ORIGINS` in Railways with your actual Vercel frontend URL.

---

## How It Works

### Local Development (Default)
- If `CORS_ORIGINS` is not set → defaults to `http://localhost:3000`
- This is fine for local testing

### Production (Railways)
- **You MUST set `CORS_ORIGINS`** in Railways environment variables
- Value should be your Vercel frontend URL
- Example: `https://searce-jarvis-poc.vercel.app,http://localhost:3000`

---

## Setup for Production

### Step 1: Deploy Frontend to Vercel
1. Deploy frontend → Get Vercel URL (e.g., `https://searce-jarvis-poc.vercel.app`)

### Step 2: Set CORS_ORIGINS in Railways
1. Go to **Railways** → Your Backend Service → **Variables**
2. Add/Update `CORS_ORIGINS`:
   ```
   https://searce-jarvis-poc.vercel.app,http://localhost:3000
   ```
3. **Redeploy** backend

### Step 3: Verify
After redeploying, check logs for:
```
INFO:     CORS Origins: ['https://searce-jarvis-poc.vercel.app', 'http://localhost:3000']
```

---

## Why Localhost Default?

The localhost default is:
- ✅ **Safe** - Only used if `CORS_ORIGINS` is not set
- ✅ **Convenient** - Works for local development without configuration
- ✅ **Not used in production** - As long as you set the environment variable

**In production, you MUST set `CORS_ORIGINS` in Railways!**

---

## Common Mistakes

❌ **Not setting CORS_ORIGINS in production:**
- Backend will only allow `localhost` requests
- Your Vercel frontend will get CORS errors

✅ **Correct:**
- Set `CORS_ORIGINS` in Railways with your Vercel URL
- Include both production and localhost for flexibility

---

## Current Setup Checklist

- [ ] Frontend deployed on Vercel
- [ ] Backend deployed on Railways
- [ ] `CORS_ORIGINS` set in Railways with Vercel URL
- [ ] Backend redeployed after setting CORS_ORIGINS
- [ ] Test from Vercel site - should work without CORS errors

---

## Code Explanation

The code reads `CORS_ORIGINS` directly from environment:
```python
cors_env = os.getenv("CORS_ORIGINS")
if not cors_env:
    return "http://localhost:3000"  # Default only
return cors_env  # Use what's set in environment
```

**In production (Railways), `CORS_ORIGINS` environment variable will be set, so the default is never used.**

