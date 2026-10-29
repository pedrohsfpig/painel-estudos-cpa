"""Fluxo de Pagamentos: terceira aula interna, datas, sinais e equivalência."""
from collections import Counter
from decimal import Decimal,ROUND_HALF_UP
import json,re,unittest
from pathlib import Path
from validate_bank import load_questions
from question_revision import digest
import smoke as harness
ROOT=Path(__file__).resolve().parents[1]
def read(marker):return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split(marker,1)[1])[0]

class Content(unittest.TestCase):
 def setUp(self):
  self.q=load_questions();self.bp=read('const BP=');self.al=read('const AL=');self.m=read('\n13:');self.r=json.loads((ROOT/'docs/aula-13-fluxos-cobertura.json').read_text())
 def test_internal_half_volumes_stable_ids_and_source_order(self):
  self.assertEqual([u['id'] for u in self.al[12]['b']],[1,2,3])
  self.assertEqual([len(self.q),len(self.bp),len(self.al)],[1350,675,13])
  for unit in self.al[12]['b']:
   rows=[q for q in self.q if q[0]==13 and q[1] in unit['topics']]
   self.assertEqual(Counter(r[2] for r in rows),{0:10,1:20,2:10,3:10})
   self.assertEqual(len([r for r in self.bp if r[0]==13 and r[1] in unit['topics']]),25)
  self.assertEqual(Counter(r[2] for r in self.m['b'][2]['fc']),{0:9,1:8,2:8})
  self.assertEqual(self.r['fontes']['ordem_confirmada_pelo_usuario'],['Fluxo de Pagamentos','Fluxo de Caixa'])
  self.assertEqual(len(self.r['fontes']['complementos']),3)
 def test_previous_banks_units_aggregates_and_every_authored_hash(self):
  p=self.r['preservacao']
  self.assertEqual(digest(self.q[:1300]),p['Q']['sha256']);self.assertEqual(digest(self.bp[:650]),p['BP']['sha256'])
  self.assertEqual(digest(self.al[:12]),p['AL_1_12'])
  self.assertEqual(digest(self.al[12]['b'][:2]),p['unidades_AL']);self.assertEqual(digest(self.m['b'][:2]),p['unidades_MAT'])
  self.assertEqual([r['id'] for r in self.r['itens']],list(range(1301,1351)))
  self.assertEqual(len({r['angulo'] for r in self.r['itens']}),50)
  for row in self.r['itens']:self.assertEqual(digest(self.q[row['id']-1]),row['sha256'])
  for row in self.r['bate_pronto']:self.assertEqual(digest(self.bp[row['id']-100001]),row['sha256'])
  for key in ['r','d','p','n']:self.assertEqual(self.al[12][key],[r for u in self.al[12]['b'] for r in u[key]])
  for key in ['dg','tb','tl','fc']:self.assertEqual(self.m[key],[r for u in self.m['b'] for r in u[key]])
 def test_new_questions_are_not_copies_arithmetic_only_or_unsupported_sac_tax_tables(self):
  rows=self.q[1300:]
  self.assertEqual(len({r[3] for r in rows}),50)
  for q in rows:
   self.assertNotIn(q[3],[r[3] for r in self.q[:1300]])
   self.assertEqual(len(set(q[11])),4);self.assertEqual(q[9],0)
   self.assertNotRegex(q[3],r'(?i)\baula\b|slides?|professor|calcule|quanto (?:é|resulta)')
   self.assertFalse(any(re.fullmatch(r'R\$\s*[\d.,]+\.?',o) for o in q[4:8]))
   self.assertNotRegex(' '.join(q[3:8]),r'(?i)\bSAC\b|\bPRICE\b|tabela regressiva|22,5%|15%|\bTIR\b|payback')
  for r in self.bp[650:]:
   self.assertLessEqual(len(r[2].split()),12);self.assertLessEqual(max(len(o.split()) for o in r[3:5]),10)
   self.assertEqual(self.q[r[7]-1][:2],r[:2])
 def test_financial_examples_have_verified_periods_values_and_qualifiers(self):
  self.assertEqual(Decimal('2000')*Decimal('1.05')**2,Decimal('2205.0000'))
  self.assertEqual(Decimal('1050')/Decimal('1.05'),1000)
  self.assertEqual(Decimal('1102.50')/Decimal('1.05')**2,1000)
  pv=Decimal('2205')/Decimal('1.06')**2
  self.assertEqual(pv.quantize(Decimal('.01'),rounding=ROUND_HALF_UP),Decimal('1962.44'))
  self.assertEqual((pv-2000).quantize(Decimal('.01'),rounding=ROUND_HALF_UP),Decimal('-37.56'))
  text=json.dumps(self.m['b'][2],ensure_ascii=False)
  for term in ['1.962,44','37,56','regime composto','projetado','perspectiva','não significa','tribut']:
   self.assertIn(term,text)
  for title,head,rows in self.m['b'][2]['tb']:self.assertTrue(all(len(r)==len(head) for r in rows),title)

