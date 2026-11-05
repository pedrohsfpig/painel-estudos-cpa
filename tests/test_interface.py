"""Legibilidade e preservação dos fluxos após a revisão visual global."""
import unittest
import smoke as harness


class InterfaceTests(unittest.TestCase):
    setUpClass = classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass = classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp = harness.PainelCPA.setUp
    tearDown = harness.PainelCPA.tearDown

    def assert_readable(self):
        problems = self.page.locator('body').evaluate('''e => [...e.querySelectorAll('*')]
          .filter(n => !n.closest('svg,.sr-only') && n.getClientRects().length &&
            getComputedStyle(n).visibility !== 'hidden' &&
            [...n.childNodes].some(c => c.nodeType === 3 && c.textContent.trim()) &&
            parseFloat(getComputedStyle(n).fontSize) < 13)
          .map(n => ({tag:n.tagName, cls:n.className, text:n.textContent.slice(0,80),
            size:getComputedStyle(n).fontSize}))''')
        self.assertEqual(problems, [])
        self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth > innerWidth'))

    def test_every_area_remains_readable_on_desktop_tablet_and_phone(self):
        self.page.evaluate("H=[[1,true,1700000000000,0],[2,false,1700000000001,0]];go()")
        for width in [390,768,1024,1440,1920]:
            self.page.set_viewport_size(dict(width=width,height=1000))
            for theme in ['light','dark']:
                for view in ['d','t','c','q','e','m','x','stats','exam']:
                    with self.subTest(width=width,theme=theme,view=view):
                        self.page.evaluate('''([theme,v])=>{document.documentElement.dataset.theme=theme;
                          view=v;qz=null;go();document.querySelectorAll('.lesson-section').forEach(n=>n.open=true)}''',[theme,view])
                        self.assert_readable()
                        self.assertEqual(self.page.locator('.nav-item[aria-current="page"]').count(),1)

    def test_materials_keep_readable_text_and_all_lesson_content(self):
        before=self.page.evaluate('JSON.stringify([Q,BP,AL,MAT,H,cfg])')
        for width in [390,1024,1440]:
            self.page.set_viewport_size(dict(width=width,height=1000))
            for theme in ['light','dark']:
                for lesson,kind in [(1,'geral'),(7,'geral'),(1,'mapa'),(13,'mapa'),(1,'diag'),
                                    (13,'diag'),(7,'tab'),(13,'tab'),(3,'tl'),(13,'tl'),(1,'visual'),(13,'fc')]:
                    with self.subTest(width=width,theme=theme,lesson=lesson,kind=kind):
                        self.page.evaluate('''([theme,a,c])=>{document.documentElement.dataset.theme=theme;
                          view='m';mt={a,c};fi=0;ff=0;go()}''',[theme,lesson,kind])
                        self.assert_readable()
        self.assertEqual(before,self.page.evaluate('JSON.stringify([Q,BP,AL,MAT,H,cfg])'))

    def test_phone_session_summary_keeps_lesson_and_filter_controls_unobstructed(self):
        self.page.set_viewport_size(dict(width=390,height=900))
        self.page.evaluate("view='q';qz=null;go()")
        boxes=[self.page.locator(s).bounding_box() for s in
               ['.practice-lesson-panel','.practice-launch','.practice-options','.practice-timer-note']]
        for first,second in zip(boxes,boxes[1:]):
            self.assertLessEqual(first['y']+first['height'],second['y'])
        self.page.locator('.practice-launch button').click()
        self.assertEqual(self.page.evaluate('qz.ids.length'),10)

    def test_visual_navigation_and_theme_preserve_answered_session_and_timer(self):
        self.page.evaluate("begin([1,2,3],'e');pick(qz.o.findIndex(o=>o[1]))")
        before=self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT,qz])')
        for theme in ['light','dark']:
            for view in ['d','m','stats','c','t','x','exam','e','q']:
                self.page.evaluate('''([theme,v])=>{document.documentElement.dataset.theme=theme;view=v;go()}''',[theme,view])
                self.assertEqual(before,self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT,qz])'))
        self.assertEqual(self.page.locator('.fb-option').count(),4)
        self.assertEqual(self.page.locator('.quiz-progress-segment').count(),3)
        self.assert_readable()
        self.page.evaluate('nextQuestion()')
        self.assertEqual(self.page.evaluate('[qz.i,qz.ids.length,H.length]'),[1,3,1])

    def test_quick_practice_flashcard_and_results_have_legible_labels(self):
        for theme in ['light','dark']:
            self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
            self.page.evaluate("begin([BP_FIRST_ID,BP_FIRST_ID+1],'b')")
            self.assert_readable()
            self.page.evaluate('pick(qz.o.findIndex(o=>o[1]))')
            self.assert_readable()
            self.page.evaluate("begin([1],'e');pick(qz.o.findIndex(o=>o[1]));nextQuestion()")
            self.assert_readable()
            self.page.evaluate("view='m';mt={a:1,c:'fc'};fi=0;ff=0;go();flipCard()")
            self.assert_readable()

    def test_expanded_search_statistics_and_concept_picker_are_readable(self):
        for width in [390,1024,1440]:
            self.page.set_viewport_size(dict(width=width,height=1000))
            for theme in ['light','dark']:
                self.page.evaluate('t=>{document.documentElement.dataset.theme=t;view="d";qz=null;go()}',theme)
                self.page.locator('#content-search-input').fill('liquidez')
                self.assert_readable()
                for area in ['questoes','materiais','trilha','all']:
                    self.page.locator(f'[data-search-area="{area}"]').click()
                    self.assert_readable()
                    if area=='questoes':
                        self.page.get_by_role('combobox',name='Modo das questões encontradas',exact=True).click()
                        self.assert_readable()
                        self.page.keyboard.press('Escape')
                self.page.evaluate("view='stats';H=[[1,true,1700000000000,0],[2,false,1700000000001,0]];go();document.querySelectorAll('.stats-section').forEach(n=>n.open=true)")
                self.assert_readable()
                self.page.evaluate("view='m';mt={a:3,c:'mapa'};go()")
                self.page.locator('.mind-branch .active-study-options-trigger').first.click()
                self.assert_readable()
                self.page.keyboard.press('Escape')


if __name__ == '__main__':
    unittest.main(verbosity=2)
