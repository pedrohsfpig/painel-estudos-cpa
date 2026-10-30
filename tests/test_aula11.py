"""Aula 11: proporções solicitadas, cobertura, conceitos e integração; não certificação normativa."""
from collections import Counter
import json
from pathlib import Path
import re
import unittest
from validate_bank import load_questions,validate_questions
from question_revision import digest
from numbers_revision import restore_before_numbers
import smoke as harness
ROOT=Path(__file__).resolve().parents[1]
def content(marker):return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split(marker,1)[1])[0]
class Aula11Content(unittest.TestCase):
 def setUp(self):
  self.all=load_questions();self.rows=self.all[1000:1100];self.bp=content('const BP=');self.al=content('const AL=');self.mat=content('\n11:');self.report=json.loads((ROOT/'docs/aula-11-cobertura.json').read_text())
 def test_quantities_difficulties_and_60_30_10_within_each_level(self):
  self.assertEqual(len(self.rows),100);self.assertEqual(Counter(q[2] for q in self.rows),{0:20,1:40,2:20,3:20})
  self.assertTrue(validate_questions(self.all))
  for b,n in zip(self.al[10]['b'],[10,30,60]):
   group=[q for q in self.rows if q[1] in b['topics']]
   self.assertEqual(len(group),n);self.assertEqual(Counter(q[2] for q in group),{0:n//5,1:n*2//5,2:n//5,3:n//5})
  for b,n in zip(self.al[10]['b'],[5,15,30]):self.assertEqual(sum(x[1] in b['topics'] for x in self.bp[500:550]),n)
  self.assertEqual({q[0] for q in self.rows},{11});self.assertTrue(all(q[9]==0 for q in self.rows))
 def test_all_sources_are_mapped_and_every_new_item_is_traced(self):
  self.assertEqual({p for c in self.report['cobertura'] for p in c['slides']},set(range(1,15)))
  self.assertEqual({c['transcricao'] for c in self.report['cobertura']},{16,18,22})
  self.assertEqual([r['id'] for r in self.report['questoes']],list(range(1001,1101)))
  for r in self.report['questoes']:self.assertEqual(digest(self.all[r['id']-1]),r['hash'])
  for r in self.report['bate_pronto']:self.assertEqual(digest(self.bp[r['id']-100001]),r['hash'])
  self.assertFalse(self.report['consulta_normativa']['certificacao_de_vigencia'])
  self.assertEqual(self.report['trilha_sha256'],digest(self.al[10]));self.assertEqual(self.report['materiais_sha256'],digest(self.mat))
 def test_previous_ids_answers_feedbacks_and_reading_are_preserved(self):
  p=self.report['preservacao'];self.assertEqual(digest(self.all[:1000]),p['hash_primeiras_1000']);self.assertEqual(digest(self.bp[:500]),p['hash_primeiros_500_bp']);self.assertEqual(digest(restore_before_numbers(self.al)[:10]),p['hash_aulas_1_a_10'])
 def test_materials_aggregate_all_blocks_and_preserve_table_cells(self):
  for k in ['r','d','p','n']:self.assertEqual(self.al[10][k],sum((b[k] for b in self.al[10]['b']),[]))
  for k in ['dg','tb','tl','fc']:self.assertEqual(self.mat[k],sum((b[k] for b in self.mat['b']),[]))
  self.assertEqual(self.mat['mm'][1],sum((b['mm'][1] for b in self.mat['b']),[]))
  self.assertEqual(len(self.mat['fc']),50)
  for title,head,rows in self.mat['tb']:self.assertTrue(all(len(r)==len(head) for r in rows),title)
 def test_financial_distinctions_and_historical_references_are_explicit(self):
  text=json.dumps([self.al[10],self.mat],ensure_ascii=False)
  for phrase in ['Déficit: fluxo','Dívida: estoque','7,61% é exemplo','60% IPA','LC 200/2023','não atua como contraparte central','rendimento misto bruto']:
   self.assertIn(phrase.casefold(),text.casefold())
  for q in self.rows:
   self.assertNotRegex(' '.join(q[3:9]+[q[10]]+q[11]),r'(?i)\baula\b|\bslides?\b|professor|transcrição')
   if re.search(r'\bI\. ',q[3]):self.assertEqual(len(re.findall(r'^[IVX]+\. ',q[3],re.M)),4)
  # A ponderação não é fornecida no desafio que exige conhecê-la.
  self.assertNotIn('60%',self.all[1078][3]);self.assertIn('0,9%',self.all[1078][11][0])
  self.assertFalse(any('20 anos' in q[4] for q in self.rows))
class Aula11Browser(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
 tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp
 tearDown=harness.PainelCPA.tearDown
 click=harness.PainelCPA.click
 answer=harness.PainelCPA.answer
 assert_material_content=harness.PainelCPA.assert_material_content
 def test_blocks_keep_sections_open_and_all_material_text_accessible(self):
  self.page.evaluate("view='t';tr=11;go()")
  for d in self.page.locator('details.lesson-section').all():d.evaluate('n=>n.open=true')
  for block in [1,2,3,0]:
   self.page.locator(f'button[data-lesson-block="{block}"]').click()
   self.assertTrue(self.page.locator('details.lesson-section').evaluate_all('es=>es.every(e=>e.open)'))
  self.page.evaluate("mt.a=11;view='m';go()")
  for block in [1,2,3,0]:
   self.page.evaluate('b=>chooseLessonBlock(11,b)',block)
   for name,key in [('Ramificações','mapa'),('Diagramas','diag'),('Tabelas','tab'),('Linha do tempo','tl'),('Flashcards','fc')]:
    self.page.evaluate('k=>{mt.c=k;go()}',key);self.assert_material_content(name)
 def test_feedback_answers_history_and_results_in_all_modes(self):
  for mode,ids in [('e',[1001,1018,1070]),('h',[1009,1039,1099]),('b',[100501,100527,100550]),('s',[1001,1021,1042])]:
   self.page.evaluate('x=>{H=[[1,1,1700000000000,0]];begin(x.ids,x.mode)}',dict(ids=ids,mode=mode))
   for i,id in enumerate(ids):
    self.assertEqual(self.page.locator('.fb-option').count(),0);self.answer(correct=i!=1)
    self.assertEqual(self.page.evaluate('H.at(-1)[0]'),id)
    if mode!='s':
     self.assertEqual(self.page.locator('.fb-option').count(),2 if mode=='b' else 4)
     for row in self.page.locator('.fb-option').all():
      index=int(row.get_attribute('data-option-index'));self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('x=>questionById(x.id)[11][x.i]',dict(id=id,i=index)))
     self.click('Próxima' if i<2 else 'Ver resultado')
   self.assertEqual(self.page.evaluate('H[0][0]'),1)
   self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'2 de 3 (67%)')
 def test_eleven_lesson_daily_plan_and_block_practice_keep_allocation(self):
  daily=self.page.evaluate('dailyPlan(dailyDate())');self.assertEqual(len(daily['ids']),20);self.assertEqual(len(set(daily['ids'])),20)
  rows=self.page.evaluate('dailyPlan(dailyDate()).ids.map(id=>questionById(id))')
  self.assertEqual(Counter(r[2] for r in rows),{0:5,1:10,2:5});self.assertEqual({r[0] for r in rows},set(range(1,self.page.evaluate('AL.length')+1)))
  counts=Counter(r[0] for r in rows);self.assertLessEqual(max(counts.values())-min(counts.values()),1)
  for b,n in [(1,8),(2,24),(3,48)]:self.assertEqual(self.page.evaluate('b=>{cfg={a:11,as:[],n:-1,m:"all",c:20,md:"e",b};return pool().length}',b),n)
  for mode in ['e','h','b','s']:
   self.page.evaluate('md=>{cfg={a:0,as:[9,10,11],n:-1,m:"all",c:30,md,b:0}}',mode)
   self.assertEqual(Counter(self.page.evaluate('mix(sessionPlan()).map(id=>questionById(id)[0])')),{9:10,10:10,11:10})
 def test_all_150_new_items_show_acronyms_without_mutating_banks_or_history(self):
  result=self.page.evaluate('''()=>{const before=JSON.stringify([Q,BP,H]);let checked=0;for(const q of [...Q.slice(1000,1100),...BP_Q.slice(500,550)]){const d=questionDisplay(q),a=questionDisplay(q,true),names=new Map();for(const text of [q[3],...questionOptions(q).map(o=>o[0])])for(const m of text.matchAll(new RegExp(acronymPattern,'giu'))){const e=acronymAliases.get(m[1].toLocaleLowerCase('pt-BR'));names.set(e.id,acronymMeaning(e,q))}for(const [id,name] of names){const displayed=d.deferred.includes(id)?a:d;if(!(displayed.stem+' '+displayed.options.join(' ')).includes(name))throw Error('Definição ausente: '+q[3]+' '+name)}checked++}return {checked,unchanged:before===JSON.stringify([Q,BP,H])}}''')
  self.assertEqual(result['checked'],150);self.assertTrue(result['unchanged'])
 def test_overview_filters_themes_desktop_and_acronym_visibility(self):
  for theme in ['light','dark']:
   self.page.evaluate('t=>{document.documentElement.dataset.theme=t;mt.a=11;view="m";mt.c="geral";selectedLessonBlocks[11]=0;go()}',theme)
   self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),14)
   self.assertEqual(self.page.locator('#overview-scroll thead th').count(),6)
   for b,n in [(1,2),(2,5),(3,7)]:
    self.page.evaluate('b=>chooseLessonBlock(11,b)',b);self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),n)
   for width in [1024,1280,1920]:
    self.page.set_viewport_size(dict(width=width,height=900))
    for key in ['geral','mapa','diag','tab','tl','fc']:
     self.page.evaluate('k=>{mt.c=k;go()}',key);self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(theme,width,key))
   self.page.evaluate('chooseLessonBlock(11,0);mt.c="mapa";go()');self.page.screenshot(path=f'/tmp/cpa-aula11/mapa-{theme}.png',full_page=True)
   self.page.evaluate('mt.c="geral";go()');self.page.screenshot(path=f'/tmp/cpa-aula11/quadro-{theme}.png',full_page=True)
  self.page.evaluate('begin([1093],"e")');self.assertIn('TBF (Taxa Básica Financeira)',self.page.locator('.en').inner_text())
  self.page.evaluate('begin([1041],"e")');self.assertEqual(self.page.locator('.acronym-expansion').count(),0);self.answer();self.assertGreater(self.page.locator('.acronym-expansion').count(),0)
if __name__=='__main__':unittest.main(verbosity=2)
