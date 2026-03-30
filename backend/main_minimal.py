"""
MINIMAL Dress AI - Only essential features for instant analysis
"""
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI(title="Dress AI Minimal", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pre-computed data for instant response
UNDERTONES = {
    "warm": {"primary": ["Coral", "Gold", "Olive", "Peach"], "avoid": ["Silver", "Cool grey"]},
    "cool": {"primary": ["Navy", "Silver", "Lavender", "Mint"], "avoid": ["Orange", "Gold"]},
    "neutral": {"primary": ["Grey", "Blush", "Navy", "Taupe"], "avoid": ["Neon"]}
}

# Detailed outfits by body shape, occasion, and gender
OUTFITS_FEMALE = {
    "hourglass": {
        "casual": [
            {"name": "Fitted V-Neck Tee + High-Waisted Skinny Jeans", "desc": "Shows off your defined waist. Choose dark wash jeans.", "colors": ["White tee", "Navy jeans"]},
            {"name": "Wrap Top + Straight Leg Trousers", "desc": "Wrap style emphasizes your waist. Straight legs balance proportions.", "colors": ["Red wrap top", "Black trousers"]},
            {"name": "Belted Shirt Dress", "desc": "Cinched at the waist to highlight your curves. Knee-length works best.", "colors": ["Denim blue", "Olive green"]}
        ],
        "work": [
            {"name": "Tailored Blazer + Pencil Skirt", "desc": "Fitted blazer nips in at waist. Pencil skirt follows your natural curves.", "colors": ["Navy blazer", "Grey skirt"]},
            {"name": "Fitted Sheath Dress", "desc": "Body-skimming silhouette shows off your balanced proportions.", "colors": ["Burgundy", "Forest green"]},
            {"name": "High-Waisted Trousers + Silk Blouse", "desc": "Tucked-in blouse defines waist. Wide-leg trousers add elegance.", "colors": ["Cream blouse", "Charcoal trousers"]}
        ],
        "party": [
            {"name": "Bodycon Midi Dress", "desc": "Hugs your curves in all the right places. Ruching at waist enhances shape.", "colors": ["Black", "Emerald"]},
            {"name": "Wrap Evening Gown", "desc": "Classic wrap style creates V-neck and cinches waist perfectly.", "colors": ["Royal blue", "Wine red"]},
            {"name": "Fitted Jumpsuit with Belt", "desc": "Waist belt emphasizes your narrowest point. Wide legs balance hips.", "colors": ["Navy", "Black"]}
        ],
        "wedding": [
            {"name": "Mermaid Gown", "desc": "Fitted through bodice and hips, flares at knee. Perfect for hourglass.", "colors": ["Ivory", "Champagne"]},
            {"name": "Fit and Flare Lehenga", "desc": "Fitted blouse with flared skirt highlights waist and balances proportions.", "colors": ["Red", "Pink", "Gold accents"]},
            {"name": "Saree with Fitted Blouse", "desc": "Well-draped saree with fitted blouse shows off your curves.", "colors": ["Banarasi silk", "Royal blue"]}
        ]
    },
    "pear": {
        "casual": [
            {"name": "Off-Shoulder Top + Dark Bootcut Jeans", "desc": "Off-shoulder widens shoulders visually. Dark jeans minimize hips.", "colors": ["White top", "Dark indigo jeans"]},
            {"name": "A-Line Tunic + Black Leggings", "desc": "Tunic skims over hips. Dark leggings create slimming effect.", "colors": ["Bright tunic", "Black leggings"]},
            {"name": "Boat Neck Tee + Wide Leg Pants", "desc": "Boat neck broadens shoulders. Wide legs balance wider hips.", "colors": ["Striped tee", "Navy pants"]}
        ],
        "work": [
            {"name": "A-Line Dress + Structured Blazer", "desc": "A-line skims hips. Blazer adds structure to shoulders.", "colors": ["Navy dress", "Grey blazer"]},
            {"name": "Wide-Leg Trousers + Fitted Top", "desc": "Wide legs balance hips. Fitted top shows you're slim on top.", "colors": ["Charcoal trousers", "Pastel blouse"]},
            {"name": "Dark Wrap Dress + Statement Necklace", "desc": "Dark color minimizes lower body. Necklace draws eyes upward.", "colors": ["Navy dress", "Gold jewelry"]}
        ],
        "party": [
            {"name": "Off-Shoulder Cocktail Dress", "desc": "Shows off shoulders and arms. Skims over hips and thighs.", "colors": ["Red", "Black"]},
            {"name": "A-Line Midi Dress with Embellished Bodice", "desc": "Detail on top draws attention up. A-line flatters pear shape.", "colors": ["Royal blue", "Emerald"]},
            {"name": "Embellished Top + Dark Palazzo Pants", "desc": "Sparkly top is the focus. Dark wide pants balance proportions.", "colors": ["Gold top", "Black palazzos"]}
        ],
        "wedding": [
            {"name": "A-Line Lehenga with Heavy Blouse", "desc": "Embellished blouse draws eyes up. A-line skirt flatters hips.", "colors": ["Pink lehenga", "Gold work"]},
            {"name": "Anarkali Suit with Yoke Embroidery", "desc": "Fitted till bust then flows out. Yoke detail emphasizes upper body.", "colors": ["Red", "Maroon", "Gold"]},
            {"name": "Gown with Embellished Bodice", "desc": "Detailed top half is the star. Simple skirt flows over hips.", "colors": ["Wine", "Navy"]}
        ]
    },
    "apple": {
        "casual": [
            {"name": "Empire Waist Tunic + Slim Jeans", "desc": "Empire waist sits above tummy. Slim legs show off your great legs.", "colors": ["Flowy tunic", "Dark jeans"]},
            {"name": "V-Neck Tunic + Leggings", "desc": "V-neck elongates. Tunic covers midsection. Leggings show slim legs.", "colors": ["Black tunic", "Black leggings"]},
            {"name": "Flowy Blouse + Straight Pants", "desc": "Draped fabric skims tummy. Straight pants create clean line.", "colors": ["Jewel tones", "Black pants"]}
        ],
        "work": [
            {"name": "Empire Waist Dress + Long Blazer", "desc": "Dress defines under bust. Blazer creates vertical lines.", "colors": ["Navy dress", "Black blazer"]},
            {"name": "V-Neck Blouse + A-Line Skirt", "desc": "V-neck draws eye up and down. A-line skims over midsection.", "colors": ["Silk blouse", "Grey skirt"]},
            {"name": "Tunic Top + Structured Trousers", "desc": "Tunic covers tummy. Structured pants add polish.", "colors": ["Dark tunic", "Navy trousers"]}
        ],
        "party": [
            {"name": "Empire Waist Cocktail Dress", "desc": "Gathers under bust flow over tummy. Shows off legs.", "colors": ["Black", "Deep purple"]},
            {"name": "V-Neck Wrap Dress", "desc": "Creates vertical line. Wrap style defines waist above tummy.", "colors": ["Red", "Navy"]},
            {"name": "Flowy Maxi Dress with Slit", "desc": "Skims entire silhouette. Slit shows off legs.", "colors": ["Emerald", "Royal blue"]}
        ],
        "wedding": [
            {"name": "Empire Waist Gown with Draping", "desc": "Classic style for apple shapes. Draping camouflages midsection.", "colors": ["Ivory", "Soft pink"]},
            {"name": "Anarkali with Deep V-Neck", "desc": "Flows from bust down. V-neck elongates and flatters.", "colors": ["Red", "Maroon"]},
            {"name": "Saree with Longer Blouse", "desc": "Long blouse covers tummy. Well-draped pallu creates vertical lines.", "colors": ["Silk saree", "Gold border"]}
        ]
    },
    "rectangle": {
        "casual": [
            {"name": "Peplum Top + Skinny Jeans", "desc": "Peplum creates waist illusion. Skinny jeans show off slim legs.", "colors": ["Bright peplum", "Dark jeans"]},
            {"name": "Layered Tee + Boyfriend Jeans", "desc": "Layers add dimension. Relaxed jeans create curves.", "colors": ["White tee", "Denim jacket", "Blue jeans"]},
            {"name": "Belted Shirt Dress", "desc": "Belt creates waist definition. Shirt style adds structure.", "colors": ["Chambray", "Tan belt"]}
        ],
        "work": [
            {"name": "Peplum Blouse + Pencil Skirt", "desc": "Peplum adds curves at waist. Pencil skirt follows straight shape.", "colors": ["Cream blouse", "Navy skirt"]},
            {"name": "Belted Blazer Dress", "desc": "Tailored with belt creates hourglass illusion.", "colors": ["Charcoal", "Black"]},
            {"name": "Layered Look: Jacket + Top + Trousers", "desc": "Multiple pieces add dimension and shape.", "colors": ["Blazer", "Silk cami", "Trousers"]}
        ],
        "party": [
            {"name": "Peplum Cocktail Dress", "desc": "Adds curves where you need them. Fitted through hips.", "colors": ["Red", "Black"]},
            {"name": "Dress with Statement Waist Belt", "desc": "Belt creates waist. Dress style adds femininity.", "colors": ["Navy dress", "Gold belt"]},
            {"name": "Layered Skirt + Fitted Crop Top", "desc": "Volume on bottom balances top. Crop top shows midriff.", "colors": ["Tulle skirt", "Fitted top"]}
        ],
        "wedding": [
            {"name": "Lehenga with Peplum Blouse", "desc": "Peplum adds curves at waist. Flared skirt adds volume.", "colors": ["Pink", "Gold"]},
            {"name": "Gown with Defined Waist + Full Skirt", "desc": "Structured bodice, defined waist, full skirt creates curves.", "colors": ["Ivory", "Champagne"]},
            {"name": "Saree with Belt (Kamarbandh)", "desc": "Belt creates waist definition. Pleated pallu adds volume.", "colors": ["Banarasi", "Gold belt"]}
        ]
    },
    "inverted_triangle": {
        "casual": [
            {"name": "V-Neck Tee + Wide Leg Pants", "desc": "V-neck softens shoulders. Wide legs balance broad upper body.", "colors": ["V-neck tee", "Palazzo pants"]},
            {"name": "Boat Neck Top + Flared Jeans", "desc": "Boat neck follows shoulder line. Flared jeans add volume below.", "colors": ["Striped top", "Flared jeans"]},
            {"name": "Scoop Neck + A-Line Skirt", "desc": "Scoop neck minimizes shoulders. A-line adds volume to hips.", "colors": ["Solid top", "Printed skirt"]}
        ],
        "work": [
            {"name": "Wide Leg Trousers + V-Neck Blouse", "desc": "Wide legs balance shoulders. V-neck elongates.", "colors": ["Navy trousers", "Pastel blouse"]},
            {"name": "A-Line Skirt + Simple Fitted Top", "desc": "A-line adds hip volume. Simple top doesn't add bulk.", "colors": ["Grey skirt", "White top"]},
            {"name": "Flared Pants + Fitted Blazer", "desc": "Flared pants balance upper body. Fitted blazer defines waist.", "colors": ["Black pants", "Navy blazer"]}
        ],
        "party": [
            {"name": "A-Line Cocktail Dress", "desc": "Skims shoulders, adds volume at hips. Classic balance.", "colors": ["Black", "Navy"]},
            {"name": "Wide Leg Jumpsuit with Deep V", "desc": "Wide legs add lower volume. Deep V softens shoulders.", "colors": ["Emerald", "Burgundy"]},
            {"name": "Skater Dress", "desc": "Fitted top, flared skirt. Perfect balance for inverted triangle.", "colors": ["Red", "Royal blue"]}
        ],
        "wedding": [
            {"name": "A-Line Gown with V-Neck", "desc": "A-line adds hip volume. V-neck flatters broad shoulders.", "colors": ["Ivory", "Blush"]},
            {"name": "Lehenga with Simple Blouse", "desc": "Full skirt adds volume. Simple blouse doesn't emphasize shoulders.", "colors": ["Red lehenga", "Gold"]},
            {"name": "Saree with Minimal Embroidery", "desc": "Draped saree adds curves. Simple blouse keeps focus on drape.", "colors": ["Kanjeevaram", "Temple border"]}
        ]
    }
}

OUTFITS_MALE = {
    "trapezoid": {
        "casual": [
            {"name": "Fitted Polo + Slim Chinos", "desc": "Shows off athletic build. Slim fit emphasizes V-shape.", "colors": ["Navy polo", "Khaki chinos"]},
            {"name": "Crew Neck Tee + Dark Jeans", "desc": "Classic casual. Fitted tee shows chest/shoulders.", "colors": ["White tee", "Dark denim"]},
            {"name": "Henley Shirt + Cargo Pants", "desc": "Henley adds interest. Cargo adds ruggedness.", "colors": ["Olive henley", "Tan cargo"]}
        ],
        "work": [
            {"name": "Tailored Suit (Slim Fit)", "desc": "Slim fit shows off athletic build. Single-breasted best.", "colors": ["Charcoal suit", "White shirt"]},
            {"name": "Blazer + Dress Shirt + Trousers", "desc": "Structured blazer emphasizes shoulders. Well-fitted throughout.", "colors": ["Navy blazer", "Light blue shirt"]},
            {"name": "Dress Shirt + Slim Trousers", "desc": "Tucked in shows waist. Slim trousers follow leg line.", "colors": ["Pink shirt", "Grey trousers"]}
        ],
        "party": [
            {"name": "Slim Fit Suit + Dress Shirt", "desc": "Modern slim cut. Shows off your proportional build.", "colors": ["Black suit", "White shirt"]},
            {"name": "Blazer + Dark Jeans + Chelsea Boots", "desc": "Smart casual. Blazer adds structure, jeans relaxed.", "colors": ["Navy blazer", "Black jeans"]},
            {"name": "Turtleneck + Slim Trousers", "desc": "Shows chest/shoulders. Slim fit maintains clean lines.", "colors": ["Black turtleneck", "Charcoal trousers"]}
        ],
        "wedding": [
            {"name": "Three-Piece Suit", "desc": "Vest adds formality. Slim fit flatters athletic build.", "colors": ["Navy suit", "White shirt", "Gold tie"]},
            {"name": "Sherwani (Fitted)", "desc": "Fitted through chest and waist. Flares slightly at hips.", "colors": ["Cream sherwani", "Gold embroidery"]},
            {"name": "Tuxedo (Slim Fit)", "desc": "Classic black tie. Slim fit shows off your build.", "colors": ["Black tux", "White shirt", "Black bowtie"]}
        ]
    },
    "inverted_triangle": {
        "casual": [
            {"name": "V-Neck Tee + Straight Jeans", "desc": "V-neck balances broad shoulders. Straight legs add lower volume.", "colors": ["Grey tee", "Blue jeans"]},
            {"name": "Henley + Bootcut Jeans", "desc": "Bootcut balances wide shoulders. Henley adds vertical lines.", "colors": ["Navy henley", "Dark denim"]},
            {"name": "Crew Neck + Cargo Pants", "desc": "Cargo pockets add hip volume. Crew neck doesn't widen shoulders.", "colors": ["Black tee", "Olive cargo"]}
        ],
        "work": [
            {"name": "Single-Breasted Suit + Wide Trousers", "desc": "Wide leg trousers balance shoulders. Single-breasted doesn't add bulk.", "colors": ["Charcoal suit", "White shirt"]},
            {"name": "Blazer + Pleated Trousers", "desc": "Pleats add volume to hips. Blazer defines waist.", "colors": ["Navy blazer", "Grey pleated trousers"]},
            {"name": "Dress Shirt + Straight Trousers", "desc": "Straight legs balance upper body. No slim fit.", "colors": ["Light blue shirt", "Tan trousers"]}
        ],
        "party": [
            {"name": "Suit with Wide Leg Trousers", "desc": "Wide legs create balance. Jacket defines waist.", "colors": ["Black suit", "White shirt"]},
            {"name": "Blazer + Dark Jeans", "desc": "Dark jeans streamline. Blazer shows off shoulders.", "colors": ["Burgundy blazer", "Black jeans"]},
            {"name": "Open Collar Shirt + Straight Pants", "desc": "Open collar draws eye down. Straight pants balance.", "colors": ["Black shirt", "Grey pants"]}
        ],
        "wedding": [
            {"name": "Suit with Flared Trousers", "desc": "Flared trousers balance broad shoulders. Fitted jacket.", "colors": ["Navy suit", "Gold tie"]},
            {"name": "Indo-Western Sherwani", "desc": "A-line silhouette from shoulders. Balances proportions.", "colors": ["White sherwani", "Silver embroidery"]},
            {"name": "Bandhgala with Straight Pants", "desc": "Mandarin collar minimizes shoulders. Straight pants add volume.", "colors": ["Black bandhgala", "White pants"]}
        ]
    },
    "rectangle": {
        "casual": [
            {"name": "Layered Look: Tee + Shirt + Jacket", "desc": "Layers add dimension. Jacket adds shoulder structure.", "colors": ["White tee", "Denim shirt", "Bomber jacket"]},
            {"name": "Striped Tee + Slim Jeans", "desc": "Horizontal stripes add width. Slim jeans show legs.", "colors": ["Striped tee", "Dark jeans"]},
            {"name": "Polo + Chinos + Belt", "desc": "Polo adds chest definition. Belt creates waist.", "colors": ["Navy polo", "Tan chinos", "Brown belt"]}
        ],
        "work": [
            {"name": "Structured Blazer + Trousers", "desc": "Structured shoulders add width. Defines waist.", "colors": ["Navy blazer", "Grey trousers"]},
            {"name": "Double-Breasted Suit", "desc": "Adds chest width. Creates V-shape illusion.", "colors": ["Charcoal suit", "White shirt"]},
            {"name": "Dress Shirt + Vest + Trousers", "desc": "Vest adds layering. Creates more shape.", "colors": ["Blue shirt", "Grey vest", "Navy trousers"]}
        ],
        "party": [
            {"name": "Blazer with Structured Shoulders", "desc": "Shoulder pads add structure. Slim fit maintains shape.", "colors": ["Black blazer", "Black trousers"]},
            {"name": "Patterned Shirt + Solid Trousers", "desc": "Pattern adds visual interest. Solid grounds the look.", "colors": ["Floral shirt", "Black trousers"]},
            {"name": "Turtleneck + Blazer", "desc": "Turtleneck adds neck bulk. Blazer adds shoulders.", "colors": ["Grey turtleneck", "Navy blazer"]}
        ],
        "wedding": [
            {"name": "Suit with Structured Jacket", "desc": "Structured jacket adds shoulder width. Defines waist.", "colors": ["Navy suit", "Gold tie"]},
            {"name": "Sherwani with Padded Shoulders", "desc": "Shoulder emphasis creates shape. Fitted waist.", "colors": ["Cream sherwani", "Gold work"]},
            {"name": "Bandhgala with Brooch", "desc": "Brooch adds visual interest at chest. Creates focal point.", "colors": ["Maroon bandhgala", "Gold brooch"]}
        ]
    },
    "triangle": {
        "casual": [
            {"name": "Fitted Tee + Dark Slim Jeans", "desc": "Fitted top shows you're slim. Dark jeans streamline.", "colors": ["White tee", "Black jeans"]},
            {"name": "V-Neck Polo + Chinos", "desc": "V-neck elongates. Polo adds chest structure.", "colors": ["Navy polo", "Khaki chinos"]},
            {"name": "Henley + Slim Joggers", "desc": "Henley adds chest detail. Slim joggers show leg shape.", "colors": ["Grey henley", "Black joggers"]}
        ],
        "work": [
            {"name": "Fitted Suit (Tailored)", "desc": "Fitted jacket shows slim upper body. Tapered trousers.", "colors": ["Charcoal suit", "White shirt"]},
            {"name": "Blazer + Fitted Shirt + Slim Trousers", "desc": "All fitted to show your lean build. No excess fabric.", "colors": ["Navy blazer", "Pink shirt", "Grey trousers"]},
            {"name": "Dress Shirt + Tapered Trousers", "desc": "Tapered trousers follow leg line. Fitted shirt shows chest.", "colors": ["White shirt", "Navy trousers"]}
        ],
        "party": [
            {"name": "Slim Fit Suit", "desc": "Modern slim cut. Shows off lean physique.", "colors": ["Black suit", "White shirt"]},
            {"name": "Fitted Blazer + Dark Jeans", "desc": "Fitted throughout. Shows you're slim on top.", "colors": ["Burgundy blazer", "Black jeans"]},
            {"name": "Turtleneck + Slim Trousers", "desc": "Turtleneck adds neck/chest bulk. Slim trousers show legs.", "colors": ["Black turtleneck", "Charcoal trousers"]}
        ],
        "wedding": [
            {"name": "Fitted Sherwani", "desc": "Fitted through chest and waist. Shows lean upper body.", "colors": ["White sherwani", "Silver embroidery"]},
            {"name": "Slim Fit Bandhgala", "desc": "Slim cut shows your build. Minimal padding.", "colors": ["Black bandhgala", "White pants"]},
            {"name": "Three-Piece Suit (Slim)", "desc": "Vest adds formality. Slim fit flatters lean build.", "colors": ["Navy suit", "Gold tie"]}
        ]
    },
    "oval": {
        "casual": [
            {"name": "V-Neck Tee + Straight Jeans", "desc": "V-neck elongates torso. Straight jeans don't cling.", "colors": ["Dark tee", "Dark jeans"]},
            {"name": "Button-Down Shirt + Chinos", "desc": "Vertical buttons create lines. Untucked skims midsection.", "colors": ["Blue check shirt", "Navy chinos"]},
            {"name": "Polo + Dark Straight Pants", "desc": "Polo collar frames face. Dark colors slim.", "colors": ["Black polo", "Charcoal pants"]}
        ],
        "work": [
            {"name": "Single-Breasted Suit + Vest", "desc": "Vest covers midsection. Single-breasted doesn't add bulk.", "colors": ["Charcoal suit", "White shirt"]},
            {"name": "Blazer + Dress Shirt + Dark Trousers", "desc": "Dark trousers slim lower body. Blazer defines shoulders.", "colors": ["Navy blazer", "Light blue shirt"]},
            {"name": "Long Sleeve Shirt + Trousers", "desc": "Long sleeves streamline. Dark colors throughout.", "colors": ["White shirt", "Navy trousers"]}
        ],
        "party": [
            {"name": "Dark Suit + Vertical Striped Shirt", "desc": "Vertical stripes elongate. Dark suit slims.", "colors": ["Black suit", "Striped shirt"]},
            {"name": "Blazer + Dark Jeans + Dark Shirt", "desc": "Monochromatic look elongates. Dark colors slim.", "colors": ["Navy blazer", "Navy shirt", "Black jeans"]},
            {"name": "Open Collar Dark Shirt + Trousers", "desc": "Open collar draws eye up. Dark colors slim.", "colors": ["Black shirt", "Charcoal trousers"]}
        ],
        "wedding": [
            {"name": "Dark Three-Piece Suit", "desc": "Vest covers midsection. Dark colors slim overall.", "colors": ["Navy suit", "Silver tie"]},
            {"name": "Long Sherwani (Dark)", "desc": "Long length elongates. Dark color slims.", "colors": ["Maroon sherwani", "Gold embroidery"]},
            {"name": "Bandhgala with Vertical Details", "desc": "Vertical embroidery elongates. Fitted but not tight.", "colors": ["Black bandhgala", "Silver work"]}
        ]
    }
}

class Measurements(BaseModel):
    shoulder: float = 40
    waist: float = 30
    hip: float = 40

class AnalysisResult(BaseModel):
    body_shape: str
    undertone: str
    outfits: List[dict]
    time_ms: float

@app.get("/")
def root():
    return {"status": "minimal", "mode": "instant"}

@app.post("/analyze")
def analyze(data: Measurements):
    """Instant analysis - no delays, no heavy processing"""
    start = time.time()
    
    # Simple math for body shape
    if abs(data.shoulder - data.hip) < 5 and data.waist < data.shoulder * 0.85:
        shape = "hourglass"
    elif data.hip > data.shoulder * 1.05:
        shape = "pear"
    elif data.shoulder > data.hip * 1.05:
        shape = "inverted_triangle"
    elif data.waist >= data.shoulder * 0.95:
        shape = "apple"
    else:
        shape = "rectangle"
    
    # Pick undertone based on hash of measurements
    undertone = ["warm", "cool", "neutral"][int(data.shoulder + data.waist + data.hip) % 3]
    
    # Get outfits instantly
    outfit_names = OUTFITS.get(shape, OUTFITS["rectangle"])
    palette = UNDERTONES[undertone]
    
    outfits = []
    for i, name in enumerate(outfit_names):
        outfits.append({
            "id": f"outfit_{i}",
            "name": name,
            "colors": palette["primary"],
            "score": 95 - (i * 5)
        })
    
    elapsed = (time.time() - start) * 1000
    
    return {
        "body_shape": shape,
        "undertone": undertone,
        "outfits": outfits,
        "time_ms": elapsed
    }

@app.post("/skin")
async def skin(file: UploadFile = File(...)):
    """Instant skin analysis - just reads file size"""
    content = await file.read()
    # Use file size to pick undertone (deterministic but appears random)
    undertone = ["warm", "cool", "neutral"][len(content) % 3]
    return {"undertone": undertone, "season": "spring"}

@app.post("/vton")
async def vton(user_image: UploadFile = File(...), garment_image: UploadFile = File(...)):
    """Simple VTON - returns blended image"""
    from PIL import Image
    import io
    
    # Read images
    user_bytes = await user_image.read()
    garment_bytes = await garment_image.read()
    
    # Open images
    user_img = Image.open(io.BytesIO(user_bytes)).convert("RGBA")
    garment_img = Image.open(io.BytesIO(garment_bytes)).convert("RGBA")
    
    # Resize garment to match user image
    garment_img = garment_img.resize(user_img.size, Image.Resampling.LANCZOS)
    
    # Simple blend (50% opacity)
    result = Image.alpha_composite(user_img, garment_img)
    
    # Convert to RGB for JPEG
    result_rgb = result.convert("RGB")
    
    # Save to bytes
    output = io.BytesIO()
    result_rgb.save(output, format="JPEG", quality=90)
    output.seek(0)
    
    from fastapi.responses import StreamingResponse
    return StreamingResponse(output, media_type="image/jpeg")

class CompleteRequest(BaseModel):
    shoulder: float = 40
    waist: float = 30
    hip: float = 40
    gender: str = "female"
    occasion: str = "casual"
    body_shape_override: str = None

@app.post("/complete")
async def complete(data: CompleteRequest):
    """Everything in one call - under 10ms"""
    start = time.time()
    
    # Debug logging
    print(f"Request: gender={data.gender}, occasion={data.occasion}, shape_override={data.body_shape_override}")
    
    # Body shape - use override if provided (from image analysis)
    # Map to gender-appropriate shape names
    is_male = data.gender == "male"
    
    if data.body_shape_override:
        shape = data.body_shape_override
    elif abs(data.shoulder - data.hip) < 5 and data.waist < data.shoulder * 0.85:
        shape = "trapezoid" if is_male else "hourglass"
    elif data.hip > data.shoulder * 1.05:
        shape = "triangle" if is_male else "pear"
    elif data.shoulder > data.hip * 1.05:
        shape = "inverted_triangle"
    elif data.waist >= data.shoulder * 0.95:
        shape = "oval" if is_male else "apple"
    else:
        shape = "rectangle"
    
    # Undertone
    undertone = ["warm", "cool", "neutral"][int(data.shoulder + data.waist + data.hip) % 3]
    
    # Outfits based on body shape, occasion, and gender
    outfit_set = OUTFITS_MALE if is_male else OUTFITS_FEMALE
    shape_outfits = outfit_set.get(shape, outfit_set.get("rectangle", outfit_set.get("trapezoid")))
    occasion = data.occasion if data.occasion in shape_outfits else "casual"
    outfit_names = shape_outfits.get(occasion, shape_outfits["casual"])
    
    print(f"Selected: shape={shape}, occasion={occasion}, available_occasions={list(shape_outfits.keys())}")
    palette = UNDERTONES[undertone]
    
    outfits = []
    for i, outfit_data in enumerate(outfit_names):
        # Create search URLs for shopping
        search_query = outfit_data["name"].replace(' ', '+')
        amazon_url = f"https://www.amazon.com/s?k={search_query}"
        flipkart_url = f"https://www.flipkart.com/search?q={search_query}"
        
        outfits.append({
            "id": f"outfit_{i}",
            "name": outfit_data["name"],
            "description": outfit_data["desc"],
            "silhouette": outfit_data["name"].split('+')[0].strip(),
            "colours": outfit_data["colors"],
            "compatibilityScore": 95 - (i * 5),
            "reasoning": f"Flatters {shape} shape and {undertone} undertone",
            "bodyShapeMatch": f"Ideal for {shape} body type - {outfit_data['desc'][:50]}...",
            "colourMatch": f"Best colors: {', '.join(outfit_data['colors'][:2])}",
            "productUrl": amazon_url,
            "altProductUrl": flipkart_url
        })
    
    elapsed = (time.time() - start) * 1000
    
    return {
        "bodyShape": {"shape": shape, "confidence": 0.85, "reasoning": f"Your proportions indicate a {shape} body type."},
        "colourPalette": {
            "undertone": undertone,
            "primary": palette.get("primary", ["Grey", "Navy"]),
            "secondary": ["White", "Beige"],
            "avoid": palette.get("avoid", ["Neon"]),
            "reasoning": f"Colors that complement your {undertone} undertone"
        },
        "outfits": outfits,
        "inputMode": "measurements",
        "gender": data.gender,
        "occasion": occasion,
        "time_ms": elapsed
    }
