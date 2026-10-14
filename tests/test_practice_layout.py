"""Regressões de acesso aos controles da prática no computador."""
import unittest
import smoke as harness

class PracticeLayoutTests(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click

    def launch_is_accessible(self):
        self.assertTrue(self.page.locator('.practice-launch button').evaluate('''b=>{
          const r=b.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
          return r.top>=0&&r.bottom<=innerHeight&&b.contains(hit);
        }'''))
        self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'))

    def test_start_visible_without_scrolling_in_all_modes_and_pc_sizes(self):
        for width,height in [(1024,768),(1280,720),(1366,768),(1440,900),(1920,1080)]:
            self.page.set_viewport_size({'width':width,'height':height})
            for theme in ['light','dark']:
                for mode,label in [('e','estudo'),('s','simulado'),('h','hardcore'),('b','bate-pronto')]:
                    with self.subTest(width=width,height=height,theme=theme,mode=mode):
                        self.page.evaluate('''([theme,mode])=>{
                          document.documentElement.dataset.theme=theme;view='q';qz=null;
                          cfg={a:0,as:[],n:-1,m:'all',c:10,md:mode,b:0};go();scrollTo(0,0);
                        }''',[theme,mode])
                        self.launch_is_accessible()
                        self.assertEqual(self.page.get_by_role('button',name='Iniciar '+label,exact=True).count(),1)
                        self.assertEqual(self.page.locator('.practice-modes [aria-pressed="true"]').count(),1)
                        self.assertEqual(self.page.get_by_text('Qual dificuldade?',exact=True).count(),0 if mode in ['h','b'] else 1)
                        self.assertEqual(self.page.locator('.practice-lessons [data-practice-lesson]').count(),self.page.evaluate('AL.length+1'))

    def test_multi_lesson_details_persist_and_the_same_plan_starts(self):
        self.click('Praticar')
        for lesson in [1,2,3]:self.page.locator(f'[data-practice-lesson="{lesson}"]').click()
        self.page.locator('.practice-breakdown summary').click()
        self.page.wait_for_function('practiceDistributionOpen')
        self.page.locator('.practice-options button.oc').filter(has=self.page.get_by_text('30',exact=True)).click()
        self.assertTrue(self.page.locator('.practice-breakdown').evaluate('e=>e.open'))
        plan=self.page.evaluate('sessionPlan()')
        self.assertEqual(self.page.locator('.session-distribution>div').count(),3)
        self.assertEqual([g['count'] for g in plan['groups']],[10,10,10])
        self.launch_is_accessible()
        self.click('Iniciar estudo')
        self.assertEqual(self.page.evaluate('qz.ids.length'),30)
        self.assertEqual(self.page.evaluate('[1,2,3].map(a=>qz.ids.filter(id=>questionById(id)[0]===a).length)'),[10,10,10])
        self.assertEqual(self.page.locator('.practice-launch').count(),0)
        self.assertEqual(self.page.locator('.practice-content').count(),0)

    def test_blocks_last_lesson_keyboard_and_unavailable_filters(self):
        self.page.set_viewport_size({'width':1280,'height':720})
        self.click('Praticar')
        self.page.locator('[data-practice-lesson="9"]').click()
        self.assertEqual(self.page.evaluate('selectedPracticeLessons()'),[9])
        self.page.locator('[data-practice-lesson="9"]').click()
        self.page.locator('[data-practice-lesson="7"]').click()
        self.page.locator('.practice-blocks [data-lesson-block="2"]').click()
        self.assertEqual(self.page.evaluate('cfg.b'),2)
        self.assertIn('Crédito',self.page.locator('.practice-launch').inner_text())
        self.launch_is_accessible()
        self.page.locator('.practice-launch button').focus()
        self.page.keyboard.press('Enter')
        self.assertIsNotNone(self.page.evaluate('qz'))
        self.click('Encerrar')
        self.page.locator('.practice-options button.oc').filter(has=self.page.get_by_text('As que errei',exact=True)).click()
        self.assertTrue(self.page.locator('.practice-launch button').is_disabled())
        self.assertIn('Sem questões disponíveis',self.page.locator('.sum').inner_text())
        self.launch_is_accessible()

    def test_start_stays_accessible_when_lesson_list_grows_and_page_scrolls(self):
        self.page.set_viewport_size({'width':1280,'height':720})
        self.page.evaluate("AL.push(...AL.slice(0,9).map(a=>({...a})));view='q';go();scrollTo(0,0)")
        self.launch_is_accessible()
        self.page.evaluate('scrollTo(0,document.documentElement.scrollHeight/2)')
        self.launch_is_accessible()
        self.page.evaluate('scrollTo(0,document.documentElement.scrollHeight)')
        self.launch_is_accessible()

if __name__=='__main__':unittest.main(verbosity=2)
