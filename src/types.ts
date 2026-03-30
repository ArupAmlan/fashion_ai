export type BodyShape =
  | 'hourglass'
  | 'pear'
  | 'inverted_triangle'
  | 'rectangle'
  | 'apple'
  // common menswear-focused shape labels
  | 'trapezoid'
  | 'triangle'

export type Undertone = 'warm' | 'cool' | 'neutral'

export type InputMode = 'measurements' | 'image'

export type Gender = 'female' | 'male' | 'non_binary'

export type Occasion = 'casual' | 'formal' | 'party' | 'sport';

export interface Measurements {
  shoulder: number // inches or cm
  waist: number
  hip: number
  unit: 'in' | 'cm'
}

export interface BodyShapeResult {
  shape: BodyShape
  confidence: number
  reasoning: string
}

export interface ColourPalette {
  undertone: Undertone
  primary: string[]
  secondary: string[]
  avoid: string[]
  reasoning: string
}

export interface OutfitSuggestion {
  id: string
  name: string
  description: string
  silhouette: string
  colours: string[]
  compatibilityScore: number
  reasoning: string
  bodyShapeMatch: string
  colourMatch: string
  imageUrl?: string
  productUrl?: string
  altProductUrl?: string
}

export interface AnalysisResult {
  bodyShape: BodyShapeResult
  colourPalette: ColourPalette
  outfits: OutfitSuggestion[]
  inputMode: InputMode
  gender: Gender
  occasion?: Occasion
}
