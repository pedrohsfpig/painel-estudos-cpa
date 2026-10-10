"""Regressões editoriais identificadas nesta revisão, não certificação pedagógica."""
import collections
import json
import re
from pathlib import Path
import unittest

from validate_bank import load_questions

ROOT = Path(__file__).resolve().parents[1]


class QuestionDesignTests(unittest.TestCase):
    def setUp(self):
        self.q = load_questions()

    def test_lessons_keep_the_same_volume_and_difficulty_distribution(self):
        for lesson in sorted({q[0] for q in self.q}):
            rows = [q for q in self.q if q[0] == lesson]
            self.assertEqual(collections.Counter(q[2] for q in rows),
                             {0:20, 1:40, 2:20, 3:20}, f"Aula {lesson}")

    def test_cnpc_regression_does_not_supply_duration_for_a_sum(self):
        question = self.q[495]
        self.assertEqual(question[2], 3)
        self.assertNotRegex(question[3].lower(), r"(?:2|dois) anos.*recondução")
        self.assertTrue(all(not re.fullmatch(r"\d+ anos[.]?", option) for option in question[4:8]))
        self.assertIn("designação", question[3].lower())
        self.assertIn("presidência", question[3].lower())

    def test_provided_member_list_and_cooperative_factors_are_not_counting_exercises(self):
        for number in [105,400,595,596,671,698]:
            question = self.q[number-1]
            self.assertNotRegex(question[3].lower(), r"quantos membros.*total|quantas pessoas.*20 pessoas cada")
            self.assertTrue(any(re.search(r"[a-zA-Z]{4}", option) for option in question[4:8]))

    def test_explicit_roman_references_are_uppercase_in_every_field(self):
        for number, question in enumerate(self.q,1):
            for text in question[3:9]+[question[10]]+question[11]:
                self.assertNotRegex(text, r"\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\)", f"Questão {number}")

    def test_assertion_answers_do_not_always_choose_the_first_two(self):
        choices = []
        for question in self.q:
            if len(re.findall(r"^[IVX]+\. ", question[3], re.M)) == 4:
                match = re.fullmatch(r"Apenas ([IVX]+) e ([IVX]+)\.", question[4])
                if match:
                    choices.append(match.groups())
        self.assertGreater(len(choices), 30)
        self.assertLess(max(collections.Counter(choices).values()) / len(choices), .55)

    def test_review_manifest_covers_all_original_ids_once(self):
        ledger = json.loads((ROOT/'docs/revisao-questoes-sessoes.json').read_text())
        self.assertEqual([r['id'] for r in ledger], list(range(1,701)))
        for row in ledger:
            self.assertIn(row['acao'], ['preservada','reformulada','formatação'])
            self.assertGreater(len(row['criterio']), 30)
            for key in ['hash_antes','hash_depois']:
                self.assertRegex(row[key], r"^[0-9a-f]{64}$")
            if row['acao']=='preservada':
                self.assertEqual(row['hash_antes'], row['hash_depois'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
