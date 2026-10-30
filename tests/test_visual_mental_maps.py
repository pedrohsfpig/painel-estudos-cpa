"""Mapas em imagem adicionais; Ramificações e dados de estudo preservados."""
import hashlib,json,unittest
from pathlib import Path
from PIL import Image
import smoke as harness
from final_block import before_portfolio_lesson,unit_count
ROOT=Path(__file__).resolve().parents[1]
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def catalog():return json.JSONDecoder().raw_decode((ROOT/'mental-maps-data.js').read_text().split('window.MENTAL_MAPS=',1)[1])[0]

class Content(unittest.TestCase):
 def test_every_received_lesson_and_unit_has_real_legible_assets(self):
  maps=catalog();self.assertEqual(len(maps),25+unit_count());self.assertEqual({m['lesson'] for m in maps},set(range(1,14)))
  self.assertEqual(len({m['id'] for m in maps}),25+unit_count())
  self.assertEqual({m['block'] for m in maps if m['lesson']==13},set(range(1,unit_count()+1)))
  for m in maps:
   with self.subTest(m=m['id']):
    self.assertEqual(len(m['branches']),4);self.assertTrue(m['sourceSha256'])
    self.assertTrue(all(label and 2<=len(items)<=4 for label,items in m['branches']))
    p=ROOT/m['src'];self.assertTrue(p.is_file())
    with Image.open(p) as image:self.assertGreaterEqual(image.width,1500);self.assertGreaterEqual(image.height,1000)
    self.assertLess(p.stat().st_size,1500000)

