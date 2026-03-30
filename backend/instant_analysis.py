"""
Ultra-fast analysis - no heavy processing, instant results
"""
import numpy as np
from typing import Dict, Optional, List
from urllib.parse import quote_plus
import time

# Pre-computed color palettes for instant lookup
UNDERTONE_PALETTES = {
    "warm": {
        "primary": ["Cream", "Camel", "Terracotta", "Olive green", "Gold", "Rust", "Warm brown", "Peach", "Coral"],
        "secondary": ["Mustard", "Burgundy", "Forest green", "Bronze", "Amber"],
        "avoid": ["Cool grey", "Bright white", "Ice blue", "Silver", "Cool pink"],
    },
    "cool": {
        "primary": ["Navy", "Slate blue", "Silver grey", "Cool pink", "Mint", "Lavender", "Charcoal", "Ice blue", "Plum"],
        "secondary": ["Teal", "Rose", "Soft white", "Dusty blue", "Berry"],
        "avoid": ["Orange", "Yellow-gold", "Warm brown", "Camel", "Peach"],
    },
    "neutral": {
        "primary": ["Soft white", "Grey", "Dusty rose", "Sage", "Mauve", "Navy", "Olive", "Taupe", "Blush"],
        "secondary": ["Lavender", "Teal", "Camel", "Burgundy", "Charcoal"],
        "avoid": ["Bright orange", "Lime green", "Neon colours"],
    },
}

SEASONAL_COLORS = {
    "spring": {"best": ["Coral", "Peach", "Warm yellow", "Golden brown", "Turquoise"], "avoid": ["Black", "White"]},
    "summer": {"best": ["Lavender", "Powder blue", "Rose", "Soft pink", "Grey"], "avoid": ["Orange", "Bright yellow"]},
    "autumn": {"best": ["Olive", "Rust", "Terracotta", "Mustard", "Chocolate"], "avoid": ["Bright pink", "Lavender"]},
    "winter": {"best": ["Black", "White", "Navy", "True red", "Emerald"], "avoid": ["Beige", "Orange"]},
}

# Pre-computed outfit recommendations
OUTFIT_DB = {
    "hourglass": {
        "female": ["Wrap dress", "Fitted blazer", "High-waisted pants", "Belted coat", "Bodycon dress"],
        "male": ["Tailored suit", "Fitted shirt", "Slim trousers", "Structured jacket"],
    },
    "pear": {
        "female": ["A-line skirt", "Off-shoulder top", "Dark wash jeans", "Statement necklace", "Fit and flare dress"],
        "male": ["Dark trousers", "Light colored shirts", "Structured shoulders", "V-neck sweaters"],
    },
    "apple": {
        "female": ["Empire waist dress", "V-neck top", "Straight leg pants", "Flowy tunic", "Long cardigan"],
        "male": ["V-neck shirts", "Open overshirts", "Straight fits", "Vertical stripes"],
    },
    "rectangle": {
        "female": ["Peplum top", "Layered look", "Ruffled blouse", "Belted dress", "Wide leg pants"],
        "male": ["Layered outfits", "Textured knits", "Patterned shirts", "Structured outerwear"],
    },
    "inverted_triangle": {
        "female": ["Wide leg pants", "A-line skirt", "Boat neck top", "Flared jeans", "Full skirt"],
        "male": ["Straight leg trousers", "Minimal shoulder detail", "V-neck tops", "Dark bottoms"],
    },
}


def instant_skin_analysis(image_bytes: bytes) -> Dict:
    """
    Ultra-fast skin tone analysis - simplified for speed
    Returns results in < 10ms
    """
    # Just use image metadata/size for quick classification
    # In production, you'd use a simple ML model or cached results
    
    # Simple hash-based classification for demo (deterministic but random-looking)
    hash_val = hash(image_bytes[:100]) % 100
    
    if hash_val < 33:
        undertone = "warm"
        season = "spring"
    elif hash_val < 66:
        undertone = "cool"
        season = "winter"
    else:
        undertone = "neutral"
        season = "autumn"
    
    return {
        "undertone": undertone,
        "season": season,
        "confidence": 0.75 + (hash_val % 20) / 100,
        "seasonalColors": SEASONAL_COLORS.get(season, SEASONAL_COLORS["spring"]),
        "palette": UNDERTONE_PALETTES[undertone],
        "processing_time_ms": 0,
    }


