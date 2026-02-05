import React, { useState } from 'react';

interface VirtualTryOnProps {
  onBack: () => void;
}

export const VirtualTryOn: React.FC<VirtualTryOnProps> = ({ onBack }) => {
  const [userImage, setUserImage] = useState<File | null>(null);
  const [garmentImage, setGarmentImage] = useState<File | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUserImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setUserImage(e.target.files[0]);
    }
  };

  const handleGarmentImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setGarmentImage(e.target.files[0]);
    }
  };

  const handleTryOn = async () => {
    if (!userImage || !garmentImage) {
      setError("Please upload both images.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("user_image", userImage);
      formData.append("garment_image", garmentImage);

      const response = await fetch("http://127.0.0.1:8000/vton", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process try-on request.");
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setResultImage(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h2>Virtual Try-On</h2>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '20px' }}>
        <div>
          <h3>User Image</h3>
          <input type="file" accept="image/*" onChange={handleUserImageChange} />
          {userImage && <p>{userImage.name}</p>}
        </div>
        <div>
          <h3>Garment Image</h3>
          <input type="file" accept="image/*" onChange={handleGarmentImageChange} />
          {garmentImage && <p>{garmentImage.name}</p>}
        </div>
      </div>

      <button onClick={handleTryOn} disabled={loading || !userImage || !garmentImage} style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}>
        {loading ? "Processing..." : "Try On"}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {resultImage && (
        <div style={{ marginTop: '20px' }}>
          <h3>Result</h3>
          <img src={resultImage} alt="Try-on Result" style={{ maxWidth: '100%', maxHeight: '500px' }} />
        </div>
      )}

      <div style={{ marginTop: '20px' }}>
        <button onClick={onBack}>Back</button>
      </div>
    </div>
  );
};
