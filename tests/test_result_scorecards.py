"""Indicadores por resposta e ordenação devem facilitar a leitura sem alterar a sessão."""
import unittest
import smoke as harness

class ResultScorecards(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    answer=harness.PainelCPA.answer
    click=harness.PainelCPA.click
    complete_ids=harness.PainelCPA.complete_ids

    def test_individual_marks_match_actual_answers_in_each_lesson_and_level(self):
        self.complete_ids([1,2,21,101,102],'e',{0,2,3})
        result=self.page.evaluate('''()=>{const a=sessionAnalysis();return [...a.lessons.map(g=>[g,'lesson']),...a.levels.map(g=>[g,'level'])].map(([g,kind])=>{const card=document.querySelector(`[data-result-${kind}="${g.key}"]`);return {expected:g.rows.map(r=>r.ok),marks:[...card.querySelectorAll('.result-answer-mark')].map(n=>!n.classList.contains('is-error')),ok:g.ok,n:g.n,wrong:g.wrong,text:card.textContent,label:card.querySelector('[role="img"]').getAttribute('aria-label')};})}''')
        for r in result:
            self.assertEqual(r['marks'],r['expected'])
            self.assertIn(f"{r['ok']} de {r['n']} corretas",r['text'])
            self.assertIn(f"{r['ok']} acertos e {r['wrong']} erros",r['label'])
        self.assertIn('Um ponto por resposta',self.page.locator('.result-marks-legend').inner_text())

    def test_keyboard_sort_prioritizes_errors_and_preserves_history_timer_and_open_review(self):
        ids=self.page.evaluate("[...Q.map((q,i)=>({q,id:i+1})).filter(x=>x.q[0]===1&&x.q[2]<3).slice(0,3),...Q.map((q,i)=>({q,id:i+1})).filter(x=>x.q[0]===2&&x.q[2]<3).slice(0,2),...Q.map((q,i)=>({q,id:i+1})).filter(x=>x.q[0]===3&&x.q[2]<3).slice(0,3)].map(x=>x.id)")
        self.complete_ids(ids,'e',{0,3,4})
        self.page.locator('details.rv summary').first.click()
        initial=self.page.evaluate('JSON.stringify([qz,H,Q,BP])')
        def order():return self.page.locator('.result-lessons>[data-result-lesson]').evaluate_all('nodes=>nodes.map(n=>Number(n.dataset.resultLesson))')
        self.assertEqual(order(),[1,2,3])
        button=self.page.get_by_role('button',name='Mais erros',exact=True)
        button.focus();self.page.keyboard.press('Enter')
        self.assertEqual(order(),[3,1,2])
        self.assertEqual(button.get_attribute('aria-pressed'),'true')
        self.assertTrue(button.evaluate('n=>n===document.activeElement'))
        self.assertEqual(self.page.locator('details.rv[open]').count(),1)
        self.assertEqual(self.page.evaluate('JSON.stringify([qz,H,Q,BP])'),initial)
        self.click('Por aula');self.assertEqual(order(),[1,2,3])
        self.page.evaluate('orderResultLessons("invalid")');self.assertEqual(order(),[1,2,3])
        self.assertEqual(self.page.evaluate('JSON.stringify([qz,H,Q,BP])'),initial)

    def test_many_answers_show_explicit_truncation_but_keep_full_percentages_and_counts(self):
        ids=self.page.evaluate("Q.map((q,i)=>({q,id:i+1})).filter(x=>x.q[0]===1&&x.q[2]<3).slice(0,20).map(x=>x.id)")
        self.complete_ids(ids,'e',set(range(12)))
        card=self.page.locator('[data-result-lesson="1"]')
        self.assertEqual(card.locator('.result-answer-mark').count(),12)
        self.assertEqual(card.locator('.result-answer-mark.is-error').count(),0)
        self.assertIn('60%',card.inner_text())
        self.assertIn('12 de 20 corretas',card.inner_text())
        self.assertIn('8 erros',card.inner_text())
        self.assertEqual(card.locator('.result-marks-more').inner_text(),'+8')
        self.assertIn('Primeiras 12 respostas por grupo',self.page.locator('.result-marks-legend').inner_text())
        self.assertIn('pontos mostram as primeiras 12',card.locator('[role="img"]').get_attribute('aria-label'))
        self.assertEqual(self.page.evaluate('H.length'),20)

    def test_percentages_are_neutral_and_plots_do_not_use_red_green_split(self):
        self.complete_ids([1,2,21],'e',{0,2})
        for theme in ['light','dark']:
            self.page.evaluate('x=>document.documentElement.dataset.theme=x',theme)
            self.assertTrue(self.page.locator('.result-percent').evaluate_all('nodes=>nodes.every(n=>getComputedStyle(n).color===getComputedStyle(document.body).color)'))
            self.assertEqual(self.page.locator('.result-bar,.result-rate').count(),0)
            styles=self.page.evaluate('''()=>{const root=getComputedStyle(document.documentElement);const probe=document.createElement('i');document.body.append(probe);const color=v=>{probe.style.color=v;return getComputedStyle(probe).color};const forbidden=[color(root.getPropertyValue('--ok')),color(root.getPropertyValue('--hd'))];probe.remove();return {forbidden,marks:[...document.querySelectorAll('.result-charts .result-answer-mark')].map(n=>({fill:getComputedStyle(n).backgroundColor,border:getComputedStyle(n).borderTopColor})),ring:[...document.querySelectorAll('.result-ring circle')].map(n=>getComputedStyle(n).stroke)};}''')
            self.assertTrue(styles['marks'])
            for mark in styles['marks']:
                self.assertNotIn(mark['fill'],styles['forbidden'])
                self.assertNotIn(mark['border'],styles['forbidden'])
            for color in styles['ring']:self.assertNotIn(color,styles['forbidden'])

if __name__=='__main__':unittest.main(verbosity=2)
