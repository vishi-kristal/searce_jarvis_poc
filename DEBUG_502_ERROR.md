# Debugging 502 Error

## Current Status

The backend is returning 502 errors, which means the application is crashing on startup.

## What to Check

### Step 1: Check Railways Logs

Go to **Railways** → Your Service → **Logs** tab and look for:

**Look for these errors:**
- `CORS_ORIGINS` parsing errors
- `SettingsError` or `JSONDecodeError`
- Import errors
- Port binding errors
- Any Python traceback

**Look for these success messages:**
- `INFO:     Starting Kristal Agent PoC API`
- `INFO:     Uvicorn running on http://0.0.0.0:XXXX`
- `INFO:     Application startup complete`

### Step 2: Share the Error

Please share:
1. **The exact error message** from the logs (copy the traceback)
2. **The last few lines** before the crash
3. **Any startup messages** you see

### Step 3: About Agent API URL

**Changing the Agent API URL won't fix the 502 error** because:
- The backend crashes **before** it can make any API calls
- The 502 means the app isn't running at all
- We need to fix the startup crash first

**However**, you can update it later:
- Current: `https://kristal-agent-953081186136.asia-southeast1.run.app`
- Alternative: `https://google-portal.kristal.ai`

But **first**, we need to get the backend running.

---

## Most Likely Issue

The backend is still crashing due to **CORS_ORIGINS parsing**. Even though we fixed it with `@computed_field`, there might be:
1. An old deployment still running
2. The fix hasn't been deployed yet
3. Another configuration issue

---

## Quick Fixes to Try

### Fix 1: Verify Latest Code is Deployed

Check that the latest commit with `@computed_field` fix is deployed:
- Go to Railways → Deployments
- Check the latest deployment commit hash
- Should match the latest commit in GitHub

### Fix 2: Check CORS_ORIGINS in Railways

1. Go to Railways → Variables
2. Check `CORS_ORIGINS` value
3. Make sure it's a simple string: `https://searce-jarvis-poc.vercel.app,http://localhost:3000`
4. No JSON, no arrays, just a comma-separated string

### Fix 3: Temporarily Remove CORS_ORIGINS

For testing, you can temporarily:
1. Delete `CORS_ORIGINS` from Railways Variables
2. Redeploy
3. The code will use default: `http://localhost:3000`

This will help us isolate if CORS_ORIGINS is the issue.

---

## Next Steps

1. **Check Railways logs** and share the error
2. **Verify latest code is deployed**
3. **Check CORS_ORIGINS variable** format
4. Once backend is running, we can update Agent API URL if needed

The Agent API URL change can wait - first priority is getting the backend to start!

