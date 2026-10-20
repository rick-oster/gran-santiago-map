import sys
import tempfile
import unittest
from pathlib import Path
import geopandas as gpd
from shapely.geometry import box
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from m1_pipeline import (
    EXPECTED_52, DEFAULT_34, normalize_name, verified_id_map,
    require_geometries, rings_and_vertices, compute_adjacency, ValidationError, process
)

class PipelineContracts(unittest.TestCase):
    def test_52_names_and_34_preset(self):
        self.assertEqual(len(EXPECTED_52),52)
        self.assertEqual(len(DEFAULT_34),34)
        self.assertEqual(len({normalize_name(x) for x in EXPECTED_52}),52)
        self.assertTrue(set(map(normalize_name,DEFAULT_34)).issubset(set(map(normalize_name,EXPECTED_52))))
    def test_accent_insensitive_match(self):
        self.assertEqual(normalize_name('ÑUÑOA'),normalize_name('ñuñoa'))
        self.assertEqual(normalize_name('TIL TIL'),normalize_name('Tiltil'))
    def test_rejects_made_up_ids_and_missing_records(self):
        with self.assertRaises(ValidationError):
            verified_id_map(['13001']*52, EXPECTED_52)
        with self.assertRaises(ValidationError):
            verified_id_map([f'{i:05d}' for i in range(52)], EXPECTED_52)
        with self.assertRaises(ValidationError):
            verified_id_map([], [])
    def test_shared_border_vs_vertex_contact(self):
        geoms=[box(0,0,1,1),box(1,0,2,1),box(2,1,3,2)]
        graph=compute_adjacency(['A','B','C'],geoms)
        self.assertEqual(graph,{'A':['B'],'B':['A'],'C':[]})
    def test_shape_validity_and_vertex_fingerprint(self):
        poly=box(0,0,1,1)
        require_geometries([poly]); self.assertEqual(rings_and_vertices(poly),(1,1,5))
        with self.assertRaises(ValidationError):
            require_geometries([poly.boundary])
    def test_rejects_incomplete_dataset_even_with_valid_crs(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'in.geojson'
            layer=gpd.GeoDataFrame({'CUT_COM':['13001'],'NOM_COM':['Santiago'],'CUT_REG':['13']},geometry=[box(-70.7,-33.5,-70.6,-33.4)],crs='EPSG:4326')
            layer.to_file(src,driver='GeoJSON')
            with self.assertRaisesRegex(ValidationError,'Expected 52'):
                process(src,Path(tmp)/'out','stage',expected_crs='EPSG:4326')
            self.assertFalse((Path(tmp)/'out').exists())

if __name__=='__main__': unittest.main()
