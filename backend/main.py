from fastapi import FastAPI, UploadFile, File, HTTPException, Response, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from body_shape import get_body_shape_from_measurements
from colour_harmony import get_colour_palette_for_undertone
from models import AnalyzeRequest, AnalysisResult, InputMode, Measurements, BodyShapeResult
from recommendations import get_outfit_recommendations
from pathlib import Path
import json
import numpy as np
import io
from typing import Optional

# New imports for enhanced features
from database import init_db, get_db, AnalysisHistory, FavoriteOutfit
from vton_service import virtual_try_on, generate_outfit_image
from pose_service import get_pose_analyzer
from image_utils import compress_for_analysis, compress_for_vton, extract_face_region
from cache_service import cached, get_cached_result, set_cached_result
from ecommerce_service import get_ecommerce_searcher
from fast_ai_service import get_fast_ai
from instant_analysis import get_instant_analyzer, instant_recommendations, instant_skin_analysis, instant_body_shape
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import time

try:
    import cv2  # type: ignore
except Exception:
    cv2 = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    await init_db()
    yield


app = FastAPI(
    title="StyleMatch Fashion API",
    description="Enhanced backend with VTON, AI image generation, pose detection, caching, and e-commerce integration.",
    version="2.0.0",
    lifespan=lifespan,
)

# Allow local frontend during development
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5174",
    "http://localhost:5174",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_season_lab_means():
    data_path = Path(__file__).parent / "season_lab_ranges.json"
    if not data_path.exists():
        return {}
    with data_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return {k: np.array(v["lab_mean"], dtype=np.float32) for k, v in data.items()}


SEASON_LAB_MEANS = _load_season_lab_means()


def _classify_undertone_from_lab(lab_vec: np.ndarray) -> str:
    a = float(lab_vec[1])
    b = float(lab_vec[2])
    if (b - a) > 10:
        return "warm"
    if (a - b) > 5:
        return "cool"
    return "neutral"


def _nearest_season(lab_vec: np.ndarray) -> tuple[str, float]:
    if not SEASON_LAB_MEANS:
        return "neutral", 0.0
    best_name = "neutral"
    best_dist = float("inf")
    for name, mean in SEASON_LAB_MEANS.items():
        d = float(np.linalg.norm(lab_vec - mean))
        if d < best_dist:
            best_dist = d
            best_name = name
    conf = max(0.0, 1.0 - best_dist / 100.0)
    return best_name, conf


@app.post("/skin_tone")
async def skin_tone(file: UploadFile = File(...)):
    """Enhanced skin tone analysis with face detection and seasonal colors"""
    if cv2 is None:
        raise HTTPException(status_code=500, detail="OpenCV not available on server")
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file")
    
    content = await file.read()
    
    # Compress image for faster processing
    content = await compress_for_analysis(content)
    
    # Try to extract face region for better skin tone analysis
    face_region = extract_face_region(content)
    if face_region is not None:
        content = face_region
    
    buf = np.frombuffer(content, dtype=np.uint8)
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Could not decode image")
    
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)
    mask = cv2.inRange(ycrcb, lower, upper)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
    
    if int(mask.sum()) == 0:
        h, w = img.shape[:2]
        x0 = int(w * 0.3)
        y0 = int(h * 0.1)
        x1 = int(w * 0.7)
        y1 = int(h * 0.35)
        roi = img[y0:y1, x0:x1]
    else:
        roi = cv2.bitwise_and(img, img, mask=mask)
    
    lab = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)
    lab_pixels = lab.reshape(-1, 3)
    lab_pixels = lab_pixels[np.any(lab_pixels != 0, axis=1)]
    
    if lab_pixels.size == 0:
        raise HTTPException(status_code=400, detail="No skin pixels found")
    
    mean_lab = lab_pixels.mean(axis=0)
    undertone = _classify_undertone_from_lab(mean_lab)
    season, confidence = _nearest_season(mean_lab)
    
    # Enhanced seasonal color analysis
    seasonal_colors = get_seasonal_colors(season)
    
    return {
        "undertone": undertone,
        "season": season,
        "confidence": confidence,
        "lab_mean": [float(mean_lab[0]), float(mean_lab[1]), float(mean_lab[2])],
        "seasonalColors": seasonal_colors,
        "faceDetected": face_region is not None,
    }


