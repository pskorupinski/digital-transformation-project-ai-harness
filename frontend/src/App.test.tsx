import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'

describe('walking skeleton', () => {
  afterEach(() => vi.unstubAllGlobals())

  it('shows backend health', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ status: 'ok', integrations_mode: 'fake' }), { status: 200 }),
      ),
    )
    render(<App />)
    expect(await screen.findByRole('status')).toHaveTextContent('Backend: ok · integrations: fake')
  })
})
