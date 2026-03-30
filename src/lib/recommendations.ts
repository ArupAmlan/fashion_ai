import type { BodyShape, ColourPalette, Gender, OutfitSuggestion, Undertone } from '../types'
import { getBodyShapeName } from './bodyShape'

interface OutfitTemplate {
  id: string
  name: string
  description: string
  bodyShapes: BodyShape[]
  colourTags: Record<Undertone, string[]>
  silhouette: string
}

interface SilhouetteRule {
  bodyShapes: BodyShape[]
  silhouette: string
  description: string
  reasoning: string
}

const SILHOUETTE_RULES_FEMALE: SilhouetteRule[] = [
  {
    bodyShapes: ['hourglass'],
    silhouette: 'Fitted waist, A-line skirts, wrap dresses',
    description: 'Structured waist definition and balanced proportions',
    reasoning: 'Define your natural waist; avoid boxy or oversized shapes that hide your curves.',
  },
  {
    bodyShapes: ['pear'],
    silhouette: 'Structured shoulders, A-line skirts, dark bottoms',
    description: 'Balance hips with shoulder detail and streamlined lower half',
    reasoning: 'Add volume or detail at the shoulders; choose A-line or straight silhouettes for the lower body.',
  },
  {
    bodyShapes: ['inverted_triangle'],
    silhouette: 'V-necks, flared bottoms, wide-leg trousers',
    description: 'Soften shoulders and add volume at hips',
    reasoning: 'Avoid heavy shoulder detail; use V-necks and flared or wide-leg styles to balance your frame.',
  },
  {
    bodyShapes: ['rectangle'],
    silhouette: 'Layered tops, belted looks, peplum, ruffles',
    description: 'Create curves with layers and waist definition',
    reasoning: 'Add dimension with belts, peplum, or layered pieces to create the illusion of a defined waist.',
  },
  {
    bodyShapes: ['apple'],
    silhouette: 'V-necks, empire waist, flowy fabrics, straight legs',
    description: 'Elongate torso and draw eyes to neckline and legs',
    reasoning: 'Empire lines and V-necks lengthen the torso; avoid tight waistbands; choose flowy fabrics.',
  },
]

const SILHOUETTE_RULES_MALE: SilhouetteRule[] = [
  {
    bodyShapes: ['trapezoid'],
    silhouette: 'Fitted tees, structured jackets, straight/athletic fit',
    description: 'Highlight shoulders while keeping lines clean',
    reasoning: 'A tailored fit through the torso enhances your athletic frame; avoid overly boxy cuts.',
  },
  {
    bodyShapes: ['inverted_triangle'],
    silhouette: 'Open collars, minimal shoulder padding, tapered/straight trousers',
    description: 'Balance broad shoulders with clean lower-half volume',
    reasoning: 'Keep tops streamlined; add structure with straight or slightly wider-leg trousers to balance proportions.',
  },
  {
    bodyShapes: ['triangle'],
    silhouette: 'Darker bottoms, structured shoulders, vertical layers',
    description: 'Draw attention upward and streamline the lower half',
    reasoning: 'Use jackets with structure and avoid overly tight bottoms; darker colours below create balance.',
  },
  {
    bodyShapes: ['apple'],
    silhouette: 'V-necks, open overshirts, straight fits, longer layers',
    description: 'Lengthen the torso with vertical lines',
    reasoning: 'Choose comfortable, breathable fabrics with vertical layering; avoid tight waist emphasis.',
  },
  {
    bodyShapes: ['rectangle'],
    silhouette: 'Layering, overshirts, textured knits, tailored outerwear',
    description: 'Add dimension with layers and texture',
    reasoning: 'Use layering and texture to build shape; aim for tailored shoulders and clean waist lines.',
  },
]

/**
 * Outfit templates: each has suggested silhouettes and colour tags.
 * We match by body shape (silhouette) and undertone (colours).
 */