class Browser(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
 tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp;tearDown=harness.PainelCPA.tearDown
 answer=harness.PainelCPA.answer;click=harness.PainelCPA.click;assert_material_content=harness.PainelCPA.assert_material_content
 def test_real_third_unit_and_complete_block_balance_in_every_mode(self):
  for mode,single,total in [('e',40,120),('s',40,120),('h',10,30),('b',25,75)]:
   self.page.evaluate("md=>{cfg={a:13,as:[],b:0,us:[],md,n:-1,m:'all',c:30};qz=null;view='q';go()}",mode)
   self.assertEqual(self.page.evaluate('pool().length'),total)
   self.assertEqual({g[0] for g in self.page.evaluate('sessionPlan().groups.map(g=>[g.unit,g.count])')},{1,2,3})
   self.page.locator('.practice-blocks [data-lesson-block="3"]').click()
   self.assertEqual(self.page.evaluate('cfg.us'),[3]);self.assertEqual(self.page.evaluate('pool().length'),single)
   ids=self.page.evaluate('mix(sessionPlan())');self.assertEqual(len(ids),min(30,single))
   self.assertTrue(self.page.evaluate('ids=>ids.every(id=>AL[12].b[2].topics.includes(questionById(id)[1]))',ids))
   self.page.locator('.practice-blocks [data-lesson-block="1"]').click()
   self.assertEqual({g for g in self.page.evaluate('sessionPlan().groups.map(g=>g.unit)')},{1,3})
 def test_material_selection_preserves_all_original_nodes_and_previous_units(self):
  self.page.evaluate("view='t';tr=13;go()")
  self.page.locator('.lesson-blocks [data-lesson-block="3"]').click()
  self.assertEqual(self.page.evaluate('lessonContent(13).id'),3)
  for name,key in [('Mapa mental','mapa'),('Diagramas','diag'),('Tabelas','tab'),('Linha do tempo','tl'),('Flashcards','fc')]:
   self.page.evaluate("k=>{view='m';mt={a:13,c:k};fi=0;ff=0;go()}",key)
   self.assert_material_content(name);self.assertEqual(self.page.evaluate('currentMaterial().id'),3)
  self.page.evaluate("mt.c='geral';go()")
  self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),6)
  self.assertTrue(self.page.locator('#overview-scroll tbody tr').evaluate_all('es=>es.every(e=>e.dataset.operatorBlock==="3")'))
  self.page.evaluate('selectedLessonBlocks[13]=0;go()');self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),17)
 def test_cash_diagram_signs_and_keyboard_scroll_and_both_themes(self):
  self.page.evaluate("selectedLessonBlocks[13]=3;view='m';mt={a:13,c:'diag'};go()")
  chart=self.page.locator('.payment-flow-scroll')
  for actor,expected in [('Investidor',['out','in','in','in']),('Emissora',['in','out','out','out'])]:
   self.assertEqual(chart.locator(f'[data-payment-flow-actor="{actor}"] [data-cash-direction]').evaluate_all('es=>es.map(e=>e.dataset.cashDirection)'),expected)
  self.assertIn('Captação',chart.locator('[data-payment-flow-actor="Emissora"] [data-payment-flow-event="0"]').text_content())
  state=self.page.evaluate('JSON.stringify([Q,BP,AL,MAT,H,cfg])')
  out=Path('/tmp/cpa-aula13-fluxos/screens');out.mkdir(exist_ok=True)
  for width in [390,1280,1920]:
   self.page.set_viewport_size(dict(width=width,height=1000))
   for theme in ['dark','light']:
    self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
    self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    if width==390:
     chart.focus();self.page.keyboard.press('ArrowRight');self.page.wait_for_function('document.querySelector(".payment-flow-scroll").scrollLeft>0')
    if width==1280:chart.screenshot(path=str(out/f'cash-{theme}.png'))
    self.assertEqual(self.page.evaluate('JSON.stringify([Q,BP,AL,MAT,H,cfg])'),state)
 def test_concept_scopes_include_integrated_questions_and_exclude_other_meanings(self):
  for label,id in [('Cronograma contratual',1301),('Caixa e perspectivas',1313),('Equivalência temporal',1323),('Valor presente líquido',1334),('Cupons e retorno líquido',1345)]:
   ids=self.page.evaluate('s=>ActiveStudy.matching(s)',dict(lesson=13,label=label,text='',whole=True))
   self.assertIn(id,ids);self.assertTrue(set(range(401,501)).isdisjoint(ids));self.assertTrue(set(range(1101,1201)).isdisjoint(ids))
  self.page.evaluate("selectedLessonBlocks[13]=3;view='m';mt={a:13,c:'mapa'};go()")
  for panel in self.page.locator('.mind-branch').all():
   e=self.page.evaluate('k=>ActiveStudy.audit().find(r=>r.key===k)',panel.get_attribute('data-active-study'))
   self.assertTrue(any(1301<=id<=1350 for id in e['ids']))
  self.assertIn(1340,self.page.evaluate("ActiveStudy.matching({lesson:13,label:'Cupons e retorno líquido',text:'',whole:true})"))
 def test_every_mode_feedback_and_acronym_expansions_remain_correct(self):
  for mode,ids in [('e',[1316,1334,1341]),('s',[1316,1334,1341]),('h',[1330,1339,1350]),('b',[100661,100666,100675])]:
   self.page.evaluate('x=>{H=[[1,true,1000,0]];begin(x.ids,x.mode)}',dict(ids=ids,mode=mode))
   for i,id in enumerate(ids):
    if id==1316:self.assertIn('Letra do Tesouro Nacional',self.page.locator('.en').inner_text())
    if id==1334:self.assertIn('Valor Presente Líquido',self.page.locator('.en').inner_text())
    self.answer(correct=i!=1)
    if mode!='s':
     self.assertEqual(self.page.locator('.fb-option').count(),2 if mode=='b' else 4)
     for row in self.page.locator('.fb-option').all():
      index=int(row.get_attribute('data-option-index'));self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('x=>questionById(x.id)[11][x.index]',dict(id=id,index=index)))
     self.click('Próxima' if i<2 else 'Ver resultado')
   self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'2 de 3 (67%)')
   self.assertEqual(self.page.evaluate('H.map(r=>r[0])'),[1,*ids])
 def test_consulta_search_and_readability_on_every_new_surface(self):
  for query,term in [('O que significa VPL zero?','critério'),('Como funciona carência de principal?','principal'),('Qual a diferença entre valor presente e futuro?','valor')]:
   r=self.page.evaluate('q=>Consulta.answer(q,[],{lessons:[13]})',query)
   self.assertTrue(r['items']);self.assertIn(term,' '.join(' '.join(x['record']['lines']) for x in r['items']).lower())
  self.assertTrue(self.page.evaluate("contentSearchIndex().some(r=>r.lesson===13&&/VPL/.test(r.text))"))
  self.page.evaluate("begin([1301,1334],'e');selectedLessonBlocks[13]=3;view='m';mt={a:13,c:'mapa'};go()")
  stable=self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,qz,cfg])')
  for width in [390,1280]:
   self.page.set_viewport_size(dict(width=width,height=1000))
   for theme in ['dark','light']:
    self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
    for kind in ['mapa','diag','tab','tl','fc','geral']:
     self.page.evaluate('k=>{mt.c=k;go()}',kind)
     self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(kind,width,theme))
     self.assertEqual(self.page.locator('.mind-node .active-study-button,.diagram-step .active-study-button').count(),0)
     self.assertEqual(self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,qz,cfg])'),stable)
if __name__=='__main__':unittest.main(verbosity=2)
