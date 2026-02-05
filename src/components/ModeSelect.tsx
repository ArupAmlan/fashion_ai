import type { InputMode } from '../types'
import styles from './ModeSelect.module.css'

interface ModeSelectProps {
  onSelect: (mode: InputMode) => void
}

export function ModeSelect({ onSelect }: ModeSelectProps) {
  return (
    <section className={styles.section} aria-labelledby="mode-heading">
      <h2 id="mode-heading" className={styles.heading}>Choose your input mode</h2>
      <p className={styles.subtext}>
        Your data stays on your device. We never send measurements or images to any server.
      </p>

      <div className={styles.cards}>
        <article className={styles.card}>
          <span className={styles.badge}>Safe mode</span>
          <h3 className={styles.cardTitle}>Measurement-only</h3>
          <p className={styles.cardDesc}>
            Enter your shoulder, waist, and hip measurements. We determine your body shape and recommend silhouettes that flatter your proportions.
          </p>
          <button
            type="button"
            className={styles.primaryBtn}
            onClick={() => onSelect('measurements')}
          >
            Use measurements
          </button>
        </article>

        <article className={styles.card}>
          <span className={styles.badge}>AI mode (optional)</span>
          <h3 className={styles.cardTitle}>Optional image analysis</h3>
          <p className={styles.cardDesc}>
            You may optionally upload a full-body image. We analyse body proportions in your browser only—your photo never leaves your device.
          </p>
          <button
            type="button"
            className={styles.secondaryBtn}
            onClick={() => onSelect('image')}
          >
            Try image analysis
          </button>
        </article>
      </div>
    </section>
  )
}
