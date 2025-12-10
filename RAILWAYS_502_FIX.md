# Fixing 502 Error - Application Failed to Respond

## Issue

Your backend domain is working (`searcejarvispoc-production.up.railway.app`), but you're getting:
```json
{"status":"error","code":502,"message":"Application failed to respond"}
```

This means:
- ✅ Domain is exposed correctly
- ❌ Backend application isn't running or not responding

---

## Step 1: Check Backend Logs

1. Go to **Railways** → Your Service
2. Click **"View logs"** button (or go to **Deployments** → Latest → **Logs**)
3. Look for:
   - **Startup errors**
   - **Port binding errors**
   - **Application crashes**
   - **Import errors**

**Common issues to look for:**
- `Address already in use` - Port conflict
- `ModuleNotFoundError` - Missing dependencies
- `ImportError` - Code errors
- `Connection refused` - App not listening on correct port

---

## Step 2: Verify Deployment Status

1. In Railways → **Deployments** tab
2. Check if latest deployment shows:
   - ✅ **"Deployment successful"** (green)
   - ❌ **"Deployment failed"** (red)
   - ⏳ **"Deploying..."** (still building)

If deployment failed, check the logs for errors.

---

## Step 3: Check Port Configuration

### In Railways Settings:

1. Go to **Settings** → **Networking**
2. Verify the port is set to **8000**
3. Check if there's a **"Start Command"** setting

### Verify Start Command:

The start command should be:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Or if Railways sets PORT automatically:
```bash
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

---

## Step 4: Check Environment Variables

1. Go to **Variables** tab
2. Verify these are set:
   - `AGENT_API_URL`
   - `RELATIONSHIP_MANAGER_ID`
   - `CORS_ORIGINS`

Missing required variables might cause startup failures.

---

## Step 5: Common Fixes

### Fix 1: Redeploy Backend

Sometimes a redeploy fixes issues:

1. Go to **Deployments**
2. Click **"Redeploy"** on latest deployment
3. Wait for build to complete
4. Check logs for errors

### Fix 2: Check Root Directory

1. Go to **Settings** → **Service**
2. Verify **Root Directory** is set to: `backend`
3. If not set, update it and redeploy

### Fix 3: Verify Dockerfile

Make sure your `backend/Dockerfile` exists and is correct:
- Uses Python 3.11
- Installs requirements.txt
- Exposes port 8000
- Runs uvicorn command

### Fix 4: Check Python Version

Railways might be using wrong Python version. Verify in:
- `backend/Dockerfile` - Should specify Python version
- `backend/requirements.txt` - Should have all dependencies

---

## Step 6: Test After Fix

After fixing the issue and redeploying:

1. **Wait 1-2 minutes** for deployment to complete
2. **Test health endpoint:**
   ```bash
   curl https://searcejarvispoc-production.up.railway.app/api/health
   ```

3. **Check logs** for startup messages:
   ```
   Starting Kristal Agent PoC API
   CORS Origins: [...]
   ```

---

## Quick Diagnostic Checklist

- [ ] Backend deployment shows "successful" (green)
- [ ] Logs show "Starting Kristal Agent PoC API"
- [ ] No errors in logs (red error messages)
- [ ] Port is set to 8000 in Networking settings
- [ ] Root Directory is set to `backend`
- [ ] Environment variables are set
- [ ] Dockerfile exists and is correct

---

## Still Getting 502?

If you've checked everything and still getting 502:

1. **Share backend logs** - Copy the error messages from Railways logs
2. **Share deployment status** - Is it successful or failed?
3. **Check if app is listening** - Look for "Uvicorn running on" in logs

The logs will tell us exactly what's wrong!

