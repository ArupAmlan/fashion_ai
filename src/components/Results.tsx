import type { AnalysisResult, OutfitSuggestion } from '../types'
import { getBodyShapeName } from '../lib/bodyShape'
import styles from './Results.module.css'

interface ResultsProps {
  result: AnalysisResult
  onStartOver: () => void
  onOpenVTON: () => void
}

function OutfitCard({ outfit }: { outfit: OutfitSuggestion }) {
  const pct = Math.round(outfit.compatibilityScore)
  return (
    <article className={styles.outfitCard}>
      <div className={styles.outfitHeader}>
        <h4 className={styles.outfitName}>{outfit.name}</h4>
        <span className={styles.score} aria-label={`Compatibility ${pct} percent`}>
          {pct}% match
        </span>
      </div>
      {outfit.imageUrl && (
        <img
          src={outfit.imageUrl}
          alt={outfit.name}
          className={styles.outfitImage}
          style={{ width: '100%', height: 'auto', marginBottom: '1rem', borderRadius: '4px', objectFit: 'cover' }}
        />
      )}
      <p className={styles.outfitDesc}>{outfit.description}</p>
      <p className={styles.silhouette}>
        <strong>Silhouette:</strong> {outfit.silhouette}
      </p>
      {outfit.colours.length > 0 && (
        <p className={styles.colours}>
          <strong>Colours:</strong> {outfit.colours.join(', ')}
        </p>
      )}
      <div className={styles.outfitReasoning}>
        <p>{outfit.bodyShapeMatch}</p>
        <p>{outfit.colourMatch}</p>
      </div>
    </article>
  )
}

export function Results({ result, onStartOver, onOpenVTON }: ResultsProps) {
  const { bodyShape, colourPalette, outfits, inputMode } = result

  return (
    <section className={styles.section} aria-labelledby="results-heading">
      <h2 id="results-heading" className={styles.heading}>Your style profile</h2>

      <div className={styles.summary}>
        <div className={styles.block}>
          <h3 className={styles.blockTitle}>Body shape</h3>
          <p className={styles.shapeName}>{getBodyShapeName(bodyShape.shape)}</p>
          <p className={styles.reasoning}>{bodyShape.reasoning}</p>
          {inputMode === 'image' && (
            <p className={styles.note}>Identified from your image (analysed only on your device).</p>
          )}
        </div>

        <div className={styles.block}>
          <h3 className={styles.blockTitle}>Colour palette</h3>
          <p className={styles.undertone}>Undertone: <strong>{colourPalette.undertone}</strong></p>
          <p className={styles.reasoning}>{colourPalette.reasoning}</p>
          <div className={styles.swatches}>
            <div className={styles.swatchRow}>
              <span className={styles.swatchLabel}>Best:</span>
              <span className={styles.swatchList}>{colourPalette.primary.join(', ')}</span>
            </div>
            <div className={styles.swatchRow}>
              <span className={styles.swatchLabel}>Also good:</span>
              <span className={styles.swatchList}>{colourPalette.secondary.join(', ')}</span>
            </div>
            <div className={styles.swatchRow}>
              <span className={styles.swatchLabel}>Avoid:</span>
              <span className={styles.swatchListMuted}>{colourPalette.avoid.join(', ')}</span>
            </div>
          </div>
        </div>
      </div>

      <h3 className={styles.outfitsTitle}>Outfit suggestions</h3>
      <p className={styles.outfitsIntro}>
        Ranked by how well they flatter your silhouette and suit your colour palette.
      </p>
      <div className={styles.outfitGrid}>
        {outfits.map((outfit) => (
          <OutfitCard key={outfit.id} outfit={outfit} />
        ))}
      </div>

      <div className={styles.actions}>
        <button type="button" className={styles.startOverBtn} onClick={onStartOver}>
          Start over
        </button>
        <button type="button" onClick={onOpenVTON} style={{ marginLeft: '10px', padding: '10px 20px' }}>
          Virtual Try-On
        </button>
      </div>
    </section>
  )
}
