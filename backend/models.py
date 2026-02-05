from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel


class BodyShape(str, Enum):
    hourglass = "hourglass"
    pear = "pear"
    inverted_triangle = "inverted_triangle"
    rectangle = "rectangle"
    apple = "apple"
    trapezoid = "trapezoid"
    triangle = "triangle"


class Undertone(str, Enum):
    warm = "warm"
    cool = "cool"
    neutral = "neutral"


class Gender(str, Enum):
    female = "female"
    male = "male"
    non_binary = "non_binary"


class InputMode(str, Enum):
    measurements = "measurements"
    image = "image"


class Measurements(BaseModel):
    shoulder: float
    waist: float
    hip: float
    unit: Literal["in", "cm"] = "in"


class BodyShapeResult(BaseModel):
    shape: BodyShape
    confidence: float
    reasoning: str


class ColourPalette(BaseModel):
    undertone: Undertone
    primary: List[str]
    secondary: List[str]
    avoid: List[str]
    reasoning: str


class OutfitSuggestion(BaseModel):
    id: str
    name: str
    description: str
    silhouette: str
    colours: List[str]
    compatibilityScore: float
    reasoning: str
    bodyShapeMatch: str
    colourMatch: str
    imageUrl: Optional[str] = None


class AnalysisResult(BaseModel):
    bodyShape: BodyShapeResult
    colourPalette: ColourPalette
    outfits: List[OutfitSuggestion]
    inputMode: InputMode
    gender: Gender


class AnalyzeRequest(BaseModel):
    gender: Gender
    inputMode: InputMode
    measurements: Optional[Measurements] = None
    undertone: Undertone
    imageBodyShape: Optional[BodyShapeResult] = None

