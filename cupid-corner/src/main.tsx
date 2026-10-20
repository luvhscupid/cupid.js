import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { SmoothScrollProvider } from './components/smooth-scroll-provider'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <SmoothScrollProvider>
      <App />
    </SmoothScrollProvider>
  </StrictMode>,
)
