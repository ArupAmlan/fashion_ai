# StyleMatch: AI-Powered Privacy-First Fashion Recommendation System

**Project Type:** M.Tech Major Project  
**Domain:** Artificial Intelligence, Computer Vision, Edge Computing  
**Author:** [User Name]  
**Date:** May 12, 2026  

---

## 1. Abstract
StyleMatch is a dual-mode fashion recommendation system designed to bridge the gap between privacy and personalization. The system utilizes a hybrid architecture that performs heavy computer vision tasks (Pose Estimation) on the client side using TensorFlow.js to ensure user privacy, while leveraging a FastAPI backend for advanced colorimetric analysis and expert-rule recommendations. The project introduces an automated skin tone detection algorithm using CIE-LAB color space and a proportional body-shape classification model, providing users with scientifically backed style advice.

---

## 2. Introduction
### 2.1 Problem Statement
The fashion industry is shifting towards personalization, yet most existing solutions require users to upload sensitive personal images to remote servers for analysis, posing significant privacy risks. Furthermore, recommendations are often subjective rather than based on anatomical proportions and chromatic harmony.

### 2.2 Objectives
- To develop a **Privacy-First** architecture where raw body images are processed locally.
- To implement **Automated Body Shape Classification** using skeleton keypoint ratios.
- To build a **Chromatographic Skin Analysis** engine for seasonal color palette selection.
- To provide a **Rule-Based Expert System** for personalized outfit suggestions.

---

## 3. System Architecture
StyleMatch employs a **Hybrid Edge-Cloud Architecture**:

1.  **Client-Side (Edge):**
    *   **Framework:** React 18, TypeScript.
    *   **ML Engine:** TensorFlow.js with MoveNet model.
    *   **Task:** Real-time pose estimation and keypoint extraction.
2.  **Server-Side (API):**
    *   **Framework:** FastAPI (Python).
    *   **CV Engine:** OpenCV, NumPy.
    *   **Task:** Skin pixel masking (YCrCb), LAB-space color quantization, and Recommendation logic.

---

## 4. Methodology
### 4.1 Body Shape Analysis
The system identifies body shapes (Hourglass, Pear, Inverted Triangle, etc.) by calculating Euclidean distances between detected keypoints:
- **Formula:** $Ratio = \frac{ShoulderWidth}{HipWidth}$
- **Logic:** If $HipWidth > ShoulderWidth \times 1.05 \implies$ Pear Shape.

### 4.2 Automated Skin Tone Detection
1.  **Preprocessing:** Image compression and face region extraction.
2.  **Segmentation:** YCrCb color masking to isolate skin pixels.
3.  **Quantization:** Conversion to CIE-LAB space for perceptual uniformity.
4.  **Classification:** K-Nearest Neighbor (KNN) distance calculation against pre-trained seasonal centroids.

### 4.3 Recommendation Engine
A deterministic expert system that maps `{BodyShape, Undertone}` pairs to a database of curated outfit templates, silhouettes, and color palettes.

---

## 5. Technical Stack
- **Frontend:** React, Vite, TypeScript, Tailwind-inspired CSS Modules.
- **AI/ML:** TensorFlow.js, MoveNet.
- **Backend:** Python, FastAPI, Uvicorn, Pydantic.
- **Computer Vision:** OpenCV, NumPy.
- **Data Persistence:** JSON-based Centroid Dataset.

---

## 6. Implementation Details
### 6.1 Key Modules
- `src/lib/imageAnalysis.ts`: Client-side keypoint-to-measurement mapping.
- `backend/main.py`: REST API endpoints and OpenCV skin analysis.
- `backend/body_shape.py`: Multi-gender body shape classification logic.
- `backend/recommendations.py`: Fashion expert system rules.

---

## 7. Results and Evaluation
The system successfully identifies 5 major body shapes for females and 5 for males with a high degree of consistency. The automated skin tone detection demonstrates robustness across different lighting conditions due to YCrCb luma-normalization.

---

## 8. Conclusion and Future Scope
StyleMatch proves that high-performance fashion AI can coexist with strict data privacy. 

**Future Enhancements:**
- **Virtual Try-On (VTON):** Integrating Generative Adversarial Networks (GANs) for cloth warping.
- **3D Reconstruction:** Utilizing SMPL-X models for a full 3D body mesh.
- **Database Scaling:** Integrating PostgreSQL for user profile management.

---
*End of Report*
