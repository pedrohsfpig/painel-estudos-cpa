"""Rastreabilidade editorial e regressões dos exemplos reais; não certificação normativa."""
from collections import Counter
import copy
import json
from pathlib import Path
import unittest
from validate_bank import load_questions
from question_revision import digest,questions_before_teaching_revision,questions_before_grammar_revision,bate_pronto_before_grammar_revision,questions_before_clue_revision
import smoke as harness

ROOT=Path(__file__).resolve().parents[1]
def bp_bank():
    return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split('const BP=',1)[1])[0]

class TeachingRevision(unittest.TestCase):
    def test_actual_counts_and_historical_chain(self):
        live=load_questions();latest=questions_before_grammar_revision(live);before=questions_before_teaching_revision(live)
        report=json.loads((ROOT/'docs/revisao-justificativas-contexto.json').read_text());counts=report['contagens']
        self.assertEqual(counts['questoes_revisadas'],len(report['questoes']))
        self.assertGreaterEqual(len(latest),len(report['questoes']))
        self.assertEqual(counts['questoes_alteradas'],sum(a!=b for a,b in zip(before,latest)))
        self.assertEqual(counts['enunciados_alterados'],sum(a[3]!=b[3] for a,b in zip(before,latest)))
        self.assertEqual(counts['feedbacks_alterados'],sum(x!=y for a,b in zip(before,latest) for x,y in zip(a[11],b[11])))
        self.assertEqual(counts['questoes_com_feedback_alterado'],sum(a[11]!=b[11] for a,b in zip(before,latest)))
        corrupted=copy.deepcopy(live);corrupted[582][11][1]='Só atende cooperados.'
        with self.assertRaises(AssertionError):questions_before_teaching_revision(corrupted)
        bp=bate_pronto_before_grammar_revision(bp_bank());previous=copy.deepcopy(bp)
        for i,row in enumerate(report['bate_pronto']):
            self.assertEqual(row['id'],100001+i);self.assertEqual(row['hash_depois'],digest(bp[i]))
            for k,change in row['campos'].items():
                self.assertEqual(bp[i][int(k)],change['depois']);previous[i][int(k)]=change['antes']
            self.assertEqual(row['hash_antes'],digest(previous[i]))
        self.assertEqual(counts['bate_pronto_revisados'],len(report['bate_pronto']))
        self.assertGreaterEqual(len(bp),len(report['bate_pronto']))
        self.assertEqual(counts['bate_pronto_alterados'],sum(a!=b for a,b in zip(previous,bp)))
        self.assertEqual(counts['bate_pronto_feedbacks_alterados'],sum(a[j]!=b[j] for a,b in zip(previous,bp) for j in [5,6]))

    def test_editorial_changes_preserve_pools_answers_and_ids(self):
        live=load_questions();latest=questions_before_clue_revision(live);before=questions_before_teaching_revision(live)
        for a,b in zip(before,latest):
            for i in [0,1,2,4,5,6,7,9,10]:self.assertEqual(a[i],b[i])
        self.assertEqual(Counter((r[0],r[2],r[9]) for r in before),Counter((r[0],r[2],r[9]) for r in latest))
        report=json.loads((ROOT/'docs/revisao-justificativas-contexto.json').read_text())
        for row,r in zip(report['bate_pronto'],bate_pronto_before_grammar_revision(bp_bank())):
            self.assertTrue(set(row['campos'])<=set(['2','5','6']))
            self.assertLessEqual(len(r[2].split()),12)

    def test_cooperative_distribution_explains_investment_and_membership_exception(self):
        q=load_questions()[582]
        self.assertIn('cooperativa de crédito',q[3]);self.assertEqual(q[4],'Associados e não associados')
        self.assertIn('patrimônio de um fundo',q[11][0])
        self.assertIn('permissões específicas',q[11][0])
        self.assertIn('depósitos e crédito cooperativo',q[11][1])
        self.assertIn('não depósito cooperativo',q[11][1])
        self.assertIn('sem excluir os cooperados',q[11][2])
        self.assertIn('captação de depósitos',q[11][3])
        self.assertEqual(q[8],q[11][0])
        self.assertEqual(len(set(q[11])),4)

    def test_active_operation_names_the_actor_and_explains_each_debt_relationship(self):
        q=load_questions()[543]
        self.assertIn('banco comercial',q[3])
        self.assertIn('direito de receber',q[11][0])
        self.assertIn('passiva para o emissor',q[11][1])
        self.assertIn('devedor do depositante',q[11][2])
        self.assertIn('obrigação de restituição',q[11][3])
        self.assertIn('recebe os recursos',load_questions()[542][3])

class TeachingBrowser(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click
    answer=harness.PainelCPA.answer

    def test_revised_feedback_maps_to_shuffled_alternatives_and_history(self):
        self.page.evaluate("H=[[1,1,1700000000000,0]];save();begin([583,544],'e')")
        for id in [583,544]:
            self.assertEqual(self.page.locator('.fb-option').count(),0)
            q=self.page.evaluate('id=>questionById(id)',id)
            self.page.locator('button.o').filter(has_text=q[5]).click()
            self.assertEqual(self.page.locator('.fb-option').count(),4)
            for row in self.page.locator('.fb-option').all():
                original=int(row.get_attribute('data-option-index'))
                self.assertEqual(row.locator('p').inner_text(),q[11][original])
            self.click('Próxima' if id==583 else 'Ver resultado')
        h=self.page.evaluate('H');self.assertEqual([r[0] for r in h],[1,583,544])
        self.assertIn('583',self.page.evaluate("localStorage.getItem('cpaH')"))
        self.page.reload();self.assertEqual(self.page.evaluate('H'),h)

    def test_simulation_continues_without_immediate_feedback(self):
        self.page.evaluate("begin([544],'s')")
        self.answer()
        self.assertEqual(self.page.locator('.fb-option').count(),0)
        self.assertIn('Resultado',self.page.inner_text('#app'))
        self.assertEqual(self.page.evaluate('questionById(544)[8]'),load_questions()[543][8])

if __name__=='__main__':unittest.main(verbosity=2)
