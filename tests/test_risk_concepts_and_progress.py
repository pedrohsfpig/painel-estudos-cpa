"""Questões conceituais de riscos, novos tamanhos de sessão e progresso por pergunta."""
from collections import Counter
from decimal import Decimal
import json
from pathlib import Path
import re
import unittest
from validate_bank import load_questions
from question_revision import digest,questions_before_risk_concept_revision
from final_block import before_private_credit
import smoke as harness
ROOT=Path(__file__).resolve().parents[1]

class RiskContent(unittest.TestCase):
 def test_authorized_revision_preserves_ids_levels_and_initial_content(self):
  current=load_questions();before=questions_before_risk_concept_revision(current)
  report=json.loads((ROOT/'docs/revisao-aula-13-conceitos.json').read_text())
  self.assertEqual(digest(current[:1200]),report['preservacao']['primeiras_1200_Q'])
  self.assertEqual([r['id'] for r in report['revisao_das_50']],list(range(1201,1251)))
  self.assertEqual(len(report['questoes']),16)
  for a,b in zip(before,current):self.assertEqual([a[i] for i in [0,1,2,9]],[b[i] for i in [0,1,2,9]])
  self.assertEqual(Counter(q[2] for q in current[1200:1250]),{0:10,1:20,2:10,3:10})
  for q in current[1200:1250]:
   self.assertNotRegex(' '.join(q[3:9]+q[11]),r'1\.123,60|1\.040,37|1\.080,38|1\.060,00')
  for id in [1222,1223,1224,1227,1231,1239,1240,1241,1242,1245,1247,1250]:
   q=current[id-1]
   self.assertTrue(all(len(o.split())>=3 for o in q[4:8]))
   self.assertFalse(any(re.fullmatch(r'R\$ [\d.,]+\.',o) for o in q[4:8]))
  for id in [1240,1241,1242,1245,1247,1250]:self.assertRegex(current[id-1][3],r'sobe|sobem|cai|alta')
  self.assertIn('cotação isolada não identifica',current[1231][4])

 def test_new_scenarios_are_coherent_without_asking_for_basic_arithmetic(self):
  self.assertEqual(Decimal('12600')/Decimal('1.05'),Decimal('12000'))
  self.assertEqual(Decimal('12600')/Decimal('1.12'),Decimal('11250'))
  self.assertEqual(Decimal('9450')/Decimal('1.08'),Decimal('8750'))
  self.assertEqual(Decimal('9450')/Decimal('1.05'),Decimal('9000'))
  q=load_questions()
  self.assertIn('ganho acumulado',q[1241][4]);self.assertIn('fluxo contratual de R$ 15.000',q[1246][4])
  self.assertIn('Liquidez de financiamento; risco de mercado; liquidez de mercado.',q[1249][4])
  report=json.loads((ROOT/'docs/revisao-aula-13-conceitos.json').read_text())
  html=(ROOT/'index.html').read_text();mat=json.JSONDecoder().raw_decode(html.split('\n13:',1)[1])[0]
  lessons=json.JSONDecoder().raw_decode(html.split('const AL=',1)[1])[0]
  lessons,mat=before_private_credit(lessons,mat)
  self.assertIn('R$ 9.450',q[1244][3]);self.assertIn('R$ 8.750',q[1244][3])
  restored=json.loads(json.dumps(mat['fc']))
  for r in report['flashcards']:restored[r['indice']]=r['antes']
  self.assertEqual(digest(restored),report['preservacao']['flashcards_13_antes'])
  for key in ['BP','AL']:
   data=json.JSONDecoder().raw_decode(html.split('const '+key+'=',1)[1])[0]
   data=data[:625] if key=='BP' else lessons
   self.assertEqual(digest(data),report['preservacao'][key])
  stripped=json.loads(json.dumps(mat));stripped.pop('fc');stripped['b'][0].pop('fc')
  self.assertEqual(digest(stripped),report['preservacao']['materiais_13_exceto_flashcards'])
  for r in report['flashcards']:
   self.assertEqual(mat['fc'][r['indice']],r['depois']);self.assertEqual(mat['b'][0]['fc'][r['indice']],r['depois'])
   self.assertEqual(r['antes'][2],r['depois'][2])

