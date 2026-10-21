"""Relações locais: resposta pertinente, direção temporal e limites das fontes."""
import unittest
from playwright.sync_api import expect
import test_consulta as harness


class ConsultaContexto(unittest.TestCase):
    setUpClass = classmethod(harness.Consulta.setUpClass.__func__)
    tearDownClass = classmethod(harness.Consulta.tearDownClass.__func__)
    setUp = harness.Consulta.setUp
    tearDown = harness.Consulta.tearDown
    click = harness.Consulta.click
    ask = harness.Consulta.ask
    result = harness.Consulta.result

    @staticmethod
    def primary(result):
        return ' '.join(line for item in result['items'][:3] for line in item['record']['lines'])

    def test_predecessor_without_naming_it_and_temporal_direction(self):
        for query in ['Qual era a taxa antes da TLP?',
                      'O que era usado antes da Taxa de Longo Prazo?',
                      'Qual taxa antecedeu a TLP?',
                      'Qual era a referência antiga que a TLP substituiu?']:
            with self.subTest(query=query):
                result = self.result(query)
                self.assertEqual(result['status'], 'found')
                self.assertEqual(result['items'][0]['record']['label'], 'Antes de 2018')
                text = self.primary(result)
                self.assertIn('TJLP', text)
                self.assertIn('Desde janeiro de 2018', text)
                self.assertIn('contratos antigos não migram', text)
                self.assertIsNone(result['originalTable'])
        result = self.result('Qual taxa entrou no lugar da TJLP?')
        self.assertEqual(result['status'], 'found')
        self.assertEqual(result['items'][0]['record']['label'], 'Desde janeiro de 2018')
        self.assertIn('TLP nas novas operações cabíveis', self.primary(result))

    def test_change_is_not_a_rename_or_universal_contract_migration(self):
        result = self.result('A TLP é só um novo nome para TJLP?')
        self.assertEqual(result['status'], 'found')
        self.assertIn('não é simples mudança de nome nem migração automática', self.primary(result))
        result = self.result('O que substituiu o antigo teto de gastos?')
        self.assertEqual(result['status'], 'found')
        text = self.primary(result)
        self.assertIn('LC 200/2023', text)
        self.assertIn('EC 95/2016', text)
        self.assertIn('não trate o antigo limite', text)

    def test_calculation_cause_and_sequence_prioritize_the_requested_relation(self):
        result = self.result('Como é calculada a TLP?')
        self.assertEqual(result['status'], 'found')
        first = ' '.join(result['items'][0]['record']['lines'])
        self.assertIn('parcela real prefixada', first)
        self.assertIn('parcela variável pelo IPCA', first)
        result = self.result('Por que juros maiores afetam o consumo?')
        self.assertEqual(result['status'], 'found')
        self.assertIn('podem restringir crédito, consumo e investimento', self.primary(result))
        result = self.result('Por que reduzir o compulsório não obriga os bancos a emprestar?')
        self.assertEqual(result['status'], 'found')
        first = ' '.join(result['items'][0]['record']['lines'])
        self.assertIn('capital, risco e demanda', first)
        self.assertIn('condicionando o crédito', first)
        result = self.result('Como funciona a intermediação?')
        self.assertEqual(result['status'], 'found')
        self.assertIn('capta do poupador e empresta ao tomador', self.primary(result))

    def test_incidental_mentions_negated_substitution_and_unknown_context_are_not_evidence(self):
        for query in ['Qual era a taxa antes do IPCA?',
                      'Qual era a taxa antes da TLP em Marte?',
                      'Qual era a taxa antes do FGC?',
                      'Qual era antes do Bacen?',
                      'Por que o Bacen tem unicórnios?',
                      'Por que a TLP substituiu a TJLP?']:
            with self.subTest(query=query):
                result = self.result(query)
                self.assertNotEqual(result['status'], 'found')
        # IGP-M não substitui a meta: a negativa não comprova uma sucessão histórica.
        result = self.result('Qual era a taxa antes do IPCA?')
        self.assertFalse(any(item.get('relation') for item in result['items']))

    def test_followups_keep_subject_and_highlight_the_source_derived_counterpart(self):
        self.ask('TLP')
        text = self.ask('E o que era usado antes?')
        self.assertIn('TJLP', text)
        self.assertIn('Antes de 2018', text)
        marks = self.page.locator('.consult-current mark').all_text_contents()
        self.assertIn('TJLP', marks)
        self.assertFalse(self.page.locator('.consult-history').evaluate('n=>n.open'))
        self.ask('Como é calculada?')
        self.assertIn('parcela real prefixada', self.page.locator('.consult-current').inner_text())
        self.ask('composição do Bacen')
        self.assertIn('8 diretores', self.page.locator('.consult-current').inner_text())
        self.page.locator('.consult-history>summary').click()
        expect(self.page.locator('.consult-previous')).to_have_count(3)

    def test_sources_remain_literal_and_group_context_never_crosses_timelines(self):
        result = self.result('Qual era a taxa antes da TLP?')
        self.assertEqual(result['items'][0]['record']['lesson'], 11)
        source = self.page.evaluate('MAT[11].tl[1][1]')
        for item in result['items'][:2]:
            self.assertIn(item['record']['lines'], source)
            self.assertEqual(item['record']['group']['id'], 'timeline-11-1')
        self.assertNotIn('EC 95', self.primary(result))
        self.assertNotIn('LC 200', self.primary(result))
        # Nenhum fato, enunciado ou questão é reescrito pelo mecanismo.
        before = self.page.evaluate('JSON.stringify([AL,MAT,Q,BP,H,cfg])')
        self.ask('Qual era a taxa antes da TLP?')
        self.assertEqual(before, self.page.evaluate('JSON.stringify([AL,MAT,Q,BP,H,cfg])'))

    def test_new_source_relationship_is_discovered_without_a_hardcoded_answer(self):
        self.page.evaluate('''()=>{
            AL.push({t:'Referências temporais locais',r:[],d:[],p:[],n:[]});
            MAT[AL.length]={tl:[['Mudança de referência local',[
                ['Antes de 2020','XYZ era a referência anterior, conforme os contratos'],
                ['Desde 2020','Taxa Selic nas novas operações deste exemplo de teste']
            ]]]};
        }''')
        result = self.result('Qual era a referência antes da Taxa Selic?')
        self.assertEqual(result['status'], 'found')
        self.assertEqual(result['items'][0]['record']['lesson'], 12)
        self.assertIn('XYZ era a referência anterior', self.primary(result))


if __name__ == '__main__':
    unittest.main(verbosity=2)
