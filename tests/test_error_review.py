"""Cartões de pendências e configuração explícita antes de refazer erros."""
import unittest
import smoke as harness

class ErrorReview(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click
    answer=harness.PainelCPA.answer

    def seed(self):
        return self.page.evaluate('''()=>{
          const groups=['easy','medium','hard','hardcore'];const ids={};
          groups.forEach((g,level)=>ids[g]=Q.findIndex(q=>q[2]===level)+1);ids.quick=100001;
          H=Object.values(ids).map((id,i)=>[id,0,1700000000000+i,0]);
          H.push([ids.quick,0,1700000000009,3],[100002,0,1700000000010,3],[100002,1,1700000000011,3]);
          save();view='e';go();return ids;
        }''')

    def nav(self,label):self.page.locator('.nav').get_by_role('button',name=label,exact=True).click()

    def test_initial_cards_count_unique_pending_questions_and_reveal_only_selected_group(self):
        ids=self.seed();history=self.page.evaluate('H')
        self.assertEqual(self.page.locator('.error-group').count(),5)
        self.assertEqual(self.page.locator('[data-error-total]').inner_text(),'5')
        self.assertEqual(self.page.locator('.error-group[aria-pressed="true"],details.rv').count(),0)
        for group,id in ids.items():
            card=self.page.locator(f'[data-error-group="{group}"]')
            self.assertEqual(card.get_attribute('data-error-count'),'1');card.click()
            self.assertEqual(card.get_attribute('aria-pressed'),'true')
            self.assertEqual(self.page.locator('[data-error-question]').evaluate_all('els=>els.map(el=>Number(el.dataset.errorQuestion))'),[id])
            self.assertEqual(self.page.locator('details.rv').count(),1)
            self.page.locator('details.rv summary').click()
            self.assertEqual(self.page.locator('.fb-option').count(),2 if group=='quick' else 4)
        self.page.locator('[data-error-group="quick"]').click()
        self.assertEqual(self.page.locator('details.rv').count(),0)
        self.assertEqual(self.page.evaluate('H'),history)
        self.nav('Painel');self.nav('Erros (5)')
        self.assertEqual(self.page.locator('details.rv').count(),0)

    def test_retry_study_and_bate_pronto_open_config_then_start_only_their_own_errors(self):
        for mode,label,start in [('e','Refazer erros (modo estudo)','Iniciar estudo'),('b','Refazer erros bate-pronto','Iniciar bate-pronto'),('h','Refazer erros hardcore','Iniciar hardcore')]:
            ids=self.seed();self.page.evaluate("cfg.a=9;cfg.as=[9];cfg.b=2;cfg.n=2;cfg.m='new';cfg.c=50")
            history=self.page.evaluate('H');self.click(label)
            self.assertEqual(self.page.locator('.practice-setup').count(),1)
            self.assertEqual(self.page.locator('.quiz-header').count(),0)
            self.assertTrue(self.page.evaluate('qz===null'))
            self.assertEqual(self.page.evaluate('({mode:cfg.md,filter:cfg.m,lessons:selectedPracticeLessons(),block:cfg.b})'),dict(mode=mode,filter='err',lessons=[],block=0))
            self.assertEqual(self.page.evaluate('H'),history)
            self.click(start)
            selected=self.page.evaluate('qz.ids')
            self.assertEqual(set(selected),set([ids['quick']] if mode=='b' else [ids['hardcore']] if mode=='h' else [ids[g] for g in ['easy','medium','hard']]))
            self.assertEqual(self.page.locator('button.o').count(),2 if mode=='b' else 4)
            self.answer();self.assertEqual(self.page.locator('.fb-option').count(),2 if mode=='b' else 4)

    def test_selected_difficulty_drives_retry_and_correct_answer_clears_the_pending_item(self):
        ids=self.seed();self.page.locator('[data-error-group="medium"]').click();self.click('Praticar estes erros')
        self.assertEqual(self.page.evaluate('[cfg.md,cfg.n,cfg.m]'),['e',1,'err'])
        self.click('Iniciar estudo');self.assertEqual(self.page.evaluate('qz.ids'),[ids['medium']])
        self.answer();self.click('Ver resultado');self.nav('Erros (4)')
        self.assertEqual(self.page.locator('[data-error-group="medium"]').get_attribute('data-error-count'),'0')
        self.assertTrue(self.page.locator('[data-error-group="medium"]').is_disabled())
        self.assertNotIn(ids['medium'],self.page.evaluate('errs()'))
        self.assertEqual(self.page.evaluate('H.length'),9)

    def test_legacy_boolean_results_are_available_in_both_error_practice_pools(self):
        self.page.evaluate("H=[[1,false,1700000000000,0],[100001,false,1700000000001,3],[2,true,1700000000002,0]];save();view='e';go()")
        self.assertEqual(self.page.evaluate('errs().sort((a,b)=>a-b)'),[1,100001])
        self.click('Refazer erros (modo estudo)');self.assertEqual(self.page.evaluate('pool()'),[1])
        self.nav('Erros (2)');self.click('Refazer erros bate-pronto');self.assertEqual(self.page.evaluate('pool()'),[100001])

    def test_empty_review_disables_actions_without_starting_an_empty_session(self):
        self.page.evaluate("H=[];view='e';go()")
        self.assertEqual(self.page.locator('.error-group:disabled').count(),5)
        self.assertTrue(self.page.get_by_role('button',name='Refazer erros (modo estudo)',exact=True).is_disabled())
        self.assertTrue(self.page.get_by_role('button',name='Refazer erros bate-pronto',exact=True).is_disabled())
        self.assertIn('Nenhum erro pendente',self.page.inner_text('#app'))
        self.assertTrue(self.page.evaluate('qz===null'))

    def test_cards_and_feedback_fit_desktop_in_both_themes_and_work_with_keyboard(self):
        self.seed()
        for width in [1024,1280,1920]:
            self.page.set_viewport_size(dict(width=width,height=900))
            for theme in ['light','dark']:
                self.page.evaluate('t=>{document.documentElement.dataset.theme=t;reviewGroup=null;go()}',theme)
                self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),width)
                cards=self.page.locator('.error-group');heights=[c.bounding_box()['height'] for c in cards.all()]
                self.assertLessEqual(max(heights)-min(heights),1)
                self.page.locator('[data-error-group="easy"]').focus();self.page.keyboard.press('Enter')
                self.assertEqual(self.page.locator('[data-error-group="easy"]').get_attribute('aria-pressed'),'true')
                self.page.locator('details.rv summary').click()
                self.assertEqual(self.page.locator('.fb-option').count(),4)
                self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),width)
                self.assertTrue(self.page.locator('#theme-toggle').is_visible())

if __name__=='__main__':unittest.main(verbosity=2)
