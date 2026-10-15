"""Descartar a tela final ao sair, preservando histórico e sessões em andamento."""
import unittest
import smoke as harness

class PracticeNavigation(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    answer=harness.PainelCPA.answer
    click=harness.PainelCPA.click
    complete_ids=harness.PainelCPA.complete_ids
    set_daily_clock=harness.PainelCPA.set_daily_clock
    finish_daily=harness.PainelCPA.finish_daily

    def nav(self,label):self.page.locator('.nav').get_by_role('button',name=label,exact=label!='Erros').click()

    def test_completed_results_leave_to_any_tab_and_return_to_setup_in_every_mode(self):
        self.page.evaluate("cfg={a:0,as:[1,2],n:1,m:'all',c:10,md:'e',b:0}")
        cfg=self.page.evaluate('JSON.stringify(cfg)')
        for mode,ids in [('e',[1]),('s',[1]),('h',[41]),('b',[100001])]:
            for target in ['Painel','Trilha','Material de apoio','Erros','Quadro do SFN']:
                with self.subTest(mode=mode,target=target):
                    self.complete_ids(ids,mode,{0})
                    history=self.page.evaluate('H')
                    self.assertEqual(self.page.locator('.session-result').count(),1)
                    # Permanecer em Praticar ou trocar de tema não descarta o resultado.
                    self.page.evaluate('go()');self.assertEqual(self.page.locator('.session-result').count(),1)
                    self.page.locator('#theme-toggle').click()
                    self.assertEqual(self.page.locator('.session-result').count(),1)
                    self.nav(target)
                    self.assertTrue(self.page.evaluate('qz===null'))
                    self.nav('Praticar')
                    self.assertEqual(self.page.locator('.practice-setup').count(),1)
                    self.assertEqual(self.page.locator('.session-result,.quiz-header').count(),0)
                    self.assertEqual(self.page.evaluate('H'),history)
                    self.assertEqual(self.page.evaluate('JSON.stringify(cfg)'),cfg)

    def test_incomplete_questions_keep_position_choice_timer_and_feedback(self):
        for mode,ids in [('e',[1,2]),('s',[1,2]),('h',[41,42]),('b',[100001,100002])]:
            self.page.evaluate('x=>begin(x.ids,x.mode)',dict(ids=ids,mode=mode))
            self.answer()
            state=self.page.evaluate('JSON.stringify(qz)');history=self.page.evaluate('H')
            for target in ['Painel','Trilha','Material de apoio']:
                self.nav(target);self.nav('Praticar')
                self.assertEqual(self.page.evaluate('JSON.stringify(qz)'),state)
                self.assertEqual(self.page.evaluate('H'),history)
                self.assertEqual(self.page.locator('.quiz-header').count(),1)
                self.assertEqual(self.page.locator('.fb-option').count(),0 if mode=='s' else 2 if mode=='b' else 4)

    def test_daily_result_is_retired_from_practice_but_remains_explicitly_accessible(self):
        self.set_daily_clock()
        self.finish_daily(15)
        history=self.page.evaluate('H');book=self.page.evaluate('JSON.stringify(dailyBook)')
        self.nav('Painel')
        self.assertEqual(self.page.locator('[data-daily-score]').inner_text(),'75%')
        self.assertTrue(self.page.get_by_role('button',name='Concluído hoje',exact=True).is_disabled())
        self.nav('Praticar')
        self.assertEqual(self.page.locator('.practice-setup').count(),1)
        self.assertEqual(self.page.evaluate('H'),history)
        self.assertEqual(self.page.evaluate('JSON.stringify(dailyBook)'),book)
        self.nav('Painel');self.click('Ver resultado')
        self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'15 de 20 (75%)')
        self.nav('Trilha');self.nav('Praticar')
        self.assertEqual(self.page.locator('.practice-setup').count(),1)
        self.assertEqual(self.page.evaluate('H'),history)

if __name__=='__main__':unittest.main(verbosity=2)
