import { useEffect, useState } from 'react'
import type { AnalysisResult, OutfitSuggestion } from '../types'
import { getBodyShapeName } from '../lib/bodyShape'
import styles from './Results.module.css'

interface ResultsProps {
  result: AnalysisResult
  onStartOver: () => void
  onOpenVTON: () => void
}

function OutfitCard({
  outfit,
  isFavorited,
  onToggleFavorite,
}: {
  outfit: OutfitSuggestion
  isFavorited: boolean
  onToggleFavorite: (o: OutfitSuggestion) => void
}) {
  const pct = Math.round(outfit.compatibilityScore)
  return (
    <article className={styles.outfitCard}>
      <div className={styles.outfitHeader}>
        <div className={styles.nameAndImage}>
          <h4 className={styles.outfitName}>{outfit.name}</h4>
          <button
            type="button"
            aria-label={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
            onClick={() => onToggleFavorite(outfit)}
            style={{
              marginLeft: '8px',
              background: 'transparent',
              border: 'none',
              cursor: 'pointer',
              fontSize: '1.1rem',
            }}
            title={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
          >
            {isFavorited ? '❤️' : '🤍'}
          </button>
          {outfit.imageUrl && (
            <div className={styles.previewTooltip}>
              <span className={styles.previewIcon}>👁️</span>
              <div className={styles.tooltipContent}>
                <img src={outfit.imageUrl} alt={outfit.name} className={styles.tooltipImg} />
                <p className={styles.tooltipText}>Preview of style</p>
              </div>
            </div>
          )}
        </div>
        <span className={styles.score} aria-label={`Compatibility ${pct} percent`}>
          {pct}% match
        </span>
      </div>
      <div style={{ display: 'flex', gap: '8px', marginBottom: '0.75rem' }}>
        {outfit.productUrl && (
          <a
            href={outfit.productUrl}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.shopBtn}
          >
            Shop Amazon
          </a>
        )}
        {outfit.altProductUrl && (
          <a
            href={outfit.altProductUrl}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.shopBtn}
          >
            Shop Flipkart
          </a>
        )}
      </div>
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

const OCCASION_LABELS: Record<string, string> = {
  casual: 'Casual Wear',
  formal: 'Formal / Professional',
  party: 'Party / Evening',
  sport: 'Sport / Active'
}

export function Results({ result, onStartOver, onOpenVTON }: ResultsProps) {
  const { bodyShape, colourPalette, outfits, inputMode, occasion } = result
  const [favorites, setFavorites] = useState<OutfitSuggestion[]>([])
  const [history, setHistory] = useState<
    Array<{ shape: string; undertone: string; occasion?: string; ts: number }>
  >([])

  useEffect(() => {
    try {
      const rawFav = localStorage.getItem('favorite_outfits') || '[]'
      const favs: OutfitSuggestion[] = JSON.parse(rawFav)
      setFavorites(favs)
    } catch {}
    try {
      const rawHist = localStorage.getItem('analysis_history') || '[]'
      const h: Array<{ shape: string; undertone: string; occasion?: string; ts: number }> = JSON.parse(rawHist)
      setHistory(h.slice(-5).reverse())
    } catch {}
  }, [])

  const toggleFavorite = (o: OutfitSuggestion) => {
    const exists = favorites.find((f) => f.id === o.id)
    let next: OutfitSuggestion[]
    if (exists) {
      next = favorites.filter((f) => f.id !== o.id)
    } else {
      next = [{ ...o }, ...favorites].slice(0, 25)
    }
    setFavorites(next)
    try {
      localStorage.setItem('favorite_outfits', JSON.stringify(next))
    } catch {}
  }

  return (
    <section className={styles.section} aria-labelledby="results-heading">
      <h2 id="results-heading" className={styles.heading}>Your style profile</h2>
      {occasion && (
        <p className={styles.occasionTag}>{OCCASION_LABELS[occasion] || occasion}</p>
      )}

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
          <OutfitCard
            key={outfit.id}
            outfit={outfit}
            isFavorited={!!favorites.find((f) => f.id === outfit.id)}
            onToggleFavorite={toggleFavorite}
          />
        ))}
      </div>

      {favorites.length > 0 && (
        <div style={{ marginTop: '1rem', padding: '1rem', borderTop: '1px solid var(--border)' }}>
          <h4 style={{ marginBottom: '0.5rem' }}>Favorites</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {favorites.slice(0, 8).map((f) => (
              <a
                key={f.id}
                href={f.productUrl || f.altProductUrl || '#'}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.shopBtn}
                title={f.name}
              >
                {f.name}
              </a>
            ))}
          </div>
        </div>
      )}

      {history.length > 0 && (
        <div style={{ marginTop: '1rem', padding: '1rem', borderTop: '1px solid var(--border)' }}>
          <h4 style={{ marginBottom: '0.5rem' }}>Recent analyses</h4>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            {history.slice(0, 5).map((h, idx) => (
              <li key={idx} style={{ marginBottom: '6px', color: 'var(--text-muted)' }}>
                {new Date(h.ts).toLocaleString()} — {getBodyShapeName(h.shape as any)} · {h.undertone} · {h.occasion || '—'}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className={styles.actions}>
        <button type="button" className={styles.startOverBtn} onClick={onStartOver}>
          Start over
        </button>
        <button type="button" onClick={onOpenVTON} className={styles.vtonBtn}>
          📷 Virtual Try-On
        </button>
      </div>
    </section>
  )
}
