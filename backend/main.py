from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from .body_shape import get_body_shape_from_measurements
from .colour_harmony import get_colour_palette_for_undertone
from .models import AnalyzeRequest, AnalysisResult, InputMode, Measurements
from .recommendations import get_outfit_recommendations
from pathlib import Path
import json
import numpy as np
import httpx

try:
    import cv2  # type: ignore
except Exception:
    cv2 = None

app = FastAPI(
    title="StyleMatch Fashion API",
    description="Backend for dual-mode fashion recommendations (body shape + colour harmony).",
    version="1.0.0",
)

# Allow local frontend during development
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5174",
    "http://localhost:5174",
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


@app.get("/generate_image")
async def generate_image(prompt: str):
    url = f"https://image.pollinations.ai/prompt/{prompt}?nologo=true"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
    return Response(content=resp.content, media_type=resp.headers.get("content-type", "image/jpeg"))


@app.post("/skin_tone")
async def skin_tone(file: UploadFile = File(...)):
    if cv2 is None:
        raise HTTPException(status_code=500, detail="OpenCV not available on server")
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file")
    content = await file.read()
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
    return {
        "undertone": undertone,
        "season": season,
        "confidence": confidence,
        "lab_mean": [float(mean_lab[0]), float(mean_lab[1]), float(mean_lab[2])],
    }


@app.post("/analyze", response_model=AnalysisResult)
def analyze(req: AnalyzeRequest) -> AnalysisResult:
    """Combine body shape, undertone, and outfits into one response.

    - If imageBodyShape is provided, we trust that (client-side image analysis).
    - Otherwise we compute shape from measurements.
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

    return AnalysisResult(
        bodyShape=body_shape_result,
        colourPalette=palette,
        outfits=outfits,
        inputMode=req.inputMode,
        gender=gender,
    )


@app.post("/vton")
async def vton(user_image: UploadFile = File(...), garment_image: UploadFile = File(...)):
    if not user_image.content_type or not user_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="user_image must be an image")
    if not garment_image.content_type or not garment_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="garment_image must be an image")
    
    # Placeholder: In a real app, you would run IDM-VTON here.
    # For now, we simply return the user image to verify the UI hook.
    # We read the file content into memory to avoid incomplete chunked encoding errors
    # with StreamingResponse on some platforms/configurations.
    content = await user_image.read()
    return Response(content=content, media_type=user_image.content_type)


