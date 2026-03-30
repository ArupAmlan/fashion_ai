from PIL import Image
import io
import numpy as np
import cv2
from typing import Optional
import os

# Global variable for lazy loading
_vton_pipeline = None
_image_gen_pipeline = None


def get_vton_pipeline():
    """Lazy load the VTON pipeline - returns None for fast mode"""
    return None


def get_image_gen_pipeline():
    """Lazy load the image generation pipeline - returns None for fast mode"""
    return None


def create_body_mask(image: np.ndarray) -> np.ndarray:
    """Create a mask for the body area where garment will be applied"""
    h, w = image.shape[:2]
    # Create a simple elliptical mask for the torso area
    mask = np.zeros((h, w), dtype=np.uint8)
    center = (w // 2, h // 2)
    axes = (w // 4, h // 3)
    cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)
    return mask


async def virtual_try_on(
    person_image_bytes: bytes,
    garment_image_bytes: bytes,
    num_inference_steps: int = 25,
    guidance_scale: float = 7.5,
) -> bytes:
    """
    Perform virtual try-on - fast mode returns blended image.
    """
    try:
        # Load images
        person = Image.open(io.BytesIO(person_image_bytes)).convert("RGBA")
        garment = Image.open(io.BytesIO(garment_image_bytes)).convert("RGBA")
        
        # Resize to same size
        size = (384, 384)
        person = person.resize(size, Image.Resampling.LANCZOS)
        garment = garment.resize(size, Image.Resampling.LANCZOS)
        
        # Simple blend
        result = person.copy()
        for y in range(size[1]//2, size[1]):
            for x in range(size[0]//4, 3*size[0]//4):
                px = garment.getpixel((x, y))
                if px[3] > 128:
                    p_px = person.getpixel((x, y))
                    alpha = px[3] / 255.0
                    new_px = tuple(int(p_px[i] * (1-alpha) + px[i] * alpha) for i in range(3))
                    result.putpixel((x, y), new_px + (255,))
        
        result = result.convert("RGB")
        output = io.BytesIO()
        result.save(output, format="JPEG", quality=85)
        return output.getvalue()
        
    except Exception as e:
        print(f"VTON error: {e}")
        return person_image_bytes


async def generate_outfit_image(
    outfit_description: str,
    gender: str = "female",
    style: str = "casual",
    num_inference_steps: int = 20,
) -> Optional[bytes]:
    """
    Generate an outfit image - fast mode creates styled placeholder.
    """
    try:
        from PIL import ImageDraw, ImageFont
        
        size = (512, 512)
        img = Image.new('RGB', size, (245, 245, 245))
        draw = ImageDraw.Draw(img)
        
        # Background gradient
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
        
        text = outfit_description[:30]
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (size[0] - text_width) // 2
        draw.text((x, 200), text, fill=(50, 50, 50), font=font)
        
        style_text = f"{style.title()} | {gender.title()}"
        bbox2 = draw.textbbox((0, 0), style_text, font=small_font)
        style_width = bbox2[2] - bbox2[0]
        x2 = (size[0] - style_width) // 2
        draw.text((x2, 260), style_text, fill=(100, 100, 100), font=small_font)
        
        output = io.BytesIO()
        img.save(output, format="JPEG", quality=90)
        return output.getvalue()
        
    except Exception as e:
        print(f"Image generation error: {e}")
        return None


async def generate_batch_outfit_images(
    outfits: list[dict],
    gender: str = "female",
) -> list[Optional[bytes]]:
    """Generate images for multiple outfits"""
    results = []
    for outfit in outfits:
        image = await generate_outfit_image(
            outfit.get("name", ""),
            gender=gender,
            style=outfit.get("style", "casual"),
        )
        results.append(image)
    return results
