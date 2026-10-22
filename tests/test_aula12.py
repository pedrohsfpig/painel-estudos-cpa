"""Aula 12: fontes, proporções, conceitos financeiros e fluxos reais; sem certificação normativa."""
from collections import Counter
import json
from pathlib import Path
import re
import unittest
from validate_bank import load_questions,validate_questions
from question_revision import digest
import smoke as harness
ROOT=Path(__file__).resolve().parents[1]
def content(marker):return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split(marker,1)[1])[0]
class Aula12Content(unittest.TestCase):
 def setUp(self):
  self.all=load_questions();self.rows=self.all[1100:1200];self.bp=content('const BP=');self.al=content('const AL=');self.mat=content('\n12:');self.report=json.loads((ROOT/'docs/aula-12-cobertura.json').read_text())
 def test_requested_allocation_rounding_and_difficulties(self):
  self.assertEqual(len(self.rows),100);self.assertEqual(Counter(q[2] for q in self.rows),{0:20,1:40,2:20,3:20});self.assertTrue(validate_questions(self.all))
  for b,n,levels in zip(self.al[11]['b'],[43,15,42],[[9,17,8,9],[3,6,3,3],[8,17,9,8]]):
   group=[q for q in self.rows if q[1] in b['topics']];self.assertEqual(len(group),n);self.assertEqual(Counter(q[2] for q in group),dict(enumerate(levels)))
  for b,n in zip(self.al[11]['b'],[21,8,21]):self.assertEqual(sum(x[1] in b['topics'] for x in self.bp[550:600]),n)
  self.assertEqual({q[0] for q in self.rows},{12});self.assertTrue(all(q[9]==0 for q in self.rows))
 def test_all_sources_and_items_are_traced(self):
  self.assertEqual({p for c in self.report['cobertura'] for p in c['slides']},set(range(1,26)));self.assertEqual({c['transcricao'] for c in self.report['cobertura']},{19,20,21})
  self.assertEqual([r['id'] for r in self.report['questoes']],list(range(1101,1201)))
  for r in self.report['questoes']:self.assertEqual(digest(self.all[r['id']-1]),r['hash']);self.assertTrue(r['slides'])
  for r in self.report['bate_pronto']:self.assertEqual(digest(self.bp[r['id']-100001]),r['hash'])
  self.assertFalse(self.report['consulta_normativa']['certificacao_de_vigencia']);self.assertEqual(self.report['trilha_sha256'],digest(self.al[11]));self.assertEqual(self.report['materiais_sha256'],digest(self.mat))
 def test_previous_banks_are_unchanged(self):
  p=self.report['preservacao'];self.assertEqual(digest(self.all[:1100]),p['hash_primeiras_1100']);self.assertEqual(digest(self.bp[:550]),p['hash_primeiros_550_bp']);self.assertEqual(digest(self.al[:11]),p['hash_aulas_1_a_11'])
 def test_blocks_aggregate_and_materials_have_consistent_cells(self):
  for k in ['r','d','p','n']:self.assertEqual(self.al[11][k],sum((b[k] for b in self.al[11]['b']),[]))
  for k in ['dg','tb','tl','fc']:self.assertEqual(self.mat[k],sum((b[k] for b in self.mat['b']),[]))
  self.assertEqual(self.mat['mm'][1],sum((b['mm'][1] for b in self.mat['b']),[]));self.assertEqual(len(self.mat['fc']),50)
  self.assertEqual(len(self.mat['tb']),19);self.assertEqual(len(self.mat['dg']),11)
  for title,head,rows in self.mat['tb']:self.assertTrue(all(len(r)==len(head) for r in rows),title)
 def test_slide24_and25_chains_keep_assumptions_in_both_locations(self):
  tables={t:r for t,h,r in self.mat['tb']};interest=tables['Juros internos e externos: associações dos slides 24 e 25'];risk=tables['Diferencial de juros e prêmio de risco: hipóteses distintas']
  self.assertEqual(len(interest),4)
  for row,fx,currency in zip(interest,['↓','↑','↑','↓'],['apreciado','depreciado','depreciado','apreciado']):
   self.assertIn(fx,row[2]);self.assertIn(currency,row[3]);self.assertIn('constantes',row[5])
  self.assertIn('risco percebido',risk[2][0]);self.assertIn('saída',risk[2][1]);self.assertIn('não há apreciação automática',risk[2][2]);self.assertIn('pontos percentuais',risk[3][2])
  tips=' '.join(self.al[11]['b'][2]['d'])
  for x in ['Juros internos ↑','Juros externos ↑','Juros internos ↓','Juros externos ↓','importações','exportações','risco constante','risco maior']:self.assertIn(x,tips)
 def test_numbers_and_liquidation_are_reconciled(self):
  text=json.dumps([self.al[11],self.mat],ensure_ascii=False)
  for phrase in ['US$ 100 mil','US$ 300 mil','R$ 10 mil','vigência não certificada','9,28%','−7,27%','+7,84%','−1,29%','sem entrega do principal em dólares','7 pontos percentuais']:self.assertIn(phrase.casefold(),text.casefold())
  self.assertAlmostEqual((1.1365/1.04-1)*100,9.2788461538);self.assertAlmostEqual((306/310-1)*100,-1.2903225806)
  for q in self.rows:
   self.assertNotRegex(' '.join(q[3:9]+[q[10]]+q[11]),r'(?i)\baula\b|\bslides?\b|professor|transcrição')
   if re.search(r'\bI\. ',q[3]):self.assertEqual(len(re.findall(r'^[IVX]+\. ',q[3],re.M)),4)
  self.assertIn('2,61%',self.all[1155][4]);self.assertIn('pagadora',self.all[1156][4])
