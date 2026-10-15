"""Announcement evidence consistency and safe static boundaries."""
import hashlib,json,unittest
from pathlib import Path
from html.parser import HTMLParser
D=Path(__file__).resolve().parents[1]/'dist/mind'
class Mind(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=json.loads((D/'release-r5.4.json').read_text())
 def test_sources_authenticated(self):
  rows=json.loads((D/'evidence/manifest.json').read_text())
  self.assertEqual(len(rows),14)
  for r in rows:self.assertEqual(hashlib.sha256((D/'evidence'/r['file']).read_bytes()).hexdigest(),r['sha256'])
 def test_status_bound_to_readiness(self):
  r=json.loads((D/'evidence/readiness.json').read_text());d=self.data
  for key in ['scientific_updates','neural_ood_predictions']:self.assertEqual(d[key],r[key]);self.assertEqual(d[key],0)
  self.assertEqual(d['status'],r['status']);self.assertEqual(d['status'],'UNRUN')
  self.assertFalse(r['scientific_training_authorized'])
 def test_all_traces_unmodified(self):
  for i,t in enumerate(self.data['traces']):
   source=json.loads((D/t['source']).read_text());actual=source['direct']
   for key in ['prediction','output','verification']:self.assertEqual(t[key],actual[{'prediction':'prediction','output':'actual','verification':'evaluation'}[key]])
   self.assertEqual(t['input'],source['request']);self.assertEqual(t['steps'],actual['prediction'].get('steps') or source['unified']['trace']['events'])
   self.assertEqual(t['version'],'V3 historical integration');self.assertTrue(t['parity'])
  self.assertEqual([t['verification']['success'] for t in self.data['traces']],[False,False,True,True])
  self.assertEqual(self.data['traces'][0]['prediction']['answer'],'833')
 def test_math_cells_exact(self):
  original=json.loads((D/'evidence/math-summary.json').read_text())
  self.assertEqual(self.data['math'],original['metrics'])
  for method in self.data['math'].values():
   for seed in method.values():
    for cell in seed.values():self.assertAlmostEqual(cell['exact_accuracy'],cell['correct']/cell['tasks'])
 def test_physics_cells_exact(self):
  original=json.loads((D/'evidence/physics-summary.json').read_text())
  for family,cells in self.data['physics'].items():
   for key,cell in cells.items():
    raw=original['metrics'][family]['cells'][key];self.assertEqual(cell['means'],raw['means']);self.assertEqual(cell['n'],raw['independent_scenes'])
 def test_chart_combinations_available(self):
  for family in ['motion','interaction']:
   for horizon in ['8','16','32']:
    for model in ['structured','matched','v3_1_frozen','analytical_contacts']:
     cell=self.data['physics'][family][f'ood/{horizon}/{model}'];self.assertEqual(cell['n'],14)
     for metric in ['mse','success','coverage']:self.assertIsInstance(cell['means'][metric],(int,float))
 def test_architecture_source(self):
  self.assertEqual([m['parameters'] for m in self.data['models']],[2188,2124])
  protocol=(D/'evidence/protocol.md').read_text();self.assertIn('2,188 parameters',protocol);self.assertIn('2,124 parameters',protocol)
 def test_independent_verification_receipts(self):
  for name in ['math-audit.json','physics-audit.json']:
   raw=json.loads((D/'evidence'/name).read_text());self.assertEqual(raw['status'],'PASS')
  raw=json.loads((D/'evidence/integration-verification.json').read_text());self.assertEqual(raw['engineering_integration'],'PASS')
 def test_script_no_execution_or_html_injection(self):
  s=(D/'mind.js').read_text()
  for token in ['innerHTML','eval(','new Function','WebSocket','XMLHttpRequest']:self.assertNotIn(token,s)
  self.assertEqual(s.count('fetch('),1);self.assertIn('fetch(document.body.dataset.release)',s)
 def test_accessible_static_fallback(self):
  s=(D/'archive/r54/index.html').read_text()
  for token in ['<noscript>','role="tablist"','role="tabpanel"','aria-live="polite"','AI','Scientific study unrun.']:
   if token!='AI':self.assertIn(token,s)
  self.assertIn('prefers-reduced-motion',(D/'mind.css').read_text());self.assertIn("e.key==='ArrowRight'",(D/'mind.js').read_text())
if __name__=='__main__':unittest.main()
