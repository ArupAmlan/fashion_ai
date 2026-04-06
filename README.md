# StyleMatch — AI-Powered Fashion Recommendation System 🚀

**Your personal stylist powered by AI** — Get personalized outfit recommendations based on your body shape, skin undertone, and style preferences. Now with **e-commerce integration** for instant shopping!

## 🌐 Live Demo

👉 **Try it now:** [https://fashion-ai-bay.vercel.app/](https://fashion-ai-bay.vercel.app/)

## ✨ Latest Features

- 🛍️ **E-commerce Integration**: Direct shopping links to Amazon, Flipkart & Myntra
- 🔗 **Frontend-Backend Connected**: Fully integrated and tested
- ⚡ **Instant Analysis**: Get recommendations in under 100ms
- 📸 **AI Image Analysis**: Optional pose detection and skin tone analysis
- 🎨 **Smart Color Matching**: Seasonal color palette recommendations
- 👗 **Body Shape Detection**: 6 body types with tailored suggestions
- 🧘 **Virtual Try-On**: Placeholder for AI-powered garment transfer

## 🎯 Quick Start

### Local Development

```bash
# Backend (Terminal 1)
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Frontend (Terminal 2)
npm install
npm run dev
```

Open http://localhost:5173

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide to Vercel, Railway, Netlify, and more.

```bash
# Quick deploy to Vercel (frontend)
npm run build
vercel --prod

# Deploy backend to Railway
railway up --cwd backend
```

## System Requirements
- Node.js 18+
- Python 3.10+ (tested with 3.13)

## Backend Setup (FastAPI)
Install Python dependencies:
```bash
pip install fastapi uvicorn numpy httpx opencv-python
```

Run the backend:
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup (React + Vite)
Install and run:
```bash
npm install
npm run dev
```
Open http://localhost:5173

## Production Build
```bash
npm run build
npm run preview
```

## Project Structure
- `src/components/` — ModeSelect, MeasurementForm, ImageUpload, UndertoneStep, Results, VirtualTryOn
- `src/lib/` — bodyShape, colourHarmony, recommendations, imageAnalysis, poseDetection, skinUndertone
- `src/types.ts` — shared types
- `backend/` — FastAPI app: [main.py](file:///e:/dress_ai/backend/main.py), [models.py](file:///e:/dress_ai/backend/models.py), [body_shape.py](file:///e:/dress_ai/backend/body_shape.py), [colour_harmony.py](file:///e:/dress_ai/backend/colour_harmony.py), [recommendations.py](file:///e:/dress_ai/backend/recommendations.py)

## Key Endpoints
- `POST /analyze` — returns body shape, colour palette, and ranked outfit suggestions.
  - Request: `AnalyzeRequest { gender, inputMode, undertone, measurements?, imageBodyShape? }`
  - Response: `AnalysisResult { bodyShape, colourPalette, outfits, inputMode, gender }`
- `POST /skin_tone` — optional server-side undertone suggestion from image.
  - Form field `file`: image; requires OpenCV installed; otherwise returns 500.
- `POST /vton` — placeholder Virtual Try-On. Validates image inputs and returns the user image to verify the pipeline.
- `GET /generate_image?prompt=...` — backend image proxy for generating real outfit photos, avoiding `net::ERR_BLOCKED_BY_ORB`.

## How Outfit Images Work
- The frontend requests image URLs from the backend recommendations.
- Each `imageUrl` points to the backend proxy `GET /generate_image?prompt=...`.
- The backend fetches from the upstream generator and returns image bytes from your own origin, preventing ORB/CORS issues.

## CORS
The backend allows local Vite origins:
- http://localhost:5173
- http://127.0.0.1:5173
- http://localhost:5174
- http://127.0.0.1:5174

## Troubleshooting
- ORB/CORS blocked images:
  - Ensure outfit `imageUrl` values use `http://localhost:8000/generate_image?prompt=...` (already configured in recommendations).
- OpenCV errors on `/skin_tone`:
  - Install `opencv-python`, or skip the server undertone and use the client suggestion.
- Backend not reachable:
  - Confirm the backend is running on port 8000 and CORS origins match your Vite dev URL.
- Large bundle warnings:
  - Vite warns on large chunks; use code-splitting or adjust `build.chunkSizeWarningLimit` if needed.

## Notes
- No 3D body features are present in this version.
- All analysis designed to be privacy-aware; image mode can run entirely on-device.

## Licence
MIT
