# Complete Deployment Guide

## Architecture Overview

```
┌─────────────────────┐
│  Vercel (Frontend)  │  Next.js App
│  vercel.app domain  │
└──────────┬──────────┘
           │
           │ HTTPS API Calls
           │
┌──────────▼──────────┐
│ Railways (Backend)  │  FastAPI
│ railway.app domain  │
└──────────┬──────────┘
           │
           │ HTTPS API Calls
           │
┌──────────▼──────────┐
│  Agent API (GCP)    │  Cloud Run
│  run.app domain     │
└─────────────────────┘
```

## Quick Start Deployment

### 1. Deploy Backend (Railways) - 10 minutes

```bash
# Option 1: Via Railway CLI
npm install -g @railway/cli
railway login
cd backend
railway init
railway up

# Option 2: Via GitHub (Recommended)
# 1. Push code to GitHub
# 2. Go to railways.app
# 3. New Project → Deploy from GitHub repo
# 4. Select backend/ folder
# 5. Set environment variables
# 6. Deploy
```

**Environment Variables (Railways):**
```env
AGENT_API_URL=https://kristal-agent-953081186136.asia-southeast1.run.app
AGENT_API_KEY=AIzaSyCeGoGiJI5k_E8utNO5INsmQ3NlMAPMAa4
RELATIONSHIP_MANAGER_ID=001
CORS_ORIGINS=https://your-app.vercel.app
ENVIRONMENT=production
LOG_LEVEL=INFO
```

**Note:** For production, you may need to use service account authentication instead of API key. See `backend/AUTH_SETUP.md`.

### 2. Deploy Frontend (Vercel) - 5 minutes

**Via Vercel Dashboard:**

1. **Go to vercel.com** → Add New Project
2. **Import GitHub Repository**
   - Select your repo
   - Click Import

3. **Configure Project:**
   ```
   Framework Preset: Next.js
   Root Directory: frontend  ← IMPORTANT!
   Build Command: npm run build (default)
   Output Directory: .next (default)
   ```

4. **Set Environment Variables:**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   ```
   (Get this URL from Railways after backend deployment)

5. **Deploy**
   - Click Deploy
   - Wait ~2-3 minutes
   - Your app is live!

**Via Vercel CLI:**

```bash
cd frontend
npm install -g vercel
vercel login
vercel
# Follow prompts, then:
vercel env add NEXT_PUBLIC_API_URL
# Enter your backend URL
vercel --prod
```

### 3. Update CORS

After frontend is deployed, update backend CORS:

1. Go to Railways dashboard
2. Update environment variable:
   ```
   CORS_ORIGINS=https://your-project.vercel.app
   ```
3. Redeploy backend (or it will auto-redeploy)

## Step-by-Step: Vercel Deployment

### Prerequisites Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed on Railways (get the URL)
- [ ] Vercel account created
- [ ] GitHub account connected to Vercel

### Detailed Steps

#### Step 1: Prepare Repository

```bash
# Ensure code is committed and pushed
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### Step 2: Create Vercel Project

1. **Login to Vercel**
   - Go to https://vercel.com
   - Sign in with GitHub

2. **New Project**
   - Click "Add New..." → "Project"
   - Select your repository
   - Click "Import"

3. **Project Settings**
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: Click "Edit" → Set to `frontend`
   - **Build and Output Settings**: Leave defaults
   - **Environment Variables**: Add `NEXT_PUBLIC_API_URL`

4. **Environment Variables**
   ```
   Name: NEXT_PUBLIC_API_URL
   Value: https://your-backend.railway.app
   Environment: Production, Preview, Development (select all)
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (~2-3 minutes)
   - Success! Your app is live

#### Step 3: Verify Deployment

1. **Check Build Logs**
   - Should see: "Build Completed"
   - No errors in build output

2. **Visit Your App**
   - Go to: `https://your-project.vercel.app`
   - Should see the chat interface

3. **Test Functionality**
   - Enter Client ID
   - Send a test message
   - Check browser console for errors

#### Step 4: Update Backend CORS

1. **Get Vercel URL**
   - From Vercel dashboard: `https://your-project.vercel.app`

2. **Update Railways Environment**
   ```
   CORS_ORIGINS=https://your-project.vercel.app
   ```

3. **Redeploy Backend** (if needed)
   - Or wait for auto-redeploy

## Environment Variables Reference

### Frontend (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://backend.railway.app` |

**Important:** Variables must start with `NEXT_PUBLIC_` to be accessible in the browser.

### Backend (Railways)

