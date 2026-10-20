import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './app/App'
import './styles/main.css'

const root = document.getElementById('root')
if (!root) throw new Error('Required root element not found')
createRoot(root).render(<StrictMode><App /></StrictMode>)
