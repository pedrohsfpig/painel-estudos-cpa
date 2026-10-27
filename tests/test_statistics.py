"""Análises usam dados reais; o painel permanece independente dos filtros."""
from collections import Counter,defaultdict
import json
from pathlib import Path
import unittest
import smoke as harness

class Statistics(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
 tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp
 tearDown=harness.PainelCPA.tearDown
 click=harness.PainelCPA.click
 answer=harness.PainelCPA.answer
 def fixture(self):
  return self.page.evaluate('''()=>{
   H=[[1,true,1600000000000,0],[1,false,1700000000000,0],[2,true,1700000000000,1],
      [101,false,1700000000000,0],[201,true,1700000000000,1],
      [100001,true,1700000000000,3],[100001,false,1700000000000,3],
      [999999,false,1700000000000,0]];go();return H;
  }''')
 def test_menu_and_panel_keep_basic_unfiltered_summary_and_full_evolution(self):
  self.fixture();labels=self.page.locator('.nav button>span:first-of-type').all_text_contents()
  self.assertEqual(labels[-3:],['Quadro do SFN','Estatísticas','Guia da prova']);self.assertEqual(self.page.locator('.detail-stats,.stats-filters,.dashboard-filters').count(),0)
  self.assertEqual(self.page.locator('.g4 .mv').all_text_contents(),['7','4','3','57%'])
  self.assertTrue(self.page.locator('.hoje,.evolution,.dashboard-trail-list').count()==3)
  initial=self.page.locator('[data-evolution-day]').all_text_contents()
  self.click('Ver estatísticas detalhadas');self.assertEqual(self.page.evaluate('view'),'stats')
  self.click('Difícil');self.click('Simulado');self.click('Painel')
  self.assertEqual(self.page.locator('.g4 .mv').all_text_contents(),['7','4','3','57%']);self.assertEqual(self.page.locator('[data-evolution-day]').all_text_contents(),initial)
  self.click('Estatísticas');self.assertEqual(self.page.evaluate('[fl,fm]'),[2,1])
 def test_counts_repetitions_boolean_history_and_filters_are_consistent(self):
  history=self.fixture();self.click('Estatísticas');self.assertEqual(self.page.locator('.g4 .mv').all_text_contents(),['7','4','3','57%'])
  self.assertEqual(self.page.evaluate('statisticsData().unique'),5)
  self.click('Bate-pronto');self.assertEqual(self.page.locator('.g4 .mv').all_text_contents(),['2','1','1','50%'])
  self.assertEqual(self.page.evaluate('statisticsData().unique'),1);self.assertEqual(self.page.locator('[data-stat-level="-1"] p').inner_text(),'1 de 2 corretas')
  self.click('Hardcore');self.assertEqual(self.page.locator('.g4 .mv').all_text_contents(),['0','0','0','—'])
  self.assertIn('Nenhuma resposta com estes filtros',self.page.locator('.metric-note').inner_text());self.assertEqual(self.page.evaluate('H'),history)
  self.click('Limpar filtros');self.assertEqual(self.page.locator('.g4 .mv').all_text_contents(),['7','4','3','57%'])
  self.assertEqual(self.page.evaluate('[fl,fm]'),[-1,-1])
 def test_matrix_matches_every_attempt_and_differentiates_missing_from_zero(self):
  self.fixture();self.click('Estatísticas');self.page.locator('.stats-matrix-section summary').click()
  expected=self.page.evaluate('''()=>{const m={};HF().forEach(([id,ok])=>{const q=questionById(id),k=q[0]+':'+q[2];(m[k]||=[0,0])[0]+=ok?1:0;m[k][1]++});return m}''')
  cells=self.page.locator('[data-stat-cell]').all();self.assertEqual(len(cells),self.page.evaluate('AL.length*5'))
  for cell in cells:
   key=cell.get_attribute('data-stat-cell')
   if key in expected:
    ok,n=expected[key];self.assertEqual(cell.locator('strong').inner_text(),f'{int(ok*100/n+.5)}%');self.assertEqual(cell.locator('small').inner_text(),f'{ok}/{n}')
   else:self.assertEqual(cell.inner_text(),'—');self.assertEqual(cell.locator('.stats-matrix-value').count(),0)
  level=self.page.evaluate('Q[100][2]');self.assertIn('0%',self.page.locator(f'[data-stat-cell="2:{level}"]').inner_text())
 def test_sections_tabs_query_and_filter_preserve_active_session_and_banks(self):
  self.fixture();self.page.evaluate("begin([1,2],'e')");self.answer();self.click('Estatísticas')
  before=self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz,dailyBook])')
  self.page.locator('.stats-matrix-section summary').focus();self.page.keyboard.press('Enter')
  self.page.locator('#detail-tab-lesson').focus();self.page.keyboard.press('ArrowRight')
  self.assertEqual(self.page.locator('[role="tab"][aria-selected="true"]').get_attribute('id'),'detail-tab-topic')
  self.page.get_by_role('searchbox',name='Buscar no desempenho detalhado').fill('<img src=x onerror=alert(1)>')
  self.assertEqual(self.page.locator('.detail-empty img').count(),0)
  self.click('Simulado');self.assertTrue(self.page.locator('.stats-matrix-section').evaluate('n=>n.open'))
  self.page.locator('.detail-stats summary').click();self.click('Estudo');self.assertFalse(self.page.locator('.detail-stats').evaluate('n=>n.open'))
  self.assertEqual(self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz,dailyBook])'),before)
  self.click('Praticar');self.assertEqual(self.page.evaluate('qz.i'),0);self.assertEqual(self.page.locator('.fb-option').count(),4)
 def test_pending_daily_session_survives_statistics_navigation_and_filtering(self):
  self.page.evaluate('hoje()');self.answer();self.click('Estatísticas')
  stable="JSON.stringify([H,qz,{...dailyBook,active:((({elapsed,updatedAt,...rest})=>rest)(dailyBook.active))},cfg])"
  before=self.page.evaluate(stable);elapsed=self.page.evaluate('dailyBook.active.elapsed');self.click('Médio');self.click('Simulado');self.click('Painel')
  self.assertEqual(self.page.evaluate(stable),before);self.assertGreaterEqual(self.page.evaluate('dailyBook.active.elapsed'),elapsed)
  self.page.get_by_role('button',name='Retomar').click();self.assertEqual(self.page.evaluate('qz.rev.length'),1)
 def test_empty_and_all_correct_do_not_invent_percentages_or_weaknesses(self):
  self.click('Estatísticas');self.assertEqual(self.page.locator('.g4 .mv').all_text_contents(),['0','0','0','—'])
  self.assertEqual(self.page.locator('.detail-focus').count(),0)
  self.assertEqual(self.page.locator('.stats-level .stats-ring').all_text_contents(),['—']*5)
  self.page.evaluate('H=[[1,true]];go()');self.assertEqual(self.page.locator('.detail-focus').count(),0)
  self.assertEqual(self.page.locator('.stats-score .mv').inner_text(),'100%');self.assertIn('Poucas respostas',self.page.locator('.detail-help').inner_text())
  # Um erro residual continua visível no arco, mesmo com percentual arredondado a 100%.
  ring=self.page.evaluate('''()=>{const node=document.createElement('div');node.innerHTML=statisticsRing(499,500);return {text:node.textContent.trim(),arc:node.querySelector('.stats-ring-correct').getAttribute('stroke-dasharray').split(' ').map(Number)}}''')
  self.assertEqual(ring['text'],'100%');self.assertAlmostEqual(ring['arc'][0],99.8);self.assertAlmostEqual(ring['arc'][1],.2)
 def test_both_themes_responsive_layout_accessible_charts_and_fold_state(self):
  self.fixture();self.click('Estatísticas');self.page.locator('.stats-matrix-section summary').click()
  for width in [390,768,1024,1280,1440,1920]:
   self.page.set_viewport_size(dict(width=width,height=1000))
   for theme in ['light','dark']:
    self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
    self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme))
    self.assertTrue(self.page.locator('.stats-summary,.stats-filters,.detail-stat-card,.stats-level').evaluate_all('es=>es.every(e=>e.scrollWidth<=e.clientWidth+1)'),(width,theme))
    self.assertTrue(self.page.locator('.stats-ring[role="img"]').evaluate_all('es=>es.every(e=>e.getAttribute("aria-label"))'))
  self.page.locator('#theme-toggle').click();self.assertTrue(self.page.locator('.stats-matrix-section').evaluate('n=>n.open'))
  self.click('Painel');self.click('Estatísticas');self.assertTrue(self.page.locator('.stats-matrix-section').evaluate('n=>n.open'))
if __name__=='__main__':unittest.main(verbosity=2)
