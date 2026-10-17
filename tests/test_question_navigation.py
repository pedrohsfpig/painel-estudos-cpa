"""Navegação não sequencial: estado, histórico, ajudas e checkpoint persistente."""
import json
import unittest
from pathlib import Path
import smoke as harness

class QuestionNavigation(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
 tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp
 tearDown=harness.PainelCPA.tearDown
 click=harness.PainelCPA.click
 answer=harness.PainelCPA.answer
 set_daily_clock=harness.PainelCPA.set_daily_clock
 def cell(self,index):return self.page.locator(f'[data-question-index="{index}"]')
 def jump(self,index):self.cell(index).click()
 def state(self,index):return self.cell(index).get_attribute('data-question-state')
 def test_scope_counts_and_initial_state(self):
  for mode in ['e','h']:
   for count in [10,20,40]:
    self.page.evaluate('x=>begin(Q.flatMap((q,i)=>q[2]===(x.mode==="h"?3:0)?[i+1]:[]).slice(0,x.count),x.mode)',dict(mode=mode,count=count))
    self.assertEqual(self.page.locator('.question-number').all_inner_texts(),list(map(str,range(1,count+1))))
    self.assertEqual(self.cell(0).get_attribute('aria-current'),'step')
    self.assertTrue(all(s=='unanswered' for s in self.page.locator('.question-number').evaluate_all('es=>es.map(e=>e.dataset.questionState)')))
    self.assertEqual(self.page.evaluate('H.length'),0)
  for mode,id in [('s',1),('b',100001)]:
   self.page.evaluate('x=>begin([x.id],x.mode)',dict(id=id,mode=mode))
   self.assertEqual(self.page.locator('.question-navigator').count(),0)
 def test_skip_back_preserves_shuffle_hints_and_eliminated_options(self):
  self.page.evaluate("begin([1,2,3,4],'e')")
  self.click('Dica');self.click('Eliminar 2 alternativas')
  state=self.page.evaluate('({o:qz.o,h:qz.h,x:qz.x,t0:qz.t0})')
  self.jump(3)
  self.assertEqual(self.state(0),'skipped');self.assertEqual(self.state(3),'unanswered')
  self.assertEqual(self.page.locator('.quiz-progress').get_attribute('aria-valuenow'),'0')
  self.jump(0)
  self.assertEqual(self.page.evaluate('({o:qz.o,h:qz.h,x:qz.x,t0:qz.t0})'),state)
  self.assertEqual(self.page.locator('button.o:disabled').count(),2)
  self.assertIn('Dica:',self.page.locator('.aj').inner_text())
  self.assertEqual(self.page.evaluate('H'),[])
  self.assertEqual(self.page.locator('.fb-option').count(),0)
 def test_revisiting_correct_and_wrong_answers_does_not_record_again(self):
  for mode in ['e','h']:
   self.page.evaluate('mode=>{H=[];begin([1,2,3,4],mode)}',mode)
   self.jump(3);self.answer(True)
   self.assertEqual(self.state(3),'correct')
   self.jump(1);self.answer(False)
   self.assertEqual(self.state(1),'incorrect')
   history=self.page.evaluate('H');rev=self.page.evaluate('qz.rev')
   for index in [3,1,0,3]:
    self.jump(index)
    if index in [1,3]:
     self.assertEqual(self.page.locator('.fb-option').count(),4)
     self.assertEqual(self.page.locator('button.o:disabled').count(),4)
     for row in self.page.locator('.fb-option').all():
      original=int(row.get_attribute('data-option-index'))
      self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('i=>questionById(qz.ids[qz.i])[11][i]',original))
     self.page.evaluate('pick(0)')
    else:self.assertEqual(self.page.locator('.fb-option').count(),0)
   self.assertEqual(self.page.evaluate('H'),history);self.assertEqual(self.page.evaluate('qz.rev'),rev)
   self.assertEqual(self.page.locator('.quiz-progress').get_attribute('aria-valuenow'),'2')
 def test_next_wraps_to_unanswered_and_result_needs_all_answers(self):
  self.page.evaluate("begin([1,2,3,4],'e')")
  self.jump(3);self.answer();self.click('Próxima')
  self.assertEqual(self.page.evaluate('qz.i'),0)
  self.answer(False);self.click('Próxima');self.assertEqual(self.page.evaluate('qz.i'),1)
  self.jump(2);self.answer();self.click('Próxima');self.assertEqual(self.page.evaluate('qz.i'),1)
  self.assertEqual(self.page.locator('.session-result').count(),0)
  self.answer(False)
  ended=self.page.evaluate('qz.end')
  self.assertGreater(ended,0)
  self.assertEqual(self.page.locator('.quiz-progress').get_attribute('aria-valuenow'),'4')
  self.jump(0)
  self.page.evaluate('qz.t0=qz.end-123000;Date.now=()=>qz.end+300000;go()')
  self.assertEqual(self.page.locator('#tm').inner_text(),'02:03')
  self.click('Ver resultado')
  self.assertIn('2 de 4 (50%)',self.page.locator('[data-result-score]').inner_text())
  self.assertEqual(self.page.evaluate('qz.end'),ended)
  self.assertEqual([r[0] for r in self.page.evaluate('H')],[4,1,3,2])
  self.assertEqual(self.page.locator('.question-navigator').count(),0)
  self.click('Refazer erros desta sessão')
  self.assertEqual(set(self.page.evaluate('qz.ids')),{1,2})
  self.assertEqual(self.page.locator('.question-number').count(),2)
 def test_daily_out_of_order_pause_reload_and_completion(self):
  self.set_daily_clock();self.click('Começar')
  ids=self.page.evaluate('qz.ids')
  self.click('Dica');self.click('Eliminar 2 alternativas')
  first=self.page.evaluate('({o:qz.o,h:qz.h,x:qz.x})')
  self.jump(6);self.answer(False);self.jump(19);self.answer(True);self.jump(10)
  snapshot=self.page.evaluate('({ids:qz.ids,rev:qz.rev,items:qz.items,i:qz.i,o:qz.o})');history=self.page.evaluate('H')
  self.click('Pausar');self.page.reload();self.click('Retomar')
  self.assertEqual(self.page.evaluate('({ids:qz.ids,rev:qz.rev,items:qz.items,i:qz.i,o:qz.o})'),snapshot)
  self.assertEqual(self.page.evaluate('H'),history)
  self.assertEqual(self.state(0),'skipped');self.assertEqual(self.state(6),'incorrect');self.assertEqual(self.state(19),'correct')
  self.jump(0);self.assertEqual(self.page.evaluate('({o:qz.o,h:qz.h,x:qz.x})'),first)
  order=[i for i in range(19,-1,-1) if i not in [6,19]]
  for index in order:
   self.jump(index);self.answer(True)
  self.assertEqual(self.page.evaluate('H.length'),20)
  self.assertEqual(self.page.evaluate('qz.rev.length'),20)
  self.assertEqual(self.page.evaluate('qz.ok'),19)
  self.assertEqual(self.page.evaluate('Object.values(dailyBook.results).length'),1)
  self.jump(6);self.assertEqual(self.page.evaluate('H.length'),20)
  self.page.reload();self.click('Ver resultado')
  self.assertIn('19 de 20 (95%)',self.page.locator('[data-result-score]').inner_text())
  self.click('Ver painel');self.assertEqual(self.page.locator('[data-daily-score]').inner_text(),'95%')
  self.assertTrue(self.page.get_by_role('button',name='Concluído hoje',exact=True).is_disabled())
  self.assertEqual(self.page.evaluate('H.length'),20)
  self.assertEqual({r[0] for r in self.page.evaluate('H')},set(ids))
 def test_old_linear_daily_snapshot_is_migrated_without_losing_responses(self):
  self.set_daily_clock();self.click('Começar')
  for _ in range(3):self.answer();self.click('Próxima')
  self.page.evaluate('delete dailyBook.active.items;delete dailyBook.active.navigatorScrollTop;writeDailyBook()')
  # Salvar sem disparar beforeunload de uma sessão ainda em memória.
  self.page.evaluate('qz=null')
  self.page.reload();self.click('Retomar')
  self.assertEqual(self.page.evaluate('qz.i'),3)
  self.assertEqual(self.page.locator('.question-number').count(),20)
  self.jump(0);self.assertEqual(self.state(0),'correct')
  self.assertEqual(self.page.locator('.fb-option').count(),4)
  self.assertEqual(self.page.evaluate('H.length'),3)
  self.click('Próxima');self.assertEqual(self.page.evaluate('qz.i'),3)
 def test_two_daily_tabs_keep_out_of_order_responses_and_navigation(self):
  self.set_daily_clock();self.click('Começar')
  other=self.context.new_page();other.goto(self.url);other.get_by_role('button',name='Retomar',exact=True).click()
  self.jump(7);self.answer(True)
  other.wait_for_function('qz.rev.length===1&&qz.rev[0][0]===qz.ids[7]')
  other.locator('[data-question-index="2"]').click()
  other.evaluate('pick(qz.o.findIndex(o=>!o[1]))')
  self.page.wait_for_function('qz.rev.length===2')
  self.assertEqual(self.page.evaluate('H.length'),2)
  self.assertEqual(self.state(7),'correct');self.assertEqual(self.state(2),'incorrect')
  self.assertEqual(self.page.evaluate('qz.ids'),other.evaluate('qz.ids'))
  self.assertEqual(self.page.evaluate('qz.rev'),other.evaluate('qz.rev'))
  other.close()
 def test_navigation_survives_menu_and_theme_without_mutation(self):
  self.page.evaluate("begin([1,2,3,4],'e')")
  self.jump(3);self.answer();self.jump(0)
  expected=self.page.evaluate('JSON.stringify(qz)');history=self.page.evaluate('H')
  self.page.locator('#theme-toggle').click()
  self.assertEqual(self.page.evaluate('JSON.stringify(qz)'),expected)
  for target in ['Painel','Trilha','Material de apoio']:
   self.page.locator('.nav').get_by_role('button',name=target,exact=True).click()
   self.page.locator('.nav').get_by_role('button',name='Praticar',exact=True).click()
   self.assertEqual(self.page.evaluate('JSON.stringify(qz)'),expected)
   self.assertEqual(self.page.evaluate('H'),history)
 def test_desktop_layout_colors_keyboard_and_long_grid_scroll(self):
  for theme in ['light','dark']:
   for width,height in [(1024,768),(1280,900),(1440,900),(1585,900),(1920,1080)]:
    self.page.set_viewport_size(dict(width=width,height=height))
    self.page.evaluate('theme=>{document.documentElement.dataset.theme=theme;begin(Q.flatMap((q,i)=>q[2]<3?[i+1]:[]).slice(0,40),"e")}',theme)
    self.jump(3);self.answer(True);self.jump(1);self.answer(False)
    nav=self.page.locator('.question-navigator').bounding_box();stage=self.page.locator('.question-stage').bounding_box()
    self.assertLess(nav['x']+nav['width'],stage['x'])
    if width>=1500:
     inner=self.page.locator('.main-inner').bounding_box()
     self.assertAlmostEqual(nav['x'],inner['x'],delta=1)
     self.assertAlmostEqual(nav['width'],184,delta=1)
     self.assertGreaterEqual(self.cell(0).bounding_box()['width'],34)
     self.assertLessEqual(self.cell(0).bounding_box()['width'],38)
     self.assertEqual(self.cell(0).evaluate('e=>parseFloat(getComputedStyle(e).fontSize)'),15)
     self.assertAlmostEqual(stage['x']+stage['width']/2,inner['x']+inner['width']/2,delta=1)
    self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
    colors=[self.cell(i).evaluate('e=>getComputedStyle(e).backgroundColor') for i in [0,1,3,4]]
    self.assertEqual(len(set(colors)),4)
    self.cell(0).focus();self.cell(0).press('Enter');self.assertEqual(self.page.evaluate('qz.i'),0)
    self.assertEqual(self.cell(0).get_attribute('aria-current'),'step')
    if width==1280:self.page.screenshot(path=f'/tmp/cpa-question-navigation-{theme}.png',full_page=True)
   self.page.set_viewport_size(dict(width=1024,height=768))
   self.page.evaluate('begin(Q.flatMap((q,i)=>q[2]<3?[i+1]:[]).slice(0,120),"e")')
   self.jump(115)
   self.assertGreater(self.page.locator('.question-navigator').evaluate('e=>e.scrollTop'),0)
   self.page.locator('#theme-toggle').click()
   self.assertTrue(self.cell(115).is_visible())
   visible=self.page.evaluate('''()=>{const a=document.querySelector('[aria-current="step"]').getBoundingClientRect(),b=document.querySelector('.question-navigator').getBoundingClientRect();return a.top>=b.top&&a.bottom<=b.bottom}''')
   self.assertTrue(visible)
if __name__=='__main__':unittest.main(verbosity=2)
