"""Contrato de cobertura e integridade; não certifica vigência normativa."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unittest
from validate_bank import load_questions, validate_questions
from audit_alternatives import check_balance
from question_revision import questions_before_context_revision

ROOT=Path(__file__).resolve().parents[1]

def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

class Aula9Tests(unittest.TestCase):
    def setUp(self):
        self.all=load_questions()
        self.rows=[q for q in self.all if q[0]==9]
        self.authored=questions_before_context_revision(self.all)
        self.report=json.loads((ROOT/'docs/aula-9-cobertura.json').read_text())

    def test_requested_weights_hold_in_each_level_including_hardcore(self):
        self.assertEqual(len(self.rows),100)
        for prefix,counts in [('ANBIMA:',{0:10,1:20,2:10,3:10}),
                              ('Garantias:',{0:8,1:16,2:8,3:8}),
                              ('Liberdade:',{0:2,1:4,2:2,3:2})]:
            self.assertEqual(Counter(q[2] for q in self.rows if q[1].startswith(prefix)),counts)
        self.assertTrue(validate_questions(self.rows))
        self.assertTrue(check_balance(self.rows))
        self.assertTrue(all(q[9]==0 for q in self.rows))

    def test_provenance_covers_all_pages_and_all_new_ids(self):
        self.assertEqual([r['id'] for r in self.report['questoes']],list(range(801,901)))
        self.assertEqual({p for r in self.report['cobertura'] for p in r['slides']},set(range(1,16)))
        self.assertEqual({r['transcricao'] for r in self.report['cobertura']},{1,2,3})
        for r in self.report['questoes']:
            q=self.authored[r['id']-1]
            self.assertEqual(digest(q),r['hash'])
            self.assertEqual(q[1],r['tema'])
            self.assertEqual(q[2],r['nivel'])
            self.assertTrue(all(1<=p<=15 for p in r['slides']))

    def test_prior_eight_hundred_questions_keep_ids_and_complete_content(self):
        self.assertEqual(digest(self.authored[:800]),self.report['preservacao']['hash_primeiras_800'])
        self.assertEqual(self.report['preservacao']['ids_anteriores'],list(range(1,801)))

    def test_three_blocks_retain_other_entities_and_all_materials(self):
        html=(ROOT/'index.html').read_text()
        lessons=json.JSONDecoder().raw_decode(html.split('const AL=',1)[1])[0]
        material=json.JSONDecoder().raw_decode(html[html.index('\n9:',html.index('const MAT='))+3:])[0]
        self.assertEqual(len(lessons),9)
        self.assertEqual(len(lessons[-1]['b']),3)
        self.assertEqual(len(material['b']),3)
        self.assertEqual(len(material['fc']),54)
        for key in ['r','d','p','n']:
            self.assertEqual(lessons[-1][key],[item for b in lessons[-1]['b'] for item in b[key]])
        for key in ['dg','tb','tl','fc']:
            self.assertEqual(material[key],[item for b in material['b'] for item in b[key]])
        for entity in ['ANBIMA','APIMEC','Planejar','ANCORD','FGC','FGCoop']:
            self.assertIn(entity,json.dumps(material,ensure_ascii=False))
        topics=[t for b in lessons[-1]['b'] for t in b['topics']]
        self.assertEqual(set(topics),{q[1] for q in self.rows})
        self.assertEqual(len(topics),len(set(topics)))

    def test_scope_and_source_discrepancies_are_not_silently_certified(self):
        self.assertFalse(self.report['consulta_normativa']['certificacao_de_vigencia'])
        corrections=' '.join(self.report['decisoes'])
        self.assertIn('R$ 40k',corrections)
        self.assertIn('R$ 40 milhões',corrections)
        for q in self.rows:
            self.assertNotRegex(' '.join(q[3:9]),r'0[,.]0[123]\s*%|1[.]?400|AGRO 100|CPRPPS|CGRPF')
        self.assertIn('R$ 40 milhões',self.all[887][4])
        self.assertIn('R$ 100 mil',self.all[887][4])
        self.assertIn('R$ 50 mil',self.all[884][4])
        self.assertIn('R$ 125 mil',self.all[884][4])

    def test_assertions_use_separate_uppercase_roman_lines_and_unique_questions(self):
        self.assertEqual(len({q[3] for q in self.rows}),100)
        lists=0
        for q in self.rows:
            if re.search(r'\bI\. ',q[3]):
                lists+=1
                self.assertEqual(len(re.findall(r'^[IVX]+\. ',q[3],re.M)),4)
                self.assertGreaterEqual(q[3].count('\n'),5)
            if q[2]==3:
                self.assertTrue(all(not re.fullmatch(r'R\$ [\d.,]+(?: mil| milhões)?\.?',x) for x in q[4:8]))
                self.assertGreater(len(q[3].split()),20)
        self.assertGreaterEqual(lists,6)

if __name__=='__main__':unittest.main(verbosity=2)
