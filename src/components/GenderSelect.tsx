import type { Gender } from '../types'
import styles from './GenderSelect.module.css'

interface GenderSelectProps {
  onSelect: (gender: Gender) => void
  onBack: () => void
}

export function GenderSelect({ onSelect, onBack }: GenderSelectProps) {
  return (
    <section className={styles.section} aria-labelledby="gender-heading">
      <h2 id="gender-heading" className={styles.heading}>Style fit preferences</h2>
      <p className={styles.subtext}>
        Choose the styling track you want (menswear / womenswear / inclusive). This is used only to tailor outfit templates and fit advice.
      </p>

      <div className={styles.options}>
        <button type="button" className={styles.option} onClick={() => onSelect('female')}>
          <span className={styles.optionLabel}>Female (womenswear)</span>
          <span className={styles.optionHint}>Dresses, skirts, waist definition, classic women’s silhouette guidance.</span>
        </button>
        <button type="button" className={styles.option} onClick={() => onSelect('male')}>
          <span className={styles.optionLabel}>Male (menswear)</span>
          <span className={styles.optionHint}>Menswear fits, layering, clean lines, athletic/straight silhouettes.</span>
        </button>
        <button type="button" className={styles.option} onClick={() => onSelect('non_binary')}>
          <span className={styles.optionLabel}>Non-binary / inclusive</span>
          <span className={styles.optionHint}>Mix of menswear + womenswear templates, ranked by compatibility.</span>
        </button>
      </div>

      <div className={styles.actions}>
        <button type="button" className={styles.backBtn} onClick={onBack}>Back</button>
      </div>
    </section>
  )
}

