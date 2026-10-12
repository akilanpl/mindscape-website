"""Static integrity checks: routes, local targets, current evidence and preservation."""
import hashlib,json,re,unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
D=Path(__file__).resolve().parents[1]/'dist'
ROUTES=['','about','research','research/library','research/reports','advancements','architecture','safety','safety/deployment','resources','contact']
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.links=[];self.ids=[];self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if 'id' in a:self.ids.append(a['id'])
  for k in ('href','src'):
   if a.get(k):self.links.append(a[k])
class Site(unittest.TestCase):
 def test_all_routes_current(self):
  for route in ROUTES:
   with self.subTest(route=route):
    text=(D/route/'index.html').read_text();p=Page(text)
    self.assertEqual(len(p.ids),len(set(p.ids)))
    if route in ('','about','research','research/reports','architecture'):self.assertNotIn('id="current-research"',text)
    if route=='':self.assertIn('Research Update . 12 OCTOBER 2026',text)
    if route=='research/library':self.assertNotIn('NOT YET ESTABLISHED',text)
 def test_every_local_target(self):
  missing=[]
  for path in D.rglob('*.html'):
   for target in Page(path.read_text()).links:
    u=urlsplit(target)
    if u.scheme or u.netloc or not u.path:continue
    p=(D/u.path.lstrip('/')) if u.path.startswith('/') else path.parent/unquote(u.path)
    if p.is_dir():p=p/'index.html'
    if not p.exists():missing.append((str(path.relative_to(D)),target))
  self.assertEqual(missing,[])
 def test_historical_assets_unchanged(self):
  for name,sha in json.loads((D/'assets/v3/historical-preservation.json').read_text()).items():
   self.assertEqual(hashlib.sha256((D/name).read_bytes()).hexdigest(),sha,name)
 def test_current_report_sources(self):
  rows=json.loads((D/'assets/v3/provenance.json').read_text());self.assertEqual(len(rows),10)
  for row in rows:self.assertEqual(hashlib.sha256((D/'assets/v3'/row['file']).read_bytes()).hexdigest(),row['sha256'])
 def test_faithful_demo(self):
  d=json.loads((D/'assets/v3/summary.json').read_text())
  self.assertEqual(d['engineering_integration'],'PASS');self.assertEqual([r['task_success'] for r in d['results']],[False,False,True,True])
 def test_filters_and_report_urls(self):
  rows=json.loads((D/'research-data.js').read_text().removeprefix('window.MindscapeResearch=').rstrip(';\n'))
  self.assertEqual(len(rows),55)
  for r in rows:
   p=D/r['url'].lstrip('/') if r.get('url') else D/'assets/reports'/r['file']
   self.assertTrue(p.exists(),str(p))
  self.assertEqual(sum(r['version']=='Historical V1/V2' for r in rows),45)
 def test_interactive_measurements(self):
  data=json.loads((D/'assets/v3/interactive-data.json').read_text())
  self.assertEqual(len(data['physics']),8)
  self.assertEqual(len(data['coding']),8)
  self.assertEqual(len(data['performance']),10)
  self.assertEqual(next(r for r in data['coding'] if r['condition']=='mindscape')['ood'],[8,12])
  self.assertEqual(next(r for r in data['physics'] if r['family']=='motion' and r['seed']=='11' and r['panel']=='stress')['candidate'],[.8965,1.3109,2.9402])
  self.assertTrue(all(r['budget'] in [10,25,50,100,250,500,1000] for r in data['math']))
  page=(D/'advancements/index.html').read_text()
  for kind in ['math','physics','coding','latency','performance']:self.assertEqual(page.count('data-chart="'+kind+'"'),1)
 def test_physics_is_integrated(self):
  self.assertIn('id="physics-panel"',(D/'about/index.html').read_text())
  self.assertIn('<h2>Physics</h2>',(D/'research/index.html').read_text())
  self.assertIn('Physical dynamics',(D/'research/reports/index.html').read_text())
  self.assertIn('OBSERVE → REPRESENT → PROPOSE → PREDICT → ACT → VERIFY → UPDATE',(D/'architecture/index.html').read_text())
 def test_form_boundary(self):
  p=Page((D/'contact/index.html').read_text())
  form=next(a for t,a in p.tags if t=='form')
  self.assertEqual(form['action'],'https://formsubmit.co/akilanpalaniyappan105@gmail.com')
  self.assertEqual(form['method'],'POST')
  self.assertTrue(any(a.get('name')=='_honey' for t,a in p.tags))
if __name__=='__main__':unittest.main()
