"""Guia importado do quadro do usuário, separado de questões e sorteios."""
from pathlib import Path
import unittest
import smoke as harness


class ExamGuide(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click
    answer=harness.PainelCPA.answer

    def open(self):self.click('Guia da prova')
    def lessons(self):return self.page.locator('[data-exam-lesson]').evaluate_all('es=>es.map(e=>Number(e.dataset.examLesson))')
    def filter(self,key,value):self.page.locator(f'[data-exam-filter="{key}:{value}"]').click()

    def test_import_preserves_every_row_and_marks_future_lesson_without_creating_it(self):
        self.open()
        labels=self.page.locator('.nav button>span:first-of-type').all_text_contents()
        self.assertEqual(labels[-2:],['Estatísticas','Guia da prova'])
        self.assertEqual(self.lessons(),[13,11,1,3,4,8,9,2,5,6,7,10,12])
        expected=[
            (13,'Bloco F','Métricas Matemáticas, Gestão de Riscos e Clientes','Máxima','40% da prova / 20 questões'),
            (11,'Bloco D','Macroeconomia, Atividade e Política Fiscal','Alta','20% da prova / 10 questões'),
            (1,None,'Sistema Financeiro Nacional','Alta','Base conceitual obrigatória'),
            (3,None,'Banco Central do Brasil','Média-alta','Autarquia mais cobrada'),
            (4,None,'Comissão de Valores Mobiliários','Média-alta','Mercado de Capitais'),
            (8,'Bloco A','Inovação, Pagamentos e Crédito Digital','Média','~10% a 15% da prova'),
            (9,'Bloco B','Autorregulação, Proteção e Livre Mercado','Média','~10% a 15% da prova'),
            (2,None,'Conselho Monetário Nacional','Média','Fixação de metas'),
            (5,None,'Seguros e Previdência (SUSEP/PREVIC)','Média','Estrutura técnica'),
            (6,None,'Operadores Monetários','Média','Bancos Múltiplos e Comerciais'),
            (7,None,'Operadores Não Monetários','Média','Corretoras e Financeiras'),
            (10,'Bloco C','Infraestrutura, Negociação e Risco Sistêmico','Baixa','~5% da prova'),
            (12,'Bloco E','Mercado de Câmbio e Relações Internacionais','Baixa','~5% da prova')]
        for rank,(lesson,block,topic,importance,detail) in enumerate(expected,1):
            row=self.page.locator(f'[data-exam-lesson="{lesson}"]')
            self.assertEqual(row.locator('.exam-rank').inner_text(),f'{rank}º')
            self.assertEqual(row.locator('th').inner_text(),topic)
            self.assertEqual(row.locator('.exam-importance').inner_text(),importance)
            self.assertEqual(row.locator('.exam-detail').inner_text(),detail)
            self.assertEqual(row.locator('.exam-block,.exam-no-block').count(),0)
        self.assertEqual(self.page.locator('.exam-planned').count(),0)
        self.assertNotIn('não cadastrada',self.page.locator('[data-exam-lesson="13"]').inner_text())
        self.assertEqual(self.page.evaluate('[AL.length,Q.length,BP.length]'),self.page.evaluate('[13,1200+50*AL[12].b.length,600+25*AL[12].b.length]'))
        self.page.locator('.exam-reference-notes summary').click()
        self.assertIn('não representa uma conferência independente de edital',self.page.locator('.exam-reference-notes').inner_text())

    def test_filters_intersect_and_search_handles_accents_aliases_and_empty_results(self):
        self.open();self.filter('importance','media');self.assertEqual(self.lessons(),[8,9,2,5,6,7])
        self.assertEqual(self.page.get_by_role('group',name='Bloco',exact=True).count(),0)
        self.assertEqual(self.page.get_by_role('group',name='Cadastro',exact=True).count(),0)
        self.assertNotIn('Bloco',self.page.locator('.exam-guide-page').inner_text())
        self.page.get_by_role('searchbox',name='Buscar aula, tema ou conteúdo').fill('crédito')
        self.assertEqual(self.lessons(),[8])
        self.page.get_by_role('searchbox',name='Buscar aula, tema ou conteúdo').fill('inexistente')
        self.click('Limpar filtros e busca');self.assertEqual(len(self.lessons()),13)
        search=self.page.get_by_role('searchbox',name='Buscar aula, tema ou conteúdo')
        for query,wanted in [('BACEN',[3]),('CVM',[4]),('CAMBIO',[12]),('SUSEP',[5]),('aula 03',[3]),('riscos',[13])]:
            search.fill(query);self.assertEqual(self.lessons(),wanted,query)
            self.assertTrue(search.evaluate('e=>e===document.activeElement'))
        search.fill('<img src=x onerror=alert(1)>');self.assertEqual(self.lessons(),[])
        self.assertEqual(self.page.locator('.exam-guide-page img').count(),0)
        search.press('Escape');self.assertEqual(len(self.lessons()),13)
        self.page.evaluate("window.savedFinalLesson=AL.pop();refreshExamGuide()")
        self.assertEqual(self.page.locator('.exam-planned').count(),1)
        self.page.evaluate("AL.push(window.savedFinalLesson);refreshExamGuide()")
        self.assertEqual(len(self.lessons()),13);self.assertEqual(self.page.locator('.exam-planned').count(),0)

    def test_sort_keeps_original_priority_and_choices_survive_theme_and_navigation(self):
        self.open();self.filter('importance','baixa');self.filter('sort','lesson')
        self.assertEqual(self.lessons(),[10,12]);self.assertEqual(self.page.locator('.exam-rank').all_text_contents(),['12º','13º'])
        self.page.locator('#theme-toggle').click();self.assertEqual(self.lessons(),[10,12])
        self.click('Painel');self.open();self.assertEqual(self.lessons(),[10,12])
        self.click('Limpar filtros');self.filter('sort','lesson');self.assertEqual(self.lessons(),list(range(1,14)))
        self.assertEqual(self.page.locator('[data-exam-filter^="sort:"]').all_text_contents(),['Prioridade','Aula'])
        self.filter('sort','rank');self.assertEqual(self.lessons()[0],13)

    def test_controls_and_navigation_preserve_active_practice_history_banks_and_selection(self):
        self.page.evaluate("H=[[1,true,1000,0]];begin([1,2,3],'e')");self.answer();self.open()
        stable='JSON.stringify([Q,BP,AL,MAT,H,cfg,qz,fl,fm,dailyBook])'
        before=self.page.evaluate(stable)
        self.filter('importance','maxima');self.filter('sort','lesson')
        self.page.get_by_role('searchbox',name='Buscar aula, tema ou conteúdo').fill('métricas')
        self.click('Limpar filtros');self.page.locator('#theme-toggle').click()
        self.click('Estatísticas');self.open()
        self.assertEqual(self.page.evaluate(stable),before)
        self.click('Praticar');self.assertEqual(self.page.evaluate(stable),before)
        self.assertEqual(self.page.locator('.fb-option').count(),4)

    def test_daily_checkpoint_is_not_resampled_or_completed_by_consulting_reference(self):
        self.page.evaluate('hoje()');self.answer();self.open()
        stable="JSON.stringify([H,qz,cfg,{...dailyBook,active:((({elapsed,updatedAt,...rest})=>rest)(dailyBook.active))}])"
        before=self.page.evaluate(stable)
        self.filter('importance','maxima');self.click('Painel');self.open()
        self.assertEqual(self.page.evaluate(stable),before)
        self.assertEqual(self.page.evaluate('qz.rev.length'),1)

    def test_keyboard_themes_and_responsive_readability(self):
        self.open();self.page.locator('[data-exam-filter="importance:alta"]').focus();self.page.keyboard.press('Enter')
        self.assertEqual(self.lessons(),[11,1]);self.click('Limpar filtros')
        self.page.locator('.exam-reference-notes summary').focus();self.page.keyboard.press('Enter')
        self.assertTrue(self.page.locator('.exam-reference-notes').evaluate('e=>e.open'))
        output=Path('/tmp/cpa-exam-guide');output.mkdir(exist_ok=True)
        for width in [390,768,1024,1440,1920]:
            self.page.set_viewport_size(dict(width=width,height=1000))
            for theme in ['dark','light']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme))
                self.assertTrue(self.page.locator('.exam-table td,.exam-table th,.exam-filter-group').evaluate_all('es=>es.every(e=>e.scrollWidth<=e.clientWidth+1)'),(width,theme))
                self.assertEqual(len(self.lessons()),13)
                if width in [390,1440]:self.page.screenshot(path=str(output/f'{theme}-{width}.png'),full_page=True)

if __name__=='__main__':unittest.main(verbosity=2)