class Browser(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
 tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp;tearDown=harness.PainelCPA.tearDown
 answer=harness.PainelCPA.answer;click=harness.PainelCPA.click
 def show(self,lesson=13,block=1):self.page.evaluate("([a,b])=>{view='m';mt={a,c:'visual'};selectedLessonBlocks[a]=b;go()}",[lesson,block])
 def assert_historical_arrays(self,expected):
  values=self.page.evaluate('({Q,BP,AL,MAT})')
  values['Q']=values['Q'][:1350];values['BP']=values['BP'][:675]
  values['AL'],values['MAT']['13']=before_portfolio_lesson(values['AL'],values['MAT']['13'])
  for key,value in expected.items():self.assertEqual(digest(values[key]),value,key)
 def test_preserves_every_original_array_and_ramification_renderer(self):
  expected=json.loads((ROOT/'docs/mapas-mentais-visuais.json').read_text())['preservation']
  self.assert_historical_arrays(expected)
  self.show(13,1)
  self.click('Ramificações');self.assertEqual(self.page.locator('.mind-root>span').inner_text(),'Riscos Financeiros')
  self.assertTrue(self.page.locator('.mind-branch').count()>0)
  self.click('Mapa mental');self.assertEqual(self.page.locator('[data-visual-map]').get_attribute('data-visual-map'),'aula-13-1')
  self.assert_historical_arrays(expected)
 def test_all_sources_block_filters_images_and_transcripts(self):
  for m in catalog():
   self.show(m['lesson'],m['block'])
   self.assertEqual(self.page.locator('[data-visual-map]').get_attribute('data-visual-map'),m['id'])
   image=self.page.locator('.visual-map-preview img');image.wait_for()
   self.page.wait_for_function("document.querySelector('.visual-map-preview img').complete")
   self.assertTrue(image.evaluate('n=>n.naturalWidth>=1500'))
   self.assertEqual(self.page.locator('.visual-map-transcript h4').all_text_contents(),[b[0] for b in m['branches']])
   self.assertEqual(self.page.locator('.visual-map-transcript li').all_text_contents(),[t for _,items in m['branches'] for t in items])
   self.assertTrue(self.page.locator('.visual-map-actions a').get_attribute('download'))
  self.show(7,0);self.assertEqual(self.page.locator('[data-visual-map-choice]').count(),4)
  self.page.locator('[data-visual-map-choice="aula-07-3"]').click()
  self.assertEqual(self.page.locator('[data-visual-map]').get_attribute('data-visual-map'),'aula-07-3')
  self.page.locator('.lesson-blocks [data-lesson-block="2"]').click()
  self.assertEqual(self.page.locator('[data-visual-map]').get_attribute('data-visual-map'),'aula-07-2')
 def test_amplification_keyboard_scroll_focus_and_state_preservation(self):
  self.page.evaluate("cfg={a:13,as:[],b:1,us:[1],md:'e',n:-1,m:'all',c:5};begin(mix(),'e')")
  self.answer();stable=self.page.evaluate('JSON.stringify([Q,BP,AL,MAT,H,cfg,qz])')
  self.show(13,1);self.page.locator('[data-map-open]').click()
  dialog=self.page.locator('#mental-map-viewer');self.assertTrue(dialog.is_visible())
  self.page.get_by_role('button',name='Aumentar mapa',exact=True).click()
  self.assertEqual(dialog.locator('output').inner_text(),'125%')
  dialog.locator('.mental-map-canvas').focus();self.page.keyboard.press('ArrowRight')
  self.page.wait_for_function("document.querySelector('.mental-map-canvas').scrollLeft>0")
  self.page.keyboard.press('Escape');self.assertFalse(dialog.is_visible())
  self.assertEqual(self.page.evaluate('document.activeElement.hasAttribute("data-map-open")'),True)
  self.assertEqual(self.page.evaluate('JSON.stringify([Q,BP,AL,MAT,H,cfg,qz])'),stable)
  self.page.locator('.visual-map-panel>.active-study-action .active-study-button').click()
  self.assertTrue(self.page.get_by_text('Retomar sessão',exact=True).is_visible())
 def test_new_search_type_resolves_exact_map_without_other_categories(self):
  self.show(1,0)
  self.page.locator('#content-search-input').fill('liquidez')
  self.assertTrue(self.page.locator('[data-search-source]').count()>0)
  self.assertEqual(set(self.page.locator('[data-search-source]').evaluate_all('es=>es.map(e=>e.dataset.searchSource)')),{'visual'})
  target=self.page.evaluate("contentSearchIndex().find(d=>d.type==='visual'&&d.target.map==='aula-13-1').id")
  self.page.evaluate('id=>openSearchResult(id)',target)
  self.assertEqual(self.page.locator('[data-visual-map]').get_attribute('data-visual-map'),'aula-13-1')
  self.assertTrue(self.page.locator('.visual-map-panel').evaluate('e=>e.classList.contains("search-target")'))
  self.assertEqual(self.page.evaluate('selectedLessonBlocks[13]'),1)
 def test_both_themes_mobile_desktop_selection_and_accessible_content(self):
  self.show(13,0);self.page.locator('[data-visual-map-choice="aula-13-3"]').click()
  out=Path('/tmp/cpa-visual-maps/screens');out.mkdir(exist_ok=True)
  stable=self.page.evaluate('JSON.stringify([H,cfg,qz])')
  for width in [390,1280,1920]:
   self.page.set_viewport_size(dict(width=width,height=1000))
   for theme in ['dark','light']:
    self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
    self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    self.assertEqual(self.page.locator('[data-visual-map]').get_attribute('data-visual-map'),'aula-13-3')
    self.page.locator('.visual-map-text summary').click()
    self.assertTrue(self.page.get_by_role('heading',name='Equivalência temporal',exact=True).is_visible())
    self.page.locator('.visual-map-text summary').click()
    if width==1280:self.page.locator('.material-content').screenshot(path=str(out/f'gallery-{theme}.png'))
    self.page.locator('[data-map-open]').click()
    self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    self.page.get_by_role('button',name='Aumentar mapa',exact=True).click()
    self.assertEqual(self.page.locator('#mental-map-viewer output').inner_text(),'125%')
    self.page.keyboard.press('Escape')
  self.assertEqual(stable,self.page.evaluate('JSON.stringify([H,cfg,qz])'))
 def test_new_scope_counts_deduplicate_and_children_stay_in_parent(self):
  for m in catalog():
   self.show(m['lesson'],m['block'])
   entry=self.page.evaluate("()=>ActiveStudy.audit().find(e=>e.key===document.querySelector('.visual-map-panel').dataset.activeStudy)")
   self.assertIsNotNone(entry);self.assertEqual(len(entry['ids']),len(set(entry['ids'])))
   self.assertEqual(self.page.locator('.visual-map-preview .active-study-button').count(),0)
   self.assertEqual(self.page.locator('.visual-map-transcript .active-study-button').count(),0)
   self.assertEqual(self.page.locator('.visual-map-panel>.active-study-action').count(),1)
   shown=self.page.locator('.visual-map-panel>.active-study-action .active-study-count').inner_text()
   self.assertEqual(int(shown.split()[0]),len(entry['ids']))
   parent=set(entry['ids'])
   for child in entry['source'].get('concepts',[]):self.assertTrue(set(self.page.evaluate('s=>ActiveStudy.matching(s)',child)).issubset(parent))
   if m['lesson']==13:
    expected=set(range(1201+(m['block']-1)*50,1251+(m['block']-1)*50))
    self.assertTrue(expected.issubset(parent),f"{m['id']}: faltam {sorted(expected-parent)}")
    if m['block']==2:
     repayment=entry['source']['concepts'][2]
     self.assertEqual(self.page.evaluate('s=>ActiveStudy.profile(s).owners',repayment),['debt-repayment'])
     self.assertTrue(set(range(1201,1211)).isdisjoint(self.page.evaluate('s=>ActiveStudy.matching(s)',repayment)))

if __name__=='__main__':unittest.main(verbosity=2)
