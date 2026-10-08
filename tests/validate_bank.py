"""Validação do conteúdo, sem pacotes externos: python3 tests/validate_bank.py."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_questions():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    return json.loads(html.split("const Q=", 1)[1].split("\n];", 1)[0] + "\n]")


def validate_questions(questions):
    if not isinstance(questions, list) or not questions:
        raise ValueError("O banco de questões está vazio.")
    for question_id, question in enumerate(questions, 1):
        if not isinstance(question, list) or len(question) < 12:
            raise ValueError(f"Questão {question_id}: faltam dados ou feedbacks.")
        if len(question[4:8]) != 4 or not all(
            isinstance(text, str) and text.strip() for text in question[4:8]
        ):
            raise ValueError(f"Questão {question_id}: são obrigatórias quatro alternativas.")
        if len({text.strip().lower() for text in question[4:8]}) != 4:
            raise ValueError(f"Questão {question_id}: as quatro alternativas precisam ser distintas.")
        feedbacks = question[11]
        if not isinstance(feedbacks, list) or len(feedbacks) != 4 or not all(
            isinstance(text, str) and text.strip() for text in feedbacks
        ):
            raise ValueError(f"Questão {question_id}: são obrigatórios quatro feedbacks.")
        if len(set(feedbacks)) != 4:
            raise ValueError(f"Questão {question_id}: cada alternativa precisa de explicação própria.")
    return True


class QuestionBankTests(unittest.TestCase):
    def test_full_bank_has_feedback_for_every_option(self):
        questions = load_questions()
        self.assertGreaterEqual(len(questions), 600)
        self.assertTrue(validate_questions(questions))

    def test_future_question_with_four_explanations_is_accepted(self):
        questions = load_questions()
        new_question = json.loads(json.dumps(questions[0]))
        new_question[3] = "Nova questão para validar o contrato de conteúdo"
        self.assertTrue(validate_questions([*questions, new_question]))

    def test_new_questions_cannot_omit_any_explanation(self):
        for option in range(4):
            with self.subTest(option=option):
                question = load_questions()[0]
                question[11][option] = " "
                with self.assertRaisesRegex(ValueError, "quatro feedbacks"):
                    validate_questions([question])

    def test_missing_feedback_and_wrong_lengths_are_rejected(self):
        for count in [0, 1, 2, 3, 5]:
            with self.subTest(count=count):
                question = load_questions()[0]
                question[11] = ["Explicação"] * count
                with self.assertRaises(ValueError):
                    validate_questions([question])
        with self.assertRaises(ValueError):
            validate_questions([load_questions()[0][:11]])

    def test_one_generic_explanation_cannot_replace_four_feedbacks(self):
        question = load_questions()[0]
        question[11] = ["A mesma justificativa para todas as alternativas."] * 4
        with self.assertRaisesRegex(ValueError, "explicação própria"):
            validate_questions([question])

    def test_duplicate_choices_cannot_create_multiple_identical_answers(self):
        question = load_questions()[0]
        question[5] = " " + question[4].upper() + " "
        with self.assertRaisesRegex(ValueError, "alternativas precisam ser distintas"):
            validate_questions([question])


if __name__ == "__main__":
    unittest.main(verbosity=2)