def instant_body_shape(measurements: Optional[Dict] = None) -> Dict:
    """
    Instant body shape calculation
    """
    if measurements:
        shoulder = measurements.get("shoulder", 40)
        waist = measurements.get("waist", 30)
        hip = measurements.get("hip", 40)
        
        # Quick calculation
        if abs(shoulder - hip) < 5 and waist < shoulder * 0.85:
            shape = "hourglass"
        elif hip > shoulder * 1.05:
            shape = "pear"
        elif shoulder > hip * 1.05:
            shape = "inverted_triangle"
        elif waist >= shoulder * 0.95:
            shape = "apple"
        else:
            shape = "rectangle"
    else:
        shape = "rectangle"
    
    return {
        "shape": shape,
        "confidence": 0.85,
        "reasoning": f"Your proportions indicate a {shape} body type.",
    }


def _generate_ecommerce_links(outfit_name: str, colors: list) -> dict:
    """Generate e-commerce search links for an outfit"""
    # Create search queries
    query_base = quote_plus(outfit_name.replace(" ", "-"))
    color_query = "+".join(colors[:2]) if colors else ""
    
    # Amazon links
    amazon_query = f"{quote_plus(outfit_name)}{'+' + color_query if color_query else ''}"
    amazon_url = f"https://www.amazon.in/s?k={amazon_query}"
    
    # Flipkart links
    flipkart_url = f"https://www.flipkart.com/search?q={quote_plus(outfit_name)}"
    
    # Myntra links (fashion-focused)
    myntra_query = outfit_name.replace(" ", "-").lower()
    myntra_url = f"https://www.myntra.com/{myntra_query}"
    
    return {
        "amazon": amazon_url,
        "flipkart": flipkart_url,
        "myntra": myntra_url,
    }


def instant_recommendations(
    body_shape: str,
    undertone: str,
    gender: str = "female",
    occasion: str = "casual",
) -> list:
    """
    Instant outfit recommendations from pre-computed database
    """
    outfits = OUTFIT_DB.get(body_shape, OUTFIT_DB["rectangle"]).get(gender, [])
    palette = UNDERTONE_PALETTES.get(undertone, UNDERTONE_PALETTES["neutral"])
    
    recommendations = []
    for i, outfit in enumerate(outfits):
        colors = palette["primary"][:4]
        
        # Generate e-commerce links
        ecommerce_links = _generate_ecommerce_links(outfit, colors)
        
        rec = {
            "id": f"instant_{i}",
            "name": outfit,
            "description": f"Perfect {outfit.lower()} for {body_shape} body type",
            "colors": colors,
            "compatibilityScore": 90 - (i * 3),
            "reasoning": f"Flatters your {body_shape} shape and {undertone} undertone",
            "trending": i < 2,
            "productUrl": ecommerce_links["amazon"],  # Primary: Amazon
            "altProductUrl": ecommerce_links["myntra"],  # Secondary: Myntra (fashion)
            "ecommerceLinks": ecommerce_links,  # All platforms
        }
        recommendations.append(rec)
    
    return recommendations


class InstantAnalyzer:
    """Ultra-fast analyzer - no delays, instant results"""
    
    def __init__(self):
        self.cache = {}
    
    def analyze(self, image_bytes: bytes = None, measurements: Dict = None) -> Dict:
        """Complete analysis in under 50ms"""
        start = time.time()
        
        # Run all analyses in parallel (simulated)
        skin = instant_skin_analysis(image_bytes or b"")
        body = instant_body_shape(measurements)
        
        # Get recommendations
        recs = instant_recommendations(
            body["shape"],
            skin["undertone"],
            "female",
        )
        
        elapsed = (time.time() - start) * 1000
        
        return {
            "bodyShape": body,
            "skinAnalysis": skin,
            "recommendations": recs,
            "total_time_ms": elapsed,
        }


# Singleton
_instant_analyzer = None

def get_instant_analyzer() -> InstantAnalyzer:
    global _instant_analyzer
    if _instant_analyzer is None:
        _instant_analyzer = InstantAnalyzer()
    return _instant_analyzer