def get_seasonal_colors(season: str) -> dict:
    """Get color recommendations for each season"""
    seasonal_palettes = {
        "spring": {
            "best": ["Coral", "Peach", "Warm yellow", "Golden brown", "Turquoise", "Cream"],
            "good": ["Salmon", "Aqua", "Light green", "Camel", "Apricot"],
            "avoid": ["Black", "White", "Cool pastels", "Dark navy"],
        },
        "summer": {
            "best": ["Lavender", "Powder blue", "Rose", "Soft pink", "Grey", "Navy"],
            "good": ["Plum", "Sage", "Dusty blue", "Mauve", "Silver"],
            "avoid": ["Orange", "Bright yellow", "Warm brown", "Gold"],
        },
        "autumn": {
            "best": ["Olive", "Rust", "Terracotta", "Mustard", "Chocolate", "Burnt orange"],
            "good": ["Forest green", "Camel", "Gold", "Bronze", "Deep peach"],
            "avoid": ["Bright pink", "Lavender", "Cool grey", "Neon colors"],
        },
        "winter": {
            "best": ["Black", "White", "Navy", "True red", "Emerald", "Ice blue"],
            "good": ["Hot pink", "Royal blue", "Purple", "Silver", "Charcoal"],
            "avoid": ["Beige", "Orange", "Gold", "Peach", "Muted tones"],
        },
    }
    return seasonal_palettes.get(season.lower(), seasonal_palettes["spring"])


@app.post("/analyze", response_model=AnalysisResult)
async def analyze(
    req: AnalyzeRequest,
    db: AsyncSession = Depends(get_db),
) -> AnalysisResult:
    """Combine body shape, undertone, and outfits into one response.
    
    - If imageBodyShape is provided, we trust that (client-side image analysis).
    - Otherwise we compute shape from measurements.
    - Results are cached and saved to history.
    """
    gender = req.gender

    if req.imageBodyShape is not None:
        body_shape_result = req.imageBodyShape
    else:
        if req.measurements is None:
            raise ValueError("measurements are required when imageBodyShape is not provided")
        body_shape_result = get_body_shape_from_measurements(req.measurements, gender)

    palette = get_colour_palette_for_undertone(req.undertone)
    outfits = get_outfit_recommendations(body_shape_result.shape, palette, gender)
    
    # Save to history
    try:
        history = AnalysisHistory(
            body_shape=body_shape_result.shape.value,
            undertone=req.undertone.value,
            season="unknown",
            outfits=[o.dict() for o in outfits[:5]],
        )
        db.add(history)
        await db.commit()
    except Exception as e:
        print(f"Failed to save history: {e}")

    return AnalysisResult(
        bodyShape=body_shape_result,
        colourPalette=palette,
        outfits=outfits,
        inputMode=req.inputMode,
        gender=gender,
    )


@app.post("/vton")
async def vton(
    user_image: UploadFile = File(...),
    garment_image: UploadFile = File(...),
):
    """Virtual try-on with AI-powered garment transfer"""
    if not user_image.content_type or not user_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="user_image must be an image")
    if not garment_image.content_type or not garment_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="garment_image must be an image")
    
    # Read and compress images
    user_content = await user_image.read()
    garment_content = await garment_image.read()
    
    user_content = await compress_for_vton(user_content)
    garment_content = await compress_for_vton(garment_content)
    
    # Perform VTON
    result = await virtual_try_on(user_content, garment_content)
    
    return Response(content=result, media_type="image/png")


@app.post("/pose/measurements")
async def pose_measurements(
    file: UploadFile = File(...),
    height_cm: float = 170.0,
):
    """Estimate body measurements from pose detection"""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file")
    
    content = await file.read()
    content = await compress_for_analysis(content)
    
    analyzer = get_pose_analyzer()
    measurements = analyzer.get_measurements_for_height(content, height_cm)
    
    if measurements is None:
        raise HTTPException(status_code=400, detail="Could not detect pose in image")
    
    # Calculate body shape from estimated measurements
    from models import Measurements as MeasurementsModel, Gender
    m = MeasurementsModel(
        shoulder=measurements["shoulder"],
        waist=measurements["waist"],
        hip=measurements["hip"],
    )
    body_shape = get_body_shape_from_measurements(m, Gender.female)
    
    return {
        "measurements": measurements,
        "bodyShape": body_shape,
    }


