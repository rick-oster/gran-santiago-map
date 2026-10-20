import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages serves project repos under /<repository-name>/.
// Keep dev/preview at '/' unless explicitly overridden by the deployment workflow.
export default defineConfig({
  plugins: [react()],
  base: process.env.GITHUB_PAGES_BASE || '/',
})
