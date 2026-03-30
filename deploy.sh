#!/bin/bash
# Quick Deploy Script for Dress AI
# This script helps you deploy to GitHub and hosting platforms

echo "🚀 Dress AI - Quick Deploy Script"
echo "=================================="
echo ""

# Step 1: Git Commit & Push
echo "📦 Step 1: Committing changes to Git..."
git add .
git commit -m "Deploy updates $(date '+%Y-%m-%d %H:%M')"
git push origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""

# Step 2: Frontend Deployment Options
echo "🌐 Step 2: Choose frontend deployment:"
echo "   1) Vercel (Recommended)"
echo "   2) Netlify"
echo "   3) Skip for now"
read -p "Enter choice (1-3): " frontend_choice

case $frontend_choice in
    1)
        echo ""
        echo "🔵 Deploying to Vercel..."
        npm run build
        if command -v vercel &> /dev/null; then
            vercel --prod
        else
            echo "⚠️  Vercel CLI not found. Install with: npm install -g vercel"
            echo "Then run: vercel --prod"
        fi
        ;;
    2)
        echo ""
        echo "🟣 Deploying to Netlify..."
        npm run build
        if command -v netlify &> /dev/null; then
            netlify deploy --prod --dir=dist
        else
            echo "⚠️  Netlify CLI not found. Install with: npm install -g netlify-cli"
            echo "Then run: netlify deploy --prod --dir=dist"
        fi
        ;;
    *)
        echo "⏭️  Skipping frontend deployment"
        ;;
esac

echo ""
echo "=================================="
echo "✨ Deployment Summary"
echo "=================================="
echo ""
echo "GitHub: ✅ Code pushed"
echo "Frontend: $([ $frontend_choice -eq 1 ] && echo 'Vercel' || ([ $frontend_choice -eq 2 ] && echo 'Netlify' || echo 'Not deployed'))"
echo ""
echo "Next steps for backend deployment:"
echo "1. Go to https://railway.app or https://render.com"
echo "2. Connect your GitHub repository"
echo "3. Set root directory to 'backend'"
echo "4. Set build command: pip install -r requirements.txt"
echo "5. Set start command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo "6. Add environment variables (DATABASE_URL, etc.)"
echo ""
echo "🎉 Happy deploying!"
