/**
 * Optional image-based body shape analysis.
 * Runs entirely in the browser; images are never sent to any server.
 * Uses pose detection keypoints to estimate shoulder/hip (and derived waist) proportions.
 */

import type { BodyShapeResult, Gender } from '../types'
import { getBodyShapeFromMeasurements } from './bodyShape'
import type { Measurements } from '../types'

export type PoseKeypoints = {
  leftShoulder?: { x: number; y: number }
  rightShoulder?: { x: number; y: number }
  leftHip?: { x: number; y: number }
  rightHip?: { x: number; y: number }
  leftElbow?: { x: number; y: number }
  rightElbow?: { x: number; y: number }
}

function distance(a: { x: number; y: number }, b: { x: number; y: number }): number {
  return Math.hypot(b.x - a.x, b.y - a.y)
}

/**
 * Derive shoulder, waist, and hip "widths" from pose keypoints (normalized 0–1 or pixel coords).
 * Waist is estimated as 85% of the smaller of shoulder/hip to approximate a natural waist.
 */
export function keypointsToMeasurements(keypoints: PoseKeypoints): Measurements | null {
  const ls = keypoints.leftShoulder
  const rs = keypoints.rightShoulder
  const lh = keypoints.leftHip
  const rh = keypoints.rightHip
  if (!ls || !rs || !lh || !rh) return null

  const shoulder = distance(ls, rs)
  const hip = distance(lh, rh)
  
  // Refined waist estimation:
  // Use elbows as a proxy for waist level. If elbows are detected, we can 
  // estimate the waist width at that vertical midpoint.
  // For now, we use a more dynamic ratio: 
  // If shoulders and hips are balanced, we assume a slightly more defined waist (0.78)
  // which can trigger "Hourglass" if the measurements are close enough.
  const isBalanced = Math.abs(shoulder - hip) / Math.max(shoulder, hip) < 0.1
  const ratio = isBalanced ? 0.78 : 0.85
  const waist = Math.min(shoulder, hip) * ratio
  
  return {
    shoulder,
    waist,
    hip,
    unit: 'in', // arbitrary units; ratios matter for shape
  }
}

/**
 * Get body shape result from pose keypoints.
 * Uses same measurement-based classifier with derived proportions.
 */
export function getBodyShapeFromKeypoints(keypoints: PoseKeypoints): BodyShapeResult | null {
  const m = keypointsToMeasurements(keypoints)
  if (!m) return null
  const result = getBodyShapeFromMeasurements(m, 'female')
  return {
    ...result,
    reasoning: `${result.reasoning} (Estimated from your photo—analysis was done only on your device; the image was not sent anywhere.)`,
  }
}

export function getBodyShapeFromKeypointsWithGender(keypoints: PoseKeypoints, gender: Gender): BodyShapeResult | null {
  const m = keypointsToMeasurements(keypoints)
  if (!m) return null
  const result = getBodyShapeFromMeasurements(m, gender)
  return {
    ...result,
    reasoning: `${result.reasoning} (Estimated from your photo—analysis was done only on your device; the image was not sent anywhere.)`,
  }
}
