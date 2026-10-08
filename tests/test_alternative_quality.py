"""Regressões editoriais: python3 tests/test_alternative_quality.py."""

import copy
import unittest

from audit_alternatives import audit, check_balance, rank_rates
from validate_bank import load_questions


class AlternativeQualityTests(unittest.TestCase):
    def test_current_bank_has_no_dominant_length_strategy(self):
        self.assertTrue(check_balance(load_questions()))

    def test_ties_are_counted_as_random_choice_among_tied_options(self):
        row = [None] * 4 + ["aaa", "bbb", "ccc", "ddd"]
        self.assertEqual(rank_rates([row], len), [0.25] * 4)
        row[7] = "ee"
        self.assertEqual(rank_rates([row], len), [0, 1 / 3, 1 / 3, 1 / 3])

    def test_longest_shortest_and_middle_answer_patterns_are_rejected(self):
        for correct in ["a", "bbb", "cccc", "ddddd"]:
            with self.subTest(correct=correct):
                bank = copy.deepcopy(load_questions()[:80])
                for row in bank:
                    row[0], row[2] = 1, 0
                    row[4:8] = [correct] + [text for text in ["a", "bbb", "cccc", "ddddd"] if text != correct]
                with self.assertRaisesRegex(ValueError, "acerta 100.0%"):
                    check_balance(bank)

    def test_disproportionate_explanation_in_any_answer_is_flagged(self):
        for option in [4, 5]:
            with self.subTest(option=option):
                row = copy.deepcopy(load_questions()[0])
                row[4:8] = ["Uma alternativa curta."] * 4
                row[option] = "Uma explicação detalhada que aparece somente nesta opção. " * 6
                with self.assertRaisesRegex(ValueError, "extensão desproporcional"):
                    check_balance([row])

    def test_normal_and_hardcore_are_audited_separately(self):
        questions = load_questions()
        report = audit(questions)
        self.assertEqual(report["normal"]["questions"], sum(row[2] < 3 for row in questions))
        self.assertEqual(report["hardcore"]["questions"], sum(row[2] == 3 for row in questions))


if __name__ == "__main__":
    unittest.main(verbosity=2)
