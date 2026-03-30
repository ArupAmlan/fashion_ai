import { useState, useEffect } from 'react'
import { ModeSelect } from './components/ModeSelect'
import { MeasurementForm } from './components/MeasurementForm'
import { ImageUpload } from './components/ImageUpload'
import { UndertoneStep } from './components/UndertoneStep'
import { Results } from './components/Results'
import { LoadingSpinner } from './components/LoadingSpinner'
import type { InputMode, AnalysisResult, Measurements, Undertone, Gender, Occasion } from './types'
import { getBodyShapeFromKeypointsWithGender } from './lib/imageAnalysis'
import { detectPoseFromImageSource, createImageFromFile, preloadPoseDetector } from './lib/poseDetection'
import { getUndertoneFromImage } from './lib/skinUndertone'
import { GenderSelect } from './components/GenderSelect'
import { OccasionSelect } from './components/OccasionSelect'
import { VirtualTryOn } from './components/VirtualTryOn'
import { ThreeBackground } from './components/ThreeBackground'
import { getColourPaletteForUndertone } from './lib/colourHarmony'
import { getBodyShapeFromMeasurements } from './lib/bodyShape'
import { getOutfitRecommendations } from './lib/recommendations'

type Step = 'mode' | 'gender' | 'input' | 'undertone' | 'occasion' | 'results' | 'vton'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [step, setStep] = useState<Step>('mode')
  const [inputMode, setInputMode] = useState<InputMode | null>(null)
  const [gender, setGender] = useState<Gender | null>(null)
  const [measurements, setMeasurements] = useState<Measurements | null>(null)
  const [undertone, setUndertone] = useState<Undertone | null>(null)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [imageBodyShape, setImageBodyShape] = useState<ReturnType<typeof getBodyShapeFromKeypointsWithGender> | null>(null)
  const [imageUndertone, setImageUndertone] = useState<Undertone | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [useMeasurementsInImageMode, setUseMeasurementsInImageMode] = useState(false)
  const [occasion, setOccasion] = useState<Occasion>('casual')
  const [showBackground, setShowBackground] = useState(true)
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking')

  useEffect(() => {
    preloadPoseDetector().catch(() => {})
    
    // Check backend health
    const checkBackend = async () => {
      try {
        const res = await fetch(`${API_URL}/health`)
        if (res.ok) setBackendStatus('online')
        else setBackendStatus('offline')
      } catch (e) {
        console.error("Backend unreachable:", e)
        setBackendStatus('offline')
      }
    }
    checkBackend()
  }, [])

  const handleModeSelect = (mode: InputMode) => {
    setInputMode(mode)
    setStep('gender')
    setError(null)
    setUseMeasurementsInImageMode(false)
  }

  const handleGenderSelect = (g: Gender) => {
    setGender(g)
    setStep('input')
    setError(null)
  }

  const handleMeasurementsSubmit = (m: Measurements) => {
    setMeasurements(m)
    setStep('undertone')
  }

  const handleImageSubmit = async (file: File) => {
    setLoading(true)
    setError(null)
    try {
      const img = await createImageFromFile(file)
      const canvas = document.createElement('canvas')
      const poseResult = await detectPoseFromImageSource(img)
      if (!poseResult.success) {
        setError(poseResult.error ?? 'Could not analyse image.')
        setLoading(false)
        return
      }
      const g = gender ?? 'female'
      const bodyShapeFromImage = getBodyShapeFromKeypointsWithGender(poseResult.keypoints, g)
      setImageBodyShape(bodyShapeFromImage)
      let undertoneComputed: Undertone | null = null
      try {
        const fd = new FormData()
        fd.append('file', file, file.name)
        // Use MINIMAL skin analysis endpoint
        const res = await fetch(`${API_URL}/instant/skin`, {
          method: 'POST',
          body: fd,
        })
        if (res.ok) {
          const data: { undertone: Undertone; processing_time_ms?: number } = await res.json()
          undertoneComputed = data.undertone
          console.log(`Skin analysis completed in ${data.processing_time_ms || 0}ms`)
        }
      } catch (_) {
        // ignore, will fall back to client-side estimation
      }
      const undertoneFromImage = undertoneComputed ?? getUndertoneFromImage(img, canvas)
      setImageUndertone(undertoneFromImage)
      setStep('undertone')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Image analysis failed.')
    } finally {
      setLoading(false)
    }
  }

  const handleUndertoneSubmit = (u: Undertone) => {
    setUndertone(u)
    setStep('occasion')
  }
  
  const handleOccasionSelect = (o: Occasion) => {
    setOccasion(o)
    computeAndShowResults()
  }

  const computeLocalInstantResults = () => {
    const g = gender ?? 'female'
    const shape =
      imageBodyShape?.shape ??
      getBodyShapeFromMeasurements(
        {
          shoulder: measurements?.shoulder ?? 40,
          waist: measurements?.waist ?? 30,
          hip: measurements?.hip ?? 40,
          unit: 'in',
        },
        g
      ).shape
    const u = undertone ?? imageUndertone ?? 'neutral'
    const palette = getColourPaletteForUndertone(u)
    const outfits = getOutfitRecommendations(shape, palette, g)
    const transformedData: AnalysisResult = {
      bodyShape: {
        shape,
        confidence: 0.85,
        reasoning: 'Instant local analysis',
      },
      colourPalette: palette,
      outfits,
      inputMode: inputMode || 'measurements',
      gender: g,
      occasion,
    }
    setResult(transformedData)
    try {
      const raw = localStorage.getItem('analysis_history') || '[]'
      const arr = JSON.parse(raw) as Array<{ shape: string; undertone: string; occasion?: string; ts: number }>
      arr.push({ shape, undertone: u, occasion, ts: Date.now() })
      const trimmed = arr.slice(-20)
      localStorage.setItem('analysis_history', JSON.stringify(trimmed))
    } catch {}
    setStep('results')
  }

  const computeAndShowResults = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const g = gender ?? 'female'
      
      const bodyShapeOverride = imageBodyShape?.shape
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 1500) // 1.5s timeout
      
      let usedLocal = false
      try {
        const response = await fetch(`${API_URL}/instant/complete`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            shoulder: measurements?.shoulder || 40,
            waist: measurements?.waist || 30,
            hip: measurements?.hip || 40,
            gender: g,
            occasion: occasion,
            body_shape_override: bodyShapeOverride,
          }),
          signal: controller.signal,
        })
        
        clearTimeout(timeoutId)
        
        if (!response.ok) {
          throw new Error(`Backend error: ${response.status}`)
        }
        
        const data = await response.json() as any
        
        const transformedData: AnalysisResult = {
          bodyShape: data.analysis.bodyShape,
          colourPalette: {
            undertone: data.analysis.undertone as Undertone,
            primary: data.analysis.palette?.primary || [],
            secondary: data.analysis.palette?.secondary || [],
            avoid: data.analysis.palette?.avoid || [],
            reasoning: `Based on your ${data.analysis.undertone} undertone and ${data.analysis.season} season`,
          },
          outfits: data.outfits.map((outfit: any) => ({
            id: outfit.id,
            name: outfit.name,
            description: outfit.description,
            silhouette: 'custom',
            colours: outfit.colors,
            compatibilityScore: outfit.compatibilityScore,
            reasoning: outfit.reasoning,
            bodyShapeMatch: data.analysis.bodyShape.shape,
            colourMatch: data.analysis.undertone,
            imageUrl: outfit.imageUrl ? (outfit.imageUrl.startsWith('http') ? outfit.imageUrl : `${API_URL}${outfit.imageUrl}`) : null,
            productUrl: outfit.productUrl || null,
            altProductUrl: outfit.altProductUrl || null,
          })),
          inputMode: inputMode || 'measurements',
          gender: g,
        }
        
        setResult(transformedData)
        setStep('results')
      } catch (e) {
        console.warn("Backend failed or timed out, falling back to local analysis:", e)
        usedLocal = true
      } finally {
        clearTimeout(timeoutId)
      }
      
      if (usedLocal) {
        computeLocalInstantResults()
      }
    } catch (e) {
      console.error(e)
      // Final fallback if everything fails
      computeLocalInstantResults()
    } finally {
      setLoading(false)
    }
  }

  const handleBack = () => {
    if (step === 'gender') setStep('mode')
    else if (step === 'input') setStep('gender')
    else if (step === 'undertone') setStep('input')
    else if (step === 'occasion') setStep('undertone')
    else if (step === 'results') setStep('occasion')
    else if (step === 'vton') setStep('results')
    setError(null)
  }

  const handleStartOver = () => {
    setStep('mode')
    setInputMode(null)
    setGender(null)
    setMeasurements(null)
    setUndertone(null)
    setResult(null)
    setImageBodyShape(null)
    setImageUndertone(null)
    setError(null)
  }

  return (
    <div className="app">
      <ThreeBackground />
      <header className="header">
        <div className="backend-status" style={{ position: 'absolute', top: '10px', right: '10px', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '5px' }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: backendStatus === 'online' ? '#4ade80' : backendStatus === 'offline' ? '#f87171' : '#fbbf24' }}></span>
          {backendStatus === 'online' ? 'Backend Connected' : backendStatus === 'offline' ? 'Backend Offline' : 'Checking Backend...'}
        </div>
        <h1 className="logo">StyleMatch</h1>
        <p className="tagline">Personal fashion advice from your shape & colour</p>
      </header>

      <main className="main">
        {loading && (
          <div className="loading-overlay">
            <LoadingSpinner message="Analyzing your style..." size="large" />
          </div>
        )}
        
        {!loading && step === 'mode' && (
          <ModeSelect onSelect={handleModeSelect} />
        )}

        {!loading && step === 'gender' && (
          <GenderSelect onSelect={handleGenderSelect} onBack={handleBack} />
        )}

        {!loading && step === 'input' && inputMode === 'measurements' && (
          <MeasurementForm onSubmit={handleMeasurementsSubmit} onBack={handleBack} />
        )}

        {!loading && step === 'input' && inputMode === 'image' && !useMeasurementsInImageMode && (
          <ImageUpload
            onImageSubmit={handleImageSubmit}
            onUseMeasurements={() => setUseMeasurementsInImageMode(true)}
            onBack={handleBack}
            loading={loading}
            error={error}
          />
        )}

        {!loading && step === 'input' && inputMode === 'image' && useMeasurementsInImageMode && (
          <MeasurementForm onSubmit={handleMeasurementsSubmit} onBack={() => setUseMeasurementsInImageMode(false)} />
        )}

        {!loading && step === 'undertone' && (
          <UndertoneStep
            onSubmit={handleUndertoneSubmit}
            onBack={handleBack}
            suggestedFromImage={imageUndertone}
          />
        )}
        
        {!loading && step === 'occasion' && (
          <OccasionSelect
            onSelect={handleOccasionSelect}
            onBack={() => setStep('undertone')}
          />
        )}
        
        {!loading && error && (
          <div style={{ padding: '20px', textAlign: 'center', color: 'red' }}>
            <p>Error: {error}</p>
            <button onClick={() => setError(null)}>Dismiss</button>
          </div>
        )}

        {!loading && step === 'results' && result && (
          <Results 
            result={result} 
            onStartOver={handleStartOver}
            onOpenVTON={() => setStep('vton')}
          />
        )}
        
        {!loading && step === 'results' && !result && (
          <div style={{ padding: '20px', textAlign: 'center' }}>
            <p>No results available. Please try again.</p>
            <button onClick={handleStartOver}>Start Over</button>
          </div>
        )}

        {!loading && step === 'vton' && (
          <VirtualTryOn onBack={() => setStep('results')} />
        )}

      </main>

      <footer className="footer">
        <p>Your data stays on your device. No images or measurements are sent to any server.</p>
      </footer>
    </div>
  )
}
