"""Consulta: esclarecimento, recortes, filtros e características comparáveis."""
import unittest
from playwright.sync_api import expect
import test_consulta as harness


class ConsultaRefinamentos(unittest.TestCase):
    setUpClass = classmethod(harness.Consulta.setUpClass.__func__)
    tearDownClass = classmethod(harness.Consulta.tearDownClass.__func__)
    setUp = harness.Consulta.setUp
    tearDown = harness.Consulta.tearDown
    click = harness.Consulta.click
    ask = harness.Consulta.ask
    result = harness.Consulta.result

    def filtered(self, query, options):
        return self.page.evaluate('([q,o])=>Consulta.answer(q,[],o)', [query, options])

    def test_ambiguous_acronym_requires_a_choice_and_keeps_meanings_separate(self):
        self.ask('TR')
        choices = self.page.locator('.consult-meaning-options button')
        expect(choices).to_have_count(2)
        self.assertEqual(self.page.locator('.consult-current .consult-extract').count(), 0)
        self.assertTrue(choices.first.evaluate('n=>n===document.activeElement'))
        self.page.get_by_role('button', name='Taxa Referencial', exact=True).click()
        text = self.page.locator('.consult-current').inner_text()
        self.assertIn('TBF', text)
        self.assertIn('Aula 11', text)
        self.assertNotIn('Trade Repository', text)
        self.assertEqual(self.page.locator('.consult-history').count(), 0)
        self.click('Limpar')
        self.ask('TR')
        self.page.get_by_role('button', name='Trade Repository — entidade registradora', exact=True).press('Enter')
        text = self.page.locator('.consult-current').inner_text()
        self.assertIn('registr', text.lower())
        self.assertNotIn('Taxa Referencial', text)
        self.assertIn('Aula 8', text)

    def test_full_names_context_and_scopes_resolve_without_unnecessary_prompts(self):
        for query, name in [('TR (Taxa Referencial)', 'Taxa Referencial'),
                            ('TR (Trade Repository)', 'Trade Repository — entidade registradora'),
                            ('TR na poupança', 'Taxa Referencial')]:
            with self.subTest(query=query):
                result = self.result(query)
                self.assertNotEqual(result['status'], 'clarify')
                self.assertEqual(result['request']['subjects'][0]['name'], name)
        self.assertEqual(self.result('trs')['status'], 'clarify')
        result = self.filtered('TR', {'lessons': [11]})
        self.assertEqual(result['request']['subjects'][0]['name'], 'Taxa Referencial')
        self.assertNotEqual(result['status'], 'clarify')
        result = self.filtered('TR', {'lessons': [8]})
        self.assertEqual(result['request']['subjects'][0]['name'], 'Trade Repository — entidade registradora')

    def test_scope_intersects_lessons_types_comparisons_and_original_tables(self):
        result = self.filtered('Bacen', {'lessons': [1, 7], 'types': ['Resumo', 'Tabela']})
        self.assertTrue(result['items'])
        self.assertTrue(all(i['record']['lesson'] in [1, 7] and i['record']['type'] in ['Resumo', 'Tabela'] for i in result['items']))
        result = self.filtered('comparação entre CMN e Bacen', {'lessons': [2, 3], 'types': ['Resumo']})
        self.assertTrue(result['comparisons'])
        self.assertIsNone(result['originalTable'])
        records = [i['record'] for row in result['comparisons'] for cell in row['cells'] for i in cell]
        self.assertTrue(all(r['lesson'] in [2, 3] and r['type'] == 'Resumo' for r in records))
        result = self.filtered('TLP', {'lessons': [1], 'types': ['Resumo']})
        self.assertEqual(result['status'], 'missing')
        self.assertEqual(result['items'], [])
        result = self.filtered('diferença entre SCD e SEP', {'lessons': [1]})
        self.assertIsNone(result['originalTable'])
        self.assertFalse(result['comparisons'])

    def test_refinement_is_closed_keyboard_accessible_and_refreshes_without_new_history(self):
        self.ask('Bacen')
        details = self.page.locator('.consult-refine')
        self.assertFalse(details.evaluate('n=>n.open'))
        details.locator('summary').focus()
        self.page.keyboard.press('Enter')
        self.assertTrue(details.evaluate('n=>n.open'))
        for number in [1, 7]:
            self.page.locator(f'[data-filter="lesson-{number}"]').click()
        for index in [0, 5]:
            self.page.locator(f'[data-filter="type-{index}"]').click()
        self.assertEqual(self.page.locator('#consult-question').input_value(), 'Bacen')
        self.assertEqual(self.page.locator('.consult-history').count(), 0)
        self.assertIn('Aulas 1, 7', self.page.locator('.consult-scope').inner_text())
        self.assertTrue(self.page.locator('[data-filter="type-5"]').evaluate('n=>n===document.activeElement'))
        self.assertEqual(self.page.locator('[data-filter="type-5"]').get_attribute('aria-pressed'), 'true')
        before = self.page.locator('.consult-current').inner_text()
        self.page.locator('#consult-question').fill('TLP')
        self.page.locator('[data-filter="lesson-all"]').click()
        self.assertEqual(self.page.locator('.consult-current').inner_text(), before)
        self.click('Consultar')
        self.assertIn('Todas as aulas', self.page.locator('.consult-scope').inner_text())
        self.assertEqual(self.page.locator('.consult-history').count(), 1)

    def test_dynamic_comparison_features_can_be_hidden_selected_and_restored(self):
        self.ask('comparação entre CVM e Susep')
        details = self.page.locator('.consult-characteristics')
        details.locator('summary').click()
        selected = details.locator('button[aria-pressed="true"][data-feature]:not([data-feature="all"])').evaluate_all('nodes=>nodes.map(n=>n.dataset.feature)')
        for feature in selected:
            self.page.locator(f'[data-feature="{feature}"]').click()
        self.assertEqual(self.page.locator('.consult-current table').count(), 0)
        self.assertIn('Selecione uma característica', self.page.locator('.consult-current').inner_text())
        self.page.locator('[data-feature="nature"]').press('Enter')
        rows = self.page.locator('.consult-current tbody tr')
        expect(rows).to_have_count(1)
        self.assertIn('Natureza e vinculação', rows.inner_text())
        self.assertTrue(self.page.locator('[data-feature="nature"]').evaluate('n=>n===document.activeElement'))
        self.page.locator('[data-feature="all"]').click()
        self.assertGreater(self.page.locator('.consult-current tbody tr').count(), 1)
        self.assertEqual(self.page.locator('.consult-history').count(), 0)
        # A composição de um conselho não comprova a duração de um mandato.
        row = self.page.locator('tbody tr').filter(has=self.page.get_by_role('rowheader', name='Mandato', exact=True))
        self.assertIn('Não encontrei essa característica', row.locator('td').last.inner_text())
        self.assertNotIn('Conselho Diretor de 5 membros', row.locator('td').last.inner_text())

    def test_existing_table_features_preserve_projection_and_restore_original_rows(self):
        self.ask('diferenças entre SCD e SEP')
        original = self.page.evaluate("MAT[8].tb.find(t=>t[0]==='SCD e SEP')")
        details = self.page.locator('.consult-characteristics')
        details.locator('summary').click()
        for i in range(1, len(original[2])):
            self.page.locator(f'[data-feature="row-{i}"]').click()
        expect(self.page.locator('.consult-current tbody tr')).to_have_count(1)
        self.assertEqual(self.page.locator('.consult-current tbody tr>*').all_text_contents(), original[2][0])
        self.assertEqual(self.page.locator('.consult-current thead th').all_text_contents(), original[1])
        self.page.locator('[data-feature="all"]').click()
        self.assertEqual(self.page.locator('.consult-current tbody tr').count(), len(original[2]))

    def test_filter_change_rebuilds_features_and_history_preserves_previous_selection(self):
        self.ask('comparação entre CVM e Susep')
        self.page.locator('.consult-characteristics>summary').click()
        selected = self.page.locator('.consult-characteristics button[aria-pressed="true"]:not([data-feature="all"])').evaluate_all('nodes=>nodes.map(n=>n.dataset.feature)')
        for feature in selected:
            if feature != 'nature': self.page.locator(f'[data-feature="{feature}"]').click()
        self.ask('Bacen')
        self.page.locator('.consult-history>summary').click()
        expect(self.page.locator('.consult-previous')).to_have_count(1)
        self.page.locator('.consult-previous>summary').click()
        expect(self.page.locator('.consult-previous tbody tr')).to_have_count(1)
        self.assertEqual(self.page.locator('.consult-previous [data-feature]').count(), 0)
        self.assertIn('Natureza', self.page.locator('.consult-previous tbody tr').inner_text())
        self.click('Limpar')
        self.ask('diferenças entre SCD e SEP')
        self.page.locator('.consult-characteristics>summary').click()
        self.page.locator('[data-feature="row-0"]').click()
        self.page.locator('.consult-refine>summary').click()
        self.page.locator('[data-filter="type-0"]').click()
        self.assertEqual(self.page.locator('[data-feature^="row-"]').count(), 0)
        self.assertGreater(self.page.locator('.consult-current tbody tr').count(), 0)
        self.assertEqual(self.page.locator('.consult-history').count(), 0)

    def test_pending_scope_resolution_replaces_current_response_without_duplicate_history(self):
        self.click('Consulta')
        self.page.locator('.consult-refine>summary').click()
        self.page.locator('[data-filter="lesson-11"]').click()
        self.ask('TR')
        self.assertEqual(self.page.locator('.consult-clarify').count(), 0)
        self.page.locator('[data-filter="lesson-all"]').click()
        expect(self.page.locator('.consult-clarify')).to_have_count(1)
        self.page.get_by_role('button', name='Taxa Referencial', exact=True).click()
        self.assertEqual(self.page.locator('.consult-history').count(), 0)
        self.assertIn('TBF', self.page.locator('.consult-current').inner_text())

    def test_short_extract_retains_qualifications_and_full_context_verbatim(self):
        paragraph = ('Introdução: a leitura de um material pode exigir distinguir o assunto principal das observações complementares. '
                     'Uma apresentação extensa reúne informações para consulta posterior e ajuda a localizar o conteúdo dentro do caderno. '
                     'O balizador identifica o trecho específico solicitado nesta consulta. '
                     'Essa indicação não altera contratos anteriores nem dispensa as condições expressamente previstas. '
                     'As demais informações complementares continuam preservadas para permitir a leitura integral da fonte utilizada.')
        self.page.evaluate('text=>{AL.push({t:"Caderno de leitura",r:[text],d:[],p:[],n:[]});MAT[AL.length]={}}', paragraph)
        self.ask('balizador')
        card = self.page.locator('.consult-extract').first
        self.assertIn('O balizador identifica', card.locator('.consult-passage').inner_text())
        self.assertIn('não altera contratos anteriores', card.locator('.consult-passage').inner_text())
        self.assertNotIn('demais informações complementares', card.locator('.consult-passage').inner_text())
        self.assertGreater(card.locator('.consult-key-sentence').count(), 0)
        details = card.locator('.consult-context')
        self.assertFalse(details.evaluate('n=>n.open'))
        details.locator('summary').focus()
        self.page.keyboard.press('Enter')
        self.assertEqual(details.locator('li').inner_text(), paragraph)
        self.assertIn(f"Aula {self.page.evaluate('AL.length')}", card.locator('.consult-source').inner_text())

    def test_new_source_acronym_collision_is_detected_from_explicit_definitions(self):
        self.page.evaluate('''()=>{
          AL.push({t:'Caderno de siglas',r:['XYZ — Xilografia Zoológica: estudo fictício para verificar identificação.',
              'XYZ — Xadrez Zonal: outra definição fictícia usada apenas neste teste.'],d:[],p:[],n:[]});MAT[AL.length]={};
        }''')
        # As iniciais precisam corresponder à sigla; uma legenda não vira significado.
        self.assertNotEqual(self.result('XYZ')['status'], 'clarify')
        self.page.evaluate('''()=>{
          AL.push({t:'Outro caderno',r:['ABC — Associação Bancária Central: definição fictícia do teste.',
              'ABC — Agência Brasileira de Crédito: segunda definição fictícia do teste.'],d:[],p:[],n:[]});MAT[AL.length]={};
        }''')
        result = self.result('ABC')
        self.assertEqual(result['status'], 'clarify')
        self.assertEqual({e['name'] for e in result['request']['ambiguities'][0]['candidates']}, {'Associação Bancária Central', 'Agência Brasileira de Crédito'})

    def test_features_filters_and_clarification_preserve_study_state_without_network(self):
        self.page.evaluate("H=[[1,false,1700000000000,0]];begin([1,2],'e');pick(0);view='d';go()")
        before = self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz,fl,fm,mt,selectedLessonBlocks])')
        self.click('Consulta')
        requests=[]
        self.page.on('request', lambda request: requests.append(request.url))
        self.page.route('**/*', lambda route: route.abort())
        self.ask('TR')
        self.page.get_by_role('button', name='Taxa Referencial', exact=True).click()
        self.ask('comparação entre CVM e Susep')
        self.page.locator('.consult-characteristics>summary').click()
        self.page.locator('[data-feature="nature"]').click()
        self.page.locator('.consult-refine>summary').click()
        self.page.locator('[data-filter="lesson-4"]').click()
        self.page.locator('[data-filter="type-0"]').click()
        self.click('Painel');self.click('Consulta')
        self.assertEqual(self.page.locator('[data-filter="lesson-4"]').get_attribute('aria-pressed'), 'true')
        self.click('Limpar')
        self.assertEqual(before, self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz,fl,fm,mt,selectedLessonBlocks])'))
        self.assertEqual(requests, [])
        self.assertEqual(self.page.locator('[data-filter="lesson-all"]').get_attribute('aria-pressed'), 'true')

    def test_opening_history_during_clarification_does_not_reorder_saved_questions(self):
        self.ask('composição do Bacen')
        self.ask('limites do FGC')
        self.ask('TR')
        self.page.locator('.consult-history>summary').click()
        expect(self.page.locator('.consult-previous')).to_have_count(2)
        self.assertEqual(self.page.locator('.consult-previous>summary').all_text_contents(), ['limites do FGC', 'composição do Bacen'])
        self.page.get_by_role('button', name='Taxa Referencial', exact=True).click()
        self.page.locator('.consult-history>summary').click()
        expect(self.page.locator('.consult-previous')).to_have_count(2)
        self.assertEqual(self.page.locator('.consult-previous>summary').all_text_contents(), ['limites do FGC', 'composição do Bacen'])

    def test_refinement_ambiguities_and_comparison_fit_both_themes_and_widths(self):
        self.click('Consulta')
        for width in [390, 1024, 1440]:
            self.page.set_viewport_size(dict(width=width, height=1000))
            for theme in ['light','dark']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t', theme)
                self.click('Limpar')
                self.page.locator('.consult-refine>summary').click()
                for query in ['TR', 'comparação entre CVM e Susep']:
                    self.ask(query)
                    if self.page.locator('.consult-characteristics').count():self.page.locator('.consult-characteristics>summary').click()
                    self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'), (width,theme,query))
                    self.assertTrue(self.page.locator('.consult-page').evaluate('n=>n.scrollWidth<=n.clientWidth+1'))
                    self.assertEqual(self.page.locator('.consult-examples').count(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
