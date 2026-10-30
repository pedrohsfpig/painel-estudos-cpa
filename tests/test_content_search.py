"""Busca contextual em cada tela; consulta geral e filtros somente no painel."""
import unittest
import smoke as harness

class ContentSearch(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click
    answer=harness.PainelCPA.answer

    def search(self,query,view='t',kind=None):
        self.page.evaluate("([v,k])=>{view=v;if(k)mt.c=k;go()}",[view,kind])
        self.page.locator('#content-search-input').fill(query)

    def sources(self):
        return self.page.locator('[data-search-source]').evaluate_all('nodes=>nodes.map(n=>n.dataset.searchSource)')

    def test_aliases_accents_combined_terms_and_index_cover_every_content_area(self):
        result=self.page.evaluate('''()=>{
          const ids=q=>searchContent(q,'all').map(d=>d.id);
          return {aliases:['Bacen','BCB','BC','Banco Central','Banco Central do Brasil'].map(ids),
            accent:ids('compulsório'),plain:ids('compulsorio'),
            lessons:[...new Set(searchContent('compulsório','all').map(d=>d.lesson))],
            types:[...new Set(contentSearchIndex().map(d=>d.type))],
            safe:searchContent('IP','all').every(d=>d.words.includes(searchCanonical('IP'))),
            empty:searchContent('de da do','all').length};
        }''')
        self.assertGreater(len(result['aliases'][0]),100)
        for ids in result['aliases']:self.assertEqual(ids,result['aliases'][0])
        self.assertEqual(result['accent'],result['plain'])
        self.assertTrue({3,10}.issubset(result['lessons']))
        self.assertEqual(set(result['types']),{'aula','trilha','mapa','visual','diag','tab','tl','fc','geral','questao','bate','sfn'})
        self.assertTrue(result['safe']);self.assertEqual(result['empty'],0)
        self.assertTrue(self.page.evaluate("searchContent('Bacen compulsório','all').every(d=>searchTokens('Bacen compulsório').every(t=>d.words.some(w=>w.startsWith(t))))"))

    def test_local_searches_never_return_other_sections(self):
        self.search('Bacen','t')
        self.assertTrue(set(self.sources()).issubset({'aula','trilha'}))
        self.assertEqual(self.page.locator('.search-global-filters').count(),0)
        for kind in ['mapa','visual','diag','tab','tl','fc','geral']:
            self.search('Bacen','m',kind)
            self.assertTrue(self.sources(),kind)
            self.assertEqual(set(self.sources()),{kind})
            self.assertEqual(self.page.locator('.search-global-filters').count(),0)
            self.assertTrue(self.page.get_by_text('Buscar em '+self.page.evaluate('k=>searchTypeNames[k]',kind),exact=True).is_visible())
        self.search('inflação','q')
        self.assertEqual(set(self.sources()),{'questao'})
        self.assertTrue(self.page.evaluate('filteredSearchResults().every(d=>questionById(d.target.questionId)[2]<3)'))
        self.assertEqual(self.page.locator('.fb-option').count(),0)

    def test_global_search_below_daily_can_filter_each_area_and_material_kind(self):
        self.search('inflação','d')
        self.assertTrue(self.page.locator('.hoje').evaluate("n=>n.nextElementSibling.classList.contains('search-global')"))
        self.assertEqual(self.page.locator('[data-search-area]').count(),4)
        for area,allowed in [('trilha',{'aula','trilha'}),('questoes',{'questao','bate'}),('materiais',{'mapa','visual','diag','tab','tl','fc','geral','sfn'})]:
            self.page.locator(f'[data-search-area="{area}"]').click()
            self.assertTrue(set(self.sources()).issubset(allowed))
            if area=='trilha':
                self.assertGreater(self.page.locator('[data-search-lesson]').count(),0)
                self.assertEqual(self.page.locator('[data-search-result]').count(),0)
                self.page.locator('[data-search-lesson]').first.click()
            self.assertTrue(self.sources())
        self.page.locator('[data-search-material="tab"]').click()
        self.assertEqual(set(self.sources()),{'tab'})
        self.page.locator('[data-search-area="all"]').click()
        self.assertGreater(self.page.evaluate('filteredSearchResults().length'),self.page.evaluate("searchContent('inflação','tab').length"))

    def test_queries_are_independent_between_views_and_material_tabs(self):
        self.search('Bacen','t');self.search('inflação','m','tab')
        self.page.evaluate("view='t';go()")
        self.assertEqual(self.page.locator('#content-search-input').input_value(),'Bacen')
        self.page.evaluate("view='m';mt.c='mapa';go()")
        self.assertEqual(self.page.locator('#content-search-input').input_value(),'')
        self.search('FGC','d');self.page.evaluate("view='m';mt.c='tab';go()")
        self.assertEqual(self.page.locator('#content-search-input').input_value(),'inflação')
        self.page.evaluate("view='q';go()")
        self.assertEqual(self.page.locator('#content-search-input').input_value(),'')
        self.assertEqual(self.page.locator('[data-practice-lesson]:visible').count(),self.page.evaluate('AL.length+1'))

    def test_compact_pagination_reaches_every_match_without_an_inner_scroll_list(self):
        self.search('inflação','d')
        self.assertEqual(self.page.locator('[data-search-result]').count(),4)
        self.assertEqual(self.page.locator('.search-result-list,.search-matches').count(),0)
        self.assertEqual(self.page.locator('.search-result-grid').evaluate('n=>getComputedStyle(n).overflowY'),'visible')
        total=self.page.evaluate('filteredSearchResults().length');seen=set()
        pages=(total+3)//4
        for page in range(pages):
            self.page.get_by_role('combobox',name='Página dos resultados').select_option(str(page))
            self.assertLessEqual(self.page.locator('[data-search-result]').count(),4)
            seen.update(self.page.locator('[data-search-result]').evaluate_all('nodes=>nodes.map(n=>Number(n.dataset.searchResult))'))
        self.assertEqual(len(seen),total)
        self.assertTrue(self.page.get_by_role('button',name='Próxima página de resultados',exact=True).is_disabled())
        self.page.get_by_role('button',name='Recolher resultados',exact=True).click()
        self.assertEqual(self.page.locator('[data-search-result]').count(),0)
        self.page.get_by_role('button',name='Mostrar resultados',exact=True).click()
        self.assertGreater(self.page.locator('[data-search-result]').count(),0)

    def test_exact_content_destinations_open_the_requested_source(self):
        for kind in ['aula','trilha','mapa','diag','tab','tl','fc','geral','sfn']:
            doc=self.page.evaluate("kind=>contentSearchIndex().find(d=>d.type===kind&&d.lesson===(kind==='mapa'?3:1))",kind)
            self.page.evaluate('id=>openSearchResult(id)',doc['id'])
            target=self.page.locator('.search-target')
            self.assertEqual(target.count(),1,kind)
            self.assertTrue(target.evaluate('n=>n===document.activeElement'))
            if kind=='trilha':self.assertTrue(self.page.locator('#'+doc['target']['section']).evaluate('n=>n.open'))
            elif kind=='mapa':self.assertEqual(target.get_attribute('data-source-index'),str(doc['target']['index']))
            elif kind=='fc':self.assertEqual(self.page.evaluate('[fi,ff]'),[doc['target']['index'],0])
            elif kind=='geral':self.assertEqual(target.get_attribute('data-operator'),doc['target']['row'])
            elif kind=='sfn':self.assertEqual(self.page.evaluate('view'),'x')
        self.page.evaluate("openSearchResult(contentSearchIndex().find(d=>d.type==='aula'&&d.lesson===7&&d.target.block===2).id)")
        self.assertEqual(self.page.evaluate('[view,tr,selectedLessonBlocks[7]]'),['t',7,2])

    def test_question_search_honors_mode_level_and_history_filters_without_answer_leaks(self):
        for mode,kind,level in [('e','questao',0),('s','questao',1),('h','questao',3),('b','bate',-1)]:
            self.page.evaluate("([mode,level])=>{view='q';qz=null;cfg.md=mode;cfg.n=level===3?1:level;cfg.m='all';go()}",[mode,level])
            self.page.locator('#content-search-input').fill('Bacen')
            docs=self.page.evaluate('filteredSearchResults().map(d=>({kind:d.type,id:d.target.questionId,level:questionById(d.target.questionId)[2],onlyStudy:questionById(d.target.questionId)[9]}))')
            self.assertTrue(docs,mode)
            self.assertTrue(all(d['kind']==kind and d['level']==level for d in docs),mode)
            if mode=='s':self.assertTrue(all(not d['onlyStudy'] for d in docs))
        self.page.evaluate("view='q';cfg.md='e';cfg.n=-1;cfg.m='err';H=[[1,false,1,0],[2,true,2,0]];go()")
        self.page.locator('#content-search-input').fill('SFN')
        self.assertEqual(self.page.evaluate('filteredSearchResults().map(d=>d.target.questionId)'),[1])
        self.assertEqual(self.page.locator('.fb-option,.feedback,.fb-correct').count(),0)

    def test_question_action_is_explicit_and_never_overwrites_an_existing_session(self):
        self.search('inflação','q')
        cfg=self.page.evaluate('JSON.stringify(cfg)')
        doc=self.page.evaluate('filteredSearchResults()[0]')
        self.assertIsNone(self.page.evaluate('qz'))
        self.page.locator('[data-search-result]').first.click()
        self.assertEqual(self.page.evaluate('qz.ids'),[doc['target']['questionId']])
        self.assertEqual(self.page.evaluate('H'),[])
        self.assertEqual(self.page.evaluate('JSON.stringify(cfg)'),cfg)
        self.answer();self.page.evaluate("qz=null;begin([1,2],'e');view='d';go()")
        state=self.page.evaluate('JSON.stringify([qz,H,cfg])')
        self.page.locator('#content-search-input').fill('inflação')
        self.page.locator('[data-search-area="questoes"]').click()
        self.assertIn('Continuar sessão',self.page.locator('[data-search-result]').first.inner_text())
        self.page.locator('[data-search-result]').first.click()
        self.assertEqual(self.page.evaluate('JSON.stringify([qz,H,cfg])'),state)
        self.assertEqual(self.page.evaluate('view'),'q')

    def test_practice_keeps_hidden_selections_and_the_original_balanced_plan(self):
        self.click('Praticar');self.page.locator('[data-practice-lesson="1"]').click()
        self.page.locator('#content-search-input').fill('compulsório')
        self.assertFalse(self.page.locator('[data-practice-lesson="1"]').is_visible())
        self.assertTrue(self.page.get_by_role('button',name='Remover aula 1 da seleção',exact=True).is_visible())
        self.page.locator('[data-practice-lesson="10"]').click()
        self.assertEqual(self.page.evaluate('selectedPracticeLessons()'),[1,10])
        plan=self.page.evaluate('sessionPlan()');self.assertEqual([g['count'] for g in plan['groups']],[5,5])
        self.page.locator('#content-search-input').fill('nenhumtermoencontradoteste')
        self.assertIn('Nenhum resultado',self.page.locator('.search-empty').inner_text())
        self.assertEqual(self.page.evaluate('sessionPlan()'),plan)
        self.page.locator('#content-search-input').press('Escape')
        self.assertEqual(self.page.locator('[data-practice-lesson]:visible').count(),self.page.evaluate('AL.length+1'))
        self.click('Iniciar estudo')
        self.assertEqual(self.page.evaluate('[1,10].map(a=>qz.ids.filter(id=>questionById(id)[0]===a).length)'),[5,5])

    def test_query_markup_is_safe_and_consulting_keeps_an_incomplete_session(self):
        self.page.evaluate("begin([1,2],'e');view='t';go()")
        state=self.page.evaluate('JSON.stringify([qz,H,cfg,Q,BP,AL,MAT])')
        self.page.locator('#content-search-input').fill('<img src=x onerror="window.searchInjected=true">')
        self.page.evaluate('go()')
        self.assertEqual(self.page.locator('.content-search img').count(),0)
        self.assertFalse(self.page.evaluate('Boolean(window.searchInjected)'))
        self.page.locator('.search-clear').click()
        self.assertEqual(self.page.locator('.tr .st:visible').count(),self.page.evaluate('AL.length'))
        self.page.evaluate("view='m';mt.c='tab';go()")
        self.page.locator('#content-search-input').fill('Bacen');self.page.locator('[data-search-result]').first.click()
        self.page.locator('#theme-toggle').click()
        self.assertEqual(self.page.evaluate('JSON.stringify([qz,H,cfg,Q,BP,AL,MAT])'),state)
        self.page.locator('.nav').get_by_role('button',name='Praticar',exact=True).click()
        self.assertEqual(self.page.locator('#content-search-input').count(),0)
        self.assertEqual(self.page.locator('.quiz-header').count(),1)

    def test_future_lessons_enter_the_index_and_layout_fits_both_themes(self):
        for width in [390,1024,1280,1440,1920]:
            self.page.set_viewport_size(dict(width=width,height=900))
            for theme in ['light','dark']:
                self.page.evaluate('theme=>document.documentElement.dataset.theme=theme',theme)
                for screen,kind in [('d',None),('t',None),('q',None),('m','tab')]:
                    self.search('inflação',screen,kind)
                    self.assertEqual(self.page.locator('#content-search-input').count(),1)
                    self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'),(width,theme,screen))
                    self.assertTrue(self.page.locator('.content-search').evaluate('n=>n.scrollWidth<=n.clientWidth+1'))
        next_lesson=self.page.evaluate('AL.length+1')
        self.page.evaluate("n=>{AL.push({...AL[0],t:`Aula ${n}: Reservafutura`,o:'Conceitofuturo exclusivo'});view='t';go()}",next_lesson)
        self.page.locator('#content-search-input').fill('conceitofuturo')
        self.assertEqual(self.page.evaluate('filteredSearchResults().map(d=>d.lesson)'),[next_lesson])

if __name__=='__main__':unittest.main(verbosity=2)
