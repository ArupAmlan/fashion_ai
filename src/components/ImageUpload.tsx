import { useRef } from 'react'
import styles from './ImageUpload.module.css'

interface ImageUploadProps {
  onImageSubmit: (file: File) => void
  onUseMeasurements: () => void
  onBack: () => void
  loading: boolean
  error: string | null
}

export function ImageUpload({
  onImageSubmit,
  onUseMeasurements,
  onBack,
  loading,
  error,
}: ImageUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && file.type.startsWith('image/')) {
      onImageSubmit(file)
    }
    e.target.value = ''
  }

  return (
    <section className={styles.section} aria-labelledby="image-heading">
      <h2 id="image-heading" className={styles.heading}>Optional image analysis</h2>
      <p className={styles.privacy}>
        Your photo is processed only in your browser. It is never sent to any server or stored.
      </p>

      <div className={styles.uploadZone}>
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          onChange={handleFile}
          disabled={loading}
          className={styles.hiddenInput}
          aria-label="Upload full-body image"
        />
        <button
          type="button"
          className={styles.uploadBtn}
          onClick={() => inputRef.current?.click()}
          disabled={loading}
        >
          {loading ? 'Analysing…' : 'Choose a full-body image'}
        </button>
        <p className={styles.hint}>
          For best results: full-body, facing the camera, good lighting.
        </p>
      </div>

      {error && (
        <p className={styles.error} role="alert">
          {error}
        </p>
      )}

      <div className={styles.divider}>
        <span>or</span>
      </div>

      <button
        type="button"
        className={styles.measurementsLink}
        onClick={onUseMeasurements}
        disabled={loading}
      >
        Use measurements instead
      </button>

      <div className={styles.actions}>
        <button type="button" className={styles.backBtn} onClick={onBack}>
          Back
        </button>
      </div>
    </section>
  )
}
