import styles from './OccasionSelect.module.css';
import type { Occasion } from '../types';

const occasions: { id: Occasion; name: string; emoji: string; description: string }[] = [
  { id: 'casual', name: 'Casual', emoji: '👕', description: 'Everyday wear, relaxed outings' },
  { id: 'formal', name: 'Formal / Professional', emoji: '💼', description: 'Office, business, ceremonies' },
  { id: 'party', name: 'Party / Evening', emoji: '🎉', description: 'Social events, night out' },
  { id: 'sport', name: 'Sport / Active', emoji: '🏃', description: 'Athleisure, training, outdoor' },
];

interface OccasionSelectProps {
  onSelect: (occasion: Occasion) => void;
  onBack: () => void;
}

export function OccasionSelect({ onSelect, onBack }: OccasionSelectProps) {
  return (
    <section className={styles.container}>
      <h2 className={styles.heading}>What's the Occasion?</h2>
      <p className={styles.subheading}>Select the context for your outfit recommendations.</p>
      <div className={styles.grid}>
        {occasions.map((occasion) => (
          <button 
            key={occasion.id} 
            className={styles.card} 
            onClick={() => onSelect(occasion.id)}
          >
            <span className={styles.emoji}>{occasion.emoji}</span>
            <h3 className={styles.cardTitle}>{occasion.name}</h3>
            <p className={styles.cardDescription}>{occasion.description}</p>
          </button>
        ))}
      </div>
      <div className={styles.actions}>
        <button type="button" className={styles.backBtn} onClick={onBack}>
          Back
        </button>
      </div>
    </section>
  );
}