| Variable | Description | Example |
|----------|-------------|---------|
| `AGENT_API_URL` | Agent API endpoint | `https://kristal-agent-...run.app` |
| `AGENT_API_KEY` | API key (or use gcloud) | `AIzaSy...` |
| `RELATIONSHIP_MANAGER_ID` | Default RM ID | `001` |
| `CORS_ORIGINS` | Allowed origins | `https://app.vercel.app` |
| `ENVIRONMENT` | Environment | `production` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Vercel Configuration

### Automatic Deployments

Vercel automatically:
- ✅ Deploys on push to `main` branch
- ✅ Creates preview deployments for PRs
- ✅ Runs builds automatically
- ✅ Provides HTTPS certificates

### Custom Domain

1. Go to Project → Settings → Domains
2. Add your domain
3. Update DNS records as shown
4. Update `CORS_ORIGINS` in backend

### Preview Deployments

Every pull request gets a preview URL:
- Format: `https://your-project-git-branch.vercel.app`
- Useful for testing before merging
- Update `CORS_ORIGINS` to include preview URLs if needed

## Troubleshooting

### Build Fails

**Error: "Cannot find module"**
- Check `Root Directory` is set to `frontend`
- Verify `package.json` has all dependencies

**Error: TypeScript errors**
```bash
cd frontend
npm run type-check
# Fix errors, then redeploy
```

### Frontend Can't Connect

**CORS Errors:**
- Verify backend `CORS_ORIGINS` includes Vercel URL
- Check `NEXT_PUBLIC_API_URL` is correct
- Ensure backend is deployed and accessible

**Network Errors:**
- Test backend directly: `curl https://your-backend.railway.app/api/health`
- Check backend logs in Railways
- Verify environment variables are set

### Environment Variables Not Working

- Must start with `NEXT_PUBLIC_` for client-side
- Redeploy after adding variables
- Check Vercel dashboard → Settings → Environment Variables

## Production Optimizations

### 1. Enable Analytics

In Vercel Dashboard:
- Project → Settings → Analytics
- Enable Web Analytics

### 2. Optimize Images

Already configured in `next.config.js`:
- Google Cloud Storage domains allowed
- Image optimization enabled

### 3. Error Tracking

Add Sentry or similar:
```bash
npm install @sentry/nextjs
```

### 4. Performance Monitoring

- Use Vercel Analytics
- Monitor Core Web Vitals
- Check backend response times

## CI/CD Workflow

### Automatic Deployment Flow

```
Developer pushes to GitHub
    ↓
Vercel detects changes
    ↓
Builds Next.js app
    ↓
Runs tests (if configured)
    ↓
Deploys to production
    ↓
Sends notification
```

### Manual Deployment

```bash
# Deploy specific branch
vercel --prod

# Deploy preview
vercel
```

## Monitoring & Logs

### Vercel Logs

1. Go to Project → Deployments
2. Click on a deployment
3. View "Function Logs" or "Build Logs"

### Backend Logs (Railways)

1. Go to Railways dashboard
2. Select your backend service
3. View "Logs" tab

## Rollback

If deployment fails:

1. Go to Vercel → Deployments
2. Find last working deployment
3. Click "..." → "Promote to Production"

## Security Checklist

- [ ] Environment variables set (not hardcoded)
- [ ] API keys secured
- [ ] CORS properly configured
- [ ] HTTPS enabled (automatic on Vercel)
- [ ] No sensitive data in client-side code
- [ ] Error messages don't expose internals

## Cost Estimation

### Vercel (Frontend)
- **Hobby Plan**: Free
  - 100GB bandwidth/month
  - Unlimited deployments
  - Perfect for PoC

### Railways (Backend)
- **Free Trial**: $5 credit/month
- **Pro Plan**: Pay as you go
  - ~$5-10/month for small app

## Next Steps

1. ✅ Deploy backend to Railways
2. ✅ Deploy frontend to Vercel
3. ✅ Test end-to-end functionality
4. ✅ Set up monitoring
5. ✅ Configure custom domain (optional)
6. ✅ Add error tracking
7. ✅ Set up CI/CD workflows

## Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Next.js Deployment**: https://nextjs.org/docs/deployment
- **Railways Docs**: https://docs.railway.app
- **Vercel Discord**: https://vercel.com/discord

## Quick Commands Reference

```bash
# Deploy to Vercel
cd frontend
vercel --prod

# View deployments
vercel ls

# View logs
vercel logs

# Remove deployment
vercel remove

# Link local project
vercel link
```

