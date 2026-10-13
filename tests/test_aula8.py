"""Contrato editorial da aula 8; não certifica normas ou dificuldade pedagógica."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unittest

from validate_bank import load_questions, validate_questions
from audit_alternatives import check_balance

ROOT=Path(__file__).resolve().parents[1]

class Aula8Tests(unittest.TestCase):
    def setUp(self):
        self.all_questions=load_questions()
        self.questions=[q for q in self.all_questions if q[0]==8]
        self.report=json.loads((ROOT/'docs/aula-8-cobertura.json').read_text())

    def test_final_fifty_fifty_split_is_preserved_at_every_level(self):
        self.assertEqual(len(self.questions),100)
        for topic,counts in [('IP',{0:5,1:10,2:5,3:5}),('Fintechs',{0:5,1:10,2:5,3:5}),('SPB',{0:10,1:20,2:10,3:10})]:
            self.assertEqual(Counter(q[2] for q in self.questions if q[1].startswith(topic+':')),counts)
        self.assertTrue(validate_questions(self.questions))
        self.assertTrue(check_balance(self.questions))

    def test_added_ids_and_provenance_match_the_authored_bank(self):
        ledger=self.report['questoes']
        self.assertEqual([row['id'] for row in ledger],list(range(701,801)))
        for row in ledger:
            question=self.all_questions[row['id']-1]
            digest=hashlib.sha256(json.dumps(question,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
            self.assertEqual(digest,row['hash'])
            self.assertTrue(row['slides'])
            self.assertTrue(all(1<=page<=19 for page in row['slides']))
            self.assertEqual(question[1],row['tema'])
            self.assertEqual(question[2],row['nivel'])
        self.assertFalse(self.report['consulta_normativa']['certificacao_de_vigencia'])

    def test_numeric_references_with_unconfirmed_scope_are_not_exam_answers(self):
        for q in self.questions:
            self.assertFalse(q[9], 'Os 80 itens normais são compartilhados com o simulado')
            for text in q[3:9]:
                self.assertNotRegex(text,r'15[. ]?000|20\s+bilh|100\s+milh')
        html=(ROOT/'index.html').read_text()
        material=json.JSONDecoder().raw_decode(html[html.index('\n8:',html.index('const MAT='))+3:])[0]
        self.assertEqual(len(material['fc']),52)
        references=[table for block in material['b'] for table in block['tb'] if table[0].startswith('Referência')]
        self.assertEqual(len(references),2)
        self.assertIn('15.000',json.dumps(references,ensure_ascii=False))
        self.assertIn('20 bilhões',json.dumps(references,ensure_ascii=False))

    def test_payment_modalities_and_financial_roles_are_not_collapsed(self):
        expected={701:'sem realizar intermediação',709:'funding',732:'BNDES',742:'crédito próprio',
                  764:'arranjo',766:'Liquidação',782:'II e III',795:'relações distintas',799:'participante direto'}
        for number,phrase in expected.items():
            self.assertIn(phrase,self.all_questions[number-1][4])
        self.assertNotRegex(self.all_questions[778][4],r'dispensa|cancela')

    def test_hardcore_does_not_turn_the_supplied_numbers_into_simple_sums(self):
        hardcore=[q for q in self.questions if q[2]==3]
        self.assertEqual(len(hardcore),20)
        for q in hardcore:
            self.assertTrue(all(not re.fullmatch(r'\d+[.,]?\d*\s*(?:anos|reais|meses)?[.]?',x) for x in q[4:8]))
            self.assertGreater(len(q[3].split()),20)
        self.assertEqual(self.all_questions[715][3].count('\n'),5)

if __name__=='__main__':unittest.main(verbosity=2)
