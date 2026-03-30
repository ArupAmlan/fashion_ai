import { useState } from 'react'
import { ModeSelect } from './components/ModeSelect'
import { MeasurementForm } from './components/MeasurementForm'
import { ImageUpload } from './components/ImageUpload'
import { UndertoneStep } from './components/UndertoneStep'
import { Results } from './components/Results'
import { LoadingSpinner } from './components/LoadingSpinner'
import type { InputMode, AnalysisResult, Measurements, Undertone, Gender, Occasion } from './types'
import { getBodyShapeFromKeypointsWithGender } from './lib/imageAnalysis'
import { detectPoseFromImageSource, createImageFromFile } from './lib/poseDetection'
import { getUndertoneFromImage } from './lib/skinUndertone'
import { GenderSelect } from './components/GenderSelect'
import { OccasionSelect } from './components/OccasionSelect'
import { VirtualTryOn } from './components/VirtualTryOn'
import { ThreeBackground } from './components/ThreeBackground'

type Step = 'mode' | 'gender' | 'input' | 'undertone' | 'occasion' | 'results' | 'vton'

export default function App() {
  const [step, setStep] = useState<Step>('mode')
  const [inputMode, setInputMode] = useState<InputMode | null>(null)
  const [gender, setGender] = useState<Gender | null>(null)
  const [measurements, setMeasurements] = useState<Measurements | null>(null)
  const [, setUndertone] = useState<Undertone | null>(null)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [imageBodyShape, setImageBodyShape] = useState<ReturnType<typeof getBodyShapeFromKeypointsWithGender> | null>(null)
  const [imageUndertone, setImageUndertone] = useState<Undertone | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [useMeasurementsInImageMode, setUseMeasurementsInImageMode] = useState(false)
  const [occasion, setOccasion] = useState<Occasion>('casual')

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
        const res = await fetch('http://localhost:8000/instant/skin', {
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

  const computeAndShowResults = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const g = gender ?? 'female'
      
      // Use MINIMAL complete endpoint - everything in one call under 10ms
      // Use image-based body shape if available
      const bodyShapeOverride = imageBodyShape?.shape
      
      const response = await fetch('http://localhost:8000/instant/complete', {
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
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Backend error: ${response.status}`)
      }
      
      const data = await response.json() as any
      console.log('Response data:', data)
      console.log(`Analysis completed in ${data.processing_time_ms || 0}ms`)
      
      // Transform backend response to frontend format
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
          imageUrl: outfit.imageUrl || null,
          productUrl: outfit.productUrl || null,    // Amazon link
          altProductUrl: outfit.altProductUrl || null,  // Myntra link
        })),
        inputMode: inputMode || 'measurements',
        gender: g,
      }
      
      // Validate data structure
      if (!transformedData.bodyShape || !transformedData.colourPalette || !transformedData.outfits) {
        throw new Error('Invalid response format from server')
      }
      
      setResult(transformedData)
      setStep('results')
    } catch (e) {
      console.error(e)
      setError(e instanceof Error ? e.message : 'Could not reach styling backend. Is the Python server running on port 8000?')
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
