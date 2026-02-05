import { useState } from 'react'
import { ModeSelect } from './components/ModeSelect'
import { MeasurementForm } from './components/MeasurementForm'
import { ImageUpload } from './components/ImageUpload'
import { UndertoneStep } from './components/UndertoneStep'
import { Results } from './components/Results'
import type { InputMode, AnalysisResult, Measurements, Undertone, Gender } from './types'
import { getBodyShapeFromKeypointsWithGender } from './lib/imageAnalysis'
import { detectPoseFromImageSource, createImageFromFile } from './lib/poseDetection'
import { getUndertoneFromImage } from './lib/skinUndertone'
import { GenderSelect } from './components/GenderSelect'
import { VirtualTryOn } from './components/VirtualTryOn'

type Step = 'mode' | 'gender' | 'input' | 'undertone' | 'results' | 'vton'

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
        const res = await fetch('http://127.0.0.1:8000/skin_tone', {
          method: 'POST',
          body: fd,
        })
        if (res.ok) {
          const data: { undertone: Undertone } = await res.json()
          undertoneComputed = data.undertone
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
    computeAndShowResults(u)
  }

  const computeAndShowResults = (finalUndertone: Undertone) => {
    const g = gender ?? 'female'
    const input: any = {
      gender: g,
      inputMode: inputMode ?? 'measurements',
      undertone: finalUndertone,
      measurements: measurements ?? undefined,
      imageBodyShape: inputMode === 'image' ? imageBodyShape ?? undefined : undefined,
    }

    // Call Python backend; fall back to local error message if it fails.
    fetch('http://127.0.0.1:8000/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    })
      .then(async (res) => {
        if (!res.ok) throw new Error(`Backend error: ${res.status}`)
        const data: AnalysisResult = await res.json()
        setResult(data)
        setStep('results')
      })
      .catch((e) => {
        console.error(e)
        setError('Could not reach styling backend. Is the Python server running on port 8000?')
      })
  }

  const handleBack = () => {
    if (step === 'gender') setStep('mode')
    else if (step === 'input') setStep('gender')
    else if (step === 'undertone') setStep('input')
    else if (step === 'results') setStep('undertone')
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
      <header className="header">
        <h1 className="logo">StyleMatch</h1>
        <p className="tagline">Personal fashion advice from your shape & colour</p>
      </header>

      <main className="main">
        {step === 'mode' && (
          <ModeSelect onSelect={handleModeSelect} />
        )}

        {step === 'gender' && (
          <GenderSelect onSelect={handleGenderSelect} onBack={handleBack} />
        )}

        {step === 'input' && inputMode === 'measurements' && (
          <MeasurementForm onSubmit={handleMeasurementsSubmit} onBack={handleBack} />
        )}

        {step === 'input' && inputMode === 'image' && !useMeasurementsInImageMode && (
          <ImageUpload
            onImageSubmit={handleImageSubmit}
            onUseMeasurements={() => setUseMeasurementsInImageMode(true)}
            onBack={handleBack}
            loading={loading}
            error={error}
          />
        )}

        {step === 'input' && inputMode === 'image' && useMeasurementsInImageMode && (
          <MeasurementForm onSubmit={handleMeasurementsSubmit} onBack={() => setUseMeasurementsInImageMode(false)} />
        )}

        {step === 'undertone' && (
          <UndertoneStep
            onSubmit={handleUndertoneSubmit}
            onBack={handleBack}
            suggestedFromImage={imageUndertone}
          />
        )}

        {step === 'results' && result && (
          <Results 
            result={result} 
            onStartOver={handleStartOver}
            onOpenVTON={() => setStep('vton')}
          />
        )}

        {step === 'vton' && (
          <VirtualTryOn onBack={() => setStep('results')} />
        )}

      </main>

      <footer className="footer">
        <p>Your data stays on your device. No images or measurements are sent to any server.</p>
      </footer>
    </div>
  )
}
