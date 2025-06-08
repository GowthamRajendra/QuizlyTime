import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from './context/AuthProvider.jsx'
import { MultiplayerSocketProvider } from './context/MultiplayerSocketProvider.jsx'
// import './index.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <MultiplayerSocketProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </MultiplayerSocketProvider>
    </AuthProvider>
  </StrictMode>,
)
