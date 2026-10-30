"""Aulas 26+27 reunidas: contas exatas, calendário, fontes e prática integrada."""
import ast,copy,json,operator,re,unittest
from fractions import Fraction
from collections import Counter
from pathlib import Path
from validate_bank import load_questions
from question_revision import digest
from final_block import before_portfolio_lesson,unit_count
from numbers_revision import restore_before_numbers
import smoke as harness
ROOT=Path(__file__).resolve().parents[1]
def read(marker):return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split(marker,1)[1])[0]
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}
def exact(node):
 if isinstance(node,ast.Constant):return Fraction(str(node.value))
 if isinstance(node,ast.UnaryOp):return -exact(node.operand)
 return OPS[type(node.op)](exact(node.left),exact(node.right))
class Content(unittest.TestCase):
 def setUp(self):
  self.q=load_questions();self.bp=read('const BP=');self.al=read('const AL=');self.m=read('\n13:');self.report=json.loads((ROOT/'docs/aula-13-carteiras-cobertura.json').read_text())
 def test_four_units_half_volumes_and_individual_angles(self):
  self.assertEqual((len(self.q),len(self.bp)),(1400,700));self.assertEqual([u['id'] for u in self.al[12]['b']],[1,2,3,4])
  self.assertEqual(Counter(q[2] for q in self.q[1350:]),{0:10,1:20,2:10,3:10})
  self.assertEqual(Counter(q[1] for q in self.q[1350:]),{t:10 for t in self.al[12]['b'][3]['topics']})
  self.assertEqual(len(self.bp[675:]),25);self.assertEqual(Counter(c[2] for c in self.m['b'][3]['fc']),{0:8,1:8,2:9})
  self.assertEqual(Counter(c[2] for c in self.m['fc']),{0:34,1:33,2:33})
  self.assertEqual(len({x['angulo'] for x in self.report['itens']}),50)
  self.assertEqual(len({q[3] for q in self.q}),len(self.q))
  for q in self.q[1350:]:self.assertEqual(len(set(q[11])),4);self.assertEqual(q[9],0)
 def test_every_authored_calculation_is_exact_and_bound_to_the_answer(self):
  checked=0
  for row in self.report['itens']:
   self.assertEqual(digest(self.q[row['id']-1]),row['sha256'])
   for c in row.get('calculos',[]):
    self.assertEqual(exact(ast.parse(c['expressao'],mode='eval').body),Fraction(c['resultado']),row['id'])
    self.assertIn(c['trecho_correto'],self.q[row['id']-1][4]);checked+=1
  self.assertGreaterEqual(checked,60)
  # Independent economic identities, not just the authored numerical ledger.
  initial=[Fraction(2000),Fraction(3000),Fraction(5000)];returns=[Fraction('0.20'),0,Fraction('-0.04')]
  final=sum(v*(1+r) for v,r in zip(initial,returns))
  self.assertEqual((final/sum(initial)-1)*100,2)
  self.assertEqual(sum(w*t for w,t in zip([Fraction('.3'),Fraction('.7')],[6,30])),Fraction('22.8'))
  self.assertLess(Fraction('22.8'),24);self.assertLess(30000,48000)
  self.assertEqual((Fraction(160)/128-1)*100,25)
 def test_prior_arrays_are_preserved_except_authorized_number_cards(self):
  oldal,oldm=before_portfolio_lesson(self.al,self.m);p=self.report['preservacao']
  self.assertEqual(digest(self.q[:1350]),p['Q']['sha256']);self.assertEqual(digest(self.bp[:675]),p['BP']['sha256'])
  self.assertEqual(digest(oldal),p['AL']);self.assertEqual(digest(oldm['b']),p['unidades_MAT'])
  for key in ['r','d','p','n']:self.assertEqual(self.al[12][key],[x for u in self.al[12]['b'] for x in u[key]])
  for key in ['dg','tb','tl','fc']:self.assertEqual(self.m[key],[x for u in self.m['b'] for x in u[key]])
  a=json.loads((ROOT/'docs/revisao-numeros-para-decorar.json').read_text());self.assertEqual(a['aulas_verificadas'],list(range(1,14)));self.assertEqual(a['entradas_removidas'],13)
  for c in a['alteracoes']:
   current=self.al[c['aula']-1]['n'];current=current[:-2] if c['aula']==13 else current
   self.assertEqual(current,c['depois'])
   for row in c['removidos']:self.assertNotIn(row['item'],current)
  for c in self.al[12]['n']:self.assertNotRegex(' '.join(c),r'R\$|1\.123|160 mil|19,63|20,38|2 semestres|3 eixos')
 def test_sources_formulas_examples_and_conceptual_recall(self):
  self.assertEqual(self.report['fontes']['transcricao']['aulas'],[26,27])
  self.assertEqual(len(self.report['fontes']['slides']['paginas']),2)
  text=json.dumps(self.m['b'][3],ensure_ascii=False)
  for term in ['18 meses','12,5%','6,6%','9,4%','inicial','mesmo','ponderada','esperado','vencimento']:self.assertIn(term,text)
  for table,heads,rows in self.m['b'][3]['tb']:self.assertTrue(all(len(row)==len(heads) for row in rows),table)
  for q in self.bp[675:]:
   self.assertNotRegex(q[2],r'(?i)calcule|quanto|R\$|\d+%');self.assertEqual(self.q[q[7]-1][:2],q[:2])
  for c in self.m['b'][3]['fc']:self.assertNotRegex(c[0],r'(?i)calcule|quanto|R\$|\d+%')
