# Quick Deployment Guide for Vercel & Railways

## ✅ Code Status
- **Repository**: https://github.com/vishi-kristal/searce_jarvis_poc.git
- **Status**: Code successfully pushed to GitHub
- **Branch**: `main`

---

## 🚀 Deploy Frontend to Vercel

### Step 1: Import Repository
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New..."** → **"Project"**
3. Click **"Import Git Repository"**
4. Search for: `vishi-kristal/searce_jarvis_poc`
5. Click **"Import"**

### Step 2: Configure Project
1. **Framework Preset**: Next.js (auto-detected)
2. **Root Directory**: `frontend` ⚠️ **IMPORTANT**
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)
5. **Install Command**: `npm install` (default)

### Step 3: Set Environment Variables
Click **"Environment Variables"** and add:

```
NEXT_PUBLIC_API_URL=https://your-railways-backend-url.up.railway.app
```

**Note**: You'll need to deploy the backend first to get the URL, or use a placeholder and update later.

### Step 4: Deploy
1. Click **"Deploy"**
2. Wait for build to complete (~2-3 minutes)
3. Your frontend will be live at: `https://your-project.vercel.app`

---

## 🚂 Deploy Backend to Railways

### Step 1: Create Account & Project
1. Go to [railways.app](https://railways.app) and sign in with GitHub
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Find and select: `vishi-kristal/searce_jarvis_poc`

### Step 2: Configure Service
1. **Service Name**: `kristal-agent-backend` (or your choice)
2. **Root Directory**: `backend` ⚠️ **IMPORTANT**
3. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Dockerfile**: Auto-detected from `backend/Dockerfile`

### Step 3: Set Environment Variables
Go to **"Variables"** tab and add:

```bash
# Agent API Configuration
AGENT_API_URL=https://kristal-agent-953081186136.asia-southeast1.run.app
AGENT_API_KEY=your-api-key-if-needed
RELATIONSHIP_MANAGER_ID=001

# CORS Configuration (update with your Vercel URL after deployment)
CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000

# Environment
ENVIRONMENT=production
LOG_LEVEL=INFO

# Session Configuration
SESSION_TIMEOUT_MINUTES=60
```

### Step 4: Deploy
1. Click **"Deploy"**
2. Wait for build to complete (~3-5 minutes)
3. Your backend will be live at: `https://your-service.up.railway.app`

### Step 5: Get Backend URL
1. After deployment, go to **"Settings"** → **"Networking"**
2. Copy the **Public Domain** URL (e.g., `https://kristal-agent-backend.up.railway.app`)
3. Update Vercel environment variable `NEXT_PUBLIC_API_URL` with this URL
4. Redeploy frontend on Vercel

---

## 🔄 Update CORS After Deployment

Once both are deployed:

1. **Get Vercel Frontend URL**: `https://your-project.vercel.app`
2. **Update Railways Backend Environment Variable**:
   ```
   CORS_ORIGINS=https://your-project.vercel.app,http://localhost:3000
   ```
3. **Redeploy Backend** on Railways

---

## ✅ Verification Checklist

- [ ] Frontend deployed on Vercel
- [ ] Backend deployed on Railways
- [ ] `NEXT_PUBLIC_API_URL` set in Vercel
- [ ] All environment variables set in Railways
- [ ] CORS updated with Vercel URL
- [ ] Test login: `admin@kristal.ai` / `Krist@l123!`
- [ ] Test chat functionality

---

## 🔗 Quick Links

- **GitHub Repo**: https://github.com/vishi-kristal/searce_jarvis_poc
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Railways Dashboard**: https://railways.app/dashboard

---

## 🆘 Troubleshooting

### Frontend Issues
- **Build fails**: Check `frontend/package.json` dependencies
- **API errors**: Verify `NEXT_PUBLIC_API_URL` is correct
- **CORS errors**: Update `CORS_ORIGINS` in backend

### Backend Issues
- **Build fails**: Check `backend/requirements.txt`
- **401 errors**: Verify `AGENT_API_KEY` or gcloud auth token
- **Port errors**: Ensure `$PORT` is used in start command

### Common Fixes
1. **Clear build cache** on both platforms
2. **Redeploy** after environment variable changes
3. **Check logs** in Vercel/Railways dashboards

---

## 📝 Next Steps

1. Deploy backend first (Railways)
2. Get backend URL
3. Deploy frontend (Vercel) with backend URL
4. Update CORS in backend
5. Test the application

**Your app will be live and ready for internal testing!** 🎉

