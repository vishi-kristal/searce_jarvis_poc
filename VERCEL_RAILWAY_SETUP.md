# Complete Vercel + Railways Setup Guide

## Both Environment Variables Are Required!

You need to set environment variables in **BOTH** Vercel and Railways.

---

## 🚀 Step 1: Set Railway URL in Vercel (Frontend)

### Why?
The frontend needs to know where to send API requests.

### How to Set:

1. Go to **Vercel Dashboard** → Your Project (`searce-jarvis-poc`)
2. Click **Settings** → **Environment Variables**
3. Click **"Add New"**
4. Add this variable:

**Variable Name:**
```
NEXT_PUBLIC_API_URL
```

**Value:**
```
https://kristal-backend.up.railway.app
```

**Environments:** Select all (Production, Preview, Development)

5. Click **"Save"**
6. **Redeploy** your frontend (go to Deployments → Latest → Redeploy)

### Verify:
After redeploy, check your frontend code is using the correct URL. The frontend uses:
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

---

## 🚂 Step 2: Set CORS in Railways (Backend)

### Why?
The backend needs to allow requests from your Vercel frontend domain.

### How to Set:

1. Go to **Railways Dashboard** → Your Backend Service
2. Click **Variables** tab
3. Find or add `CORS_ORIGINS`
4. Set it to:

```
https://searce-jarvis-poc.vercel.app,http://localhost:3000
```

5. **Redeploy** backend (Railways may auto-redeploy, or manually redeploy)

---

## ✅ Complete Setup Checklist

### Vercel Environment Variables:
- [ ] `NEXT_PUBLIC_API_URL` = `https://kristal-backend.up.railway.app`
- [ ] Frontend redeployed after setting variable

### Railways Environment Variables:
- [ ] `AGENT_API_URL` = `https://kristal-agent-953081186136.asia-southeast1.run.app`
- [ ] `RELATIONSHIP_MANAGER_ID` = `001`
- [ ] `CORS_ORIGINS` = `https://searce-jarvis-poc.vercel.app,http://localhost:3000`
- [ ] Backend redeployed after setting CORS_ORIGINS

---

## 🔍 How to Verify

### 1. Check Frontend is Using Correct Backend URL:
Open browser console on your Vercel site and check network requests. They should go to:
```
https://kristal-backend.up.railway.app/api/chat
```

### 2. Test Backend Health:
```bash
curl https://kristal-backend.up.railway.app/api/health
```

Should return: `{"status": "healthy"}`

### 3. Test CORS from Browser:
On your Vercel site, open browser console and run:
```javascript
fetch('https://kristal-backend.up.railway.app/api/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

If this works without CORS errors, you're all set!

---

## 🆘 Common Issues

### Issue: "Failed to connect to server"
**Solution:** Check `NEXT_PUBLIC_API_URL` is set correctly in Vercel and frontend is redeployed.

### Issue: CORS error
**Solution:** 
1. Check `CORS_ORIGINS` includes exact Vercel URL (no typos, no trailing slash)
2. Backend must be redeployed after changing CORS_ORIGINS
3. Clear browser cache

### Issue: 404 on `/api/chat`
**Solution:** 
1. Check backend is running (test `/api/health`)
2. Check backend logs in Railways
3. Verify route exists: `POST /api/chat`

---

## 📝 Summary

**Vercel needs:**
- `NEXT_PUBLIC_API_URL` → Points to your Railways backend

**Railways needs:**
- `CORS_ORIGINS` → Includes your Vercel frontend URL
- Other backend config variables

**Both need to be set and both services need to be redeployed!**

