"""Classificação: limiares estritos, condições cumulativas, categorias e recursos."""
import copy,json,re,unittest
from collections import Counter
from pathlib import Path
from validate_bank import load_questions
from question_revision import digest
from final_block import before_investor_lesson,unit_count
import smoke as harness
ROOT=Path(__file__).resolve().parents[1]
def read(marker):return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split(marker,1)[1])[0]
class Content(unittest.TestCase):
 def setUp(self):
  self.q=load_questions();self.bp=read('const BP=');self.al=read('const AL=');self.m=read('\n13:');self.r=json.loads((ROOT/'docs/aula-13-investidores-cobertura.json').read_text())
 def test_appended_ids_half_volumes_unique_topics_and_angles(self):
  self.assertEqual((len(self.q),len(self.bp),len(self.al)),(1450,725,13))
  unit=self.al[12]['b'][4];self.assertEqual(unit['id'],5)
  self.assertEqual(Counter(q[2] for q in self.q[1400:]),{0:10,1:20,2:10,3:10})
  self.assertEqual(Counter(q[1] for q in self.q[1400:]),{t:10 for t in unit['topics']})
  self.assertEqual(Counter(f[2] for f in self.m['b'][4]['fc']),{0:8,1:9,2:8})
  self.assertEqual(Counter(f[2] for f in self.m['fc']),{0:42,1:42,2:41})
  self.assertEqual(len({q[3] for q in self.q}),len(self.q));self.assertEqual(len({x['angulo'] for x in self.r['itens']}),50)
  for q in self.q[1400:]:self.assertEqual(len(set(q[11])),4);self.assertEqual(q[9],0)
  for row in self.bp[700:]:
   self.assertLessEqual(len(row[2].split()),12);self.assertLessEqual(max(len(o.split()) for o in row[3:5]),10)
   self.assertEqual(self.q[row[7]-1][:2],row[:2])
 def test_prior_questions_and_materials_are_not_rewritten(self):
  p=self.r['preservacao'];a,m=before_investor_lesson(self.al,self.m)
  self.assertEqual(digest(self.q[:1400]),p['Q']['sha256']);self.assertEqual(digest(self.bp[:700]),p['BP']['sha256'])
  self.assertEqual(digest(a),p['AL']);self.assertEqual(digest(m['b']),p['unidades_MAT'])
  for item in self.r['itens']:self.assertEqual(digest(self.q[item['id']-1]),item['sha256'])
  for item in self.r['bate_pronto']:self.assertEqual(digest(self.bp[item['id']-100001]),item['sha256'])
  for key in ['r','d','p','n']:self.assertEqual(self.al[12][key],[x for u in self.al[12]['b'] for x in u[key]])
  for key in ['dg','tb','tl','fc']:self.assertEqual(self.m[key],[x for u in self.m['b'] for x in u[key]])
 def test_numbers_are_actual_thresholds_not_counts_variables_or_example_answers(self):
  self.assertEqual(self.al[12]['n'],self.al[12]['b'][4]['n']);self.assertEqual(len(self.al[12]['n']),2)
  for unit in self.al[12]['b'][:4]:self.assertEqual(unit['n'],[])
  for amount,text in self.al[12]['n']:
   self.assertTrue(amount.startswith('Mais de R$ '));self.assertIn('investimentos financeiros',text);self.assertIn('ateste escrito',text)
  audit=json.loads((ROOT/'docs/revisao-numeros-bloco-final.json').read_text());self.assertEqual(len(audit['removidos']),7);self.assertFalse(audit['alteracoes_fora_aula13'])
  self.assertNotIn('1k',json.dumps(self.al[12],ensure_ascii=False))
  # Boundary and missing-document counterexamples require different correct reasoning.
  self.assertIn('superior',self.q[1412][4]);self.assertIn('superior',self.q[1413][4])
  self.assertIn('não o conjunto',self.q[1414][4]);self.assertIn('ateste específico',self.q[1416][4])
  self.assertIn('financeiros',self.q[1415][4]);self.assertIn('ordem',self.q[1419][4])
 def test_source_conflicts_scope_of_operational_rules_and_no_invented_dates(self):
  self.assertEqual(self.r['fontes']['transcricao']['aula'],29);self.assertFalse(self.r['consulta_normativa']['certificacao_de_vigencia'])
  text=json.dumps(self.m['b'][4],ensure_ascii=False)
  for term in ['superiores a R$ 1 milhão','superiores a R$ 10 milhões','recursos próprios','regime aplicável','um ou mais cotistas','não garante']:self.assertIn(term,text)
  self.assertEqual(self.m['b'][4]['tl'],[])
  for title,headers,rows in self.m['b'][4]['tb']:self.assertTrue(all(len(row)==len(headers) for row in rows),title)
  # NR-to-professional inclusion is explicitly validated as a case premise, not a new universal rule.
  self.assertIn('enquadramento profissional já validado',self.q[1408][3])
  for id in [1445,1447,1448,1449]:self.assertRegex(self.q[id-1][3],r'exige|exigência|sujeita a registro')
