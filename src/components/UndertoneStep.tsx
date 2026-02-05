import type { Undertone } from '../types'
import styles from './UndertoneStep.module.css'

interface UndertoneStepProps {
  onSubmit: (u: Undertone) => void
  onBack: () => void
  suggestedFromImage: Undertone | null
}

const OPTIONS: { value: Undertone; label: string; hint: string }[] = [
  {
    value: 'warm',
    label: 'Warm',
    hint: 'Golden, peachy, yellow undertones. Veins may look green; gold jewellery often flatters.',
  },
  {
    value: 'cool',
    label: 'Cool',
    hint: 'Pink, red, or blue undertones. Veins may look blue; silver jewellery often flatters.',
  },
  {
    value: 'neutral',
    label: 'Neutral',
    hint: 'A mix of warm and cool. Both gold and silver can look good.',
  },
]

export function UndertoneStep({
  onSubmit,
  onBack,
  suggestedFromImage,
}: UndertoneStepProps) {
  return (
    <section className={styles.section} aria-labelledby="undertone-heading">
      <h2 id="undertone-heading" className={styles.heading}>Your skin undertone</h2>
      <p className={styles.subtext}>
        We use this to suggest colours that complement your complexion.
      </p>

      {suggestedFromImage && (
        <p className={styles.suggested}>
          From your image we suggest: <strong>{suggestedFromImage}</strong>. You can confirm or change below.
        </p>
      )}

      <div className={styles.options}>
        {OPTIONS.map((opt) => (
          <button
            key={opt.value}
            type="button"
            className={styles.option}
            onClick={() => onSubmit(opt.value)}
          >
            <span className={styles.optionLabel}>{opt.label}</span>
            <span className={styles.optionHint}>{opt.hint}</span>
          </button>
        ))}
      </div>

      <div className={styles.actions}>
        <button type="button" className={styles.backBtn} onClick={onBack}>
          Back
        </button>
      </div>
    </section>
  )
}
