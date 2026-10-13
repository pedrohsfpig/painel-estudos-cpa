"""Regressões de contexto, preservação e estatísticas; não certificação normativa."""
from collections import Counter
import json
import re
from pathlib import Path
import unittest
from validate_bank import load_questions
from question_revision import FIELD_INDEX,digest,questions_before_context_revision

ROOT=Path(__file__).resolve().parents[1]
EXTERNAL=re.compile(r'\baula\b|\bslides?\b|\btranscri[çc][ãa]o\b|professor (?:disse|recomenda|ensinou)|(?:no|do|conforme o|segundo o) material\b|conteúdo enviado|quadro da aula|regra[s]? estudad[ao]s?',re.I)

class QuestionContextTests(unittest.TestCase):
    def setUp(self):
        self.current=load_questions()
        self.before=questions_before_context_revision(self.current)
        self.report=json.loads((ROOT/'docs/revisao-enunciados-autossuficientes.json').read_text())
        self.ledger=self.report['questoes']

    def test_all_modes_have_independent_stems_options_hints_and_explanations(self):
        for id,q in enumerate(self.current,1):
            for text in q[3:9]+[q[10]]+q[11]:
                self.assertNotRegex(text,EXTERNAL,f'Questão {id}')
        # Materiais de escritório são uma situação concreta, não remissão ao curso.
        self.assertIsNone(EXTERNAL.search('Trocar material de escritório.'))

    def test_every_reviewed_id_is_accounted_for_and_changed_fields_are_exact(self):
        self.assertEqual([r['id'] for r in self.ledger],list(range(1,901)))
        for r in self.ledger:
            id=r['id'];a=self.before[id-1];b=self.current[id-1]
            self.assertEqual(r['hash_antes'],digest(a))
            self.assertEqual(r['hash_depois'],digest(b))
            actual={name for name,index in FIELD_INDEX.items() if a[index]!=b[index]}
            self.assertEqual(set(r['campos']),actual)
            self.assertEqual(r['acao'],'alterada' if actual else 'preservada')
            self.assertTrue(r['motivos'])

    def test_question_metadata_history_ids_and_answer_mapping_are_preserved(self):
        self.assertEqual(len(self.current),len(self.before))
        for id,(a,b) in enumerate(zip(self.before,self.current),1):
            for index in [0,1,2,9]:self.assertEqual(a[index],b[index],f'Questão {id}, campo {index}')
            self.assertEqual(self.ledger[id-1]['usada_em_simulados'],b[2]<3 and not b[9])
        self.assertEqual(Counter(q[0] for q in self.current),Counter(q[0] for q in self.before))
        self.assertEqual(Counter((q[0],q[2]) for q in self.current),Counter((q[0],q[2]) for q in self.before))
        # As únicas opções reescritas são as da SCD e o texto correto do STR;
        # o conteúdo correto continua no índice original 0.
        option_ids=[id for id,(a,b) in enumerate(zip(self.before,self.current),1) if a[4:8]!=b[4:8]]
        self.assertEqual(option_ids,[732,788])
        self.assertIn('BNDES',self.current[731][4])
        self.assertIn('Facultativa para ambas',self.current[787][4])

    def test_statistics_match_the_real_diffs_without_double_counting_fields(self):
        stats=self.report['estatisticas'];changed=[r for r in self.ledger if r['acao']=='alterada']
        self.assertEqual(stats['revisadas'],len(self.ledger))
        self.assertEqual(stats['alteradas'],len(changed))
        self.assertEqual(stats['preservadas'],len(self.ledger)-len(changed))
        stems=sum('enunciado' in r['campos'] for r in changed)
        self.assertEqual(stats['enunciados_alterados'],stems)
        self.assertEqual(stats['somente_campos_de_apoio'],len(changed)-stems)
        for name,count in stats['por_campo'].items():
            self.assertEqual(count,sum(name in r['campos'] for r in changed))
        for lesson,counts in stats['por_aula'].items():
            rows=[r for r in self.ledger if r['aula']==int(lesson)]
            self.assertEqual(counts['alteradas'],sum(r['acao']=='alterada' for r in rows))
            self.assertEqual(counts['enunciados'],sum('enunciado' in r['campos'] for r in rows))
            self.assertEqual(counts['preservadas'],sum(r['acao']=='preservada' for r in rows))
        self.assertEqual(sum(stats['por_banco'].values()),len(changed))
        self.assertEqual(sum(stats['por_nivel'].values()),len(changed))

    def test_reported_examples_identify_the_actor_object_and_requested_decision(self):
        self.assertIn('cumprimento obrigatório',self.current[807][3])
        self.assertEqual(self.current[807][4],'Deliberação.')
        self.assertIn('capacita',self.current[807][11][3])
        self.assertIn('CVM',self.current[360][3])
        self.assertNotIn('bloco',self.current[360][3])
        self.assertIn('BACEN',self.current[326][3])
        self.assertIn('ANBIMA',self.current[832][3])
        self.assertIn('STR',self.current[787][3])
        self.assertIn('FGC',self.current[877][3])

    def test_added_context_does_not_supply_the_acronym_function_or_numeric_rule(self):
        # O contexto identifica o serviço; a função da sigla permanece para recordar.
        self.assertNotIn('Liquidação Diferida',self.current[771][3])
        self.assertNotIn('Depósito Interfinanceiro',self.current[638][3])
        self.assertNotIn('10%',self.current[623][3])
        self.assertNotIn('250 mil',self.current[882][3])
        self.assertEqual(self.current[879][3].count('\n'),5)

if __name__=='__main__':unittest.main(verbosity=2)
