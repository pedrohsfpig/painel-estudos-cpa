"""Aula interna 1 do bloco final: fontes, cálculos e integração de todos os modos."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unittest
from question_revision import questions_before_risk_concept_revision
from validate_bank import load_questions
from final_block import before_private_credit,unit_count
import smoke as harness
ROOT=Path(__file__).resolve().parents[1]
def read(marker):return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split(marker,1)[1])[0]
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
class Content(unittest.TestCase):
 def setUp(self):
  self.q=load_questions();self.bp=read('const BP=');self.al=read('const AL=');self.mat=read('\n13:');self.report=json.loads((ROOT/'docs/aula-13-cobertura.json').read_text())
  self.al,self.mat=before_private_credit(self.al,self.mat)
 def test_half_volumes_preserve_normal_and_hardcore_proportions(self):
  self.assertEqual(Counter(q[2] for q in self.q[1200:1250]),{0:10,1:20,2:10,3:10})
  self.assertEqual(len(self.bp[600:625]),25);self.assertEqual(len(self.mat['fc']),25);self.assertEqual(Counter(c[2] for c in self.mat['fc']),{0:9,1:8,2:8})
  self.assertTrue(self.al[12]['internalLessons']);self.assertEqual(len(self.al[12]['b']),1)
  self.assertEqual({q[0] for q in self.q[1200:]},{13});self.assertTrue(all(q[9]==0 for q in self.q[1200:]))
 def test_sources_and_old_banks_are_preserved_and_every_new_id_is_covered(self):
  for key,rows in [('Q',self.q),('BP',self.bp),('AL',self.al)]:
   old=self.report['bancos_anteriores'][key];self.assertEqual(digest(rows[:old['count']]),old['sha256'])
  html=(ROOT/'index.html').read_text();material_prefix=html[html.index('const MAT='):html.index(',\n13:')]
  self.assertEqual(hashlib.sha256(material_prefix.encode()).hexdigest(),self.report['materiais_anteriores_sha256'])
  self.assertEqual([r['id'] for r in self.report['itens']],list(range(1201,1251)))
  self.assertEqual({i for r in self.report['itens'] for i in r['imagens']},set(range(1,7)))
  authored=questions_before_risk_concept_revision(self.q)
  for r in self.report['itens']:self.assertEqual(digest(authored[r['id']-1]),r['sha256'])
  for r in self.report['bate_pronto']:self.assertEqual(digest(self.bp[r['id']-100001]),r['sha256'])
  for r in self.bp[600:625]:self.assertEqual(self.q[r[7]-1][:2],r[:2])
 def test_aggregates_preserve_every_material_and_causal_conditions(self):
  unit=self.al[12]['b'][0];material=self.mat['b'][0]
  for key in ['r','d','p','n']:self.assertEqual(unit[key],self.al[12][key])
  for key in ['dg','tb','tl','fc']:self.assertEqual(material[key],self.mat[key])
  self.assertEqual(material['mm'][1],self.mat['mm'][1])
  for title,head,rows in self.mat['tb']:self.assertTrue(all(len(r)==len(head) for r in rows),title)
  text=json.dumps([self.mat,unit['d']],ensure_ascii=False)
  for term in ['Taxa de desconto aumenta','Taxa de desconto diminui','Prazo restante aumenta','Taxa de cupom aumenta','condições','não prevê','não são cupons']:self.assertIn(term,text)
 def test_calculations_have_correct_periods_and_explicit_comparison_bases(self):
  self.assertAlmostEqual(1000*1.06**2,1123.6)
  self.assertEqual(round(1123.6/1.08,2),1040.37);self.assertEqual(round(1123.6/1.04,2),1080.38)
  self.assertEqual(round(1060-1123.6/1.08,2),19.63);self.assertEqual(round(1123.6/1.04-1060,2),20.38)
  self.assertEqual(2000000*.08,160000)
  for q in self.q[1200:]:
   self.assertNotRegex(' '.join(q[3:9]+[q[10]]+q[11]),r'(?i)\baula\b|\bslides?\b|professor|transcrição')
   self.assertEqual(len(set(q[11])),4)
  self.assertIn('preço de marcação',self.q[1244][4])
  self.assertNotIn('taxa futura não pode subir',json.dumps(self.mat,ensure_ascii=False))
class Browser(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
 tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp
 tearDown=harness.PainelCPA.tearDown
 click=harness.PainelCPA.click
 answer=harness.PainelCPA.answer
 assert_material_content=harness.PainelCPA.assert_material_content
 def test_every_material_and_internal_reading_scope_remain_accessible(self):
  self.page.evaluate("view='t';tr=13;go()")
  self.assertIn('Riscos Financeiros',self.page.inner_text('#app'))
  self.page.locator('.lesson-blocks [data-lesson-block="1"]').click()
  self.assertEqual(self.page.evaluate('lessonContent(13).id'),1)
  self.assertEqual(self.page.get_by_role('button',name='Estudar esta aula interna',exact=True).count(),1)
  for name,key in [('Mapa mental','mapa'),('Diagramas','diag'),('Tabelas','tab'),('Linha do tempo','tl'),('Flashcards','fc')]:
   self.page.evaluate("k=>{view='m';mt={a:13,c:k};fi=0;ff=0;go()}",key);self.assert_material_content(name)
  self.page.evaluate("mt.c='geral';go()")
  self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),6)
  self.assertEqual(self.page.evaluate('[AU[13],AL[12].t,MAT[13].mm[0]]'),['Aula 13: Bloco Final']*3)
 def test_practice_internal_controls_and_all_modes_have_exact_stock(self):
  for mode,single in [('e',40),('s',40),('h',10),('b',25)]:
   n=single*unit_count()
   self.page.evaluate("md=>{cfg={a:13,as:[],b:0,us:[],md,n:-1,m:'all',c:40};qz=null;view='q';go()}",mode)
   self.assertEqual(self.page.evaluate('pool().length'),n)
   self.page.locator('.practice-blocks [data-lesson-block="1"]').click()
   self.assertEqual(self.page.evaluate('cfg.us'),[1]);self.assertEqual(self.page.evaluate('pool().length'),single)
   self.assertEqual(self.page.evaluate('sessionPlan().n'),min(40,single))
   self.assertEqual(len(set(self.page.evaluate('mix(sessionPlan())'))),min(40,single))
   self.page.locator('.practice-blocks [data-lesson-block="0"]').click();self.assertEqual(self.page.evaluate('cfg.us'),[])
 def test_multiple_internal_units_balance_without_changing_the_real_bank(self):
  original=self.page.evaluate('JSON.stringify([Q,BP,AL])')
  self.page.evaluate("""()=>{window.originalFinalUnits=AL[12].b;const u=AL[12].b[0];AL[12].b=[{...u,id:1,topics:[u.topics[0]]},{...u,id:2,topics:u.topics.slice(1)}];cfg={a:13,as:[],b:0,us:[1,2],md:'e',n:-1,m:'all',c:6};qz=null;view='q';go()}""")
  self.assertEqual(self.page.evaluate('sessionPlan().groups.map(g=>[g.unit,g.count])'),[[1,3],[2,3]])
  self.assertEqual(len(set(self.page.evaluate('mix(sessionPlan())'))),6)
  self.page.locator('.practice-blocks [data-lesson-block="1"]').click()
  self.assertEqual(self.page.evaluate('cfg.us'),[2]);self.assertEqual(self.page.evaluate('sessionPlan().groups.map(g=>g.unit)'),[2])
  self.page.evaluate('AL[12].b=window.originalFinalUnits');self.assertEqual(self.page.evaluate('JSON.stringify([Q,BP,AL])'),original)
 def test_feedback_results_and_history_in_all_four_modes(self):
  for mode,ids in [('e',[1203,1240,1245]),('h',[1209,1248,1250]),('s',[1203,1240,1245]),('b',[100601,100610,100625])]:
   self.page.evaluate("x=>{H=[[1,true,1000,0]];begin(x.ids,x.mode)}",dict(ids=ids,mode=mode))
   for i,id in enumerate(ids):
    self.assertEqual(self.page.locator('.fb-option').count(),0);self.answer(correct=i!=1)
    if mode!='s':
     self.assertEqual(self.page.locator('.fb-option').count(),2 if mode=='b' else 4)
     for row in self.page.locator('.fb-option').all():
      index=int(row.get_attribute('data-option-index'));self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('x=>questionById(x.id)[11][x.index]',dict(id=id,index=index)))
     self.click('Próxima' if i<2 else 'Ver resultado')
   self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'2 de 3 (67%)');self.assertEqual(self.page.evaluate('H[0][0]'),1)
 def test_risk_concepts_do_not_select_unrelated_credit_markets(self):
  rows=self.page.evaluate("""()=>Object.fromEntries([
   ['liquidity',{lesson:13,label:'Liquidez de financiamento',text:'Obter caixa no prazo para honrar compromissos'}],
   ['rating',{lesson:13,label:'Ratings',text:'Agências de classificação de crédito e limites das notas'}],
   ['rates',{lesson:13,label:'Juros e marcação a mercado',text:'Taxa de desconto e preço dos fluxos'}],
   ['spread',{lesson:13,label:'Spread de crédito',text:'Dívida e referência comparável'}]
  ].map(([name,source])=>[name,ActiveStudy.matching(source)]))""")
  for name,ids in rows.items():self.assertTrue(ids,name);self.assertTrue(any(id>=1201 for id in ids),name)
  self.assertIn(1202,rows['liquidity']);self.assertNotIn(1221,rows['liquidity'])
  self.assertIn(1212,rows['rating']);self.assertIn(1240,rows['rates']);self.assertIn(1221,rows['spread']);self.assertNotIn(611,rows['spread'])
  pairs=self.page.evaluate("""()=>[
   {lesson:13,label:'Cupom',text:'Pagamento periódico de juros; cupons maiores antecipam recursos',parents:['Aula 13: Bloco Final','Sensibilidade e condições'],whole:true},
   {lesson:13,label:'Mercado',text:'Negociar um ativo sem desconto significativo sobre o valor justo',parents:['Aula 13: Bloco Final','Liquidez'],whole:true}
  ].map(source=>ActiveStudy.matching(source))""")
  self.assertIn(1238,pairs[0]);self.assertNotIn(1221,pairs[0]);self.assertIn(1203,pairs[1]);self.assertNotIn(1229,pairs[1])
  asset=self.page.evaluate("ActiveStudy.matching({lesson:1,label:'Liquidez',text:'Facilidade de converter um ativo em dinheiro sem perda relevante'})")
  self.assertIn(176,asset);self.assertIn(1201,asset);self.assertIn(1203,asset);self.assertNotIn(1202,asset)
  risk=self.page.evaluate("ActiveStudy.matching({lesson:13,label:'Liquidez de mercado',text:'Negociar sem desconto significativo sobre o valor justo'})")
  self.assertIn(176,risk);self.assertIn(1203,risk)
 def test_new_content_is_in_search_and_daily_without_changing_scope(self):
  rows=self.page.evaluate('dailyPlan(dailyDate()).ids.map(id=>questionById(id))')
  self.assertEqual(Counter(q[2] for q in rows),{0:5,1:10,2:5});self.assertEqual({q[0] for q in rows},set(range(1,14)))
  self.assertTrue(self.page.evaluate("contentSearchIndex().some(r=>r.lesson===13)"))
 def test_layout_and_compact_actions_fit_both_themes(self):
  out=Path('/tmp/cpa-aula13/screens');out.mkdir(exist_ok=True)
  for theme in ['dark','light']:
   self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
   for width in [390,1280,1920]:
    self.page.set_viewport_size(dict(width=width,height=1000))
    for key in ['mapa','diag','tab','geral','tl','fc']:
     self.page.evaluate("k=>{view='m';mt={a:13,c:k};selectedLessonBlocks[13]=0;fi=0;ff=0;go()}",key)
     self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(theme,width,key))
     self.assertEqual(self.page.locator('.mind-node .active-study-button,.diagram-step .active-study-button').count(),0)
    if width==1280:
     self.page.evaluate("mt.c='mapa';go()");self.page.screenshot(path=str(out/f'map-{theme}.png'),full_page=True)
if __name__=='__main__':unittest.main(verbosity=2)
