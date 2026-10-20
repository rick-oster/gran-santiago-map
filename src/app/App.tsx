import { BUILD_MARKER, SPEC_VERSION } from './build-label'

const milestones = [
  { code: 'M0', title: 'Flujo de desarrollo móvil', state: 'En validación' },
  { code: 'M1', title: 'Datos geográficos oficiales', state: 'Pendiente' },
  { code: 'M2–M6', title: 'Mapa, colores, interacción y PWA offline', state: 'Pendiente' },
] as const

function App() {
  return (
    <main className="shell">
      <header className="topbar">
        <div className="mark" aria-hidden="true"><span /></div>
        <strong>Gran Santiago Map</strong>
        <span className="topbar-tag">V1 · M0</span>
      </header>
      <section className="content" aria-labelledby="heading">
        <p className="eyebrow">INICIO DEL PROYECTO · ESPECIFICACIÓN CONGELADA V{SPEC_VERSION}</p>
        <h1 id="heading">Gran Santiago Map</h1>
        <p className="lede">Infraestructura de desarrollo en preparación. El mapa geográfico real se incorporará cuando M1 valide los límites oficiales de las 52 comunas.</p>
        <div className="preview" aria-label="Mapa no disponible todavía">
          <div className="preview-pattern" aria-hidden="true" />
          <div className="preview-message">
            <span className="preview-icon" aria-hidden="true">◇</span>
            <strong>Sin geometría ficticia</strong>
            <span>Vista temporal de M0, no es un mapa de comunas.</span>
          </div>
        </div>
        <section aria-labelledby="progress-title" className="progress">
          <h2 id="progress-title">Estado de implementación</h2>
          <ul>
            {milestones.map((milestone) => (
              <li key={milestone.code}>
                <span className="milestone-code">{milestone.code}</span>
                <span className="milestone-title">{milestone.title}</span>
                <span className="milestone-status">{milestone.state}</span>
              </li>
            ))}
          </ul>
        </section>
        <div className="footnote">
          <span>Identificador visible para la prueba de publicación desde Android:</span>
          <output data-testid="build-marker" aria-label="Identificador de compilación">{BUILD_MARKER}</output>
        </div>
      </section>
    </main>
  )
}

export default App
