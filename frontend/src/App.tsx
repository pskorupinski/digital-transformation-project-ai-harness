import { useEffect, useState } from 'react'
import { api } from './api/client'

type Health = { status: string; integrations_mode: string }

// Walking skeleton: proves frontend → proxy → backend → database wiring.
// Replace with the first slice's UI; keep the health indicator somewhere unobtrusive.
export default function App() {
  const [health, setHealth] = useState<Health | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    api<Health>('/health')
      .then(setHealth)
      .catch(() => setError(true))
  }, [])

  return (
    <main style={{ padding: 'calc(var(--space) * 3)' }}>
      <h1>Walking skeleton</h1>
      {error && <p role="status">Backend: unreachable</p>}
      {health && (
        <p role="status">
          Backend: {health.status} · integrations: {health.integrations_mode}
        </p>
      )}
    </main>
  )
}
