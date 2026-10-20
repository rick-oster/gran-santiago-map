# Gran Santiago Map — V1 Engineering Specification

**Status:** Design frozen / implementation not yet started  
**Specification version:** 1.0  
**Date:** 2026-10-19  
**Product:** Offline-first, browser-based interactive map of comunas in the Región Metropolitana de Santiago, Chile.  
**Development constraint:** All ordinary coding, testing, reviews, releases, and acceptance checks must be operable using only an Android phone after initial account/repository setup. The Windows PC must not be needed to develop, build, host, or operate the published PWA.

## 1. Product goal

Display accurate *complete* administrative boundary polygons for selected comunas, with vivid, seemingly random, distinguishable fills; visible charcoal outlines; and permanent comuna labels. Support mouse/touch navigation, selection, search, fully local persistence, configurable geographic coverage, and offline operation after installation. No base-map tiles, street imagery, terrain, login, or backend service are required.

### Geographic definitions

- **Gran Santiago (34)** — immutable default preset: the 32 comunas of Provincia de Santiago, plus Puente Alto and San Bernardo.
- **Región Metropolitana (52)** — immutable preset: all 52 comunas of the region.
- **Personalizado** — persisted editable set of any of the 52 comunas, including zero comunas.
- Bundle and validate boundary geometry for **all 52 comunas**, even though only 34 are initially visible.
- A comuna's entire administrative boundary is included, even when mountainous, rural, or far beyond urban development.
- The 34-comuna definition is the **project's chosen default**, not a claim that every official institution uses the same definition of Greater Santiago.

The default 34 are: Cerrillos, Cerro Navia, Conchalí, El Bosque, Estación Central, Huechuraba, Independencia, La Cisterna, La Florida, La Granja, La Pintana, La Reina, Las Condes, Lo Barnechea, Lo Espejo, Lo Prado, Macul, Maipú, Ñuñoa, Pedro Aguirre Cerda, Peñalolén, Providencia, Pudahuel, Quilicura, Quinta Normal, Recoleta, Renca, San Joaquín, San Miguel, San Ramón, Santiago, Vitacura, Puente Alto, San Bernardo. All names must map to their **verified authoritative official comuna identifiers**, never invented identifiers.

## 2. Geographic data pipeline

1. Obtain an authoritative polygon dataset from an official Chilean geospatial publisher, beginning with IDE SUBDERE's *Límites Interiores DPA* downloads: https://ide.subdere.gov.cl/descargas-con-filtros/ . The currently advertised download is a 2022 DPA layer in EPSG:5360; verify field schema, provenance, publication/redistribution permission, and whether an updated authoritative dataset exists before bundling.
2. Transform geometry into WGS84 longitude/latitude (EPSG:4326) for GeoJSON using a controlled conversion step. Preserve multipolygons, holes, and detached land fragments.
3. Filter exactly the 52 Región Metropolitana records, assert the 52 expected unique official IDs, and use those IDs for lookups, selection, color maps, and storage.
4. Validate feature geometry, polygon winding and topology; compare source extent and record counts; document provenance, transformation parameters, and checksums.
5. Produce production-optimized GeoJSON or equivalent compact static vector data, retaining enough precision that borders align cleanly. Generate a geographic neighbor/adjacency graph for color assignment.
6. Bundle the finalized geometry and metadata with the PWA's versioned offline assets. No runtime GIS API calls.
7. Geographic dataset updates use versioned, tested migrations and preserve custom settings by stable comuna ID.

## 3. UI structure

### Main window

- Full-viewport map canvas with plain **#F5F6F8** background. No street map, satellite map, OSM/Google map tiles, roads, terrain, or statistical choropleth legend.
- Responsive top toolbar: **Comunas**, **Buscar**, **Shuffle**, **Ajustes**.
- Floating camera controls: **+**, **−**, **Inicio**, **Ajustar todo**.
- Comuna count/mode indicator, compact contextual notifications, offline-ready state if useful.
- Desktop: floating search panel or side overlay; Android: touch-friendly bottom sheet; overlays do not resize the underlying map viewport or move its geographic center.
- Accessible touch targets, keyboard navigation, focus indicators, screen-reader labels, Spanish UI.

### Polygon visual design

