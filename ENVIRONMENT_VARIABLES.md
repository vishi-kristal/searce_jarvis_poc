# Environment Variables Guide

Complete list of environment variables needed for Vercel (Frontend) and Railways (Backend) deployment.

---

## 🚀 Vercel (Frontend) Environment Variables

### Required Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `NEXT_PUBLIC_API_URL` | **REQUIRED** - Backend API URL (from Railways) | `https://your-backend.up.railway.app` |

**Note**: After deploying backend on Railways, copy the public domain URL and set it here.

---

## 🚂 Railways (Backend) Environment Variables

### Required Variables

| Variable | Description | Example Value | Required |
|----------|-------------|---------------|----------|
| `AGENT_API_URL` | Agent API Cloud Run endpoint | `https://kristal-agent-953081186136.asia-southeast1.run.app` | ✅ Yes |
| `RELATIONSHIP_MANAGER_ID` | Relationship Manager ID for agent API | `001` | ✅ Yes |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `https://your-frontend.vercel.app,http://localhost:3000` | ✅ Yes |

### Optional Variables (with defaults)

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `AGENT_API_KEY` | API key for agent authentication (if not using gcloud token) | `AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4` | ❌ No* |
| `ENVIRONMENT` | Environment name | `development` | ❌ No |
| `LOG_LEVEL` | Logging level | `INFO` | ❌ No |
| `SESSION_TIMEOUT_MINUTES` | Session timeout in minutes | `60` | ❌ No |

**Note**: `AGENT_API_KEY` is optional because the backend tries to use `gcloud auth print-identity-token` first. If gcloud is not available in Railways, you may need to set this.

---

## 📋 Quick Setup Guide

### Step 1: Deploy Backend First (Railways)

1. Go to Railways → Your Project → Variables
2. Add these **Required** variables:

```bash
AGENT_API_URL=https://kristal-agent-953081186136.asia-southeast1.run.app
RELATIONSHIP_MANAGER_ID=001
CORS_ORIGINS=http://localhost:3000
```

3. Deploy and copy the **Public Domain** URL (e.g., `https://kristal-backend.up.railway.app`)

### Step 2: Deploy Frontend (Vercel)

1. Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**
2. Click **"Add New"**
3. Add this **Required** variable:

**Variable Name:**
```
NEXT_PUBLIC_API_URL
```

**Value:**
```
https://kristal-backend.up.railway.app
```
(Use the Railways backend URL from Step 1)

**Environments:** Select all (Production, Preview, Development)

4. Click **"Save"**
5. **Redeploy** your frontend (go to Deployments → Latest → Redeploy)

**⚠️ Important:** The frontend must be redeployed after setting this environment variable!

### Step 3: Update CORS in Backend

1. After Vercel deployment, copy your Vercel URL (e.g., `https://searce-jarvis-poc.vercel.app`)
2. Go back to Railways → Variables
3. Update `CORS_ORIGINS`:

```bash
CORS_ORIGINS=https://searce-jarvis-poc.vercel.app,http://localhost:3000
```

**Important**: 
- No spaces after commas
- Include `https://` protocol
- No trailing slashes
- Exact URL match (case-sensitive domain)

4. **Redeploy backend on Railways** (this is critical - env vars require redeploy)

---

## 🔧 Complete Environment Variable Examples

### Vercel (Frontend) - Complete Example

```bash
NEXT_PUBLIC_API_URL=https://kristal-agent-backend.up.railway.app
```

### Railways (Backend) - Complete Example

```bash
# Required
AGENT_API_URL=https://kristal-agent-953081186136.asia-southeast1.run.app
RELATIONSHIP_MANAGER_ID=001
CORS_ORIGINS=https://kristal-agent-poc.vercel.app,http://localhost:3000

# Optional (with defaults)
ENVIRONMENT=production
LOG_LEVEL=INFO
SESSION_TIMEOUT_MINUTES=60

# Optional (only if gcloud auth doesn't work)
AGENT_API_KEY=AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4
```

---

## 🔐 Security Notes

1. **Never commit** `.env` files to git
2. **Use Vercel/Railways** environment variable UI (not code)
3. **Rotate tokens** if exposed
4. **Use different values** for production vs development

---

## ✅ Verification Checklist

After setting environment variables:

- [ ] Backend deployed on Railways with all required variables
- [ ] Frontend deployed on Vercel with `NEXT_PUBLIC_API_URL`
- [ ] CORS updated with Vercel frontend URL
- [ ] Test login: `admin@kristal.ai` / `Krist@l123!`
- [ ] Test chat functionality
- [ ] Check browser console for CORS errors
- [ ] Check backend logs for authentication errors

---

## 🆘 Troubleshooting

### Frontend can't connect to backend
- ✅ Check `NEXT_PUBLIC_API_URL` is correct
- ✅ Verify backend is deployed and accessible
- ✅ Check CORS settings in backend

### Backend can't connect to Agent API
- ✅ Check `AGENT_API_URL` is correct
- ✅ Verify `RELATIONSHIP_MANAGER_ID` is set
- ✅ Check if `AGENT_API_KEY` is needed (if gcloud auth fails)

### CORS errors
- ✅ Update `CORS_ORIGINS` with exact Vercel URL (including `https://`)
- ✅ No trailing slashes in URLs
- ✅ Redeploy backend after CORS changes

---

## 📝 Notes

- **Vercel**: Only `NEXT_PUBLIC_*` variables are exposed to the browser
- **Railways**: All variables are server-side only
- **Order matters**: Deploy backend first, then frontend, then update CORS
- **Case sensitive**: Environment variable names are case-sensitive

