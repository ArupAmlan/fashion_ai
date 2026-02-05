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

async function loadPoseDetector(): Promise<unknown> {
  const poseDetection = await import('@tensorflow-models/pose-detection')
  const tf = await import('@tensorflow/tfjs-core')
  await import('@tensorflow/tfjs-backend-webgl')
  await tf.ready()
  const detector = await poseDetection.createDetector(poseDetection.SupportedModels.MoveNet)
  return detector
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
  }
}

export async function detectPoseFromImageSource(
  imageSource: HTMLImageElement | HTMLCanvasElement
): Promise<PoseDetectionResult> {
  try {
    const detector = await loadPoseDetector() as { estimatePoses: (img: HTMLImageElement | HTMLCanvasElement) => Promise<Array<{ keypoints: Array<{ name?: string; x: number; y: number }> }>> }
    const poses = await detector.estimatePoses(imageSource)
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