class SegmentedProgress(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
 tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp
 tearDown=harness.PainelCPA.tearDown
 click=harness.PainelCPA.click
 answer=harness.PainelCPA.answer
 set_daily_clock=harness.PainelCPA.set_daily_clock
 def test_five_presets_in_all_modes_start_fifteen_questions(self):
  for mode in ['e','h','s','b']:
   self.page.evaluate("md=>{cfg={a:1,as:[],b:0,md,c:10,n:-1,m:'all'};qz=null;view='q';go()}",mode)
   buttons=self.page.locator('.practice-options .og.qt button')
   self.assertEqual(buttons.all_inner_texts(),['5','10','15','20','30'])
   buttons.get_by_text('15',exact=True).click();self.assertEqual(self.page.evaluate('cfg.c'),15)
   self.page.locator('.practice-launch button').click()
   self.assertEqual(self.page.evaluate('qz.ids.length'),15)
   self.assertEqual(self.page.locator('.quiz-progress-segment').count(),15)
   self.assertEqual(self.page.locator('.quiz-progress .is-complete').count(),0)
   self.answer();self.assertEqual(self.page.locator('.quiz-progress .is-complete').count(),1)
   self.assertEqual(self.page.locator('.quiz-progress').get_attribute('aria-valuenow'),'1')

 def test_out_of_order_answers_fill_the_corresponding_segments_and_do_not_repeat(self):
  self.page.evaluate("begin([1,2,3,4,5],'e');jumpQuestion(3)")
  self.answer(False)
  self.assertEqual(self.page.locator('.is-complete[data-progress-index]').evaluate_all('es=>es.map(e=>+e.dataset.progressIndex)'),[3])
  self.page.evaluate('jumpQuestion(1)');self.answer(True)
  self.assertEqual(self.page.locator('.is-complete[data-progress-index]').evaluate_all('es=>es.map(e=>+e.dataset.progressIndex)'),[1,3])
  before=self.page.evaluate('JSON.stringify([H,qz.rev,qz.t0])')
  self.page.evaluate('jumpQuestion(3);pick(0)')
  self.page.locator('#theme-toggle').click()
  self.assertEqual(self.page.evaluate('JSON.stringify([H,qz.rev,qz.t0])'),before)
  self.assertEqual(self.page.locator('.quiz-progress .is-complete').count(),2)
  self.assertEqual(self.page.locator('.quiz-progress').get_attribute('aria-valuemax'),'5')

 def test_daily_pause_reload_restores_segments_and_unanswered_stays_empty(self):
  self.set_daily_clock();self.page.evaluate('hoje();jumpQuestion(7)');self.answer(False)
  ids=self.page.evaluate('qz.ids');self.click('Pausar');self.page.reload();self.click('Retomar')
  self.assertEqual(self.page.evaluate('qz.ids'),ids)
  self.assertEqual(self.page.locator('.quiz-progress-segment').count(),20)
  self.assertEqual(self.page.locator('.is-complete[data-progress-index]').evaluate_all('es=>es.map(e=>+e.dataset.progressIndex)'),[7])

 def test_height_colors_and_arbitrary_session_lengths_fit_both_themes(self):
  out=Path('/tmp/cpa-riscos-revisao/screens');out.mkdir(exist_ok=True)
  for width in [390,1280]:
   self.page.set_viewport_size(dict(width=width,height=900))
   for theme in ['dark','light']:
    for count in [10,15,30,312,1250]:
     self.page.evaluate("x=>{document.documentElement.dataset.theme=x.theme;begin(Q.slice(0,x.count).map((_,i)=>i+1),'e')}",dict(theme=theme,count=count))
     self.assertEqual(self.page.locator('.quiz-progress-segment').count(),count)
     self.assertEqual(self.page.locator('.quiz-progress').evaluate('e=>e.getBoundingClientRect().height'),6)
     self.assertTrue(self.page.locator('.quiz-progress').evaluate('e=>e.scrollWidth<=e.clientWidth+1'))
     self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
     if count==15:
      self.answer();self.page.screenshot(path=str(out/f'progress-{theme}-{width}.png'))
      self.assertTrue(self.page.locator('.quiz-progress').evaluate("""e=>{const ref=document.createElement('span');ref.style.background='var(--ac)';document.body.append(ref);const complete=getComputedStyle(ref).backgroundColor;ref.style.background='var(--bd)';const empty=getComputedStyle(ref).backgroundColor;ref.remove();return getComputedStyle(e.querySelector('.is-complete')).backgroundColor===complete&&getComputedStyle(e.querySelector('span:not(.is-complete)')).backgroundColor===empty}"""))
if __name__=='__main__':unittest.main(verbosity=2)