class Aula12Browser(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
 tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp
 tearDown=harness.PainelCPA.tearDown
 click=harness.PainelCPA.click
 answer=harness.PainelCPA.answer
 assert_material_content=harness.PainelCPA.assert_material_content
 def test_blocks_and_every_material_text_remain_accessible(self):
  self.page.evaluate("view='t';tr=12;go()")
  for d in self.page.locator('details.lesson-section').all():d.evaluate('n=>n.open=true')
  for b in [1,2,3,0]:
   self.page.locator(f'button[data-lesson-block="{b}"]').click();self.assertTrue(self.page.locator('details.lesson-section').evaluate_all('es=>es.every(e=>e.open)'))
  self.page.evaluate("mt.a=12;view='m';go()")
  for b in [1,2,3,0]:
   self.page.evaluate('b=>chooseLessonBlock(12,b)',b)
   for name,key in [('Mapa mental','mapa'),('Diagramas','diag'),('Tabelas','tab'),('Linha do tempo','tl'),('Flashcards','fc')]:
    self.page.evaluate('k=>{mt.c=k;go()}',key);self.assert_material_content(name)
 def test_feedback_and_results_for_all_four_modes(self):
  for mode,ids in [('e',[1106,1148,1186]),('h',[1135,1157,1195]),('b',[100551,100576,100600]),('s',[1104,1150,1189])]:
   self.page.evaluate('x=>{H=[[1,1,1700000000000,0]];begin(x.ids,x.mode)}',dict(ids=ids,mode=mode))
   for i,id in enumerate(ids):
    self.assertEqual(self.page.locator('.fb-option').count(),0);self.answer(correct=i!=1);self.assertEqual(self.page.evaluate('H.at(-1)[0]'),id)
    if mode!='s':
     self.assertEqual(self.page.locator('.fb-option').count(),2 if mode=='b' else 4)
     for row in self.page.locator('.fb-option').all():
      index=int(row.get_attribute('data-option-index'));self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('x=>questionById(x.id)[11][x.i]',dict(id=id,i=index)))
     self.click('Próxima' if i<2 else 'Ver resultado')
   self.assertEqual(self.page.evaluate('H[0][0]'),1);self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'2 de 3 (67%)')
 def test_daily_covers_all_lessons_and_practice_respects_block_and_mode(self):
  rows=self.page.evaluate('dailyPlan(dailyDate()).ids.map(id=>questionById(id))');self.assertEqual(len(rows),20);self.assertEqual(Counter(r[2] for r in rows),{0:5,1:10,2:5});self.assertEqual({r[0] for r in rows},set(range(1,self.page.evaluate('AL.length')+1)))
  counts=Counter(r[0] for r in rows);self.assertLessEqual(max(counts.values())-min(counts.values()),1)
  for b,n in [(1,34),(2,12),(3,34)]:self.assertEqual(self.page.evaluate('b=>{cfg={a:12,as:[],n:-1,m:"all",c:20,md:"e",b};return pool().length}',b),n)
  for mode in ['e','h','b','s']:
   self.page.evaluate('md=>{cfg={a:0,as:[10,11,12],n:-1,m:"all",c:30,md,b:0}}',mode);self.assertEqual(Counter(self.page.evaluate('mix(sessionPlan()).map(id=>questionById(id)[0])')),{10:10,11:10,12:10})
 def test_acronym_census_and_previous_material_integrity(self):
  result=self.page.evaluate('''()=>{const before=JSON.stringify([Q,BP,H]);let checked=0;for(const q of [...Q.slice(1100,1200),...BP_Q.slice(550,600)]){const d=questionDisplay(q),a=questionDisplay(q,true),names=new Map();for(const text of [q[3],...questionOptions(q).map(o=>o[0])])for(const m of text.matchAll(new RegExp(acronymPattern,'giu'))){const e=acronymAliases.get(m[1].toLocaleLowerCase('pt-BR'));names.set(e.id,acronymMeaning(e,q))}for(const [id,name] of names){const displayed=d.deferred.includes(id)?a:d;if(!(displayed.stem+' '+displayed.options.join(' ')).includes(name))throw Error('Nome ausente: '+q[3]+' '+name)}checked++}return {checked,unchanged:before===JSON.stringify([Q,BP,H])}}''');self.assertEqual(result['checked'],150);self.assertTrue(result['unchanged'])
  report=json.loads((ROOT/'docs/aula-12-cobertura.json').read_text());p=report['preservacao']
  actual=self.page.evaluate('(()=>{const {groups,...data}=LESSON_OVERVIEWS[12];return data})()');self.assertEqual(digest(actual),report['comparativo_sha256'])
  self.assertEqual(self.page.evaluate('[AU[12],AL[11].t,MAT[12].mm[0]]'),[report['titulo']]*3)
  for i in range(1,12):self.assertEqual(digest(self.page.evaluate(f'MAT[{i}]')),p['materiais_1_a_11'][str(i)])
  self.page.evaluate('begin([1106],"e")');self.assertEqual(self.page.locator('.acronym-expansion').count(),0);self.answer();self.assertGreater(self.page.locator('.acronym-expansion').count(),0)
  self.page.evaluate('begin([1117],"e")');self.assertIn('ACC (Adiantamento sobre Contrato de Câmbio)',self.page.locator('.en').inner_text())
 def test_overview_filters_both_themes_and_desktop_widths(self):
  Path('/tmp/cpa-aula12').mkdir(exist_ok=True)
  for theme in ['light','dark']:
   self.page.evaluate('t=>{document.documentElement.dataset.theme=t;mt.a=12;view="m";mt.c="geral";selectedLessonBlocks[12]=0;go()}',theme)
   self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),19);self.assertEqual(self.page.locator('#overview-scroll thead th').count(),6)
   for b,n in [(1,11),(2,3),(3,5)]:
    self.page.evaluate('b=>chooseLessonBlock(12,b)',b);self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),n)
   for width in [1024,1280,1920]:
    self.page.set_viewport_size(dict(width=width,height=900))
    for key in ['geral','mapa','diag','tab','tl','fc']:
     self.page.evaluate('k=>{mt.c=k;go()}',key);self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(theme,width,key))
   self.page.evaluate('chooseLessonBlock(12,0);mt.c="mapa";go()');self.page.screenshot(path=f'/tmp/cpa-aula12/mapa-{theme}.png',full_page=True)
   self.page.evaluate('mt.c="geral";go()');self.page.screenshot(path=f'/tmp/cpa-aula12/quadro-{theme}.png',full_page=True)
if __name__=='__main__':unittest.main(verbosity=2)