const OUTFIT_TEMPLATES_FEMALE: OutfitTemplate[] = [
  {
    id: 'wrap-dress',
    name: 'Wrap dress',
    description: 'A wrap dress that defines the waist and suits multiple occasions.',
    bodyShapes: ['hourglass', 'pear', 'rectangle'],
    colourTags: {
      warm: ['Camel', 'Rust', 'Olive green', 'Terracotta'],
      cool: ['Navy', 'Plum', 'Dusty rose', 'Slate blue'],
      neutral: ['Dusty rose', 'Sage', 'Navy', 'Taupe'],
    },
    silhouette: 'Fitted waist, V-neck, flattering wrap',
  },
  {
    id: 'structured-blazer',
    name: 'Structured blazer + tailored trousers',
    description: 'Sharp blazer with tailored trousers for a polished look.',
    bodyShapes: ['rectangle', 'pear', 'inverted_triangle'],
    colourTags: {
      warm: ['Camel', 'Warm brown', 'Olive', 'Gold'],
      cool: ['Navy', 'Charcoal', 'Slate blue', 'Plum'],
      neutral: ['Charcoal', 'Navy', 'Taupe', 'Dusty rose'],
    },
    silhouette: 'Structured shoulders, clean lines',
  },
  {
    id: 'a-line-midi',
    name: 'A-line midi skirt + fitted top',
    description: 'A-line skirt that skims the hips with a fitted top.',
    bodyShapes: ['pear', 'hourglass', 'apple'],
    colourTags: {
      warm: ['Cream', 'Terracotta', 'Peach', 'Olive green'],
      cool: ['Cool pink', 'Lavender', 'Mint', 'Ice blue'],
      neutral: ['Blush', 'Sage', 'Mauve', 'Soft white'],
    },
    silhouette: 'A-line skirt, fitted or tucked top',
  },
  {
    id: 'v-neck-flowy',
    name: 'V-neck flowy top + straight-leg trousers',
    description: 'Flowing top with a V-neck and straight-leg trousers.',
    bodyShapes: ['apple', 'inverted_triangle', 'rectangle'],
    colourTags: {
      warm: ['Peach', 'Coral', 'Cream', 'Terracotta'],
      cool: ['Lavender', 'Soft white', 'Plum', 'Mint'],
      neutral: ['Blush', 'Sage', 'Soft white', 'Mauve'],
    },
    silhouette: 'V-neck, flowy fabric, straight legs',
  },
  {
    id: 'empire-waist-dress',
    name: 'Empire waist dress',
    description: 'Dress with a high waistline that elongates the torso.',
    bodyShapes: ['apple', 'rectangle', 'pear'],
    colourTags: {
      warm: ['Peach', 'Gold', 'Camel', 'Rust'],
      cool: ['Lavender', 'Cool pink', 'Navy', 'Plum'],
      neutral: ['Dusty rose', 'Sage', 'Mauve', 'Navy'],
    },
    silhouette: 'Empire waist, flowy skirt',
  },
  {
    id: 'wide-leg-jumpsuit',
    name: 'Wide-leg jumpsuit',
    description: 'One-piece with wide legs and a defined or relaxed waist.',
    bodyShapes: ['inverted_triangle', 'rectangle', 'hourglass'],
    colourTags: {
      warm: ['Terracotta', 'Olive', 'Camel', 'Warm brown'],
      cool: ['Navy', 'Charcoal', 'Plum', 'Teal'],
      neutral: ['Charcoal', 'Navy', 'Taupe', 'Dusty rose'],
    },
    silhouette: 'Wide legs, balanced proportions',
  },
  {
    id: 'peplum-top',
    name: 'Peplum top + slim trousers',
    description: 'Peplum adds waist definition; pair with slim or straight trousers.',
    bodyShapes: ['rectangle', 'pear'],
    colourTags: {
      warm: ['Coral', 'Cream', 'Olive green', 'Gold'],
      cool: ['Cool pink', 'Lavender', 'Navy', 'Mint'],
      neutral: ['Blush', 'Sage', 'Mauve', 'Charcoal'],
    },
    silhouette: 'Peplum waist, slim lower half',
  },
  {
    id: 'layered-outerwear',
    name: 'Layered look with belt',
    description: 'Layered top or dress with a belt to define the waist.',
    bodyShapes: ['rectangle', 'apple', 'hourglass'],
    colourTags: {
      warm: ['Camel', 'Rust', 'Olive', 'Warm brown'],
      cool: ['Navy', 'Charcoal', 'Dusty blue', 'Plum'],
      neutral: ['Taupe', 'Navy', 'Dusty rose', 'Charcoal'],
    },
    silhouette: 'Layers with waist definition',
  },
]

