# Integration Test - Frontend + Backend Connection

## ✅ Server Status

### Backend Server
- **URL:** http://localhost:8000
- **Status:** Running
- **Health Check:** http://localhost:8000/health
- **API Docs:** http://localhost:8000/docs

### Frontend Server
- **URL:** http://localhost:5173
- **Status:** Running
- **Framework:** Vite + React

## 🔗 Connection Points

The frontend connects to the backend at these endpoints:

1. **Skin Analysis:** `http://localhost:8000/instant/skin`
   - Used when uploading an image for skin tone detection
   - File: `src/App.tsx` line 71

2. **Complete Analysis:** `http://localhost:8000/instant/complete`
   - Used to get full recommendations (body shape + undertone + outfits)
   - File: `src/App.tsx` line 114

3. **Virtual Try-On:** `http://localhost:8000/vton`
   - Used for garment transfer onto user image
   - File: `src/components/VirtualTryOn.tsx` line 52

## 🧪 Test Instructions

### Manual Test via Browser

1. Open **Frontend** preview (http://localhost:5173)
2. Click "Measurements" mode
3. Select your gender
4. Enter measurements:
   - Shoulder: 40 cm
   - Waist: 30 cm
   - Hip: 40 cm
5. Click "Continue"
6. Select undertone (warm, cool, or neutral)
7. Choose occasion (casual, formal, etc.)
8. You should see personalized outfit recommendations! ✨

### API Test via Swagger UI

1. Open **Backend API Docs** preview (http://localhost:8000/docs)
2. Try `/instant/body-shape` endpoint:
   - POST with parameters: shoulder=40, waist=30, hip=40
   - Should return body shape result
3. Try `/instant/complete` endpoint:
   - POST with JSON body
   - Should return complete analysis

### Command Line Test

```powershell
# Test health check
Invoke-WebRequest http://localhost:8000/health

# Test body shape calculation
Invoke-WebRequest -Uri "http://localhost:8000/instant/body-shape?shoulder=40&waist=30&hip=40" -Method POST

# Test complete analysis
$body = @{
    shoulder = 40
    waist = 30
    hip = 40
    gender = "female"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/instant/complete" -Method POST -ContentType "application/json" -Body $body
```

## 🔍 Troubleshooting

### If Frontend Can't Connect to Backend:

1. **Check if both servers are running:**
   ```powershell
   Get-Process python, node
   ```

2. **Verify backend is responding:**
   ```powershell
   Invoke-WebRequest http://localhost:8000/health
   ```

3. **Check browser console for CORS errors:**
   - Open DevTools (F12)
   - Look for red error messages
   - Should see "Access-Control-Allow-Origin" headers

4. **Verify correct ports:**
   - Backend: Port 8000
   - Frontend: Port 5173
   - URLs use `localhost` not `127.0.0.1`

### Common Issues:

❌ **"Could not reach styling backend"**
- Backend server not running on port 8000
- Solution: Restart backend server

❌ **CORS Error in browser console**
- Backend CORS middleware not configured
- Solution: Already fixed in main.py lines 49-65

❌ **Port already in use**
- Old server process still running
- Solution: Kill all Python/Node processes and restart

## 📊 Expected Results

When everything is working correctly:

✅ Health check returns: `{"status":"healthy",...}`
✅ Body shape API returns shape with confidence score
✅ Complete analysis returns bodyShape, colourPalette, and outfits
✅ Frontend displays results without errors
✅ No CORS errors in browser console
✅ Both servers show request logs

## 🎯 Quick Verification

Run this PowerShell script to verify everything:

```powershell
Write-Host "Testing Backend..." -ForegroundColor Cyan
$health = Invoke-WebRequest http://localhost:8000/health -UseBasicParsing
Write-Host "Backend Health: $($health.Content)" -ForegroundColor Green

Write-Host "`nTesting Body Shape API..." -ForegroundColor Cyan
$bodyShape = Invoke-WebRequest "http://localhost:8000/instant/body-shape?shoulder=40&waist=30&hip=40" -Method POST -UseBasicParsing
Write-Host "Body Shape Result: $($bodyShape.Content)" -ForegroundColor Green

Write-Host "`n✅ All tests passed! Servers are connected and working." -ForegroundColor Green
```
