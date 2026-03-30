from PIL import Image
import io
import numpy as np
import cv2
from typing import Optional, List, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor
import hashlib
import time

# Thread pool for CPU-bound operations
_executor = ThreadPoolExecutor(max_workers=4)

# Model cache
_model_cache = {}


class FastAIProcessor:
    """Ultra-fast AI processing with optimizations"""
    
    def __init__(self):
        self.vton_pipe = None
        self.gen_pipe = None
    
    async def fast_virtual_tryon(
        self,
        person_bytes: bytes,
        garment_bytes: bytes,
        style: str = "casual",
    ) -> bytes:
        """Ultra-fast VTON - simple overlay blend"""
        start_time = time.time()
        
        def _process():
            # Load images
            person = Image.open(io.BytesIO(person_bytes)).convert("RGBA")
            garment = Image.open(io.BytesIO(garment_bytes)).convert("RGBA")
            
            # Resize to same size
            size = (384, 384)
            person = person.resize(size, Image.Resampling.LANCZOS)
            garment = garment.resize(size, Image.Resampling.LANCZOS)
            
            # Create a simple blend - overlay garment on lower half of person
            result = person.copy()
            
            # Paste garment with transparency
            for y in range(size[1]//2, size[1]):
                for x in range(size[0]//4, 3*size[0]//4):
                    px = garment.getpixel((x, y))
                    if px[3] > 128:  # If not transparent
                        # Blend with person
                        p_px = person.getpixel((x, y))
                        alpha = px[3] / 255.0
                        new_px = tuple(int(p_px[i] * (1-alpha) + px[i] * alpha) for i in range(3))
                        result.putpixel((x, y), new_px + (255,))
            
            # Convert to RGB
            result = result.convert("RGB")
            
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=85)
            return output.getvalue()
        
        # Run in thread pool
        result = await asyncio.get_event_loop().run_in_executor(_executor, _process)
        print(f"Fast VTON completed in {time.time() - start_time:.2f}s")
        return result
    
    async def fast_generate_outfit(
        self,
        description: str,
        gender: str = "female",
        style: str = "modern",
        colors: List[str] = None,
    ) -> bytes:
        """Generate outfit image - creates a styled placeholder"""
        start_time = time.time()
        
        def _process():
            # Create a styled placeholder image with text
            size = (512, 512)
            img = Image.new('RGB', size, (245, 245, 245))
            
            # Add some color blocks representing the outfit
            color_str = ", ".join(colors[:3]) if colors else "Fashion Colors"
            
            # Draw color swatches
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            
            # Background gradient effect
            for y in range(size[1]):
                r = int(240 + (y / size[1]) * 15)
                g = int(240 + (y / size[1]) * 10)
                b = int(245 + (y / size[1]) * 5)
                draw.line([(0, y), (size[0], y)], fill=(r, g, b))
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 32)
                small_font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Draw text
            text = description[:30]
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (size[0] - text_width) // 2
            draw.text((x, 200), text, fill=(50, 50, 50), font=font)
            
            # Draw style info
            style_text = f"{style.title()} | {gender.title()}"
            bbox2 = draw.textbbox((0, 0), style_text, font=small_font)
            style_width = bbox2[2] - bbox2[0]
            x2 = (size[0] - style_width) // 2
            draw.text((x2, 260), style_text, fill=(100, 100, 100), font=small_font)
            
            # Draw colors
            draw.text((x2, 300), f"Colors: {color_str}", fill=(100, 100, 100), font=small_font)
            
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=90)
            return output.getvalue()
        
        result = await asyncio.get_event_loop().run_in_executor(_executor, _process)
        print(f"Fast Generation completed in {time.time() - start_time:.2f}s")
        return result
    
    async def batch_analyze(
        self,
        images: List[bytes],
        analysis_type: str = "all",
    ) -> List[Dict]:
        """Analyze multiple images in parallel"""
        tasks = [self._analyze_single(img, analysis_type) for img in images]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _analyze_single(self, image_bytes: bytes, analysis_type: str) -> Dict:
        """Single image analysis"""
        results = {}
        
        if analysis_type in ("all", "skin"):
            results["skin"] = await self._fast_skin_analysis(image_bytes)
        
        if analysis_type in ("all", "pose"):
            results["pose"] = await self._fast_pose_analysis(image_bytes)
        
        return results
    
    async def _fast_skin_analysis(self, image_bytes: bytes) -> Dict:
        """Ultra-fast skin tone analysis"""
        def _process():
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                return {"undertone": "neutral", "confidence": 0.5}
            
            # Resize for speed
            img = cv2.resize(img, (256, 256))
            
            # Fast skin detection
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower = np.array([0, 20, 70], dtype=np.uint8)
            upper = np.array([50, 170, 255], dtype=np.uint8)
            mask = cv2.inRange(hsv, lower, upper)
            
            # Quick undertone classification
            mean_hsv = cv2.mean(hsv, mask=mask)
            hue = mean_hsv[0]
            sat = mean_hsv[1]
            
            if hue < 15 or sat < 40:
                undertone = "warm"
            elif hue > 25:
                undertone = "cool"
            else:
                undertone = "neutral"
            
            return {
                "undertone": undertone,
                "confidence": 0.75,
                "hue": float(hue),
                "saturation": float(sat),
            }
        
        return await asyncio.get_event_loop().run_in_executor(_executor, _process)
    
    async def _fast_pose_analysis(self, image_bytes: bytes) -> Dict:
        """Fast pose detection using lightweight model"""
        def _process():
            import mediapipe as mp
            
            mp_pose = mp.solutions.pose
            pose = mp_pose.Pose(
                static_image_mode=True,
                model_complexity=0,  # Fastest
                min_detection_confidence=0.5,
            )
            
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                return None
            
            # Resize for speed
            img = cv2.resize(img, (320, 320))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            results = pose.process(img_rgb)
            
            if not results.pose_landmarks:
                return None
            
            landmarks = results.pose_landmarks.landmark
            
            # Quick measurements
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            
            shoulder_width = abs(left_shoulder.x - right_shoulder.x)
            hip_width = abs(left_hip.x - right_hip.x)
            
            return {
                "shoulder_width": float(shoulder_width),
                "hip_width": float(hip_width),
                "waist_estimate": float(hip_width * 0.75),
                "confidence": float(min(left_shoulder.visibility, right_shoulder.visibility)),
            }
        
        return await asyncio.get_event_loop().run_in_executor(_executor, _process)
    
    async def smart_recommendations(
        self,
        body_shape: str,
        undertone: str,
        gender: str,
        occasion: str = "casual",
        season: str = None,
    ) -> List[Dict]:
        """AI-powered smart recommendations"""
        
        # Trending styles database
        trends = {
            "summer_2024": ["linen suits", "oversized shirts", "wide leg pants", "pastel colors"],
            "winter_2024": ["layered knits", "structured coats", "leather boots", "earth tones"],
            "spring_2024": ["floral prints", "lightweight blazers", "midi skirts", "soft pastels"],
        }
        
        # Body shape specific recommendations
        shape_outfits = {
            "hourglass": ["wrap dresses", "fitted blazers", "high-waisted pants", "belted coats"],
            "pear": ["A-line skirts", "structured shoulders", "dark bottoms", "statement necklaces"],
            "apple": ["empire waist dresses", "V-neck tops", "straight leg pants", "flowy tunics"],
            "rectangle": ["peplum tops", "layered looks", "ruffled details", "belted dresses"],
            "inverted_triangle": ["wide leg pants", "flared skirts", "boat neck tops", "A-line dresses"],
        }
        
        # Color recommendations based on undertone
        color_palettes = {
            "warm": ["coral", "peach", "gold", "olive", "terracotta", "cream"],
            "cool": ["navy", "silver", "rose", "lavender", "mint", "ice blue"],
            "neutral": ["taupe", "gray", "blush", "sage", "mauve", "soft white"],
        }
        
        base_outfits = shape_outfits.get(body_shape, shape_outfits["rectangle"])
        colors = color_palettes.get(undertone, color_palettes["neutral"])
        
        # Generate smart combinations
        recommendations = []
        for i, outfit in enumerate(base_outfits[:5]):
            rec = {
                "id": f"smart_{i}",
                "name": outfit.title(),
                "description": f"Perfect for {body_shape} body type with {undertone} undertone",
                "colors": colors[:4],
                "style_tips": [
                    f"Pair with {colors[0]} accessories",
                    f"Try {colors[1]} for a fresh look",
                    "Add layers for dimension",
                ],
                "confidence_score": 0.85 + (0.03 * i),
                "trending": i < 2,
            }
            recommendations.append(rec)
        
        return recommendations


# Singleton
_fast_ai = None

def get_fast_ai() -> FastAIProcessor:
    global _fast_ai
    if _fast_ai is None:
        _fast_ai = FastAIProcessor()
    return _fast_ai