class Browser(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__);tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp;tearDown=harness.PainelCPA.tearDown
 answer=harness.PainelCPA.answer;click=harness.PainelCPA.click;assert_material_content=harness.PainelCPA.assert_material_content
 def show(self,kind='tab'):
  self.page.evaluate("k=>{view='m';mt={a:13,c:k};selectedLessonBlocks[13]=5;go()}",kind)
 def test_fifth_unit_and_combined_selection_in_all_four_modes(self):
  for mode,size in [('e',40),('s',40),('h',10),('b',25)]:
   self.page.evaluate("md=>{cfg={a:13,as:[],b:0,us:[],md,n:-1,m:'all',c:30};qz=null;view='q';go()}",mode)
   self.assertEqual(self.page.evaluate('pool().length'),size*5)
   self.page.locator('.practice-blocks [data-lesson-block="5"]').click();self.assertEqual(self.page.evaluate('pool().length'),size)
   self.assertEqual(self.page.evaluate('sessionPlan().groups.map(g=>g.unit)'),[5])
   self.page.locator('.practice-blocks [data-lesson-block="1"]').click();self.assertEqual(self.page.evaluate('pool().length'),size*2)
   self.assertEqual(set(self.page.evaluate('sessionPlan().groups.map(g=>g.unit)')),{1,5})
 def test_all_feedbacks_original_indices_after_correct_and_wrong_answers(self):
  for mode,ids in [('e',[1413,1414,1427]),('h',[1409,1430,1439]),('s',[1413,1414,1427]),('b',[100706,100718,100725])]:
   self.page.evaluate('x=>{H=[];qz=null;begin(x.ids,x.mode)}',dict(ids=ids,mode=mode))
   for i,id in enumerate(ids):
    self.answer(correct=i!=1)
    if mode!='s':
     self.assertEqual(self.page.locator('.fb-option').count(),2 if mode=='b' else 4)
     for row in self.page.locator('.fb-option').all():
      oi=int(row.get_attribute('data-option-index'));self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('x=>questionById(x.id)[11][x.oi]',dict(id=id,oi=oi)))
     self.click('Próxima' if i<2 else 'Ver resultado')
   self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'2 de 3 (67%)')
 def test_new_material_texts_thresholds_and_no_fake_timeline(self):
  for kind,name in [('mapa','Ramificações'),('diag','Diagramas'),('tab','Tabelas'),('fc','Flashcards')]:self.show(kind);self.assert_material_content(name)
  self.show('geral');self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),5);self.assertEqual(self.page.locator('.overview-missing').count(),0)
  self.page.evaluate("view='t';tr=13;selectedLessonBlocks[13]=0;go()")
  self.assertEqual(self.page.locator('#lesson-numbers .m').count(),2)
  for b in range(1,5):
   self.page.evaluate('b=>{selectedLessonBlocks[13]=b;go()}',b);self.assertEqual(self.page.locator('#lesson-numbers').count(),0)
  self.page.evaluate('selectedLessonBlocks[13]=5;go()');self.assertEqual(self.page.locator('#lesson-numbers .m').count(),2)
 def test_concept_sources_are_precise_and_complete(self):
  labels=['Categorias e relações','Limites e ateste','Profissionais e recursos próprios','Qualificação e gestão de clubes','Não residentes e representação']
  for i,label in enumerate(labels):
   ids=self.page.evaluate('s=>ActiveStudy.matching(s)',dict(lesson=13,label=label,text='',whole=True))
   self.assertTrue(set(range(1401+i*10,1411+i*10)).issubset(ids),(label,ids))
   self.assertTrue(set(range(1,1401)).isdisjoint(ids),(label,ids))
  self.page.evaluate("view='t';tr=13;selectedLessonBlocks[13]=5;go()")
  audit=self.page.evaluate('ActiveStudy.audit().filter(e=>e.source.lesson===13)')
  self.assertTrue(all(e['ids'] for e in audit),[(e['source']['label'],e['profile']) for e in audit if not e['ids']])
  self.show('visual');self.assertEqual(self.page.locator('[data-visual-map]').get_attribute('data-visual-map'),'aula-13-5')
 def test_consulta_search_both_themes_small_screens_and_pending_session(self):
  for query,term in [('Qual o limite do investidor qualificado?','milhão'),('Quem gere o clube de investimento profissional?','administrador')]:
   response=self.page.evaluate('q=>Consulta.answer(q,[],{lessons:[13]})',query);self.assertTrue(response['items'])
   self.assertIn(term,' '.join(' '.join(x['record']['lines']) for x in response['items']).lower())
  self.assertTrue(self.page.evaluate("contentSearchIndex().some(r=>r.lesson===13&&/Classificação de Investidores/.test(r.text+' '+r.title))"))
  self.page.evaluate("begin([1413,1430],'e')");state=self.page.evaluate('JSON.stringify([H,cfg,qz])')
  out=Path('/tmp/cpa-aula13-investidores/screens');out.mkdir(exist_ok=True)
  for width in [390,1280,1920]:
   self.page.set_viewport_size(dict(width=width,height=1000))
   for theme in ['dark','light']:
    self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
    for kind in ['mapa','diag','tab','geral','fc','visual']:
     self.show(kind);self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme,kind));self.assertEqual(self.page.evaluate('JSON.stringify([H,cfg,qz])'),state)
     if width==1280 and kind in ['tab','visual']:self.page.locator('.material-content').screenshot(path=str(out/f'{kind}-{theme}.png'))
if __name__=='__main__':unittest.main(verbosity=2)
