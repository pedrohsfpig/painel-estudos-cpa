"""Painel final compacto: mesmos dados, navegação e explicações em todos os modos."""
import json
from pathlib import Path
import unittest
import smoke as harness

class CompactResults(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    answer=harness.PainelCPA.answer
    click=harness.PainelCPA.click
    complete_ids=harness.PainelCPA.complete_ids

    def many_lessons(self):
        self.page.evaluate('''()=>{
          const ids=Array.from({length:10},(_,a)=>[0,1,2].map(l=>Q.findIndex(q=>q[0]===a+1&&q[2]===l)+1)).flat();begin(ids,'e');
          qz.rev=ids.map((id,i)=>[id,i%3!==0,questionById(id)[i%3!==0?4:5]]);qz.ok=20;qz.i=ids.length;qz.t0=Date.now()-180000;qz.end=Date.now();go();window.scrollTo(0,0);
        }''')

    def test_all_ten_lessons_and_difficulty_values_remain_readable_without_long_bars(self):
        self.many_lessons()
        self.assertEqual(self.page.locator('[data-result-lesson]').count(),10)
        self.assertEqual(self.page.locator('.result-level-card').count(),3)
        self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'20 de 30 (67%)')
        self.assertEqual(self.page.locator('.result-stat strong').all_text_contents(),['10','10','03:00'])
        for i in range(1,11):
            card=self.page.locator(f'[data-result-lesson="{i}"]')
            self.assertIn(self.page.evaluate('i=>AU[i]',i),card.inner_text())
            self.assertIn('2 de 3 corretas',card.inner_text())
        for level,score in [(0,'0%'),(1,'100%'),(2,'100%')]:
            self.assertIn(score,self.page.locator(f'[data-result-level="{level}"]').inner_text())
        self.assertEqual(self.page.locator('.result-review details.rv').count(),10)
        self.assertEqual(self.page.locator('.result-priority').count(),3)
        self.assertIn('4 dos 10 erros',self.page.locator('.result-patterns').inner_text())

    def test_desktop_layout_reduces_scrolling_in_both_themes_without_mutation(self):
        self.many_lessons();state=self.page.evaluate('JSON.stringify([qz,H,Q,BP])')
        for width in [1024,1280,1440,1920]:
            self.page.set_viewport_size(dict(width=width,height=1000))
            for theme in ['light','dark']:
                self.page.evaluate('x=>document.documentElement.dataset.theme=x',theme)
                self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'))
                self.assertLess(self.page.locator('.result-actions').bounding_box()['y'],460)
                self.assertLess(self.page.locator('.result-charts').bounding_box()['height'],600)
                self.assertTrue(self.page.locator('.result-panel,.result-overview,.result-stat').evaluate_all('nodes=>nodes.every(n=>n.scrollWidth<=n.clientWidth+1)'))
                if width>=1280:
                    lesson=self.page.locator('[data-result-lesson="1"]').bounding_box()
                    second=self.page.locator('[data-result-lesson="2"]').bounding_box()
                    self.assertEqual(lesson['y'],second['y'])
                    self.assertGreater(second['x'],lesson['x'])
                self.assertEqual(self.page.evaluate('JSON.stringify([qz,H,Q,BP])'),state)

    def test_feedback_review_expands_full_width_and_retries_only_current_errors(self):
        self.complete_ids([967,978,980],'e',{1})
        history=self.page.evaluate('H')
        self.page.locator('details.rv summary').first.click()
        self.assertEqual(self.page.locator('details.rv[open] .fb-option').count(),4)
        self.assertAlmostEqual(self.page.locator('details.rv[open]').bounding_box()['width'],self.page.locator('.result-review-list').bounding_box()['width'],delta=2)
        self.click('Refazer erros desta sessão')
        self.assertEqual(self.page.evaluate('qz.ids'),[967,980])
        self.assertEqual(self.page.evaluate('H'),history)

    def test_same_dashboard_handles_every_mode_and_daily_label(self):
        for mode,ids in [('e',[1,2,16]),('s',[1,2,16]),('h',[81,82,83]),('b',[100001,100002,100003])]:
            self.complete_ids(ids,mode,{1})
            self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'1 de 3 (33%)')
            self.assertEqual(self.page.locator('details.rv').count(),2)
            if mode=='b':
                self.assertGreater(self.page.locator('[data-result-topic]').count(),0)
                self.assertEqual(self.page.locator('.result-level-card').count(),0)
            self.page.locator('details.rv summary').first.click()
            self.assertEqual(self.page.locator('details.rv[open] .fb-option').count(),0 if mode=='s' else 2 if mode=='b' else 4)
        self.page.evaluate('qz.dailyId="2026-10-19";go()')
        self.assertIn('Resultado do estudo de hoje',self.page.locator('.result-overview').inner_text())

    def test_one_priority_uses_available_width_and_keeps_its_content_shortcut(self):
        self.complete_ids([967,978],'e',{1})
        self.assertEqual(self.page.locator('.result-priority').count(),1)
        self.assertAlmostEqual(self.page.locator('.result-priority').bounding_box()['width'],self.page.locator('.result-priorities').bounding_box()['width'],delta=2)
        self.click('Revisar conteúdo da aula 10')
        self.assertTrue(self.page.evaluate('qz===null'))
        self.assertTrue(self.page.locator('#lesson-summary').evaluate('n=>n.open'))

    def test_small_screens_and_many_bate_pronto_topics_keep_every_item_accessible(self):
        self.page.evaluate('''()=>{const ids=BP_Q.map((_,i)=>100001+i).slice(450,500);begin(ids,'b');qz.rev=ids.map((id,i)=>[id,i%2,questionById(id)[i%2?4:5]]);qz.i=ids.length;go()}''')
        topics=self.page.evaluate('sessionAnalysis().topics.length')
        self.assertEqual(self.page.locator('.result-groups-topics [data-result-topic]').count(),topics)
        self.assertEqual(self.page.locator('.result-groups-topics').get_attribute('tabindex'),'0')
        for width in [390,680,850,1024]:
            self.page.set_viewport_size(dict(width=width,height=900))
            self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'))
        self.page.locator('.result-groups-topics').focus()
        self.page.keyboard.press('End')
        self.page.wait_for_function("document.querySelector('.result-groups-topics').scrollTop>0")

if __name__=='__main__':unittest.main(verbosity=2)
