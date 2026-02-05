import { useState } from 'react'
import type { Measurements } from '../types'
import styles from './MeasurementForm.module.css'

interface MeasurementFormProps {
  onSubmit: (m: Measurements) => void
  onBack: () => void
}

export function MeasurementForm({ onSubmit, onBack }: MeasurementFormProps) {
  const [shoulder, setShoulder] = useState('')
  const [waist, setWaist] = useState('')
  const [hip, setHip] = useState('')
  const [unit, setUnit] = useState<'in' | 'cm'>('in')
  const [touched, setTouched] = useState(false)

  const shoulderNum = parseFloat(shoulder)
  const waistNum = parseFloat(waist)
  const hipNum = parseFloat(hip)
  const valid =
    !Number.isNaN(shoulderNum) &&
    !Number.isNaN(waistNum) &&
    !Number.isNaN(hipNum) &&
    shoulderNum > 0 &&
    waistNum > 0 &&
    hipNum > 0

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setTouched(true)
    if (!valid) return
    onSubmit({
      shoulder: shoulderNum,
      waist: waistNum,
      hip: hipNum,
      unit,
    })
  }

  return (
    <section className={styles.section} aria-labelledby="measure-heading">
      <h2 id="measure-heading" className={styles.heading}>Your measurements</h2>
      <p className={styles.subtext}>
        Measure around the fullest part. Shoulder: across the back; waist: narrowest point; hip: widest part.
      </p>

      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.unitRow}>
          <label className={styles.label}>Unit</label>
          <div className={styles.radioGroup}>
            <label className={styles.radio}>
              <input
                type="radio"
                name="unit"
                checked={unit === 'in'}
                onChange={() => setUnit('in')}
              />
              Inches
            </label>
            <label className={styles.radio}>
              <input
                type="radio"
                name="unit"
                checked={unit === 'cm'}
                onChange={() => setUnit('cm')}
              />
              cm
            </label>
          </div>
        </div>

        <div className={styles.field}>
          <label htmlFor="shoulder" className={styles.label}>Shoulder (around)</label>
          <input
            id="shoulder"
            type="number"
            min="1"
            step="0.5"
            value={shoulder}
            onChange={(e) => setShoulder(e.target.value)}
            placeholder={unit === 'in' ? 'e.g. 38' : 'e.g. 96'}
            className={styles.input}
            aria-required="true"
          />
        </div>
        <div className={styles.field}>
          <label htmlFor="waist" className={styles.label}>Waist</label>
          <input
            id="waist"
            type="number"
            min="1"
            step="0.5"
            value={waist}
            onChange={(e) => setWaist(e.target.value)}
            placeholder={unit === 'in' ? 'e.g. 28' : 'e.g. 71'}
            className={styles.input}
            aria-required="true"
          />
        </div>
        <div className={styles.field}>
          <label htmlFor="hip" className={styles.label}>Hip</label>
          <input
            id="hip"
            type="number"
            min="1"
            step="0.5"
            value={hip}
            onChange={(e) => setHip(e.target.value)}
            placeholder={unit === 'in' ? 'e.g. 38' : 'e.g. 96'}
            className={styles.input}
            aria-required="true"
          />
        </div>

        {touched && !valid && (
          <p className={styles.error} role="alert">
            Please enter valid positive numbers for all three measurements.
          </p>
        )}

        <div className={styles.actions}>
          <button type="button" className={styles.backBtn} onClick={onBack}>
            Back
          </button>
          <button type="submit" className={styles.submitBtn} disabled={!valid}>
            Continue
          </button>
        </div>
      </form>
    </section>
  )
}
