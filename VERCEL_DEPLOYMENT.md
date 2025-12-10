# Vercel Deployment Guide

## Overview

This guide covers deploying the **Next.js frontend** to Vercel. The FastAPI backend should be deployed separately (Railways recommended).

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **Backend Deployed**: Backend should be deployed first (Railways or similar)

## Step 1: Prepare Your Repository

### 1.1 Push Code to GitHub

```bash
# Initialize git if not already done
cd /Users/vishirajvanshi/Documents/agent_engg_bcamp/gcp_jarvis_ui
git init
git add .
git commit -m "Initial commit"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/yourusername/kristal-agent-poc.git
git branch -M main
git push -u origin main
```

### 1.2 Update .gitignore

Ensure `.gitignore` excludes sensitive files:
```
frontend/.env
frontend/.env.local
backend/.env
backend/venv/
node_modules/
```

## Step 2: Deploy Backend First (Railways)

Before deploying frontend, deploy backend to get the API URL:

1. Go to [Railways](https://railways.app)
2. Create new project
3. Connect your GitHub repository
4. Select the `backend` folder as root
5. Set environment variables:
   ```
   AGENT_API_URL=https://kristal-agent-953081186136.asia-southeast1.run.app
   AGENT_API_KEY=AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4
   RELATIONSHIP_MANAGER_ID=001
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```
6. Deploy and note the backend URL (e.g., `https://your-backend.railway.app`)

## Step 3: Deploy Frontend to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com)
   - Click "Add New Project"

2. **Import Repository**
   - Connect your GitHub account if not already connected
   - Select your repository: `kristal-agent-poc`
   - Click "Import"

3. **Configure Project**
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend` (IMPORTANT: Set this!)
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)
   - **Install Command**: `npm install` (default)

4. **Environment Variables**
   Click "Environment Variables" and add:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   ```
   (Replace with your actual backend URL from Railways)

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live at `https://your-project.vercel.app`

### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

4. **Deploy**
   ```bash
   vercel
   ```
   Follow the prompts:
   - Set up and deploy? **Yes**
   - Which scope? Select your account
   - Link to existing project? **No** (first time)
   - Project name? `kristal-agent-poc` (or your choice)
   - Directory? `./` (current directory)
   - Override settings? **No**

5. **Set Environment Variables**
   ```bash
   vercel env add NEXT_PUBLIC_API_URL
   # Enter: https://your-backend.railway.app
   ```

6. **Redeploy with Environment Variables**
   ```bash
   vercel --prod
   ```

## Step 4: Update CORS Settings

After deploying frontend, update backend CORS to include Vercel URL:

1. Go to Railways dashboard
2. Update environment variable:
   ```
   CORS_ORIGINS=https://your-project.vercel.app,https://your-project.vercel.app
   ```
3. Redeploy backend

## Step 5: Verify Deployment

1. **Check Frontend**
   - Visit your Vercel URL: `https://your-project.vercel.app`
   - Should see the chat interface

2. **Test Connection**
   - Enter a Client ID
   - Try sending a message
   - Check browser console for errors

3. **Check Backend Logs**
   - Go to Railways dashboard
   - Check logs for incoming requests

## Configuration Files

### vercel.json (Optional)

Create `frontend/vercel.json` for custom configuration:

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "outputDirectory": ".next"
}
```

### Environment Variables Reference

**Frontend (Vercel):**
- `NEXT_PUBLIC_API_URL` - Backend API URL (required)

**Backend (Railways):**
- `AGENT_API_URL` - Agent API endpoint
- `AGENT_API_KEY` - API key (or use gcloud auth)
- `RELATIONSHIP_MANAGER_ID` - Default RM ID
- `CORS_ORIGINS` - Allowed frontend origins

## Troubleshooting

### Build Fails

**Error: Module not found**
- Check that `Root Directory` is set to `frontend`
- Verify all dependencies are in `package.json`

**Error: TypeScript errors**
- Run `npm run type-check` locally first
- Fix any type errors before deploying

### Frontend Can't Connect to Backend

**CORS Errors:**
- Verify `CORS_ORIGINS` in backend includes Vercel URL
- Check that backend URL in `NEXT_PUBLIC_API_URL` is correct
- Ensure backend is deployed and accessible

**404 Errors:**
- Verify backend URL is correct
- Check backend routes are working: `https://your-backend.railway.app/api/health`

### Environment Variables Not Working

- Ensure variables start with `NEXT_PUBLIC_` for client-side access
- Redeploy after adding environment variables
- Check Vercel dashboard → Settings → Environment Variables

## Continuous Deployment

Vercel automatically deploys on every push to main branch:

1. Push to GitHub
2. Vercel detects changes
3. Builds and deploys automatically
4. Preview deployments for PRs

## Custom Domain (Optional)

1. Go to Vercel Dashboard → Project → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update `CORS_ORIGINS` in backend to include custom domain

## Production Checklist

- [ ] Backend deployed and accessible
- [ ] Environment variables set in Vercel
- [ ] CORS configured in backend
- [ ] Frontend builds successfully
- [ ] Test chat functionality
- [ ] Test session creation
- [ ] Verify error handling
- [ ] Check mobile responsiveness

## Monitoring

- **Vercel Analytics**: Enable in project settings
- **Vercel Logs**: View in dashboard → Deployments → View Function Logs
- **Backend Logs**: View in Railways dashboard

## Rollback

If something goes wrong:

1. Go to Vercel Dashboard → Deployments
2. Find previous working deployment
3. Click "..." → "Promote to Production"

## Cost Estimation

**Vercel (Frontend):**
- Free tier: 100GB bandwidth/month
- Hobby: $0/month (suitable for PoC)
- Pro: $20/month (if needed)

**Railways (Backend):**
- Free tier: $5 credit/month
- Pro: Pay as you go

## Next Steps After Deployment

1. Test with real users
2. Monitor error rates
3. Set up error tracking (Sentry, etc.)
4. Configure custom domain
5. Set up CI/CD workflows
6. Add analytics

## Support

- **Vercel Docs**: https://vercel.com/docs
- **Next.js Deployment**: https://nextjs.org/docs/deployment
- **Railways Docs**: https://docs.railway.app

