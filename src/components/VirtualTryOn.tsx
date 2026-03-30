import React, { useState, useRef } from 'react';
import styles from './VirtualTryOn.module.css';

interface VirtualTryOnProps {
  onBack: () => void;
}

export const VirtualTryOn: React.FC<VirtualTryOnProps> = ({ onBack }) => {
  const [userImage, setUserImage] = useState<File | null>(null);
  const [userPreview, setUserPreview] = useState<string | null>(null);
  const [garmentImage, setGarmentImage] = useState<File | null>(null);
  const [garmentPreview, setGarmentPreview] = useState<string | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const userRef = useRef<HTMLInputElement>(null);
  const garmentRef = useRef<HTMLInputElement>(null);

  const handleUserImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setUserImage(file);
      setUserPreview(URL.createObjectURL(file));
    }
  };

  const handleGarmentImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setGarmentImage(file);
      setGarmentPreview(URL.createObjectURL(file));
    }
  };

  const handleTryOn = async () => {
    if (!userImage || !garmentImage) {
      setError("Please upload both images.");
      return;
    }

    setLoading(true);
    setError(null);
    const startTime = performance.now();

    try {
      const formData = new FormData();
      formData.append("user_image", userImage);
      formData.append("garment_image", garmentImage);

      // Use VTON endpoint
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/vton`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process try-on request.");
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setResultImage(url);
      
      const duration = ((performance.now() - startTime) / 1000).toFixed(2);
      console.log(`VTON request completed in ${duration}s`);

    } catch (err) {
      const message = err instanceof Error ? err.message : "An error occurred.";
      if (message.includes("Failed to fetch") || message.includes("NetworkError")) {
        setError("Virtual Try-On requires a live backend. Please ensure the Python server is running and VITE_API_URL is configured.");
      } else {
        setError(message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.heading}>Virtual Try-On</h2>
      
      <div className={styles.uploadGrid}>
        <div className={styles.uploadCard}>
          <h3 className={styles.cardTitle}>Your Photo</h3>
          {userPreview ? (
            <img src={userPreview} alt="User Preview" className={styles.previewImage} />
          ) : (
            <div className={styles.previewPlaceholder} />
          )}
          <input 
            type="file" 
            ref={userRef}
            accept="image/*" 
            className={styles.fileInput} 
            onChange={handleUserImageChange} 
          />
          <button 
            className={styles.fileLabel} 
            onClick={() => userRef.current?.click()}
          >
            {userImage ? 'Change Image' : 'Choose Photo'}
          </button>
          {userImage && <span className={styles.fileName}>{userImage.name}</span>}
        </div>

        <div className={styles.uploadCard}>
          <h3 className={styles.cardTitle}>Garment Photo</h3>
          {garmentPreview ? (
            <img src={garmentPreview} alt="Garment Preview" className={styles.previewImage} />
          ) : (
            <div className={styles.previewPlaceholder} />
          )}
          <input 
            type="file" 
            ref={garmentRef}
            accept="image/*" 
            className={styles.fileInput} 
            onChange={handleGarmentImageChange} 
          />
          <button 
            className={styles.fileLabel} 
            onClick={() => garmentRef.current?.click()}
          >
            {garmentImage ? 'Change Image' : 'Choose Garment'}
          </button>
          {garmentImage && <span className={styles.fileName}>{garmentImage.name}</span>}
        </div>
      </div>

      <button 
        className={styles.tryOnBtn} 
        onClick={handleTryOn} 
        disabled={loading || !userImage || !garmentImage}
      >
        {loading ? "Processing magic..." : "Generate Look"}
      </button>

      {error && <div className={styles.error} role="alert">{error}</div>}

      {resultImage && (
        <section className={styles.resultSection}>
          <h3 className={styles.resultTitle}>Your New Look</h3>
          <img src={resultImage} alt="Try-on Result" className={styles.resultImage} />
        </section>
      )}

      <div className={styles.actions}>
        <button type="button" className={styles.backBtn} onClick={onBack}>
          Back to Results
        </button>
      </div>
    </div>
  );
};
