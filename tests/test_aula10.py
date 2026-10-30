"""Cobertura das fontes e integração da aula 10; não certifica vigência normativa."""
from collections import Counter
import json
from pathlib import Path
import re
import unittest
from validate_bank import load_questions,validate_questions
from question_revision import digest
import smoke as harness
ROOT=Path(__file__).resolve().parents[1]
def content(marker):
 return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split(marker,1)[1])[0]
class Aula10Content(unittest.TestCase):
 def setUp(self):
  self.q=load_questions();self.bp=content('const BP=');self.al=content('const AL=')
  self.mat=content('\n10:');self.report=json.loads((ROOT/'docs/aula-10-cobertura.json').read_text())
 def test_counts_difficulties_and_unique_block_mapping(self):
  self.assertGreaterEqual(len(self.q),1000);self.assertGreaterEqual(len(self.bp),500);self.assertGreaterEqual(len(self.al),10)
  self.assertEqual(Counter(q[2] for q in self.q[900:1000]),{0:20,1:40,2:20,3:20})
  for b,count in zip(self.al[9]['b'],[30,30,40]):
   rows=[q for q in self.q[900:1000] if q[1] in b['topics']];self.assertEqual(len(rows),count)
   self.assertEqual(Counter(q[2] for q in rows),{0:count//5,1:count*2//5,2:count//5,3:count//5})
  self.assertTrue(validate_questions(self.q))
 def test_source_coverage_and_exact_provenance(self):
  self.assertEqual({p for c in self.report['cobertura'] for p in c['slides']},set(range(1,14)))
  self.assertEqual({c['transcricao'] for c in self.report['cobertura']},{1,2,3})
  self.assertEqual([c['id'] for c in self.report['questoes']],list(range(901,1001)))
  for c in self.report['questoes']:self.assertEqual(c['hash'],digest(self.q[c['id']-1]))
  for c in self.report['bate_pronto']:self.assertEqual(c['hash'],digest(self.bp[c['id']-100001]))
  self.assertFalse(self.report['consulta_normativa']['certificacao_de_vigencia'])
 def test_existing_questions_and_reading_are_unchanged(self):
  p=self.report['preservacao']
  self.assertEqual(digest(self.q[:900]),p['hash_primeiras_900'])
  self.assertEqual(digest(self.bp[:450]),p['hash_primeiros_450_bp'])
  self.assertEqual(digest(self.al[:9]),p['hash_aulas_1_a_9'])
 def test_materials_aggregate_all_blocks_without_loss(self):
  for key in ['r','d','p','n']:self.assertEqual(self.al[9][key],sum((b[key] for b in self.al[9]['b']),[]))
  for key in ['dg','tb','tl','fc']:self.assertEqual(self.mat[key],sum((b[key] for b in self.mat['b']),[]))
  self.assertEqual(self.mat['mm'][1],sum((b['mm'][1] for b in self.mat['b']),[]))
  for title,headers,rows in self.mat['tb']:
   self.assertTrue(all(len(r)==len(headers) for r in rows),title)
  self.assertEqual(len(self.mat['fc']),50)
 def test_distinctions_are_not_erased_by_transcription_errors(self):
  text=json.dumps(self.mat,ensure_ascii=False)
  for phrase in ['Não atua como contraparte central','10% não representa alíquota vigente','restrições de capital','1 presidente + 8 diretores do BACEN','8 diretores do BACEN','45 dias úteis','cestas A e B']:
   self.assertIn(phrase.lower(),text.lower())
  for q in self.q[900:1000]:
   self.assertNotRegex(' '.join(q[3:9]+[q[10]]+q[11]),r'(?i)\baula\b|\bslides?\b|segundo o professor')
  # Perguntas com afirmações têm uma por linha, sem confundir algarismos e texto corrido.
  for q in self.q[900:1000]:
   if re.search(r'\bI\. ',q[3]):self.assertEqual(len(re.findall(r'^[IVX]+\. ',q[3],re.M)),4)

class Aula10Browser(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
 tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp
 tearDown=harness.PainelCPA.tearDown
 click=harness.PainelCPA.click
 answer=harness.PainelCPA.answer
 assert_material_content=harness.PainelCPA.assert_material_content
 def test_blocks_retain_open_sections_and_all_material_text(self):
  self.page.evaluate("view='t';tr=10;go()")
  for detail in self.page.locator('details.lesson-section').all():detail.evaluate('e=>e.open=true')
  for block in [1,2,3,0]:
   self.page.locator(f'button[data-lesson-block="{block}"]').click()
   self.assertTrue(self.page.locator('details.lesson-section').evaluate_all('es=>es.every(e=>e.open)'))
  self.page.evaluate("mt.a=10;view='m';go()")
  for block in [1,2,3,0]:
   self.page.evaluate('b=>chooseLessonBlock(10,b)',block)
   for name,key in [('Ramificações','mapa'),('Diagramas','diag'),('Tabelas','tab'),('Linha do tempo','tl'),('Flashcards','fc')]:
    self.page.evaluate('k=>{mt.c=k;go()}',key)
    self.assertEqual(self.page.evaluate('currentMaterial()===MAT[10]'),block==0)
    if block:self.assertEqual(self.page.evaluate('currentMaterial().id'),block)
    self.assert_material_content(name)
 def test_new_feedback_and_history_use_original_indices_in_all_modes(self):
  for mode,ids in [('e',[917,948,985]),('h',[993,995,1000]),('b',[100451,100481,100498]),('s',[901,950,990])]:
   self.page.evaluate('x=>{H=[[1,1,1700000000000,0]];begin(x.ids,x.mode)}',dict(ids=ids,mode=mode))
   for i,id in enumerate(ids):
    self.assertEqual(self.page.locator('.fb-option').count(),0)
    self.answer(correct=i%2==0)
    self.assertEqual(self.page.evaluate('H.at(-1)[0]'),id)
    if mode!='s':
     self.assertEqual(self.page.locator('.fb-option').count(),2 if mode=='b' else 4)
     for row in self.page.locator('.fb-option').all():
      index=int(row.get_attribute('data-option-index'))
      self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('x=>questionById(x.id)[11][x.index]',dict(id=id,index=index)))
     self.click('Próxima' if i<2 else 'Ver resultado')
    else:self.assertEqual(self.page.locator('.fb-option').count(),0)
   self.assertEqual(self.page.evaluate('H[0][0]'),1)
 def test_ten_lesson_daily_and_multi_lesson_selection_keep_ratios(self):
  self.assertEqual(self.page.evaluate('dailyPlan(dailyDate()).ids.length'),20)
  counts=self.page.evaluate('dailyPlan(dailyDate()).groups.map(g=>g.count)');self.assertEqual(len(counts),self.page.evaluate('AL.length'));self.assertEqual(sum(counts),20);self.assertLessEqual(max(counts)-min(counts),1)
  for mode in ['e','h','b','s']:
   self.page.evaluate('mode=>{cfg={a:0,as:[8,9,10],n:-1,m:"all",c:30,md:mode,b:0}}',mode)
   rows=self.page.evaluate('mix(sessionPlan()).map(id=>questionById(id))')
   self.assertEqual(Counter(q[0] for q in rows),{8:10,9:10,10:10})
  self.assertEqual(self.page.evaluate('cfg.md="e";cfg.as=[];cfg.a=10;cfg.b=3;pool().length'),32)
 def test_overview_composition_and_desktop_fit_both_themes(self):
  for theme in ['light','dark']:
   self.page.evaluate('t=>{document.documentElement.dataset.theme=t;mt.a=10;view="m";selectedLessonBlocks[10]=0;mt.c="geral";go()}',theme)
   self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),12)
   for block,n in [(1,4),(2,3),(3,5)]:
    self.page.evaluate('b=>chooseLessonBlock(10,b)',block)
    self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),n)
   self.page.evaluate("mt.c='mapa';go()")
   chart=self.page.locator('.collegiate-chart[data-organ="Comef"]')
   self.assertEqual(chart.count(),1)
   self.assertIn('Presidente do BACEN',chart.locator('.collegiate-leader').inner_text())
   self.assertEqual(chart.locator('.collegiate-peer').count(),8)
   self.assertTrue(all('Diretor do BACEN' in t for t in chart.locator('.collegiate-peer').all_inner_texts()))
   for width in [1024,1280,1920]:
    self.page.set_viewport_size(dict(width=width,height=900))
    for key in ['geral','mapa','diag','tab','tl','fc']:
     self.page.evaluate('k=>{mt.c=k;go()}',key)
     self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(theme,width,key))
    if width==1280:
     self.page.evaluate("mt.c='mapa';go()")
     self.page.screenshot(path=f'/tmp/cpa-aula10-{theme}-mapa.png',full_page=True)
     self.page.evaluate("mt.c='geral';go()")
     self.page.screenshot(path=f'/tmp/cpa-aula10-{theme}-quadro.png',full_page=True)
if __name__=='__main__':unittest.main(verbosity=2)
