import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './theme.css'
import './base.css'
import App from './App.tsx'
import { BRAND } from './brand'

document.title = BRAND.name

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
