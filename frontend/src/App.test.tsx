import { render, screen, within } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import { BRAND } from './brand'

describe('walking skeleton', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ status: 'ok', integrations_mode: 'fake' }), { status: 200 }),
      ),
    )
  })
  afterEach(() => vi.unstubAllGlobals())

  it('shows backend health', async () => {
    render(<App />)
    expect(await screen.findByRole('status')).toHaveTextContent('Backend: ok · integrations: fake')
  })

  it('shows the brand name as the home link in the page header', async () => {
    render(<App />)
    const header = screen.getByRole('banner')
    expect(within(header).getByRole('link', { name: BRAND.name })).toHaveAttribute('href', '/')
    await screen.findByRole('status') // let the health request settle
  })
})
