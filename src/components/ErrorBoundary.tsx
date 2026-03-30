import { Component, ErrorInfo, ReactNode } from 'react'
import styles from './ErrorBoundary.module.css'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error, errorInfo: null }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
    this.setState({ error, errorInfo })
  }

  handleReload = () => {
    window.location.reload()
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null })
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <div className={styles.container}>
          <div className={styles.icon}>⚠️</div>
          <h2 className={styles.title}>Something went wrong</h2>
          <p className={styles.description}>
            We apologize for the inconvenience. Please try refreshing the page.
          </p>
          {this.state.error && (
            <details className={styles.details}>
              <summary>Error details</summary>
              <pre className={styles.errorText}>
                {this.state.error.toString()}
                {this.state.errorInfo?.componentStack}
              </pre>
            </details>
          )}
          <div className={styles.actions}>
            <button onClick={this.handleReload} className={styles.primaryButton}>
              Reload Page
            </button>
            <button onClick={this.handleReset} className={styles.secondaryButton}>
              Try Again
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