- Opaque vibrant random-looking fills drawn using a seeded adjacency-aware algorithm; prioritize color distinction across true shared borders.
- Default border charcoal ~1.5 CSS pixels; selected border ~3 CSS pixels and drawn above neighboring lines.
- Fixed stroke thickness in screen pixels while zooming; no shadows or gradients.
- Label text and thin halos select foreground contrast automatically, taking the color fill into account. Allow manual colors even where contrast with a neighboring fill is weak; preserve the user's selected color exactly.

### Permanent labels

- Every *visible* comuna receives a label bearing its official display name (including accents) at all allowed zoom levels. Do not silently hide labels to resolve overlap.
- Use polygon-aware placement, automatic line wrapping, variable alignment, screen-space collision management, and exception coordinates when necessary; external callouts/leader lines permitted when polygon is too narrow.
- At extreme zoom-out on a small phone, overlap or limited legibility may remain physically unavoidable; design sensible minimum zoom and accessible magnification, but do not falsify a promise of zero overlap.
- Labels must not intercept clicks/taps intended for polygon selection.

## 4. Core interactions

### Pan / zoom / camera

- Mouse drag and wheel; touch swipe and pinch; zoom buttons.
- **Selecting a comuna NEVER pans or zooms**, including opening a popup near the edge. Explicitly disable Leaflet popup `autoPan` and `keepInView` behavior that can move the viewport.
- **Inicio:** restore a versioned, tested urban Santiago camera view (optimized for common phone/desktop aspect ratios). The geometry is not clipped; it remains reachable via panning.
- **Ajustar todo:** fit complete bounds of the currently visible comuna polygons, which may zoom far out due to mountains/rural territories. If none are visible, show the empty-map recovery UI instead.
- Persist camera center `(latitude, longitude)` and Leaflet zoom after gesture completion and toolbar camera actions. Restore on reload/restart, validate bounds and schema, and fall back to Inicio if invalid.
- Opening panels, selecting polygons, shuffling colors, editing colors, and switching/adjusting membership never implicitly move the camera.

### Selection and popup

- Click/tap a visible polygon or its label: select it, draw bold outline, and show a **compact popup/card** with name, color swatch, edit-color action, and close control.
- Desktop: anchored popup where it fits, fallback to constrained viewport card; Android: small fixed/bottom floating card above map controls. No camera auto-pan.
- Only one selection at a time. Select another replaces the previous. Clicking current selection again, clicking empty space, pressing Escape, or pressing X clears selection.
- Preserve selection during color changes, panning, zooming and preset switches if its comuna remains visible; deselect when it becomes hidden.
- Search/reveal of a comuna currently offscreen may select it and show an on-screen card; user can explicitly choose **Ir a** to move to it. Never navigate on reveal.

### Search

