/**
 * Client-side pose detection using TensorFlow.js.
 * Images are processed only in the browser; nothing is sent to a server.
 */

import type { PoseKeypoints } from './imageAnalysis'

export interface PoseDetectionResult {
  keypoints: PoseKeypoints
  success: boolean
  error?: string
}

let cachedDetector: any = null

async function loadPoseDetector(): Promise<unknown> {
  if (cachedDetector) return cachedDetector
  const poseDetection = await import('@tensorflow-models/pose-detection')
  const tf = await import('@tensorflow/tfjs-core')
  let backendSet = false
  try {
    await import('@tensorflow/tfjs-backend-webgpu')
    await tf.setBackend('webgpu' as any)
    backendSet = true
  } catch {}
  if (!backendSet) {
    await import('@tensorflow/tfjs-backend-webgl')
    await tf.setBackend('webgl' as any)
  }
  await tf.ready()
  cachedDetector = await poseDetection.createDetector(poseDetection.SupportedModels.MoveNet)
  return cachedDetector
}

export async function preloadPoseDetector(): Promise<void> {
  await loadPoseDetector()
}

function mapKeypoints(keypoints: Array<{ name?: string; x: number; y: number }>): PoseKeypoints {
  const byName: Record<string, { x: number; y: number }> = {}
  for (const kp of keypoints) {
    if (kp.name) byName[kp.name] = { x: kp.x, y: kp.y }
  }
  return {
    leftShoulder: byName['left_shoulder'],
    rightShoulder: byName['right_shoulder'],
    leftHip: byName['left_hip'],
    rightHip: byName['right_hip'],
    leftElbow: byName['left_elbow'],
    rightElbow: byName['right_elbow'],
  }
}

export async function detectPoseFromImageSource(
  imageSource: HTMLImageElement | HTMLCanvasElement
): Promise<PoseDetectionResult> {
  try {
    const detector = await loadPoseDetector() as any
    let input: HTMLImageElement | HTMLCanvasElement = imageSource
    if (imageSource instanceof HTMLImageElement) {
      const maxSide = 320
      const w = imageSource.naturalWidth || imageSource.width
      const h = imageSource.naturalHeight || imageSource.height
      const scale = Math.min(1, maxSide / Math.max(w, h))
      const cw = Math.max(1, Math.floor(w * scale))
      const ch = Math.max(1, Math.floor(h * scale))
      const canvas = document.createElement('canvas')
      canvas.width = cw
      canvas.height = ch
      const ctx = canvas.getContext('2d')
      if (ctx) ctx.drawImage(imageSource, 0, 0, cw, ch)
      input = canvas
    }
    const poses = await detector.estimatePoses(input)
    if (!poses.length || !poses[0].keypoints) {
      return { keypoints: {}, success: false, error: 'No pose detected. Try a clearer full-body image.' }
    }
    const keypoints = mapKeypoints(poses[0].keypoints)
    const hasRequired =
      keypoints.leftShoulder &&
      keypoints.rightShoulder &&
      keypoints.leftHip &&
      keypoints.rightHip
    if (!hasRequired) {
      return { keypoints, success: false, error: 'Could not detect shoulders and hips. Use a full-body image facing the camera.' }
    }
    return { keypoints, success: true }
  } catch (e) {
    const message = e instanceof Error ? e.message : 'Pose detection failed.'
    return { keypoints: {}, success: false, error: message }
  }
}

export function createImageFromFile(file: File): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => resolve(img)
    img.onerror = () => reject(new Error('Failed to load image'))
    img.src = URL.createObjectURL(file)
  })
}
