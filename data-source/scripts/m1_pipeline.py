"""M1 offline geographic source inspector and strictly gated staging converter.

Candidate geometry is NEVER written to public/. Source official IDs are discovered,
not guessed. The complete 52-record dataset and true 34-member subset are required.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

DEFAULT_34 = '''Cerrillos|Cerro Navia|Conchalí|El Bosque|Estación Central|Huechuraba|Independencia|La Cisterna|La Florida|La Granja|La Pintana|La Reina|Las Condes|Lo Barnechea|Lo Espejo|Lo Prado|Macul|Maipú|Ñuñoa|Pedro Aguirre Cerda|Peñalolén|Providencia|Pudahuel|Quilicura|Quinta Normal|Recoleta|Renca|San Joaquín|San Miguel|San Ramón|Santiago|Vitacura|Puente Alto|San Bernardo'''.split('|')
EXPECTED_52 = '''Alhué|Buin|Calera de Tango|Cerrillos|Cerro Navia|Colina|Conchalí|Curacaví|El Bosque|El Monte|Estación Central|Huechuraba|Independencia|Isla de Maipo|La Cisterna|La Florida|La Granja|Lampa|La Pintana|La Reina|Las Condes|Lo Barnechea|Lo Espejo|Lo Prado|Macul|Maipú|María Pinto|Melipilla|Ñuñoa|Padre Hurtado|Paine|Pedro Aguirre Cerda|Peñaflor|Peñalolén|Pirque|Providencia|Pudahuel|Puente Alto|Quilicura|Quinta Normal|Recoleta|Renca|San Bernardo|San Joaquín|San José de Maipo|San Miguel|San Pedro|San Ramón|Santiago|Talagante|Tiltil|Vitacura'''.split('|')

class ValidationError(ValueError):
    pass

def normalize_name(s: object) -> str:
    text = unicodedata.normalize('NFD', str(s).strip().casefold())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in text if not unicodedata.combining(c)))

def require_unique_names(names: list[str]) -> None:
    actual = [normalize_name(n) for n in names]
    expected = {normalize_name(n) for n in EXPECTED_52}
    if len(actual) != 52 or len(set(actual)) != 52 or set(actual) != expected:
        missing = sorted(expected - set(actual))
        extra = sorted(set(actual) - expected)
        raise ValidationError(f'Exactly 52 verified RM names required; count={len(actual)} missing={missing} extra={extra}')

def verified_id_map(codes: list[object], names: list[str]) -> tuple[dict[str, str], list[str]]:
    require_unique_names(names)
    if len(codes) != len(names):
        raise ValidationError('Identifier and name list length mismatch')
    parsed: list[str] = []
    for val in codes:
        raw = str(val).strip()
        if not re.fullmatch(r'13\d{3}', raw):
            raise ValidationError(f'Official RM comuna CUT must be five digits beginning 13: {raw!r}')
        parsed.append(raw)
    if len(set(parsed)) != 52:
        raise ValidationError('Official IDs are not 52 unique values')
    mapping = {normalize_name(n): code for n, code in zip(names, parsed)}
    default_ids = [mapping[normalize_name(n)] for n in DEFAULT_34]
    if len(default_ids) != 34 or len(set(default_ids)) != 34:
        raise ValidationError('Exactly 34 unique default IDs required')
    return mapping, default_ids

def select_column(columns: list[str], override: str | None, aliases: tuple[str, ...], label: str) -> str:
    if override:
        if override not in columns:
            raise ValidationError(f'Explicit {label} column absent: {override}; columns={columns}')
        return override
    hits = [c for c in columns if c.lower() in aliases]
    if len(hits) != 1:
        raise ValidationError(f'{label} field is missing or ambiguous ({hits}); use --{label}-field. Columns: {columns}')
    return hits[0]

def require_geometries(geoms: list) -> None:
    for i, g in enumerate(geoms):
        if g is None or g.is_empty or g.geom_type not in ('Polygon', 'MultiPolygon') or not g.is_valid:
            raise ValidationError(f'Invalid/non-polygon/empty geometry at source feature index {i}')

def rings_and_vertices(g):
    polys = [g] if g.geom_type == 'Polygon' else list(g.geoms)
    return (len(polys), sum(1+len(p.interiors) for p in polys),
            sum(len(p.exterior.coords) + sum(len(r.coords) for r in p.interiors) for p in polys))

def compute_adjacency(ids: list[str], geoms: list) -> dict[str, list[str]]:
    from shapely.strtree import STRtree
    boundaries = [g.boundary for g in geoms]
    spatial = STRtree(geoms)
    neighbors = {i:set() for i in ids}
    for ix, geom in enumerate(geoms):
        for other in spatial.query(geom):
            j = int(other)
            if j <= ix:
                continue
            # Point-touching comunas aren't adjacent for color separation.
            if boundaries[ix].intersection(boundaries[j]).length > 1e-9:
                neighbors[ids[ix]].add(ids[j])
                neighbors[ids[j]].add(ids[ix])
    return {k:sorted(v) for k,v in sorted(neighbors.items())}

def checksum_inputs(p: Path) -> dict[str, str]:
    if p.suffix.lower() == '.shp':
        paths = sorted(x for x in p.parent.glob(p.stem+'.*') if x.is_file())
    else:
        paths = [p]
    if not paths or not all(x.is_file() for x in paths):
        raise ValidationError(f'Missing input files for {p}')
    hashes = {}
    for part in paths:
        sha = hashlib.sha256()
        with part.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024*1024), b''):
                sha.update(chunk)
        hashes[part.name] = sha.hexdigest()
    return hashes

def process(input_path: Path, output_dir: Path, mode: str, code_field: str | None = None,
            name_field: str | None = None, region_field: str | None = None, expected_crs: str = 'EPSG:5360') -> dict:
    import geopandas as gpd
    from shapely.geometry import mapping
    if not input_path.is_file():
        raise ValidationError(f'Input file missing: {input_path}')
    if mode not in ('inspect', 'stage'):
        raise ValidationError('Only inspect or stage mode allowed')
    if mode == 'stage' and ('public' in output_dir.resolve().parts):
        raise ValidationError('Unreviewed geometry may not be staged under public/')
    frame = gpd.read_file(input_path)
    columns = list(frame.columns)
    if frame.crs is None:
        raise ValidationError('Missing authoritative CRS: cannot safely reproject')
    from pyproj import CRS
    if CRS.from_user_input(frame.crs) != CRS.from_user_input(expected_crs):
        raise ValidationError(f'Source CRS {frame.crs} differs from expected {expected_crs}; inspect provenance before override')
    code_col = select_column(columns, code_field, ('cut_com','cod_com','codigo_com','codcom','cutcom'), 'code')
    name_col = select_column(columns, name_field, ('nom_com','nomcom','comuna','nombre_com','nom_comuna'), 'name')
    region_col = select_column(columns, region_field, ('cut_reg','cod_reg','codreg','region_code'), 'region')
    selected = frame.loc[frame[region_col].apply(lambda x: str(x).strip().zfill(2) == '13')].copy()
    if len(selected) != 52:
        raise ValidationError(f'Expected 52 RM source features, got {len(selected)}; no silent dissolves/filtering')
    names = [str(v).strip() for v in selected[name_col].tolist()]
    codes = [str(v).strip() for v in selected[code_col].tolist()]
    mapping_ids, default_ids = verified_id_map(codes, names)
    original = list(selected.geometry)
    require_geometries(original)
    converted = selected.to_crs('EPSG:4326')
    geo = list(converted.geometry)
    require_geometries(geo)
    if [rings_and_vertices(g) for g in original] != [rings_and_vertices(g) for g in geo]:
        raise ValidationError('Reprojection modified polygon/ring/vertex counts')
    xmin,ymin,xmax,ymax = map(float, converted.total_bounds)
    if not (-180<=xmin<xmax<=180 and -90<=ymin<ymax<=90):
        raise ValidationError('WGS84 bounds invalid')
    hashes = checksum_inputs(input_path)
    report = {'milestone':'M1','status':'CANDIDATE_NOT_APPROVED','sourceInput':str(input_path),
              'sourceSha256': hashes,'sourceCRS':str(frame.crs),'targetCRS':'EPSG:4326',
              'sourceRecordCount':len(frame),'regionalRecordCount':len(selected),
              'officialIdCount':len(set(codes)),'defaultPresetCount':len(default_ids),
              'sourceBounds':list(map(float, selected.total_bounds)),'targetBounds':[xmin,ymin,xmax,ymax],
              'codeField':code_col,'nameField':name_col,'regionField':region_col,
              'geometryRingVertexCountsPreserved':True,
              'licenseRedistributionVerified':False,'publicationApproved':False}
    if mode == 'inspect':
        return report
    output_dir.mkdir(parents=True, exist_ok=True)
    order = sorted(range(52), key=lambda i: codes[i])
    ids = [codes[i] for i in order]
    geoms = [geo[i] for i in order]
    adjacency = compute_adjacency(ids, geoms)
    features = [{'type':'Feature','id':ids[k],
                 'properties':{'id':ids[k], 'name':names[order[k]]},
                 'geometry':mapping(geoms[k])} for k in range(52)]
    def save(filename, data):
        with (output_dir / filename).open('w',encoding='utf-8',newline='\n') as f:
            json.dump(data,f,ensure_ascii=False,separators=(',',':'),sort_keys=True)
            f.write('\n')
    save('comunas-rm.CANDIDATE.geojson',{'type':'FeatureCollection','features':features})
    save('adjacency.CANDIDATE.json',adjacency)
    save('presets.CANDIDATE.json',{'greaterSantiago34Ids':default_ids,'regionMetropolitana52Ids':ids})
    save('validation.CANDIDATE.json',report)
    return report

def main() -> int:
    parser=argparse.ArgumentParser(description='Inspect or stage OFFLINE official DPA input. Nothing published.')
    parser.add_argument('mode',choices=['inspect','stage'])
    parser.add_argument('--input',type=Path,required=True,help='Extracted .shp, .gpkg, or .geojson file')
    parser.add_argument('--output',type=Path,default=Path('data-source/staging'))
    parser.add_argument('--code-field')
    parser.add_argument('--name-field')
    parser.add_argument('--region-field')
    parser.add_argument('--expected-crs',default='EPSG:5360',help='Explicit verified source CRS; default official listing EPSG:5360')
    args=parser.parse_args()
    try:
        result=process(args.input,args.output,args.mode,args.code_field,args.name_field,args.region_field,args.expected_crs)
        print(json.dumps(result,indent=2,ensure_ascii=False))
        print(f'M1_{args.mode.upper()}_CANDIDATE=PASS; M1_GATE=NOT_YET_PASSED')
        return 0
    except Exception as e:
        print(f'M1_{args.mode.upper()}_CANDIDATE=FAIL: {e}',file=sys.stderr)
        return 1

if __name__=='__main__':
    sys.exit(main())