- Search **all 52** bundled comunas, not merely visible ones, with accent-insensitive, case-insensitive substring matching; support keyboard/touch navigation and clear empty-state.
- Every result shows a swatch and **Visible**/**Oculta** state.
- A visible result offers **Seleccionar** (no camera change) and **Ir a** (explicit camera navigation).
- A hidden result offers **Mostrar**. On a Custom selection, append the comuna immediately, select it and open its popup, without moving camera.
- On a read-only 34/52 preset (only 34 normally has hidden results), Mostrar presents a confirmation that the current immutable preset will be copied to Custom with the additional comuna, **replacing the previously saved Custom membership**. Only after confirmation: atomically save new custom set, activate Custom, select/show the newly enabled comuna, preserve camera and colors, and expose Undo for the current session.
- Cancel leaves **all state unchanged**. Source presets are never changed.

### Comunas panel

- Dedicated **Comunas** toolbar button toggles the selection panel. Searchable alphabetical checklist uses official display names and color swatches.
- Mode selector **34 / 52 / Personalizado**. The preset checkboxes are visibly read-only, with lock indicator; only Custom checkboxes are editable.
- In Custom, checking/unchecking a comuna updates polygons and labels immediately without Apply/Save. Store changes immediately. The last saved Custom selection is preserved when switching to 34 or 52 and back.
- Explicit **Usar como personalizado** copies the active preset into Custom, only after confirmation of replacement; record session Undo snapshot.
- Switching modes does not modify colors, saved custom membership (unless explicit replacement), selection where still visible, or camera.
- Allow zero selected; show **No hay comunas visibles** and a **Restaurar Gran Santiago (34)** recovery button. Recovery switches active mode to 34 but **does not erase empty Custom**.

### Colors

- On first run generate a stable seeded, vivid, adjacency-aware assignment for all 52 official comuna IDs.
- A selected-comuna popup provides **Editar color**; compact picker with swatches and HEX input, plus Apply and **Restaurar automático**. Validate HEX input and reflect edit without moving camera.
- Persist `automaticColors` and `manualOverrides` separately by official ID. Rendering uses manual override where present.
- **Shuffle** regenerates **only automatic** colors, respecting fixed manual colors when trying to separate adjacent hues. Preserve manual overrides, camera, selected comuna, and membership. Keep an in-session Undo. If every visible comuna is manual, report that none of the visible colors changed (though hidden auto assignments may regenerate).
- Showing/hiding a comuna or switching presets does not reshuffle existing color assignments; never overwrite a user's manual color automatically.
- Re-evaluate label foreground/halo after color edits and shuffling. Do not alter user-selected fills to meet contrast targets; adapt typography instead.

## 5. State, storage and security

- No account, authentication, automatic sync, import/export, or cross-device configuration transfer in V1.
- Settings are independent **per browser profile and web origin**, which naturally isolates separate devices but may also isolate separate browsers on the same device.
- For this small settings object use versioned browser `localStorage` rather than introducing a database prematurely; larger structured data could migrate to IndexedDB if future requirements justify it. Bundle map geometry as static cached assets.
- Suggested state schema:

```json
{
  "schemaVersion": 1,
  "activePreset": "greater-santiago-34",
  "customComunaIds": [],
  "automaticColors": {},
  "manualOverrides": {},
  "camera": { "lat": null, "lng": null, "zoom": null },
  "appearance": { "background": "#F5F6F8", "borderPx": 1.5 }
}
```

- Store the entire versioned settings document in a single atomic storage operation for multi-field changes. Validate data on reading, provide schema migrations and error notices; never destroy a valid previous configuration on an invalid write.
- Debounce camera persistence after movement completion. Persist selection membership immediately; use session-scoped Undo snapshot for destructive Custom replacement and shuffle.
- Browser storage is **not a guaranteed backup**: data can disappear if the user clears site data, uses private browsing, or the browser evicts it. Without export/import there is deliberately no cross-device or external recovery mechanism.
- No analytics, external telemetry, paid APIs, tracking, runtime geolocation, or confidential credentials required.

## 6. Final technical stack

- **Frontend:** React + TypeScript + Vite + responsive CSS.
- **Map:** Leaflet, using bundled WGS84 GeoJSON vector polygon layers and custom permanent-label placement. No tile layer.
- **Offline:** installable PWA manifest and Workbox/service-worker pre-cache of app shell, libraries, fonts, icons, and complete 52-comuna geometry; coherent cache versioning/update policy.
- **Settings:** localStorage with schema validation and migrations.
- **Testing:** Vitest for unit/state logic; Playwright for desktop/browser and mobile-emulated end-to-end testing; on-device Android smoke checks for actual touch/pinch/install/offline.
- **Source/development:** Git/GitHub; code editing through phone browser with github.dev, optionally Codespaces within the free monthly quota when terminal debugging is needed.
- **Automated builds and testing:** GitHub Actions on pull requests and default-branch changes; publish successful reviewed builds to GitHub Pages or another HTTPS static host. GitHub Pages on a free plan requires a public repository; only choose this path if publishing the source is acceptable.
- **Runtime:** after first completed online install/cache, the PWA runs independently on Android or Windows without the Windows PC powered on and without the internet, until browser data is cleared/evicted. Internet is needed for new installs or updates.
- **Cost:** aim for no additional spend. Apply GitHub usage/budget controls; Codespaces has a finite free compute/storage quota, not unlimited free development.

## 7. Repository structure

```text
gran-santiago-map/
  README.md
  docs/
    V1_SPEC.md
    DATA_PROVENANCE.md
    ACCEPTANCE_MATRIX.md
  data-source/
    scripts/                # Fetch/convert/validate (dev/CI only)
  public/
    geo/comunas-rm.geojson  # Processed optimized 52-comuna dataset
    icons/
    manifest.webmanifest
  src/
    app/
    components/             # Toolbar, Search, Comunas, Popup, ColorEditor
    map/                    # Polygons, labels, viewport, hit-testing
    model/                  # Comuna types, official IDs, presets
    state/                  # Persistence, reducer, undo, migrations
    colors/                 # Adjacency-aware seeded assignments
    styles/
  tests/
    unit/
    e2e/
  .github/workflows/
    ci.yml
    deploy.yml
```

## 8. Implementation and release gates

**M0 — Repository & phone-only workflow**
- Create repository, GitHub Actions pipeline, branch checks, HTTPS preview/deployment, phone-accessible editing and CI receipts.
- Gate: from Android only, commit a simple change, build/test automatically, and see published update.

**M1 — Geographic source & validation**
- Inspect official 52-comuna geometry, record licensing/provenance, convert, optimize, generate adjacency and official ID map.
- Gate: 52 unique records; exactly 34 distinct IDs in default preset; full boundaries preserved; geometry checks pass.

**M2 — Real map + camera**
- Render accurate polygons, clean background and outlines; pan/zoom, Home/Fit, saved camera.
- Gate: no street tile/network dependency; reopening restores last center and zoom; selection never changes camera.

**M3 — Colors + permanent labels**
- Distinct seeded colors, persisted automatic/manual colors, Shuffle and Undo, polygon-aware labeling.
- Gate: every visible polygon carries a label at all supported zoom levels; manually edited colors survive Shuffle and restart; no hidden label rendering requirement for hidden polygons.

**M4 — Selection/search/visibility presets**
- Popup, editor, full 52-comuna search, 34/52 immutable modes, Custom, instant toggles, confirmation and Undo.
- Gate: replacing Custom always requires explicit confirmation; cancel is a no-op; source presets stay unchanged; search/reveal never auto-navigates; empty-state recovery preserves Custom.

**M5 — Offline/install/resilience**
- PWA manifest, pre-cache, update-handling, storage migrations, responsive behavior, mobile actual-device smoke tests.
- Gate: after successful online installation, enable airplane mode and cold-start the PWA; polygons, names, search, presets, colors, persistence and all interaction flows still work; no runtime network access needed.

**M6 — Release acceptance**
- CI unit and E2E suites pass; Android and Windows browser manual verification; source/data provenance recorded; release notes and rollback tag; no console errors or missing assets.

## 9. Non-goals for V1

- Cloud-hosted data storage, automatic sync, import/export, backups, routing, geolocation, offline street tiles, terrain, demographic overlays, external map APIs, analytics, user accounts, edit of administrative geometry, arbitrary custom polygon drawings, or mobile native app-store packages.

## 10. Acceptance matrix (minimum)

1. Dataset: 52 unique official RM IDs and 34 unique preset IDs; geometry includes rural/mountainous portions.
2. Map is legible and navigable on Android and Windows; every visible comuna label remains instantiated.
3. Mouse/touch selection and edge popups leave camera center/zoom unchanged.
4. Search discovers visible/hidden 52, supports accents, and differentiates Select / Ir a / Mostrar.
5. Hidden reveal from preset requires confirmation before Custom overwrite; cancel changes nothing; Undo restores previous Custom.
6. Read-only presets remain immutable after repeated switching and after restart; Custom membership survives switching.
7. Custom checkbox changes are reflected on map immediately, with no Apply button.
8. Shuffle preserves manual edits exactly and does not move map or change selected/visible IDs.
9. Camera and settings survive refresh, restart and normal PWA update while browser storage is retained.
10. Zero visible comunas shows an obvious recovery control and does not erase Custom.
11. Full PWA works after airplane mode and phone/PC independence test, with no local PC server or ongoing internet requirement.
12. All required actions (edit, commit, build, test, review, deploy, open on phone) are available from phone with no paid service requirement within provider quotas.

## 11. Reference documentation

- SUBDERE IDE geographic downloads: https://ide.subdere.gov.cl/descargas-con-filtros/
- Chilean Metropolitan Region official listing (32 comuna Santiago province / 52 regional comunas): https://dprmetropolitana.dpr.gob.cl/conozca-la-region/
- Leaflet reference: https://leafletjs.com/reference.html
- MDN installable PWA: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable
- MDN offline PWA: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Offline_and_background_operation
- GitHub github.dev vs Codespaces: https://docs.github.com/en/codespaces/the-githubdev-web-based-editor
- GitHub Pages: https://docs.github.com/en/pages/quickstart
- GitHub free usage quotas: https://docs.github.com/en/billing/reference/product-usage-included

## 12. Handoff instruction

**Start implementing M0 and M1 in the specified order.** Do not reopen the above UI-design questions. Where minor unspecified details arise, apply reasonable defaults, document the decision, and continue. Preserve the user's source and state, provide exact reproducible build/test commands and machine-readable test receipts, and do not claim a gate passed without its actual evidence. No application code or release has yet been created by this specification.
