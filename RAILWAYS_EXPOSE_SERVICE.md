# How to Expose Railways Service

## Issue: "Unexposed Service"

If your Railways service shows "Unexposed service", it means:
- The service is running but not publicly accessible
- You need to generate a public domain/URL
- This is why CORS and API calls are failing

## Solution: Generate Public Domain

### Step 1: Expose the Service

1. Go to **Railways** → Your Backend Service
2. Click on the **"Settings"** tab (in the navigation bar)
3. Scroll down to **"Networking"** section
4. Find **"Generate Domain"** or **"Public Networking"**
5. Click **"Generate Domain"** or toggle **"Public"** to ON
6. Railways will generate a public domain like: `https://your-service.up.railway.app`

### Step 2: Copy the Public Domain

After generating the domain, you'll see something like:
```
https://searce-jarvis-poc-production.up.railway.app
```
or
```
https://kristal-backend.up.railway.app
```

**Copy this exact URL** - this is your backend URL!

### Step 3: Update Vercel Environment Variable

1. Go to **Vercel** → Your Project → **Settings** → **Environment Variables**
2. Update `NEXT_PUBLIC_API_URL` with the **new public domain** from Railways
3. Value should be: `https://your-actual-railways-domain.up.railway.app`
4. **Redeploy** frontend on Vercel

### Step 4: Update CORS_ORIGINS in Railways

1. Go back to **Railways** → **Variables** tab
2. Make sure `CORS_ORIGINS` includes your Vercel URL:
   ```
   https://searce-jarvis-poc.vercel.app,http://localhost:3000
   ```
3. **Redeploy** backend on Railways

### Step 5: Verify

After exposing and updating:

1. **Test backend is accessible:**
   ```bash
   curl https://your-actual-railways-domain.up.railway.app/api/health
   ```

2. **Test debug endpoint:**
   ```bash
   curl https://your-actual-railways-domain.up.railway.app/api/debug/env
   ```

3. **Test from browser** (on your Vercel site):
   ```javascript
   fetch('https://your-actual-railways-domain.up.railway.app/api/health')
     .then(r => r.json())
     .then(console.log)
     .catch(console.error)
   ```

---

## Alternative: Custom Domain

If you want to use a custom domain instead:

1. In Railways **Settings** → **Networking**
2. Click **"Custom Domain"**
3. Add your domain
4. Update DNS records as instructed
5. Use this custom domain in Vercel's `NEXT_PUBLIC_API_URL`

---

## Important Notes

- **Unexposed services** are only accessible internally within Railways
- **Exposed services** get a public `*.up.railway.app` domain
- The public domain is **required** for Vercel to connect to your backend
- After exposing, you **must** update `NEXT_PUBLIC_API_URL` in Vercel with the new URL

---

## Quick Checklist

- [ ] Service is exposed (shows public domain, not "Unexposed")
- [ ] Copied the public domain URL from Railways
- [ ] Updated `NEXT_PUBLIC_API_URL` in Vercel with new URL
- [ ] Updated `CORS_ORIGINS` in Railways (if needed)
- [ ] Redeployed both frontend and backend
- [ ] Tested backend health endpoint
- [ ] Tested from browser console

---

## Still Having Issues?

If you've exposed the service but still getting errors:

1. **Verify the public domain** - Check Railways Settings → Networking
2. **Check backend logs** - Look for startup messages
3. **Test the domain directly** - `curl https://your-domain.up.railway.app/api/health`
4. **Check CORS_ORIGINS** - Use debug endpoint to verify

The "Unexposed service" is likely the main issue - once exposed, everything should work!

