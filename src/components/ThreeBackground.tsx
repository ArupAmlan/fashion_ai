import { useEffect, useRef } from 'react'

export function ThreeBackground() {
  const containerRef = useRef<HTMLDivElement>(null)
  const rendererRef = useRef<any>(null)
  const frameIdRef = useRef<number>(0)

  useEffect(() => {
    if (!containerRef.current) return
    let THREE: any
    let particlesGeometry: any
    let particlesMaterial: any
    let renderer: any

    const init = async () => {
      THREE = await import('three')

      // Scene setup
      const scene = new THREE.Scene()
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
      renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
      
      renderer.setSize(window.innerWidth, window.innerHeight)
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
      containerRef.current!.appendChild(renderer.domElement)
      rendererRef.current = renderer

      // Create floating particles
      particlesGeometry = new THREE.BufferGeometry()
      const particlesCount = 150
      const posArray = new Float32Array(particlesCount * 3)
      const colorsArray = new Float32Array(particlesCount * 3)

      for (let i = 0; i < particlesCount * 3; i += 3) {
        // Position
        posArray[i] = (Math.random() - 0.5) * 20
        posArray[i + 1] = (Math.random() - 0.5) * 20
        posArray[i + 2] = (Math.random() - 0.5) * 10

        // Colors - gradient from pink to purple to blue
        const colorChoice = Math.random()
        if (colorChoice < 0.33) {
          // Pink
          colorsArray[i] = 0.96
          colorsArray[i + 1] = 0.45
          colorsArray[i + 2] = 0.71
        } else if (colorChoice < 0.66) {
          // Purple
          colorsArray[i] = 0.65
          colorsArray[i + 1] = 0.55
          colorsArray[i + 2] = 0.98
        } else {
          // Blue
          colorsArray[i] = 0.38
          colorsArray[i + 1] = 0.65
          colorsArray[i + 2] = 0.98
        }
      }

      particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3))
      particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colorsArray, 3))

      particlesMaterial = new THREE.PointsMaterial({
        size: 0.08,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending
      })

      const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial)
      scene.add(particlesMesh)

      // Create floating geometric shapes
      const shapes: any[] = []
      const geometries = [
        new THREE.IcosahedronGeometry(0.3, 0),
        new THREE.OctahedronGeometry(0.25, 0),
        new THREE.TetrahedronGeometry(0.35, 0)
      ]

      for (let i = 0; i < 8; i++) {
        const geometry = geometries[Math.floor(Math.random() * geometries.length)]
        const material = new THREE.MeshBasicMaterial({
          color: i % 3 === 0 ? 0xf472b6 : i % 3 === 1 ? 0xa78bfa : 0x60a5fa,
          transparent: true,
          opacity: 0.15,
          wireframe: true
        })
        const mesh = new THREE.Mesh(geometry, material)
        
        mesh.position.set(
          (Math.random() - 0.5) * 15,
          (Math.random() - 0.5) * 15,
          (Math.random() - 0.5) * 5
        )
        
        mesh.userData = {
          rotationSpeed: {
            x: (Math.random() - 0.5) * 0.01,
            y: (Math.random() - 0.5) * 0.01
          },
          floatSpeed: Math.random() * 0.002 + 0.001,
          floatOffset: Math.random() * Math.PI * 2
        }
        
        shapes.push(mesh)
        scene.add(mesh)
      }

      camera.position.z = 5

      // Mouse interaction
      let mouseX = 0
      let mouseY = 0
      let targetX = 0
      let targetY = 0

      const handleMouseMove = (event: MouseEvent) => {
        mouseX = (event.clientX / window.innerWidth) * 2 - 1
        mouseY = -(event.clientY / window.innerHeight) * 2 + 1
      }

      window.addEventListener('mousemove', handleMouseMove, { passive: true })

      // Animation loop
      const animate = () => {
        frameIdRef.current = requestAnimationFrame(animate)

        // Smooth camera movement based on mouse
        targetX = mouseX * 0.5
        targetY = mouseY * 0.5
        camera.position.x += (targetX - camera.position.x) * 0.05
        camera.position.y += (targetY - camera.position.y) * 0.05
        camera.lookAt(scene.position)

        // Rotate particles slowly
        particlesMesh.rotation.y += 0.0005
        particlesMesh.rotation.x += 0.0002

        // Animate shapes
        const time = Date.now() * 0.001
        shapes.forEach((shape) => {
          shape.rotation.x += shape.userData.rotationSpeed.x
          shape.rotation.y += shape.userData.rotationSpeed.y
          
          // Floating motion
          shape.position.y += Math.sin(time * shape.userData.floatSpeed + shape.userData.floatOffset) * 0.002
        })

        renderer.render(scene, camera)
      }

      animate()

      // Handle resize
      const handleResize = () => {
        camera.aspect = window.innerWidth / window.innerHeight
        camera.updateProjectionMatrix()
        renderer.setSize(window.innerWidth, window.innerHeight)
      }

      window.addEventListener('resize', handleResize, { passive: true })

      // Cleanup
      return () => {
        window.removeEventListener('mousemove', handleMouseMove)
        window.removeEventListener('resize', handleResize)
        cancelAnimationFrame(frameIdRef.current)
        
        shapes.forEach(shape => {
          shape.geometry.dispose()
          ;(shape.material as any).dispose()
        })
        
        particlesGeometry.dispose()
        particlesMaterial.dispose()
        renderer.dispose()
        
        if (containerRef.current && renderer.domElement) {
          containerRef.current.removeChild(renderer.domElement)
        }
      }
    }

    const cleanupPromise = init()
    return () => {
      // ensure cleanup runs if init completed
      cleanupPromise.then((cleanup: any) => {
        if (typeof cleanup === 'function') cleanup()
      }).catch(() => {})
    }
  }, [])

  return (
    <div
      ref={containerRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        zIndex: 0,
        opacity: 0.6
      }}
    />
  )
}