const OUTFIT_TEMPLATES_MALE: OutfitTemplate[] = [
  {
    id: 'tee-overshirt-chinos',
    name: 'T-shirt + overshirt + chinos',
    description: 'Comfortable smart-casual layering with clean lines.',
    bodyShapes: ['rectangle', 'trapezoid', 'apple'],
    colourTags: {
      warm: ['Olive green', 'Camel', 'Cream', 'Warm brown'],
      cool: ['Navy', 'Charcoal', 'Slate blue', 'Soft white'],
      neutral: ['Taupe', 'Navy', 'Charcoal', 'Soft white'],
    },
    silhouette: 'Layered top, straight chinos',
  },
  {
    id: 'oxford-straight-jeans',
    name: 'Oxford shirt + straight-leg jeans',
    description: 'A classic combination that flatters most frames.',
    bodyShapes: ['rectangle', 'triangle', 'apple', 'trapezoid'],
    colourTags: {
      warm: ['Cream', 'Camel', 'Olive green', 'Rust'],
      cool: ['Soft white', 'Navy', 'Ice blue', 'Charcoal'],
      neutral: ['Soft white', 'Navy', 'Taupe', 'Charcoal'],
    },
    silhouette: 'Clean shoulder line, straight legs',
  },
  {
    id: 'polo-tapered-trousers',
    name: 'Polo + tapered trousers',
    description: 'Polished and breathable; great for warm days.',
    bodyShapes: ['trapezoid', 'rectangle', 'triangle'],
    colourTags: {
      warm: ['Olive green', 'Camel', 'Coral', 'Cream'],
      cool: ['Navy', 'Mint', 'Slate blue', 'Cool pink'],
      neutral: ['Sage', 'Navy', 'Mauve', 'Soft white'],
    },
    silhouette: 'Structured collar, tapered leg',
  },
  {
    id: 'crewneck-bomber',
    name: 'Crewneck knit + bomber jacket',
    description: 'Adds structure and dimension without bulk.',
    bodyShapes: ['rectangle', 'apple', 'inverted_triangle'],
    colourTags: {
      warm: ['Camel', 'Warm brown', 'Olive', 'Gold'],
      cool: ['Charcoal', 'Navy', 'Plum', 'Slate blue'],
      neutral: ['Charcoal', 'Taupe', 'Navy', 'Dusty rose'],
    },
    silhouette: 'Structured outerwear, straight fit',
  },
  {
    id: 'open-collar-wide-leg',
    name: 'Open-collar shirt + straight/relaxed trousers',
    description: 'Balances a broader upper body with comfort-first lines.',
    bodyShapes: ['inverted_triangle', 'trapezoid'],
    colourTags: {
      warm: ['Cream', 'Terracotta', 'Olive', 'Camel'],
      cool: ['Soft white', 'Navy', 'Lavender', 'Ice blue'],
      neutral: ['Soft white', 'Taupe', 'Navy', 'Sage'],
    },
    silhouette: 'Open collar, relaxed lower half',
  },
]

function getSilhouetteForShape(shape: BodyShape, gender: Gender): SilhouetteRule | undefined {
  const rules = gender === 'male' ? SILHOUETTE_RULES_MALE : SILHOUETTE_RULES_FEMALE
  return rules.find((r) => r.bodyShapes.includes(shape))
}

function scoreOutfit(
  template: OutfitTemplate,
  bodyShape: BodyShape,
  palette: ColourPalette,
  gender: Gender
): { score: number; bodyMatch: string; colourMatch: string; suggestedColours: string[] } {
  const shapeMatch = template.bodyShapes.includes(bodyShape)
  const silhouetteRule = getSilhouetteForShape(bodyShape, gender)
  const primaryColours = template.colourTags[palette.undertone]
  const colourMatch = primaryColours.length > 0
  const bodyMatch = shapeMatch
    ? `Ideal for ${getBodyShapeName(bodyShape)}: ${silhouetteRule?.reasoning ?? 'Flatters your proportions.'}`
    : `Can work for ${getBodyShapeName(bodyShape)} with the right fit; consider ${silhouetteRule?.silhouette}.`

  let score = 0
  if (shapeMatch) score += 50
  else score += 20
  if (colourMatch) score += 30
  score += Math.min(20, primaryColours.length * 4)
  return {
    score: Math.min(100, score),
    bodyMatch,
    colourMatch: colourMatch
      ? `Colours from your palette: ${primaryColours.slice(0, 4).join(', ')}.`
      : `Try these shades: ${primaryColours.slice(0, 4).join(', ')}.`,
    suggestedColours: primaryColours.slice(0, 5),
  }
}

export function getOutfitRecommendations(
  bodyShape: BodyShape,
  palette: ColourPalette,
  gender: Gender
): OutfitSuggestion[] {
  const toAmazon = (q: string) => `https://www.amazon.in/s?k=${encodeURIComponent(q)}`
  const toFlipkart = (q: string) => `https://www.flipkart.com/search?q=${encodeURIComponent(q)}`
  const templates =
    gender === 'male' ? OUTFIT_TEMPLATES_MALE : gender === 'female' ? OUTFIT_TEMPLATES_FEMALE : [...OUTFIT_TEMPLATES_FEMALE, ...OUTFIT_TEMPLATES_MALE]

  const results: OutfitSuggestion[] = templates.map((t) => {
    const { score, bodyMatch, colourMatch, suggestedColours } = scoreOutfit(t, bodyShape, palette, gender)
    const silhouetteRule = getSilhouetteForShape(bodyShape, gender)
    const query = `${t.name} ${suggestedColours[0] || ''}`.trim()
    return {
      id: t.id,
      name: t.name,
      description: t.description,
      silhouette: t.silhouette,
      colours: suggestedColours,
      compatibilityScore: score,
      reasoning: `${bodyMatch} ${colourMatch}`,
      bodyShapeMatch: silhouetteRule?.reasoning ?? 'Balanced silhouette.',
      colourMatch: `Best in: ${suggestedColours.join(', ')}.`,
      productUrl: toAmazon(query),
      altProductUrl: toFlipkart(query),
    }
  })

  results.sort((a, b) => b.compatibilityScore - a.compatibilityScore)
  return results
}
