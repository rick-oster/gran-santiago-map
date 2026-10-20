# M1 geographic source — first implementation

The V1 specification remains frozen. This package adds a **real offline DPA source inspector** and a conservative staging converter. It never invents a comuna ID or ships fictitious boundaries.

## Windows 11 — development without elevated privileges

Use an ordinary PowerShell 7 terminal in `F:\Projects\GranSantiago`:

```powershell
py -3 -m venv .venv-m1
.\.venv-m1\Scripts\python.exe -m pip install -r data-source/requirements-m1.txt
.\.venv-m1\Scripts\python.exe -m unittest discover -s data-source/tests -v
```

Download the official SUBDERE DPA 2023 RAR to `data-source/raw/` using the URL documented in `docs/DATA_PROVENANCE.md`. The archive is large (the SUBDERE library lists ~250MB for the 2023 publication). Extract offline to `data-source/raw/extracted/` using your trusted archive tool; do not upload the original to GitHub or commit the extracted data.

Inspect the actual extracted content to determine the correct communal polygon `.shp` file. Do **not** guess the layer from filename or use provincial boundaries:

```powershell
.\.venv-m1\Scripts\python.exe data-source/scripts/m1_pipeline.py inspect --input data-source/raw/extracted/THE_ACTUAL_COMUNA_LAYER.shp
```

The default source-CRS assertion is `EPSG:5360`; a differing declared CRS is a hard error until provenance is reviewed (only then use `--expected-crs` explicitly). If an attribute name differs, pass `--code-field`, `--region-field` or `--name-field` explicitly after inspecting the actual schema. Once inspection passes:

```powershell
.\.venv-m1\Scripts\python.exe data-source/scripts/m1_pipeline.py stage --input data-source/raw/extracted/THE_ACTUAL_COMUNA_LAYER.shp --output data-source/staging
```

The generated `*.CANDIDATE.*` files stay in gitignored `data-source/staging/`, NOT `public/geo/`. They cannot be released until legal/provenance/topology/precision gates pass. No network dependency exists for conversion after the source archive and Python dependencies have been installed.

## Android/cloud path

Codespaces from Android can run the same Python commands after cloning and installing `data-source/requirements-m1.txt` in a virtualenv. Avoid uploading huge RAR archives via the browser editor; download from SUBDERE directly in the Codespaces terminal when permitted. The eventual map does not depend on Codespaces, Python or the Windows PC.

## Gate rules

`M1_INSPECT_CANDIDATE=PASS` or `M1_STAGE_CANDIDATE=PASS` means the candidate passed a **subset** of validation checks, NOT that M1 has passed. The final 52 source identifiers, data license, geometry and adjacency topology, reproducibility, optimization and migration gates must all pass before putting static polygons into `public/geo/`.
