# Quick Deploy Script for Dress AI (PowerShell)
# This script helps you deploy to GitHub and hosting platforms

Write-Host "🚀 Dress AI - Quick Deploy Script" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Git Commit & Push
Write-Host "📦 Step 1: Committing changes to Git..." -ForegroundColor Yellow
git add .
git commit -m "Deploy updates $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main

Write-Host ""
Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green
Write-Host ""

# Step 2: Frontend Deployment Options
Write-Host "🌐 Step 2: Choose frontend deployment:" -ForegroundColor Yellow
Write-Host "   1) Vercel (Recommended)"
Write-Host "   2) Netlify"
Write-Host "   3) Skip for now"
$frontendChoice = Read-Host "Enter choice (1-3)"

switch ($frontendChoice) {
    "1" {
        Write-Host ""
        Write-Host "🔵 Deploying to Vercel..." -ForegroundColor Blue
        npm run build
        if (Get-Command vercel -ErrorAction SilentlyContinue) {
            vercel --prod
        } else {
            Write-Host "⚠️  Vercel CLI not found. Install with: npm install -g vercel" -ForegroundColor Yellow
            Write-Host "Then run: vercel --prod"
        }
    }
    "2" {
        Write-Host ""
        Write-Host "🟣 Deploying to Netlify..." -ForegroundColor Purple
        npm run build
        if (Get-Command netlify -ErrorAction SilentlyContinue) {
            netlify deploy --prod --dir=dist
        } else {
            Write-Host "⚠️  Netlify CLI not found. Install with: npm install -g netlify-cli" -ForegroundColor Yellow
            Write-Host "Then run: netlify deploy --prod --dir=dist"
        }
    }
    default {
        Write-Host "⏭️  Skipping frontend deployment" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "✨ Deployment Summary" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "GitHub: ✅ Code pushed" -ForegroundColor Green

if ($frontendChoice -eq "1") {
    $platform = "Vercel"
} elseif ($frontendChoice -eq "2") {
    $platform = "Netlify"
} else {
    $platform = "Not deployed"
}
Write-Host "Frontend: $platform" -ForegroundColor Green

Write-Host ""
Write-Host "Next steps for backend deployment:" -ForegroundColor Yellow
Write-Host "1. Go to https://railway.app or https://render.com"
Write-Host "2. Connect your GitHub repository"
Write-Host "3. Set root directory to 'backend'"
Write-Host "4. Set build command: pip install -r requirements.txt"
Write-Host "5. Set start command: uvicorn main:app --host 0.0.0.0 --port `$PORT"
Write-Host "6. Add environment variables (DATABASE_URL, etc.)"
Write-Host ""
Write-Host "🎉 Happy deploying!" -ForegroundColor Green
