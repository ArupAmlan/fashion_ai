import mediapipe as mp
import numpy as np
import cv2
from typing import Optional, Tuple
from dataclasses import dataclass

try:
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
except AttributeError:
    # Fallback for newer mediapipe versions
    from mediapipe.tasks.python import vision
    mp_pose = None
    mp_drawing = None


@dataclass
class BodyMeasurements:
    shoulder_width: float
    waist_width: float
    hip_width: float
    height_estimate: float
    confidence: float


class PoseAnalyzer:
    def __init__(self):
        if mp_pose:
            self.pose = mp_pose.Pose(
                static_image_mode=True,
                model_complexity=2,
                enable_segmentation=True,
                min_detection_confidence=0.5,
            )
        else:
            self.pose = None
    
    def analyze_image(self, image_bytes: bytes) -> Optional[BodyMeasurements]:
        """
        Analyze pose from image and estimate body measurements.
        Returns measurements in relative units (need to be scaled with actual height).
        """
        if self.pose is None or mp_pose is None:
            return None
            
        try:
            # Decode image
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                return None
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width = image.shape[:2]
            
            # Process pose
            results = self.pose.process(image_rgb)
            
            if not results.pose_landmarks:
                return None
            
            landmarks = results.pose_landmarks.landmark
            
            # Extract key points
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            left_waist = landmarks[mp_pose.PoseLandmark.LEFT_HIP]  # Approximation
            right_waist = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]  # Approximation
            nose = landmarks[mp_pose.PoseLandmark.NOSE]
            left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
            
            # Calculate widths in normalized coordinates
            shoulder_width = abs(left_shoulder.x - right_shoulder.x)
            hip_width = abs(left_hip.x - right_hip.x)
            waist_width = hip_width * 0.75  # Estimate waist as ~75% of hip
            
            # Estimate full body height
            ankle_y = (left_ankle.y + right_ankle.y) / 2
            height_estimate = abs(nose.y - ankle_y)
            
            # Calculate confidence based on visibility
            key_points = [left_shoulder, right_shoulder, left_hip, right_hip, nose, left_ankle, right_ankle]
            confidence = sum(p.visibility for p in key_points) / len(key_points)
            
            return BodyMeasurements(
                shoulder_width=shoulder_width,
                waist_width=waist_width,
                hip_width=hip_width,
                height_estimate=height_estimate,
                confidence=confidence,
            )
            
        except Exception as e:
            print(f"Pose analysis error: {e}")
            return None
    
    def get_measurements_for_height(
        self,
        image_bytes: bytes,
        actual_height_cm: float,
    ) -> Optional[dict]:
        """
        Get actual measurements in cm based on user's actual height.
        """
        measurements = self.analyze_image(image_bytes)
        if measurements is None:
            return None
        
        # Calculate scale factor based on height
        # Average person height in normalized coords is roughly the height_estimate
        scale_factor = actual_height_cm / (measurements.height_estimate * 100)
        
        # Estimate actual measurements using anthropometric ratios
        # These are approximations based on average body proportions
        shoulder_cm = measurements.shoulder_width * actual_height_cm * 0.25
        waist_cm = measurements.waist_width * actual_height_cm * 0.22
        hip_cm = measurements.hip_width * actual_height_cm * 0.24
        
        return {
            "shoulder": round(shoulder_cm, 1),
            "waist": round(waist_cm, 1),
            "hip": round(hip_cm, 1),
            "confidence": round(measurements.confidence, 2),
            "method": "pose_estimation",
        }
    
    def visualize_pose(self, image_bytes: bytes) -> Optional[bytes]:
        """Draw pose landmarks on image and return as bytes"""
        if self.pose is None or mp_drawing is None or mp_pose is None:
            return image_bytes
            
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                return None
            
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.pose.process(image_rgb)
            
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2),
                )
            
            # Encode back to bytes
            _, buffer = cv2.imencode('.png', image)
            return buffer.tobytes()
            
        except Exception as e:
            print(f"Pose visualization error: {e}")
            return None


# Singleton instance
_pose_analyzer = None


def get_pose_analyzer() -> PoseAnalyzer:
    global _pose_analyzer
    if _pose_analyzer is None:
        _pose_analyzer = PoseAnalyzer()
    return _pose_analyzer
