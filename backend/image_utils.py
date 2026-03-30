from PIL import Image
import io
from typing import Optional, Tuple
import cv2
import numpy as np


async def compress_image(
    image_bytes: bytes,
    max_size: Tuple[int, int] = (1024, 1024),
    quality: int = 85,
    format: str = "JPEG",
) -> bytes:
    """
    Compress and resize an image.
    
    Args:
        image_bytes: Original image bytes
        max_size: Maximum (width, height)
        quality: JPEG quality (1-100)
        format: Output format
    
    Returns:
        Compressed image bytes
    """
    try:
        # Open image
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Resize if too large
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save to bytes
        output = io.BytesIO()
        img.save(output, format=format, quality=quality, optimize=True)
        output.seek(0)
        
        return output.getvalue()
        
    except Exception as e:
        print(f"Image compression error: {e}")
        return image_bytes


async def compress_for_vton(image_bytes: bytes) -> bytes:
    """Compress image specifically for VTON (512x512)"""
    return await compress_image(
        image_bytes,
        max_size=(512, 512),
        quality=90,
        format="PNG",
    )


async def compress_for_analysis(image_bytes: bytes) -> bytes:
    """Compress image for skin tone/body shape analysis"""
    return await compress_image(
        image_bytes,
        max_size=(640, 640),
        quality=85,
        format="JPEG",
    )


def detect_face(image_bytes: bytes) -> Optional[Tuple[int, int, int, int]]:
    """
    Detect face in image and return bounding box (x, y, w, h).
    Returns None if no face detected.
    """
    try:
        # Load face cascade
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Decode image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return None
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100),
        )
        
        if len(faces) == 0:
            return None
        
        # Return largest face
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        return tuple(largest_face)
        
    except Exception as e:
        print(f"Face detection error: {e}")
        return None


def extract_face_region(image_bytes: bytes, padding: float = 0.3) -> Optional[bytes]:
    """
    Extract face region from image for skin tone analysis.
    Adds padding around the face.
    
    Args:
        image_bytes: Original image
        padding: Padding factor around face (0.3 = 30% extra)
    
    Returns:
        Face region as bytes
    """
    face = detect_face(image_bytes)
    if face is None:
        return None
    
    try:
        x, y, w, h = face
        
        # Decode image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return None
        
        img_h, img_w = img.shape[:2]
        
        # Add padding
        pad_x = int(w * padding)
        pad_y = int(h * padding)
        
        x1 = max(0, x - pad_x)
        y1 = max(0, y - pad_y)
        x2 = min(img_w, x + w + pad_x)
        y2 = min(img_h, y + h + pad_y)
        
        # Extract region
        face_region = img[y1:y2, x1:x2]
        
        # Encode back to bytes
        _, buffer = cv2.imencode('.jpg', face_region)
        return buffer.tobytes()
        
    except Exception as e:
        print(f"Face extraction error: {e}")
        return None


def get_image_info(image_bytes: bytes) -> dict:
    """Get image information"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        return {
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "mode": img.mode,
            "size_bytes": len(image_bytes),
        }
    except Exception as e:
        print(f"Image info error: {e}")
        return {}
