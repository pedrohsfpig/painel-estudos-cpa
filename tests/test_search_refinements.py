"""Seleção por aula, filtros de questões e identidade visual consistente."""
import unittest
import smoke as harness

class SearchRefinements(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown

    def search(self,area='all',query='Bacen'):
        self.page.locator('#content-search-input').fill(query)
        self.page.locator(f'[data-search-area="{area}"]').click()

    def test_trail_opens_a_numerically_ordered_lesson_picker_with_real_counts(self):
        self.search('trilha')
        lessons=self.page.locator('[data-search-lesson]').evaluate_all('nodes=>nodes.map(n=>Number(n.dataset.searchLesson))')
        self.assertGreater(len(lessons),4)
        self.assertEqual(lessons,sorted(lessons))
        self.assertEqual(self.page.locator('[data-search-result]').count(),0)
        total=0
        for lesson in lessons:
            count=self.page.evaluate('a=>scopedSearchResults().filter(d=>searchArea(d)==="trilha"&&d.lesson===a).length',lesson)
            self.assertIn(f'{count} informa',self.page.locator(f'[data-search-lesson="{lesson}"]').inner_text())
            total+=count
        self.assertEqual(total,self.page.evaluate('filteredSearchResults().length'))
        self.page.locator('[data-search-lesson="3"]').click()
        self.assertTrue(self.page.evaluate('filteredSearchResults().every(d=>d.lesson===3)'))
        self.assertGreater(self.page.locator('[data-search-result]').count(),0)
        self.assertEqual(self.page.locator('[data-search-lesson]').count(),0)
        self.page.get_by_role('button',name='Trocar aula',exact=True).click()
        self.assertEqual(self.page.locator('[data-search-result]').count(),0)
        self.assertEqual(self.page.locator('[data-search-lesson]').count(),len(lessons))
        self.page.evaluate("view='t';go()")
        self.page.locator('#content-search-input').fill('Bacen')
        self.assertGreater(self.page.locator('[data-search-lesson]').count(),0)
        self.assertEqual(self.page.locator('.search-global-filters').count(),0)

    def test_global_question_difficulty_mode_and_history_filters_intersect_correctly(self):
        self.search('questoes')
        ids=self.page.evaluate('filteredSearchResults().filter(d=>questionById(d.target.questionId)[2]===0).slice(0,3).map(d=>d.target.questionId)')
        self.page.evaluate('ids=>{H=[[ids[0],false,1,0],[ids[1],false,2,0],[ids[1],true,3,0]];refreshSearchResults()}',ids)
        initial=self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT])')
        for level in ['0','1','2','3','-1']:
            self.page.locator(f'[data-search-level="{level}"]').click()
            rows=self.page.evaluate('filteredSearchResults().map(d=>questionById(d.target.questionId)[2])')
            self.assertTrue(rows)
            self.assertEqual(set(rows),{int(level)})
        self.page.get_by_role('combobox',name='Modo das questões encontradas').select_option('e')
        self.assertEqual(self.page.evaluate('currentSearch().qLevel'),'all')
        self.assertTrue(self.page.evaluate('filteredSearchResults().every(d=>d.type==="questao"&&questionById(d.target.questionId)[2]<3)'))
        self.page.locator('[data-search-level="0"]').click()
        self.page.get_by_role('combobox',name='Histórico das questões encontradas').select_option('answered')
        self.assertEqual(set(self.page.evaluate('filteredSearchResults().map(d=>d.target.questionId)')),set(ids[:2]))
        self.page.get_by_role('combobox',name='Histórico das questões encontradas').select_option('err')
        self.assertEqual(self.page.evaluate('filteredSearchResults().map(d=>d.target.questionId)'),[ids[0]])
        self.assertIn('última resposta',self.page.locator('.search-filter-note').inner_text())
        self.page.get_by_role('combobox',name='Histórico das questões encontradas').select_option('new')
        self.assertTrue(self.page.evaluate('filteredSearchResults().every(d=>!H.some(r=>r[0]===d.target.questionId))'))
        self.assertEqual(self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT])'),initial)

    def test_global_simulation_and_quick_mode_and_lesson_filter_match_their_banks(self):
        self.search('questoes')
        self.page.get_by_role('combobox',name='Modo das questões encontradas').select_option('s')
        self.assertTrue(self.page.evaluate('filteredSearchResults().every(d=>d.type==="questao"&&questionById(d.target.questionId)[2]<3&&!questionById(d.target.questionId)[9])'))
        self.page.get_by_role('combobox',name='Filtrar resultados por aula').select_option('3')
        self.assertTrue(self.page.evaluate('filteredSearchResults().every(d=>d.lesson===3)'))
        expected=self.page.evaluate('filteredSearchResults()[0].target.questionId')
        self.page.locator('[data-search-result]').first.click()
        self.assertEqual(self.page.evaluate('[qz.md,qz.ids]'),['s',[expected]])
        self.page.evaluate("qz=null;view='d';go()")
        self.page.get_by_role('combobox',name='Modo das questões encontradas').select_option('b')
        self.assertTrue(self.page.evaluate('filteredSearchResults().every(d=>d.type==="bate")'))
        self.page.get_by_role('combobox',name='Filtrar resultados por aula').select_option('0')
        self.assertGreater(self.page.evaluate('filteredSearchResults().length'),0)

    def test_material_tiles_show_counts_icons_and_filter_the_actual_kind(self):
        self.search('materiais')
        self.assertEqual(self.page.locator('[data-search-material]').count(),8)
        self.assertEqual(self.page.locator('.search-material-tiles button>.ui-icon').count(),8)
        for kind in ['mapa','diag','tab','tl','fc','geral','sfn']:
            self.page.locator(f'[data-search-material="{kind}"]').click()
            self.assertTrue(self.page.evaluate('type=>filteredSearchResults().every(d=>d.type===type)',kind))
            self.assertGreater(self.page.evaluate('filteredSearchResults().length'),0,kind)
        self.page.locator('[data-search-material="all"]').click()
        self.page.get_by_role('combobox',name='Filtrar resultados por aula').select_option('3')
        self.assertTrue(self.page.evaluate('filteredSearchResults().every(d=>d.lesson===3)'))
        self.page.locator('[data-search-area="trilha"]').click()
        self.assertEqual(self.page.evaluate('currentSearch().lesson'),0)

    def test_lesson_number_color_and_icon_are_consistent_between_picker_and_cards(self):
        self.search('trilha')
        for theme in ['light','dark']:
            self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
            palette={}
            for lesson in [2,3,4,10]:
                node=self.page.locator(f'[data-search-lesson="{lesson}"]')
                palette[lesson]=node.locator('.search-lesson-number').evaluate('n=>getComputedStyle(n).color')
                self.assertEqual(node.locator('.search-lesson-number').inner_text(),str(lesson).zfill(2))
                self.assertEqual(node.locator('.search-lesson-name .ui-icon').count(),1)
            for lesson in [2,3,4,10]:
                self.page.locator(f'[data-search-lesson="{lesson}"]').click()
                cards=self.page.locator('[data-search-result]')
                for card in cards.all():
                    self.assertEqual(card.locator('.search-lesson-number').inner_text(),str(lesson).zfill(2))
                    self.assertEqual(card.locator('.search-lesson-number').evaluate('n=>getComputedStyle(n).color'),palette[lesson])
                self.page.get_by_role('button',name='Trocar aula',exact=True).click()

    def test_keyboard_filters_empty_history_and_small_screens_remain_usable(self):
        self.search('trilha')
        self.page.locator('[data-search-lesson="3"]').focus();self.page.keyboard.press('Enter')
        self.assertEqual(self.page.evaluate('currentSearch().lesson'),3)
        self.page.get_by_role('button',name='Trocar aula',exact=True).click()
        self.page.locator('[data-search-area="questoes"]').click()
        self.page.get_by_role('combobox',name='Histórico das questões encontradas').select_option('err')
        self.assertEqual(self.page.evaluate('filteredSearchResults().length'),0)
        self.assertIn('Nenhum resultado',self.page.locator('.search-empty').inner_text())
        self.page.get_by_role('combobox',name='Histórico das questões encontradas').select_option('all')
        for width in [390,1024,1280,1440,1920]:
            self.page.set_viewport_size(dict(width=width,height=950))
            for theme in ['light','dark']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
                for area in ['trilha','questoes','materiais','all']:
                    self.page.locator(f'[data-search-area="{area}"]').click()
                    self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'),(width,theme,area))
                    self.assertTrue(self.page.locator('.content-search').evaluate('n=>n.scrollWidth<=n.clientWidth+1'))

if __name__=='__main__':unittest.main(verbosity=2)