class Browser(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__);tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp;tearDown=harness.PainelCPA.tearDown
 answer=harness.PainelCPA.answer;click=harness.PainelCPA.click
 assert_material_content=harness.PainelCPA.assert_material_content
 def show(self,kind='tab'):
  self.page.evaluate("k=>{view='m';mt={a:13,c:k};selectedLessonBlocks[13]=4;go()}",kind)
 def test_fourth_unit_and_combined_selection_in_all_modes(self):
  for mode,size in [('e',40),('s',40),('h',10),('b',25)]:
   self.page.evaluate("md=>{cfg={a:13,as:[],b:0,us:[],md,n:-1,m:'all',c:30};qz=null;view='q';go()}",mode)
   self.assertEqual(self.page.evaluate('pool().length'),size*4)
   self.page.locator('.practice-blocks [data-lesson-block="4"]').click()
   self.assertEqual(self.page.evaluate('pool().length'),size)
   self.assertEqual(self.page.evaluate('sessionPlan().groups.map(g=>g.unit)'),[4])
   self.page.locator('.practice-blocks [data-lesson-block="1"]').click()
   self.assertEqual(set(self.page.evaluate('sessionPlan().groups.map(g=>g.unit)')),{1,4})
   self.assertEqual(self.page.evaluate('pool().length'),size*2)
 def test_feedback_for_calculations_in_all_practice_modes(self):
  for mode,ids in [('e',[1364,1377,1397]),('h',[1369,1390,1400]),('s',[1364,1377,1397]),('b',[100676,100690,100700])]:
   self.page.evaluate('x=>{H=[];qz=null;begin(x.ids,x.mode)}',dict(ids=ids,mode=mode))
   for i,id in enumerate(ids):
    self.answer(correct=i!=1)
    if mode!='s':
     self.assertEqual(self.page.locator('.fb-option').count(),2 if mode=='b' else 4)
     for row in self.page.locator('.fb-option').all():
      index=int(row.get_attribute('data-option-index'));self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('x=>questionById(x.id)[11][x.index]',dict(id=id,index=index)))
     self.click('Próxima' if i<2 else 'Ver resultado')
   self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'2 de 3 (67%)')
 def test_exact_concept_scopes_and_new_map_sources(self):
  labels=['Médias e pesos','Prazo médio e vencimento','Retorno histórico do ativo','Retorno histórico da carteira','Retorno esperado e comparação']
  for group,label in enumerate(labels):
   ids=self.page.evaluate('s=>ActiveStudy.matching(s)',dict(lesson=13,label=label,text='',whole=True))
   self.assertTrue(set(range(1351+10*group,1361+10*group)).issubset(ids),(label,ids))
   self.assertTrue(set(range(401,501)).isdisjoint(ids))
  self.show('visual');self.assertEqual(self.page.locator('[data-visual-map]').get_attribute('data-visual-map'),'aula-13-4')
  self.assertTrue(self.page.locator('.visual-map-preview img').evaluate('e=>e.complete&&e.naturalWidth>=1500'))
  for row in self.page.evaluate('ActiveStudy.audit().filter(e=>e.source.kind==="visual")'):
   if row['source'].get('lesson')==13 and row['source'].get('block')==4:self.assertTrue(row['ids'])
 def test_summary_tips_and_pitfalls_have_relevant_links(self):
  self.page.evaluate("view='t';tr=13;selectedLessonBlocks[13]=4;go()")
  entries=self.page.evaluate('ActiveStudy.audit().filter(e=>e.source.lesson===13)')
  self.assertGreaterEqual(len(entries),27)
  self.assertTrue(all(e['ids'] for e in entries))
  item=next(e for e in entries if e['source']['label']=='Vencimento contratual')
  self.assertEqual(item['profile']['owners'],['portfolio-maturity'])
  self.assertTrue(all(1351<=id<=1400 for id in item['ids']))
  units=next(e for e in entries if e['source']['label']=='equivalência de um ano para uniformizar a unidade dos prazos')
  self.assertEqual(set(units['ids']),{1364,1365})
 def test_every_original_material_string_and_formula_is_visible(self):
  for kind,name in [('mapa','Ramificações'),('diag','Diagramas'),('tab','Tabelas'),('tl','Linha do tempo'),('fc','Flashcards')]:
   self.show(kind);self.assert_material_content(name)
  self.show('geral');self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),5)
  self.assertEqual(self.page.locator('.overview-missing').count(),0)
 def test_retrieval_materials_numbers_themes_and_pending_session(self):
  for query,term in [('Como calcular o prazo médio da carteira?','prazo'),('Qual a diferença entre retorno histórico e esperado?','esperado')]:
   result=self.page.evaluate('q=>Consulta.answer(q,[],{lessons:[13]})',query)
   self.assertTrue(result['items']);self.assertIn(term,' '.join(' '.join(x['record']['lines']) for x in result['items']).lower())
  formula=self.page.evaluate("Consulta.answer('Como calcular o prazo médio da carteira?',[],{lessons:[13]})")
  self.assertTrue(any('Σ(t × V)' in line for item in formula['items'] for line in item['record']['lines']))
  self.assertTrue(self.page.evaluate("contentSearchIndex().some(r=>r.lesson===13&&/Prazo médio/.test(r.text))"))
  self.page.evaluate("begin([1364,1400],'e')");stable=self.page.evaluate('JSON.stringify([H,cfg,qz])')
  out=Path('/tmp/cpa-aula13-carteiras/screens');out.mkdir(exist_ok=True)
  for width in [390,1280,1920]:
   self.page.set_viewport_size(dict(width=width,height=1000))
   for theme in ['light','dark']:
    self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
    for kind in ['mapa','diag','tab','tl','fc','geral','visual']:
     self.show(kind);self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme,kind))
     self.assertEqual(self.page.evaluate('JSON.stringify([H,cfg,qz])'),stable)
     if width==1280 and kind in ['tab','visual']:self.page.locator('.material-content').screenshot(path=str(out/f'{kind}-{theme}.png'))
  self.page.evaluate("view='t';tr=13;go()")
  self.assertEqual(self.page.evaluate('lessonContent(13).id'),4)
  for item in self.page.locator('.num-grid .num-card').all():self.assertNotRegex(item.inner_text(),r'1\.123|160 mil|19,63')
if __name__=='__main__':unittest.main(verbosity=2)
