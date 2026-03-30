# 🚀 Deployment Guide - Dress AI StyleMatch

Complete guide to deploy Dress AI to production.

---

## 📋 Table of Contents

1. [GitHub Setup](#github-setup)
2. [Frontend Hosting Options](#frontend-hosting-options)
3. [Backend Hosting Options](#backend-hosting-options)
4. [Database Setup](#database-setup)
5. [Environment Configuration](#environment-configuration)
6. [Production Checklist](#production-checklist)

---

## 🔧 GitHub Setup

### Step 1: Commit Your Changes

```bash
cd e:\dress_ai

# Add all files (excluding .gitignore items)
git add .

# Commit with message
git commit -m "Add e-commerce integration and fix frontend-backend connection"

# Push to GitHub
git push origin main
```

### Step 2: Create GitHub Repository

If you haven't already:

1. Go to https://github.com/new
2. Repository name: `dress-ai` or `stylematch`
3. Visibility: Public or Private
4. Click **Create repository**
5. Follow the instructions to push your code

---

## 🌐 Frontend Hosting Options

### Option 1: Vercel (Recommended ⭐)

**Best for:** React/Vite apps, automatic deployments, free tier

#### Deploy to Vercel:

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Build the frontend:**
   ```bash
   npm run build
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

4. **Configure environment variables:**
   - In Vercel dashboard, go to Settings → Environment Variables
   - Add: `VITE_API_URL=https://your-backend-url.com`

#### Automatic Deployments:

1. Connect GitHub repository to Vercel
2. Every push to `main` triggers automatic deployment
3. Preview deployments for pull requests

**Free Tier:** ✅ Unlimited deployments, 100GB bandwidth/month

---

### Option 2: Netlify

**Best for:** Static sites, continuous deployment

#### Deploy to Netlify:

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Build:**
   ```bash
   npm run build
   ```

3. **Deploy:**
   ```bash
   netlify deploy --prod --dir=dist
   ```

**Free Tier:** ✅ Unlimited sites, 100GB bandwidth/month

---

### Option 3: GitHub Pages

**Best for:** Simple static hosting, integrated with GitHub

#### Deploy to GitHub Pages:

1. **Install gh-pages:**
   ```bash
   npm install -D gh-pages
   ```

2. **Update package.json:**
   ```json
   {
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d dist"
     },
     "homepage": "https://yourusername.github.io/dress-ai"
   }
   ```

3. **Deploy:**
   ```bash
   npm run deploy
   ```

**Free Tier:** ✅ Free for public repositories

---

## 🔙 Backend Hosting Options

### Option 1: Railway (Recommended ⭐)

**Best for:** Python/FastAPI, PostgreSQL, easy setup

#### Deploy to Railway:

1. **Create Railway account:** https://railway.app

2. **Connect GitHub:**
   - New Project → Deploy from GitHub
   - Select your dress-ai repository

3. **Configure:**
   - Root directory: `backend`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Port: Set by Railway (default 8000)

4. **Add PostgreSQL (optional):**
   - New → Database → PostgreSQL
   - Railway auto-injects `DATABASE_URL`

5. **Environment Variables:**
   ```
   DATABASE_URL=postgresql://...
   REDIS_URL=redis://...
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

**Free Tier:** $5 credit/month (enough for small apps)

---

### Option 2: Render

**Best for:** Web services, PostgreSQL included

#### Deploy to Render:

1. **Create account:** https://render.com

2. **New Web Service:**
   - Connect GitHub repository
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment:**
   - Choose Python 3 runtime
   - Add environment variables

**Free Tier:** ✅ Free web service (with limitations), PostgreSQL available

---

### Option 3: Heroku

**Best for:** Production-ready, scalable

#### Deploy to Heroku:

1. **Install Heroku CLI:**
   ```bash
   # Windows
   choco install heroku-cli
   
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create app:**
   ```bash
   cd backend
   heroku create dress-ai-api
   ```

4. **Add Procfile:**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

5. **Deploy:**
   ```bash
   git subtree push --prefix backend heroku main
   ```

**Pricing:** $7/month for basic dyno

---

### Option 4: Google Cloud Run

**Best for:** Serverless, auto-scaling, pay-per-use

#### Deploy to Cloud Run:

1. **Build Docker image:**
   ```bash
   docker build -t gcr.io/your-project/dress-ai ./backend
   ```

2. **Push to Container Registry:**
   ```bash
   docker push gcr.io/your-project/dress-ai
   ```

3. **Deploy:**
   ```bash
   gcloud run deploy dress-ai \
     --image gcr.io/your-project/dress-ai \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

**Free Tier:** ✅ 2 million requests/month free

---

## 🗄️ Database Setup

### Option 1: Railway PostgreSQL

- Automatically provisioned
- Connection string auto-injected
- No configuration needed

### Option 2: Supabase

**Free PostgreSQL hosting:**

1. Create account: https://supabase.com
2. New project → Get connection string
3. Use as `DATABASE_URL`

### Option 3: Neon

**Serverless PostgreSQL:**

1. Create account: https://neon.tech
2. Create database → Get connection string
3. Free tier: 0.5 GB storage

---

## ⚙️ Environment Configuration

### Frontend (.env)

```env
VITE_API_URL=https://your-backend-url.com
```

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis (optional for caching)
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-domain.com

# API Keys (if using external APIs)
AMAZON_API_KEY=your_key
FLIPKART_API_KEY=your_key

# App settings
ENVIRONMENT=production
DEBUG=false
```

---

## ✅ Production Checklist

### Before Deployment:

- [ ] Remove all `console.log()` statements
- [ ] Update CORS origins to production URLs
- [ ] Set up environment variables
- [ ] Configure database connection
- [ ] Test all endpoints locally
- [ ] Build frontend successfully
- [ ] Update API URLs in frontend code

### After Deployment:

- [ ] Test frontend loads correctly
- [ ] Verify API calls work
- [ ] Check CORS headers
- [ ] Test e-commerce links
- [ ] Monitor error logs
- [ ] Set up custom domain (optional)
- [ ] Enable HTTPS
- [ ] Configure CDN for static assets

---

## 🔗 Quick Deploy Commands

### Full Deployment Script:

```bash
# 1. Commit to GitHub
git add .
git commit -m "Production ready"
git push origin main

# 2. Build frontend
npm run build

# 3. Deploy frontend (Vercel)
cd dist
vercel --prod

# 4. Deploy backend (Railway)
# Use Railway dashboard or CLI
railway up --cwd backend

# 5. Update environment variables
# In Vercel: VITE_API_URL = your-railway-url.app
```

---

## 📊 Monitoring & Analytics

### Recommended Tools:

1. **Sentry** - Error tracking
   ```bash
   npm install @sentry/react  # Frontend
   pip install sentry-sdk     # Backend
   ```

2. **Google Analytics** - User analytics

3. **LogRocket** - Session replay

---

## 🎯 Cost Estimates

### Free Tier Deployment:

- **Frontend (Vercel):** $0/month
- **Backend (Railway):** ~$0-5/month (depending on usage)
- **Database (Railway):** Included
- **Total:** $0-5/month

### Production Deployment:

- **Frontend (Vercel Pro):** $20/month (optional)
- **Backend (Railway Standard):** $20/month
- **Database (Managed):** $15/month
- **Total:** ~$55/month

---

## 🆘 Troubleshooting

### Issue: Frontend can't connect to backend

**Solution:**
- Update `VITE_API_URL` in Vercel/Netlify
- Ensure CORS includes frontend URL
- Check backend is running

### Issue: Database connection fails

**Solution:**
- Verify `DATABASE_URL` format
- Check firewall allows connections
- Use connection pooling

### Issue: Build fails

**Solution:**
- Clear cache: `rm -rf node_modules package-lock.json`
- Reinstall: `npm install`
- Check Node version: `node --version` (should be 18+)

---

## 📞 Support

- **Documentation:** See README.md
- **Issues:** GitHub Issues
- **API Docs:** `/docs` endpoint on backend

---

**Ready to deploy? Start with the GitHub setup above! 🚀**