@app.post("/generate/outfit")
async def generate_outfit(
    description: str,
    gender: str = "female",
    style: str = "casual",
):
    """Generate AI image for an outfit description"""
    image_bytes = await generate_outfit_image(description, gender, style)
    
    if image_bytes is None:
        raise HTTPException(status_code=500, detail="Failed to generate image")
    
    return Response(content=image_bytes, media_type="image/png")


@app.get("/shop/search")
async def shop_search(
    query: str,
    outfit_id: str = None,
):
    """Search for products across e-commerce platforms"""
    searcher = get_ecommerce_searcher()
    
    # Check cache first
    cache_key = f"shop_search:{query}:{outfit_id}"
    cached = await get_cached_result(cache_key)
    if cached:
        return cached
    
    results = await searcher.search_all(query)
    
    # Cache for 1 hour
    await set_cached_result(cache_key, results, 3600)
    
    return results


@app.get("/shop/links")
async def shop_links(
    outfit_name: str,
    colors: str = "",  # Comma-separated
):
    """Generate affiliate links for an outfit"""
    searcher = get_ecommerce_searcher()
    color_list = [c.strip() for c in colors.split(",") if c.strip()]
    links = searcher.generate_affiliate_links(outfit_name, color_list)
    return links


@app.get("/history")
async def get_history(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """Get analysis history"""
    from sqlalchemy import select
    result = await db.execute(
        select(AnalysisHistory).order_by(AnalysisHistory.created_at.desc()).limit(limit)
    )
    history = result.scalars().all()
    return [
        {
            "id": h.id,
            "body_shape": h.body_shape,
            "undertone": h.undertone,
            "season": h.season,
            "created_at": h.created_at.isoformat() if h.created_at else None,
        }
        for h in history
    ]


@app.post("/favorites")
async def add_favorite(
    outfit_id: str,
    outfit_data: dict,
    db: AsyncSession = Depends(get_db),
):
    """Add outfit to favorites"""
    favorite = FavoriteOutfit(
        outfit_id=outfit_id,
        outfit_data=outfit_data,
    )
    db.add(favorite)
    await db.commit()
    return {"status": "added"}


@app.get("/favorites")
async def get_favorites(
    db: AsyncSession = Depends(get_db),
):
    """Get favorite outfits"""
    from sqlalchemy import select
    result = await db.execute(select(FavoriteOutfit).order_by(FavoriteOutfit.created_at.desc()))
    favorites = result.scalars().all()
    return [
        {
            "id": f.id,
            "outfit_id": f.outfit_id,
            "outfit_data": f.outfit_data,
            "created_at": f.created_at.isoformat() if f.created_at else None,
        }
        for f in favorites
    ]


# ========== FAST AI ENDPOINTS ==========

@app.post("/fast/vton")
async def fast_vton(
    user_image: UploadFile = File(...),
    garment_image: UploadFile = File(...),
    style: str = "casual",
):
    """Ultra-fast virtual try-on (under 5 seconds)"""
    start = time.time()
    
    user_content = await user_image.read()
    garment_content = await garment_image.read()
    
    # Quick compression
    user_content = await compress_for_vton(user_content)
    garment_content = await compress_for_vton(garment_content)
    
    ai = get_fast_ai()
    result = await ai.fast_virtual_tryon(user_content, garment_content, style)
    
    elapsed = time.time() - start
    print(f"Fast VTON: {elapsed:.2f}s")
    
    return Response(
        content=result,
        media_type="image/jpeg",
        headers={"X-Processing-Time": str(elapsed)}
    )


@app.post("/fast/generate")
async def fast_generate(
    description: str,
    gender: str = "female",
    style: str = "modern",
    colors: str = "",  # comma-separated
):
    """Fast outfit generation (under 5 seconds)"""
    start = time.time()
    
    color_list = [c.strip() for c in colors.split(",") if c.strip()]
    
    ai = get_fast_ai()
    result = await ai.fast_generate_outfit(description, gender, style, color_list)
    
    elapsed = time.time() - start
    print(f"Fast Generate: {elapsed:.2f}s")
    
    return Response(
        content=result,
        media_type="image/jpeg",
        headers={"X-Processing-Time": str(elapsed)}
    )


@app.post("/fast/analyze")
async def fast_analyze(
    file: UploadFile = File(...),
    height_cm: float = 170.0,
):
    """Ultra-fast complete analysis (skin + pose)"""
    start = time.time()
    
    content = await file.read()
    content = await compress_for_analysis(content)
    
    ai = get_fast_ai()
    
    # Run both analyses concurrently
    skin_task = ai._fast_skin_analysis(content)
    pose_task = ai._fast_pose_analysis(content)
    
    skin_result, pose_result = await asyncio.gather(skin_task, pose_task)
    
    # Calculate body shape if pose detected
    body_shape = None
    if pose_result:
        from models import Measurements, Gender
        m = Measurements(
            shoulder=pose_result.get("shoulder_width", 0) * 100,
            waist=pose_result.get("waist_estimate", 0) * 100,
            hip=pose_result.get("hip_width", 0) * 100,
        )
        body_shape = get_body_shape_from_measurements(m, Gender.female)
    
    elapsed = time.time() - start
    
    return {
        "skin_analysis": skin_result,
        "pose_analysis": pose_result,
        "body_shape": body_shape.dict() if body_shape else None,
        "processing_time": elapsed,
    }


@app.post("/fast/recommendations")
async def fast_recommendations(
    body_shape: str,
    undertone: str,
    gender: str = "female",
    occasion: str = "casual",
):
    """AI-powered smart recommendations"""
    ai = get_fast_ai()
    
    recommendations = await ai.smart_recommendations(
        body_shape=body_shape,
        undertone=undertone,
        gender=gender,
        occasion=occasion,
    )
    
    return {
        "recommendations": recommendations,
        "count": len(recommendations),
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mode": "instant",
        "features": ["instant_analysis", "fast_vton", "fast_generate", "smart_recommendations"],
    }


# ========== INSTANT ENDPOINTS - NO DELAY ==========

@app.post("/instant/analyze")
async def instant_analyze_endpoint(
    file: UploadFile = File(None),
    measurements: str = "",  # JSON string
):
    """Ultra-fast complete analysis - under 100ms"""
    start = time.time()
    
    # Parse measurements if provided
    m = None
    if measurements:
        try:
            import json
            m = json.loads(measurements)
        except:
            pass
    
    # Read image if provided
    image_bytes = None
    if file:
        image_bytes = await file.read()
    
    # Instant analysis
    analyzer = get_instant_analyzer()
    result = analyzer.analyze(image_bytes, m)
    
    elapsed = (time.time() - start) * 1000
    result["api_time_ms"] = elapsed
    
    return result


@app.post("/instant/skin")
async def instant_skin(file: UploadFile = File(...)):
    """Instant skin tone analysis - under 10ms"""
    content = await file.read()
    result = instant_skin_analysis(content)
    return result


@app.post("/instant/body-shape")
async def instant_body_shape_endpoint(
    shoulder: float = 40,
    waist: float = 30,
    hip: float = 40,
):
    """Instant body shape calculation"""
    measurements = {"shoulder": shoulder, "waist": waist, "hip": hip}
    result = instant_body_shape(measurements)
    return result


@app.post("/instant/recommendations")
async def instant_recommendations_endpoint(
    body_shape: str = "rectangle",
    undertone: str = "neutral",
    gender: str = "female",
):
    """Instant recommendations - under 5ms"""
    start = time.time()
    
    recs = instant_recommendations(body_shape, undertone, gender)
    
    elapsed = (time.time() - start) * 1000
    
    return {
        "recommendations": recs,
        "count": len(recs),
        "time_ms": elapsed,
    }


@app.post("/instant/complete")
async def instant_complete(
    file: UploadFile = File(None),
    shoulder: float = 40,
    waist: float = 30,
    hip: float = 40,
    gender: str = "female",
):
    """Complete instant workflow - everything in one call under 100ms"""
    start = time.time()
    
    # Parallel processing
    image_bytes = await file.read() if file else b""
    measurements = {"shoulder": shoulder, "waist": waist, "hip": hip}
    
    # All analyses
    skin = instant_skin_analysis(image_bytes)
    body = instant_body_shape(measurements)
    recs = instant_recommendations(body["shape"], skin["undertone"], gender)
    
    elapsed = (time.time() - start) * 1000
    
    return {
        "analysis": {
            "bodyShape": body,
            "undertone": skin["undertone"],
            "season": skin["season"],
            "palette": skin["palette"],
        },
        "outfits": recs,
        "processing_time_ms": elapsed,
    }


