# M1 authoritative geographic data provenance — CANDIDATE ONLY

**Status:** no actual administrative geometry has yet passed integration inspection, been approved for redistribution, or been bundled with production. `public/geo/comunas-rm.geojson` must not be populated using unverified data.

## Primary source — Chilean government

- Responsible authority: Subsecretaría de Desarrollo Regional y Administrativo (SUBDERE), Infraestructura de Datos Geoespaciales (IDE).
- Official downloads: https://ide.subdere.gov.cl/descargas-con-filtros/
- Government announcement of the DPA **2023** release: https://www.subdere.gob.cl/sala-de-prensa/subdere-publica-nueva-versi%C3%B3n-de-los-l%C3%ADmites-de-la-divisi%C3%B3n-pol%C3%ADtico-administrativa
- Archive URL published in that announcement: `https://ide.subdere.gov.cl/descargas/SHP/Limite_DPA_03082023.rar`
- DPA 2023 listing: https://ide.subdere.gov.cl/project/division-politico-administrativa-2023/
- Listed source coordinate system: `EPSG:5360`, source-layer update `2023-08-03`.
- The 2022 download from the frozen spec is retained as a documented alternative, not silently preferred over 2023.
- SUBDERE's August 2026 announcement reaffirms leadership for official DPA cartography: https://ide.subdere.gov.cl/consejo-de-ministros-ratifica-liderazgo-tecnico-de-subdere-en-la-cartografia-oficial-de-la-division-politico-administrativa-del-pais/

## Independent metadata cross-check

- BCN official listing of all 52 RM comuna names (no project IDs invented): https://www.bcn.cl/siit/mapoteca/comunas
- 2023 DPA workgroup 4326 reference mirror at SMA: https://ideserver.sma.gob.cl/arcgis/rest/services/IDE/Limites/MapServer/2
- Secondary references are NOT a silent replacement for the selected SUBDERE primary geometry. They may be used to identify discrepancies.

## Required before geometry release

1. Download/extract original archive using the Windows or cloud setup; record SHA256 of the original RAR and every relevant shapefile component.
2. Inspect exact layer schema and field types. The converter fails if source columns are missing or ambiguous.
3. Verify precisely 52 Región Metropolitana source features, 52 distinct official CUT IDs beginning `13`, names matching the 52 official BCN listings, 34 unique default IDs from the frozen spec.
4. Reproject with pyproj/GeoPandas `EPSG:5360` → `EPSG:4326`, preserve multipolygons, all holes, fragments, ring and vertex counts; reject empty/invalid features rather than repairing silently.
5. Review topology/adjacency, source extents, coordinate order, neighborhood shared-border lengths, boundary accuracy, and optimization loss before bundling. Staging adjacency is preliminary until that review passes.
6. Determine and record **explicit reuse/redistribution conditions** for this government dataset. Download availability alone does not establish permission for redistribution in a public repository. Until clear, candidate files stay outside `public/` and Git.
7. Record source publication, chosen layer and CRS, official IDs, SHA256, exact tooling versions, license evidence and source audit in this document. Commit only approved, integrity-checked production assets.

See [M1 pipeline instructions](M1_DATA_PIPELINE.md). Candidate output is not production data and M1 is not yet accepted.
