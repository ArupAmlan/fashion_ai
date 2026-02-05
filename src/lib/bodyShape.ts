import type { BodyShape, BodyShapeResult, Gender, Measurements } from '../types'

const SHAPE_NAMES: Record<BodyShape, string> = {
  hourglass: 'Hourglass',
  pear: 'Pear',
  inverted_triangle: 'Inverted Triangle',
  rectangle: 'Rectangle',
  apple: 'Apple',
  trapezoid: 'Trapezoid',
  triangle: 'Triangle',
}

function withinPercent(a: number, b: number, pct: number): boolean {
  if (b === 0) return true
  const diff = Math.abs(a - b) / b
  return diff <= pct / 100
}

function waistSmallerThan(waist: number, other: number, minPct: number): boolean {
  if (other === 0) return false
  return waist <= other * (1 - minPct / 100)
}

/**
 * Determines body shape from shoulder, waist, and hip measurements.
 * Uses standard fashion rules: hourglass (waist 25%+ smaller, shoulder≈hip),
 * pear (hip > shoulder), inverted triangle (shoulder > hip), rectangle (similar),
 * apple (waist prominent).
 */
export function getBodyShapeFromMeasurements(m: Measurements, gender: Gender = 'female'): BodyShapeResult {
  const { shoulder, waist, hip } = m
  const max = Math.max(shoulder, waist, hip)
  if (max === 0) {
    return {
      shape: 'rectangle',
      confidence: 0,
      reasoning: 'Please enter valid measurements.',
    }
  }

  // Gender-aware rules: menswear-focused shapes differ slightly in how we describe and score proportions.
  // Note: This is stylistic guidance, not a medical or identity classifier.
  if (gender === 'male') {
    // Inverted triangle: strong shoulder dominance
    if (shoulder >= waist * 1.2 && shoulder >= hip * 1.15) {
      return {
        shape: 'inverted_triangle',
        confidence: 0.9,
        reasoning: `Your shoulders (${shoulder}) are significantly broader than your waist (${waist}) and hips (${hip}), creating a strong V-shape (inverted triangle).`,
      }
    }

    // Trapezoid: broad shoulders with moderately smaller waist/hips (classic athletic frame)
    if (shoulder >= waist * 1.1 && shoulder >= hip * 1.05 && waist <= hip * 1.05) {
      return {
        shape: 'trapezoid',
        confidence: 0.88,
        reasoning: `Your shoulders (${shoulder}) are broader than your waist (${waist}) and hips (${hip}) in a balanced way—typical of a trapezoid (athletic) frame.`,
      }
    }

    // Triangle: more width through waist/hips than shoulders
    if (hip > shoulder * 1.08 || waist > shoulder * 1.05) {
      return {
        shape: 'triangle',
        confidence: 0.86,
        reasoning: `Your lower body or midsection (${waist}–${hip}) is wider than your shoulders (${shoulder}), giving a triangle frame.`,
      }
    }

    // Oval/apple: waist is most prominent
    if (waist >= shoulder * 1.05 && waist >= hip * 1.05) {
      return {
        shape: 'apple',
        confidence: 0.86,
        reasoning: `Your waist (${waist}) is your most prominent measurement compared with shoulders (${shoulder}) and hips (${hip}), which is typical of an oval/apple frame.`,
      }
    }

    // Rectangle: fairly even proportions
    return {
      shape: 'rectangle',
      confidence: 0.82,
      reasoning: `Your shoulders (${shoulder}), waist (${waist}), and hips (${hip}) are relatively even, creating a rectangle frame.`,
    }
  }

  // Hourglass: shoulder and hip within ~5%, waist at least 25% smaller than both
  if (
    withinPercent(shoulder, hip, 8) &&
    waistSmallerThan(waist, shoulder, 20) &&
    waistSmallerThan(waist, hip, 20)
  ) {
    return {
      shape: 'hourglass',
      confidence: 0.92,
      reasoning: `Your shoulder (${shoulder}) and hip (${hip}) measurements are balanced, with a defined waist (${waist}) that’s noticeably smaller—creating a classic hourglass silhouette.`,
    }
  }

  // Pear: hips wider than shoulders
  if (hip > shoulder * 1.05) {
    return {
      shape: 'pear',
      confidence: 0.88,
      reasoning: `Your hips (${hip}) are wider than your shoulders (${shoulder}), with a proportionally smaller upper body—characteristic of a pear shape.`,
    }
  }

  // Inverted triangle: shoulders wider than hips
  if (shoulder > hip * 1.05) {
    return {
      shape: 'inverted_triangle',
      confidence: 0.88,
      reasoning: `Your shoulders (${shoulder}) are broader than your hips (${hip}), creating a strong upper frame—an inverted triangle shape.`,
    }
  }

  // Apple: waist is largest or close to shoulder/hip (central prominence)
  if (waist >= shoulder * 0.95 || waist >= hip * 0.95) {
    return {
      shape: 'apple',
      confidence: 0.85,
      reasoning: `Your waist (${waist}) is close to or matches your shoulder and hip measurements, with weight carried through the midsection—an apple shape.`,
    }
  }

  // Rectangle: all three fairly similar
  if (withinPercent(shoulder, waist, 15) && withinPercent(waist, hip, 15) && withinPercent(shoulder, hip, 15)) {
    return {
      shape: 'rectangle',
      confidence: 0.86,
      reasoning: `Your shoulder (${shoulder}), waist (${waist}), and hip (${hip}) measurements are relatively similar, giving a balanced rectangular silhouette.`,
    }
  }

  // Default: rectangle with lower confidence
  return {
    shape: 'rectangle',
    confidence: 0.7,
    reasoning: `Your proportions are closest to a rectangular shape: shoulder ${shoulder}, waist ${waist}, hip ${hip}.`,
  }
}

export function getBodyShapeName(shape: BodyShape): string {
  return SHAPE_NAMES[shape]
}
