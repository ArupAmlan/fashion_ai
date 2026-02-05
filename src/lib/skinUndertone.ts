/**
 * Optional skin undertone estimation from an image.
 * Samples pixels from a region (e.g. face/chest area); runs in browser only.
 */

import type { Undertone } from '../types'

export function getUndertoneFromImageData(
  imageData: ImageData,
  x: number,
  y: number,
  width: number,
  height: number
): Undertone {
  const data = imageData.data
  let r = 0,
    g = 0,
    b = 0
  let count = 0
  for (let py = y; py < y + height && py < imageData.height; py++) {
    for (let px = x; px < x + width && px < imageData.width; px++) {
      const i = (py * imageData.width + px) * 4
      r += data[i]
      g += data[i + 1]
      b += data[i + 2]
      count++
    }
  }
  if (count === 0) return 'neutral'
  r /= count
  g /= count
  b /= count
  const diff = r - b
  if (diff > 25) return 'warm'
  if (diff < -15) return 'cool'
  return 'neutral'
}

/**
 * Sample from center-upper region of image (typical face/chest in full-body photo).
 */
export function getUndertoneFromImage(image: HTMLImageElement, canvas: HTMLCanvasElement): Undertone {
  const ctx = canvas.getContext('2d')
  if (!ctx) return 'neutral'
  const w = image.naturalWidth || image.width
  const h = image.naturalHeight || image.height
  canvas.width = w
  canvas.height = h
  ctx.drawImage(image, 0, 0)
  const imageData = ctx.getImageData(0, 0, w, h)
  const sampleW = Math.floor(w * 0.4)
  const sampleH = Math.floor(h * 0.25)
  const x = Math.floor((w - sampleW) / 2)
  const y = Math.floor(h * 0.1)
  return getUndertoneFromImageData(imageData, x, y, sampleW, sampleH)
}
