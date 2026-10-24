import { useEffect, useState } from 'react'
import { api } from './api/client'
import Layout from './components/Layout'

type Health = { status: string; integrations_mode: string }

// Walking skeleton: proves frontend → proxy → backend → database wiring.
// Replace the main content with the first slice's UI; keep the health status in the footer.
export default function App() {
  const [health, setHealth] = useState<Health | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    api<Health>('/health')
      .then(setHealth)
      .catch(() => setError(true))
  }, [])

  return (
    <Layout
      footer={
        <>
          {error && <p role="status">Backend: unreachable</p>}
          {health && (
            <p role="status">
              Backend: {health.status} · integrations: {health.integrations_mode}
            </p>
          )}
        </>
      }
    >
      <h1>Walking skeleton</h1>
      <p>Frontend, API and database are wired. The first slice replaces this page.</p>
    </Layout>
  )
}
