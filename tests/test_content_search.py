"""Busca real entre fontes e navegação, sem alterar banco, histórico ou prática."""
import unittest
import smoke as harness

class ContentSearch(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click
    answer=harness.PainelCPA.answer

    def search(self, query, view='t'):
        self.page.evaluate("v=>{view=v;go()}",view)
        self.page.locator('#content-search-input').fill(query)

    def test_aliases_accents_multiple_terms_and_all_material_sources(self):
        results=self.page.evaluate('''()=>{
            const ids=q=>searchContent(q,'all').map(d=>d.id);
            return {aliases:['Bacen','BCB','BC','Banco Central','Banco Central do Brasil'].map(ids),
              accent:ids('compulsório'),plain:ids('compulsorio'),
              lessons:[...new Set(searchContent('compulsório','all').map(d=>d.lesson))],
              types:[...new Set(searchContent('Bacen','all').map(d=>d.type))],
              and:searchContent('Bacen compulsório','all').map(d=>({words:d.words,lesson:d.lesson})),
              safe:searchContent('IP','all').every(d=>d.words.includes(searchCanonical('IP'))),
              empty:searchContent('de da do','all').length};
        }''')
        self.assertGreater(len(results['aliases'][0]),100)
        for ids in results['aliases']:self.assertEqual(ids,results['aliases'][0])
        self.assertEqual(results['accent'],results['plain'])
        self.assertEqual(results['lessons'],[3,10])
        self.assertEqual(set(results['types']),{'aula','trilha','mapa','diag','tab','tl','fc','geral'})
        self.assertTrue(results['and'])
        self.assertTrue(results['safe'])
        self.assertEqual(results['empty'],0)
        self.assertTrue(self.page.evaluate("searchContent('Bacen compulsório','all').every(d=>searchTokens('Bacen compulsório').every(t=>d.words.some(w=>w.startsWith(t))))"))

    def test_live_search_preserves_focus_shows_multiple_lessons_and_reaches_all_results(self):
        self.search('Bacen')
        self.assertTrue(self.page.locator('#content-search-input').evaluate('n=>n===document.activeElement'))
        self.assertIn('resultados em 10 aulas',self.page.locator('.search-result-status').inner_text())
        self.assertEqual(self.page.locator('.search-lesson-group').count(),10)
        self.assertEqual(self.page.locator('[data-search-result]').count(),24)
        self.page.locator('[data-search-type="mapa"]').click()
        self.assertTrue(self.page.evaluate("[...document.querySelectorAll('[data-search-result]')].every(n=>contentSearchIndex()[Number(n.dataset.searchResult)].type==='mapa')"))
        self.page.locator('[data-search-type="all"]').click()
        total=self.page.evaluate("searchContent().length")
        for _ in range((total+23)//24):
            more=self.page.locator('.search-more')
            if not more.count():break
            more.focus();self.page.keyboard.press('Enter')
        self.assertEqual(self.page.locator('[data-search-result]').count(),total)
        self.assertEqual(self.page.locator('[data-search-result]').evaluate_all('nodes=>new Set(nodes.map(n=>n.dataset.searchResult)).size'),total)
        self.assertTrue(self.page.locator('[data-search-result]').evaluate_all('nodes=>nodes.some(n=>n===document.activeElement)'))

    def test_exact_destinations_open_matching_section_branch_table_card_and_overview_row(self):
        samples=self.page.evaluate("Object.keys(searchTypeNames).map(type=>contentSearchIndex().find(d=>d.type===type&&d.lesson===(type==='mapa'?3:1))).filter(Boolean).map(d=>d.id)")
        self.assertEqual(len(samples),8)
        for doc_id in samples:
            doc=self.page.evaluate('id=>contentSearchIndex()[id]',doc_id)
            with self.subTest(type=doc['type']):
                self.page.evaluate('id=>openSearchResult(id)',doc_id)
                target=self.page.locator('.search-target')
                self.assertEqual(target.count(),1)
                self.assertTrue(target.evaluate('n=>n===document.activeElement'))
                self.assertFalse(self.page.locator('.search-matches').evaluate('n=>n.open'))
                self.assertEqual(self.page.evaluate('selectedLessonBlocks['+str(doc['lesson'])+']'),0)
                if doc['type']=='trilha':self.assertTrue(self.page.locator('#'+doc['target']['section']).evaluate('n=>n.open'))
                elif doc['type']=='mapa':self.assertEqual(target.get_attribute('data-source-index'),str(doc['target']['index']))
                elif doc['type']=='fc':
                    self.assertEqual(self.page.evaluate('[fi,ff]'),[doc['target']['index'],0])
                    self.assertEqual(target.locator('.flashcard-text').inner_text(),doc['title'])
                elif doc['type']=='geral':self.assertEqual(target.get_attribute('data-operator'),doc['target']['row'])
        self.page.evaluate("openSearchResult(contentSearchIndex().find(d=>d.type==='aula'&&d.lesson===7&&d.target.block===2).id)")
        self.assertEqual(self.page.evaluate('[view,tr,selectedLessonBlocks[7]]'),['t',7,2])
        self.assertIn('Crédito',self.page.locator('.lesson-content-filter [aria-pressed="true"]').inner_text())

    def test_search_and_material_navigation_preserve_an_incomplete_session_and_history(self):
        self.page.evaluate("cfg={a:0,as:[1,2],n:1,m:'all',c:10,md:'e',b:0};begin([1,2],'e')")
        self.answer()
        self.page.evaluate("view='t';go()")
        initial=self.page.evaluate('JSON.stringify([qz,H,cfg,Q,BP,AL,MAT])')
        self.page.locator('#content-search-input').fill('Bacen')
        self.page.locator('[data-search-type="tab"]').click()
        self.page.locator('[data-search-result]').first.click()
        self.page.locator('#theme-toggle').click()
        self.assertEqual(self.page.evaluate('JSON.stringify([qz,H,cfg,Q,BP,AL,MAT])'),initial)
        self.page.locator('.nav').get_by_role('button',name='Praticar',exact=True).click()
        self.assertEqual(self.page.locator('#content-search-input').count(),0)
        self.assertEqual(self.page.locator('.quiz-header').count(),1)
        self.assertEqual(self.page.evaluate('JSON.stringify([qz,H,cfg,Q,BP,AL,MAT])'),initial)

    def test_practice_search_keeps_hidden_selections_and_does_not_change_allocation(self):
        self.click('Praticar')
        self.page.locator('[data-practice-lesson="1"]').click()
        self.page.locator('#content-search-input').fill('compulsorio')
        self.assertFalse(self.page.locator('[data-practice-lesson="1"]').is_visible())
        self.assertEqual(self.page.locator('[data-practice-lesson]:visible').evaluate_all('nodes=>nodes.map(n=>Number(n.dataset.practiceLesson))'),[0,3,10])
        self.assertTrue(self.page.get_by_role('button',name='Remover aula 1 da seleção',exact=True).is_visible())
        self.page.locator('[data-practice-lesson="10"]').click()
        self.assertEqual(self.page.locator('#content-search-input').input_value(),'compulsorio')
        self.assertEqual(self.page.evaluate('selectedPracticeLessons()'),[1,10])
        plan=self.page.evaluate('sessionPlan()')
        self.assertEqual([g['count'] for g in plan['groups']],[5,5])
        self.page.locator('#content-search-input').fill('nenhumtermoencontradoteste')
        self.assertIn('Nenhum conteúdo encontrado',self.page.locator('.search-empty').inner_text())
        self.assertEqual(self.page.evaluate('sessionPlan()'),plan)
        self.page.locator('#content-search-input').press('Escape')
        self.assertEqual(self.page.locator('#content-search-input').input_value(),'')
        self.assertEqual(self.page.locator('[data-practice-lesson]:visible').count(),12)
        self.click('Iniciar estudo')
        self.assertEqual(self.page.evaluate('[1,10].map(a=>qz.ids.filter(id=>questionById(id)[0]===a).length)'),[5,5])

    def test_no_results_clear_and_untrusted_queries_are_safe_and_sources_remain_complete(self):
        initial=self.page.evaluate('JSON.stringify([Q,BP,AL,MAT,H])')
        self.search('<img src=x onerror="window.searchInjected=true">')
        self.assertEqual(self.page.locator('.content-search img').count(),0)
        self.assertFalse(self.page.evaluate('Boolean(window.searchInjected)'))
        self.assertEqual(self.page.locator('.tr .st:visible').count(),0)
        self.page.locator('.search-clear').click()
        self.assertEqual(self.page.locator('.tr .st:visible').count(),11)
        self.assertTrue(self.page.locator('#content-search-input').evaluate('n=>n===document.activeElement'))
        self.assertEqual(self.page.evaluate('JSON.stringify([Q,BP,AL,MAT,H])'),initial)
        self.page.evaluate("AL.push({...AL[0],t:'Aula 12: Reservafutura',o:'Conceitofuturo exclusivo'});go()")
        self.page.locator('#content-search-input').fill('conceitofuturo')
        self.assertIn('Aula 12: Reservafutura',self.page.locator('.search-lesson-group').inner_text())
        self.assertEqual(self.page.evaluate('searchContent().map(d=>d.lesson)'),[12])

    def test_shared_query_and_results_fit_desktop_mobile_and_both_themes(self):
        self.search('Bacen')
        for width in [390,1024,1280,1440,1920]:
            self.page.set_viewport_size(dict(width=width,height=900))
            for theme in ['light','dark']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
                for screen in ['t','m','q']:
                    self.page.evaluate('v=>{view=v;go()}',screen)
                    self.assertEqual(self.page.locator('#content-search-input').count(),1)
                    self.assertEqual(self.page.locator('#content-search-input').input_value(),'Bacen')
                    self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'),(width,theme,screen))
                    self.assertTrue(self.page.locator('.content-search').evaluate('n=>n.scrollWidth<=n.clientWidth+1'))

if __name__=='__main__':unittest.main(verbosity=2)
