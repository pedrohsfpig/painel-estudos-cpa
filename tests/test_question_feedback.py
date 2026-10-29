"""Regressões editoriais e integridade do banco; não certificam legislação."""
from collections import Counter
import copy
import json
from pathlib import Path
import re
import unittest
from validate_bank import load_questions,validate_questions
from final_block import unit_count
from question_revision import FIELD_INDEX,digest,questions_before_feedback_revision,questions_before_context_revision,questions_before_teaching_revision

ROOT=Path(__file__).resolve().parents[1]

class QuestionFeedbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.latest=load_questions()
        cls.current=questions_before_teaching_revision(cls.latest)
        cls.before=questions_before_feedback_revision(cls.latest)
        cls.report=json.loads((ROOT/'docs/revisao-alinhamento-feedbacks.json').read_text())

    def test_review_accounts_for_every_question_and_reports_exact_changes(self):
        rows=self.report['questoes'];stats=self.report['estatisticas']
        self.assertEqual([r['id'] for r in rows],list(range(1,901)))
        for row,a,b in zip(rows,self.before,self.current):
            actual={name for name,index in FIELD_INDEX.items() if a[index]!=b[index]}
            self.assertEqual(set(row['campos']),actual)
            self.assertEqual(row['hash_antes'],digest(a));self.assertEqual(row['hash_depois'],digest(b))
            self.assertEqual(row['acao'],'alterada' if actual else 'preservada')
        changed=sum(a!=b for a,b in zip(self.before,self.current))
        self.assertEqual(stats['alteradas'],changed)
        self.assertEqual(stats['preservadas'],900-changed)
        self.assertEqual(stats['enunciados_alterados'],sum(a[3]!=b[3] for a,b in zip(self.before,self.current)))
        self.assertEqual(stats['questoes_com_alternativas_alteradas'],sum(a[4:8]!=b[4:8] for a,b in zip(self.before,self.current)))
        self.assertEqual(stats['feedbacks_individuais_alterados'],sum(sum(x!=y for x,y in zip(a[11],b[11])) for a,b in zip(self.before,self.current)))
        for field,count in stats['por_campo'].items():
            self.assertEqual(count,sum(field in row['campos'] for row in rows))
        for lesson,count in stats['por_aula'].items():
            self.assertEqual(count,sum(row['aula']==int(lesson) and row['acao']=='alterada' for row in rows))

    def test_revision_chain_rejects_unrecorded_edits(self):
        tampered=copy.deepcopy(self.latest);tampered[835][11][1]='A adesão concede CNPI.'
        with self.assertRaises(AssertionError):questions_before_feedback_revision(tampered)
        original=questions_before_context_revision(self.latest)
        self.assertEqual(len(original),len(self.latest))

    def test_ids_lessons_difficulties_and_simulation_eligibility_are_preserved(self):
        self.assertTrue(validate_questions(self.latest))
        for a,b in zip(self.before,self.latest):
            self.assertEqual([a[i] for i in (0,1,2,9)],[b[i] for i in (0,1,2,9)])
        self.assertEqual(Counter(r[0] for r in self.latest),{n:(50*unit_count() if n==13 else 100) for n in {q[0] for q in self.latest}})
        for lesson in sorted({q[0] for q in self.latest}):
            self.assertEqual(Counter(r[2] for r in self.latest if r[0]==lesson),({0:10*unit_count(),1:20*unit_count(),2:10*unit_count(),3:10*unit_count()} if lesson==13 else {0:20,1:40,2:20,3:20}))

    def test_numeric_explanations_distinguish_possible_value_from_requested_minimum(self):
        for id,r in enumerate(self.latest,1):
            for explanation in r[11]:self.assertNotIn('O valor indicado nesta opção',explanation,f'Questão {id}')
        dates=self.latest[260]
        self.assertEqual(dates[4],'Junho de 2029')
        self.assertIn('respeita a antecedência',dates[11][3])
        self.assertIn('primeira data',dates[11][3])
        self.assertIn('12 meses',dates[11][1]);self.assertIn('36 meses',dates[11][1])
        self.assertIn('30 meses',dates[11][2]);self.assertIn('36 meses',dates[11][2])
        self.assertIn('outros títulos contábeis',self.latest[112][11][1])
        self.assertIn('alíquota',self.latest[112][11][0])

    def test_print_examples_explain_roles_and_mechanisms_instead_of_bare_negation(self):
        analyst=self.latest[835]
        self.assertIn('publicar análises',analyst[3])
        self.assertIn('APIMEC',analyst[11][1]);self.assertIn('avaliação técnica',analyst[11][1])
        self.assertIn('credenciamento',analyst[11][1]);self.assertIn('julga',analyst[11][3])
        self.assertIn('habilitação',analyst[11][2]);self.assertIn('procedimentos',analyst[11][2])
        distribution=self.latest[827]
        self.assertIn('atuação dos empregados',distribution[3]);self.assertIn('procedimentos',distribution[11][0])
        self.assertIn('avalia conhecimentos',distribution[11][3])
        confidence=self.latest[828]
        self.assertIn('financiam empresas',confidence[4]);self.assertIn('nas emissões',confidence[11][0])
        self.assertIn('riscos do negócio',confidence[11][2]);self.assertIn('FGC',confidence[11][3])
        for r in [analyst,distribution,confidence]:
            for t in r[3:9]+[r[10]]+r[11]:self.assertNotRegex(t,r'(?i)\baula\b|\bslides?\b')

    def test_roman_feedback_explains_true_items_and_combination_errors(self):
        ids=[85,100,116,144,199,200,212,271,330,380,391,399,497,538]
        for id in ids:
            r=self.latest[id-1]
            statements=re.findall(r'^([IV]+)\. ',r[3],re.M)
            for label in statements:self.assertRegex(r[11][0],rf'\b{label} é (?:verdadeira|falsa): \S')
            for option,feedback in zip(r[5:8],r[11][1:]):
                self.assertRegex(feedback,r'foi (?:incluída, mas é falsa|omitida, mas é verdadeira):')
                self.assertNotIn('que não deve fazer parte',feedback)
        # O máximo legal não pode ser confundido com um percentual abaixo dele.
        self.assertIn('teto legal',self.latest[329][3])
        self.assertIn('ações com voto',self.latest[537][3])

    def test_ambiguous_distractor_and_missing_objects_are_corrected(self):
        sep=self.latest[741]
        self.assertIn('crédito próprio',sep[4])
        self.assertIn('É permitida à SEP',sep[6])
        self.assertNotEqual(sep[6],'Aplica à SEP a mesma fonte de funding da SCD.')
        self.assertIn('empréstimo bancário',self.latest[8][3])
        self.assertIn('Como funciona',self.latest[511][3])
        self.assertNotIn('forma societária',self.latest[625][3])
        self.assertIn('assim que recebida',self.latest[761][3])

if __name__=='__main__':unittest.main(verbosity=2)
