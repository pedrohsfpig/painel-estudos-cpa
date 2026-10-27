"""Hierarquia do painel orienta ações sem alterar métricas ou dados completos."""
import unittest
import smoke as harness

class DashboardHierarchy(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click

    def test_primary_daily_next_action_and_metrics_have_clear_reading_order(self):
        self.page.set_viewport_size(dict(width=1440,height=1000))
        sections=['.hoje','.next-study-action','.dashboard-metrics','.dashboard-grid']
        positions=[self.page.locator(s).bounding_box() for s in sections]
        self.assertEqual([p['y'] for p in positions],sorted(p['y'] for p in positions))
        for a,b in zip(positions,positions[1:]):self.assertLessEqual(a['y']+a['height'],b['y'])
        self.assertIn('Comece pelos fundamentos',self.page.locator('#next-action-title').inner_text())
        self.assertEqual(self.page.locator('.g4 .mv').all_text_contents(),['0','0','0','0%'])
        self.assertLess(self.page.locator('.evolution').bounding_box()['y'],self.page.locator('.dashboard-trail-list').bounding_box()['y'])
        self.assertEqual(self.page.locator('.trail-row').count(),self.page.evaluate('AL.length'))
        self.page.locator('.next-study-action button').click()
        self.assertEqual(self.page.evaluate('[view,tr]'),['t',1])
        self.assertEqual(self.page.evaluate('H'),[])

    def test_suggestions_use_actual_pending_errors_recent_lesson_and_active_session(self):
        self.page.evaluate("H=[[1,true,1000,0],[101,false,2000,0]];go()")
        self.assertIn('Revise',self.page.locator('#next-action-title').inner_text())
        self.assertIn('1 erro pendente',self.page.locator('.next-study-action p').inner_text())
        history=self.page.evaluate('H')
        self.page.locator('.next-study-action button').click()
        self.assertEqual(self.page.evaluate('view'),'e')
        self.assertEqual(self.page.evaluate('H'),history)
        self.page.evaluate("H.push([101,true,3000,0]);view='d';go()")
        self.assertIn('Continue a última aula',self.page.locator('#next-action-title').inner_text())
        self.page.locator('.next-study-action button').click()
        self.assertEqual(self.page.evaluate('[view,tr]'),['t',2])
        self.page.evaluate("begin([1,2],'e');view='d';go()")
        state=self.page.evaluate('JSON.stringify(qz)')
        self.assertIn('sessão em andamento',self.page.locator('#next-action-title').inner_text())
        self.page.locator('.next-study-action button').click()
        self.assertEqual(self.page.evaluate('view'),'q')
        self.assertEqual(self.page.evaluate('JSON.stringify(qz)'),state)

    def test_all_lessons_and_full_evolution_remain_accessible_with_more_content(self):
        self.page.evaluate("AL.push(...AL.slice(0,9));H=[[1,1,Date.parse('2025-01-01T12:00:00Z'),0],[2,0,Date.parse('2026-10-20T12:00:00Z'),0]];go()")
        self.assertEqual(self.page.locator('.trail-row').count(),self.page.evaluate('AL.length'))
        self.assertEqual(self.page.evaluate('evolutionData().keys.length'),2)
        self.assertTrue(self.page.locator('.dashboard-trail-list').evaluate('n=>n.scrollHeight>n.clientHeight'))
        self.page.locator('.trail-row').last.focus()
        self.assertTrue(self.page.locator('.trail-row').last.evaluate('n=>n===document.activeElement'))
        self.assertTrue(self.page.locator('.trail-row').last.evaluate('n=>{const r=n.getBoundingClientRect(),p=n.parentElement.getBoundingClientRect();return r.top>=p.top&&r.bottom<=p.bottom+1}'))

    def test_dashboard_layout_preserves_history_filters_and_readability_in_both_themes(self):
        self.page.evaluate("H=[[1,1,1700000000000,0],[2,0,1700000000001,0]];fl=0;go()")
        state=self.page.evaluate('JSON.stringify([H,Q,BP,cfg,fl,fm])')
        for width in [390,1024,1280,1440,1920]:
            self.page.set_viewport_size(dict(width=width,height=900))
            for theme in ['light','dark']:
                self.page.evaluate('t=>{document.documentElement.dataset.theme=t;go()}',theme)
                self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'))
                self.assertEqual(self.page.evaluate('JSON.stringify([H,Q,BP,cfg,fl,fm])'),state)
                self.assertGreaterEqual(self.page.locator('.next-study-action p').evaluate('n=>parseFloat(getComputedStyle(n).fontSize)'),14)
                self.assertEqual(self.page.locator('.dashboard-filters,.detail-stats').count(),0)
                self.assertEqual(self.page.get_by_role('button',name='Ver estatísticas detalhadas').count(),1)
                self.assertTrue(self.page.locator('.next-study-action,.dashboard-metrics,.dashboard-column').evaluate_all('nodes=>nodes.every(n=>n.scrollWidth<=n.clientWidth+1)'))

if __name__=='__main__':unittest.main(verbosity=2)
