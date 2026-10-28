"""Estudo ativo parte do conceito exibido, com todos os IDs e sem distratores."""
import json
import re
from pathlib import Path
import unittest
import smoke as harness


class ActiveStudy(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click
    answer=harness.PainelCPA.answer

    def material(self,lesson,kind):self.page.evaluate("([n,t])=>{view='m';mt={a:n,c:t};fi=0;ff=0;go()}",[lesson,kind])
    def matching(self,**source):return self.page.evaluate('s=>ActiveStudy.matching(s)',source)
    def source_entry(self,box):
        return self.page.evaluate('k=>ActiveStudy.audit().find(e=>e.key===k)',box.get_attribute('data-active-study-key') or box.get_attribute('data-active-study'))
    def branch(self,title):
        return self.page.locator('.mind-branch').filter(has=self.page.get_by_role('heading',name=re.compile('^'+re.escape(title)+'$',re.I))).locator(':scope>.active-study-action')

    def test_composition_does_not_pick_competences_or_other_collegiates(self):
        ids=self.matching(lesson=3,label='Composição da Diretoria do BACEN',text='1 presidente e 8 diretores')
        self.assertTrue({53,283,298,299,340}.issubset(ids))
        self.assertTrue({58,69,108,284,304,343,415,419,421,484}.isdisjoint(ids),ids)
        self.assertEqual(len(ids),len(set(ids)))
        # Citar BC/CVM entre os representantes do CNSP não torna o quadro uma
        # comparação sobre o tamanho das diretorias dessas duas autarquias.
        ids=self.matching(lesson=5,label='Composição do CNSP e do CNPC',text='Fazenda, Susep, BACEN e CVM',whole=True)
        self.assertTrue({412,419,484,485}.issubset(ids))
        self.assertTrue({53,283,343,415,421,425}.isdisjoint(ids),ids)

    def test_roles_authorization_and_mandates_are_distinct_and_cross_lessons(self):
        source=dict(lesson=3,parents=['Banco Central do Brasil'])
        authorizations=self.matching(**source,label='Autorizações',text='Autorizar funcionamento, fusão e transferência de controle acionário')
        self.assertTrue({63,109,310,311,326}.issubset(authorizations),authorizations)
        self.assertTrue({53,54,283,284,304,290}.isdisjoint(authorizations),authorizations)
        mandate=self.matching(**source,label='Mandato',text='Quatro anos, com uma recondução')
        self.assertTrue({54,284,329}.issubset(mandate))
        self.assertTrue({304,343,415}.isdisjoint(mandate))
        # A comparação BC/CVM da aula 4 também pratica o mandato do BC.
        self.assertIn(143,mandate)
        self.assertIn(4,self.page.evaluate('ids=>[...new Set(ids.map(id=>questionById(id)[0]))]',mandate))
        requirements=self.matching(**source,label='Requisitos para ser diretor',text='Brasileiros idôneos, reputação ilibada e notória capacidade')
        self.assertIn(110,requirements);self.assertTrue({56,285,304}.isdisjoint(requirements))

    def test_specific_subtopics_do_not_degenerate_into_name_matching(self):
        change=self.matching(lesson=2,label='Antecedência da mudança da meta de inflação',text='36 meses')
        self.assertTrue({18,103,261}.issubset(change));self.assertNotIn(19,change);self.assertNotIn(232,change)
        ptax=self.matching(lesson=12,label='PTAX',text='Referência e metodologia de apuração')
        self.assertTrue(ptax)
        self.assertTrue(all('ptax' in self.page.evaluate('id=>JSON.stringify(questionById(id))',i).lower() for i in ptax))
        self.assertNotIn(1109,ptax)
        comef=self.matching(lesson=10,label='Composição do Comef',text='Presidente do BC e seus oito diretores')
        self.assertEqual(comef,[962]);self.assertTrue({53,283,343}.isdisjoint(comef))
        tr=self.matching(lesson=8,label='Registradora (TR)',text='Registra as operações',parents=['Funções de IMF'])
        self.assertTrue(tr);self.assertTrue(all(self.page.evaluate('id=>questionById(id)[0]',i)!=11 for i in tr))
        self.assertEqual(self.matching(lesson=12,label='Conceito ausente zzz',text=''),[])

    def test_count_matches_entire_mixed_session_without_cfg_limits_or_history_filter(self):
        self.page.evaluate("H=[[53,true,1000,0],[283,false,1001,0]];cfg.md='b';cfg.c=5;cfg.m='new';cfg.as=[12];cfg.n=0")
        self.material(3,'mapa');box=self.branch('DIRETORIA');entry=self.source_entry(box)
        before=self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT,selectedLessonBlocks])')
        self.assertGreater(len(entry['ids']),5)
        self.assertEqual(box.locator('.active-study-count').inner_text(),f"{len(entry['ids'])} disponíveis")
        box.locator('.active-study-button').click()
        actual=self.page.evaluate('qz.ids');self.assertEqual(set(actual),set(entry['ids']));self.assertEqual(len(actual),len(entry['ids']))
        self.assertEqual(self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT,selectedLessonBlocks])'),before)
        self.assertEqual(self.page.evaluate('qz.md'),'e');self.assertTrue(all(i<100001 for i in actual))
        levels=self.page.evaluate('[...new Set(qz.ids.map(id=>questionById(id)[2]))]');self.assertIn(3,levels);self.assertTrue(any(n<3 for n in levels))
        self.assertEqual(self.page.locator('.question-number').count() or self.page.locator('[data-question-index]').count(),len(actual))

    def test_hardcore_feedback_history_origin_and_return_to_source(self):
        self.material(3,'mapa');box=self.branch('DIRETORIA');entry=self.source_entry(box);box.locator('.active-study-button').click()
        self.page.evaluate('jumpQuestion(qz.ids.findIndex(id=>questionById(id)[2]===3))')
        self.assertEqual(self.page.locator('.question-stage>.quick-context').count(),0)
        self.assertIn('Hardcore',self.page.locator('.question-stage>p').inner_text())
        self.assertEqual(self.page.get_by_role('button',name='Dica',exact=True).count(),0)
        self.answer();self.assertEqual(self.page.locator('.fb-option').count(),4)
        self.assertEqual(self.page.evaluate('H.at(-1)[3]'),2)
        self.page.evaluate('jumpQuestion(qz.ids.findIndex(id=>questionById(id)[2]<3))')
        self.assertEqual(self.page.get_by_role('button',name='Dica',exact=True).count(),1)
        self.answer();self.assertEqual(self.page.evaluate('H.at(-1)[3]'),0)
        before=self.page.evaluate('JSON.stringify([H,qz])')
        self.click('Voltar ao conteúdo');self.assertEqual(self.page.evaluate('[view,mt.a,mt.c]'),['m',3,'mapa'])
        self.assertEqual(self.page.evaluate('JSON.stringify([H,qz])'),before)
        box=self.page.locator(f'[data-active-study-key="{entry["key"]}"]');box.get_by_role('button',name='Fazer questões',exact=False).click()
        self.assertIn('Conclua ou encerre',box.locator('[role="status"]').inner_text())
        box.get_by_role('button',name='Retomar sessão',exact=True).click();self.assertEqual(self.page.evaluate('JSON.stringify([H,qz])'),before)

    def test_pending_daily_checkpoint_and_normal_session_are_never_overwritten(self):
        for daily in [False,True]:
            self.page.evaluate('qz=null')
            self.page.evaluate("hoje()" if daily else "begin([1,2],'e')")
            self.answer();self.material(3,'tab')
            stable="JSON.stringify([H,qz,cfg,dailyBook.active&&((({elapsed,updatedAt,...rest})=>rest)(dailyBook.active)),dailyBook.days])"
            before=self.page.evaluate(stable)
            self.page.locator('.material-table>.active-study-action button:not([disabled])').first.click()
            self.assertEqual(self.page.evaluate(stable),before)
            self.assertEqual(self.page.evaluate('view'),'m');self.assertIn('Conclua ou encerre',self.page.locator('.active-study-pending').inner_text())
            self.click('Retomar sessão');self.assertEqual(self.page.evaluate('view'),'q');self.assertEqual(self.page.evaluate(stable),before)

    def test_all_material_types_and_trail_have_actions_and_valid_exact_counts(self):
        for lesson in range(1,self.page.evaluate("AL.length")+1):
            self.page.evaluate("n=>{view='t';tr=n;go()}",lesson)
            self.assertEqual(self.page.locator('.acb>.active-study-action').count(),self.page.locator('.lesson-section .pt').count())
            for kind in ['mapa','diag','tab','tl','fc','geral']:
                if kind=='geral' and not self.page.evaluate('n=>hasLessonOverview(n)',lesson):continue
                self.material(lesson,kind)
                selectors={'mapa':'.mind-branch','diag':'.material-panel','tab':'.material-table','tl':'.material-time-panel','fc':'.flashcard-stage','geral':'.operator-overview'}
                for node in self.page.locator(selectors[kind]).all():self.assertEqual(node.locator(':scope>.active-study-action').count(),1,(lesson,kind))
                self.assertTrue(self.page.locator('.active-study-action').evaluate_all("es=>es.every(e=>Number(e.querySelector('.active-study-count').textContent.match(/\\d+/)[0])===Number(e.querySelector('button').getAttribute('aria-label').match(/: (\\d+) dispon/)[1]))"))
        audit=self.page.evaluate('ActiveStudy.audit()');questions=self.page.evaluate('ActiveStudy.bank()')
        self.assertEqual(len(questions),self.page.evaluate("Q.length"));self.assertTrue(all(q['owners'] for q in questions))
        self.assertTrue(all(len(e['ids'])==len(set(e['ids'])) and all(1<=i<=len(questions) for i in e['ids']) for e in audit))
        self.assertTrue(any(not e['ids'] for e in audit))
        self.assertEqual(self.page.locator('.active-study-button:disabled').count(),sum(not self.source_entry(box)['ids'] for box in self.page.locator('.active-study-action').all()))
        Path('/tmp/cpa-active-study/final-links.json').write_text(json.dumps(audit,ensure_ascii=False))

    def test_block_and_flashcard_context_survive_round_trip_and_count_is_live(self):
        self.page.evaluate("selectedLessonBlocks[7]=2;view='m';mt={a:7,c:'fc'};fi=1;ff=1;go()")
        box=self.page.locator('.flashcard-stage>.active-study-action')
        if box.locator('.active-study-button').is_disabled():
            self.page.evaluate("fi=0;go()")
            box=self.page.locator('.flashcard-stage>.active-study-action')
        state=self.page.evaluate('[mt,selectedLessonBlocks[7],fi,ff]');box.locator('.active-study-button').click()
        self.click('Voltar ao conteúdo');self.assertEqual(self.page.evaluate('[mt,selectedLessonBlocks[7],fi,ff]'),state)

    def test_overview_cell_locks_to_its_operator_and_not_incidental_supervisor(self):
        self.material(7,'geral')
        row=self.page.locator('.operator-overview-table [data-operator="investimento"]')
        # Identificação por nome preserva o teste se o ID editorial mudar.
        if not row.count():row=self.page.locator('.operator-overview-table tr').filter(has=self.page.locator('.overview-operator-name',has_text='Banco de investimento'))
        box=row.locator('[data-feature="oversight"]')
        self.assertEqual(box.locator('.active-study-action').count(),0)
        entry=self.source_entry(box)
        self.assertEqual(entry['profile']['owners'],['investment'])
        self.assertTrue({53,58,69,283,304}.isdisjoint(entry['ids']))
        self.assertLessEqual(len(entry['ids']),10)

    def test_result_retry_keeps_context_and_only_repeats_actual_errors(self):
        self.material(3,'mapa');box=self.branch('DIRETORIA');box.locator('.active-study-button').click()
        # Um recorte pequeno da própria sessão exercita término e revisão.
        self.page.evaluate("qz.ids=qz.ids.slice(0,3);go()")
        self.answer(False);self.click('Próxima');self.answer();self.click('Próxima');self.answer();self.click('Ver resultado')
        wrong=self.page.evaluate('qz.rev.filter(r=>!r[1]).map(r=>r[0])');self.assertEqual(len(wrong),1)
        self.assertEqual(self.page.locator('.session-result').count(),1)
        self.click('Refazer erros desta sessão');self.assertEqual(self.page.evaluate('qz.ids'),wrong);self.assertTrue(self.page.evaluate('!!qz.contextStudy'))
        self.click('Voltar ao conteúdo');self.assertEqual(self.page.evaluate('view'),'m')

    def test_themes_keyboard_and_responsive_screens_preserve_data(self):
        self.material(3,'mapa');box=self.branch('DIRETORIA');box.locator('.active-study-button').focus();self.page.keyboard.press('Enter')
        self.assertTrue(self.page.evaluate('!!qz.contextStudy'));self.click('Voltar ao conteúdo')
        stable=self.page.evaluate('JSON.stringify([Q,BP,AL,MAT,H,cfg,qz])')
        for width in [390,768,1024,1440,1920]:
            self.page.set_viewport_size(dict(width=width,height=1000))
            for theme in ['light','dark']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
                for lesson,kind in [(3,'mapa'),(3,'tab'),(3,'tl'),(6,'diag'),(7,'geral')]:
                    self.material(lesson,kind)
                    self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme,kind))
                    if width==1440 and theme=='dark':self.page.screenshot(path=f'/tmp/cpa-active-study/{lesson}-{kind}.png',full_page=True)
        self.assertEqual(self.page.evaluate('JSON.stringify([Q,BP,AL,MAT,H,cfg,qz])'),stable)

if __name__=='__main__':unittest.main(verbosity=2)
