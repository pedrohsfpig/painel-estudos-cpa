"""Testes dos fluxos do HTML importado, usando um navegador real."""

import os
import re
from pathlib import Path
import shutil
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import unittest

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class PainelCPA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT))
        )
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"
        cls.playwright = sync_playwright().start()
        executable = os.environ.get("CHROMIUM_PATH") or shutil.which("chromium")
        options = {"headless": True}
        if executable:
            options["executable_path"] = executable
        try:
            cls.browser = cls.playwright.chromium.launch(**options)
        except Exception:
            cls.playwright.stop()
            cls.server.shutdown()
            cls.server.server_close()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        # Um contexto novo impede que respostas de um teste contaminem outro.
        self.context = self.browser.new_context(viewport={"width": 1280, "height": 900})
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.goto(self.url)
        self.page.get_by_text("Progresso salvo neste navegador.", exact=False).wait_for()

    def tearDown(self):
        error_banner = self.page.locator("#er").all_text_contents()
        self.context.close()
        self.assertEqual(self.errors, [], "Erros não tratados no navegador")
        self.assertEqual(error_banner, [], "Erro exibido pela aplicação")

    def click(self, text):
        self.page.get_by_role("button", name=text, exact=True).click()

    def configure(self, mode="Estudo", count=5):
        self.click("Praticar")
        self.page.locator("button.oc").filter(
            has=self.page.get_by_text(mode, exact=True)
        ).click()
        self.page.locator("button.oc").filter(
            has=self.page.get_by_text(str(count), exact=True)
        ).click()
        self.click("Iniciar " + mode.lower())
        self.page.locator(".en").wait_for()

    def answer(self, correct=True):
        index = self.page.evaluate(
            "correct => qz.o.findIndex(option => Boolean(option[1]) === correct)",
            correct,
        )
        self.page.locator("button.o").nth(index).click()

    def finish(self, mode="Estudo", count=5):
        for i in range(count):
            self.answer()
            if mode != "Simulado":
                self.click("Próxima" if i + 1 < count else "Ver resultado")
        self.assertIn("Resultado do " + mode.lower(), self.page.locator("#app").inner_text())
        self.assertIn(f"{count} de {count} (100%)", self.page.locator("#app").inner_text())

    def test_01_bank_and_dashboard(self):
        data = self.page.evaluate("Q")
        self.assertGreaterEqual(len(data), 600)
        self.assertTrue(all(sum(q[0] == lesson for q in data) >= 100 for lesson in range(1, 7)))
        self.assertTrue(all(sum(q[2] == level for q in data) >= count for level, count in enumerate([120, 240, 120, 120])))
        for q in data:
            self.assertTrue(all(isinstance(value, str) and value.strip() for value in q[3:9]))
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["0", "0", "0", "0%"])
        regular = sum(q[2] < 3 for q in data)
        hardcore = sum(q[2] == 3 for q in data)
        self.assertIn(f"{regular} questões da prova e {hardcore} hardcore, {len(data)} nunca respondidas", self.page.locator("#app").inner_text())

    def test_02_navigation_and_all_materials(self):
        self.click("Quadro do SFN")
        self.assertIn("Banco Central do Brasil", self.page.locator("#app").inner_text())
        self.click("Trilha")
        for lesson in range(1, 7):
            self.page.locator("button.tb").nth(lesson - 1).click()
            self.assertIn(f"Aula {lesson} de 6", self.page.locator(".hero").inner_text())
            content = self.page.evaluate("AL[tr - 1]")
            for section, title in [("r", "Resumo da aula"), ("d", "Dicas e macetes"), ("p", "Pegadinhas")]:
                accordion = self.page.locator("details.acc").filter(
                    has=self.page.get_by_text(title, exact=True)
                )
                accordion.locator("summary").click()
                expected = [re.sub(r"\{\{(?:atencao|negacao)\|([^{}]+)\}\}", r"\1", item.replace("**", "")) for item in content[section]]
                self.assertEqual(accordion.locator(".pt").all_text_contents(), expected)
                self.assertEqual(accordion.locator(".acb > p").count(), 0)
                self.assertGreater(accordion.locator(".pt strong").count(), 0)
                for selector, variable in [(".lesson-attention", "--md"), (".lesson-negative", "--hd")]:
                    colors = accordion.locator(selector).evaluate_all("""(elements, variable) => elements.map(element => {
                        const sample = document.createElement('span');
                        sample.style.color = `var(${variable})`;
                        element.append(sample);
                        const expected = getComputedStyle(sample).color;
                        sample.remove();
                        return getComputedStyle(element).color === expected;
                    })""", variable)
                    self.assertTrue(all(colors))
                self.assertGreater(len(content[section]), 0)
                self.assertEqual(len(content[section]), len(set(content[section])))
                if section == "p":
                    for item in content[section]:
                        self.assertNotIn("Armadilha:", item)
                        self.assertNotIn("Correção:", item)
                for other in (key for key in ["r", "d", "p"] if key != section):
                    self.assertFalse(set(content[section]) & set(content[other]))
            if lesson == 6:
                self.assertNotIn("cada carteira tem CNPJ", self.page.locator("#app").inner_text())
        self.page.locator(".nav").get_by_role("button", name="Material de apoio", exact=True).click()
        for lesson in range(1, 7):
            self.click(f"Aula {lesson}")
            for kind in ["Mapa mental", "Diagramas", "Tabelas", "Linha do tempo", "Flashcards"]:
                self.click(kind)
                self.assertGreater(len(self.page.locator("#app").inner_text()), 300)
            question = self.page.locator(".fcd").inner_text()
            self.click("Virar cartão")
            self.assertNotEqual(question, self.page.locator(".fcd").inner_text())
            self.click("Voltar à pergunta")
            self.assertEqual(question, self.page.locator(".fcd").inner_text())
            self.click("Próximo")
            self.click("Anterior")
            self.assertEqual(question, self.page.locator(".fcd").inner_text())

    def test_03_study_aids_and_result(self):
        self.configure()
        self.click("Dica")
        self.assertIn("Dica:", self.page.locator(".aj").inner_text())
        self.click("Eliminar 2 alternativas")
        self.assertEqual(self.page.locator("button.o:disabled").count(), 2)
        self.assertFalse(self.page.evaluate("qz.x.some(i => qz.o[i][1])"))
        self.answer()
        self.assertEqual(self.page.locator(".feedback .fb-option").count(), 4)
        self.click("Próxima")
        for i in range(4):
            self.answer()
            self.click("Próxima" if i < 3 else "Ver resultado")
        self.assertIn("5 de 5 (100%)", self.page.locator("#app").inner_text())

    def test_04_simulation_and_review(self):
        self.configure("Simulado")
        self.assertEqual(self.page.locator(".aj").count(), 0)
        self.assertEqual(self.page.locator(".feedback").count(), 0)
        self.answer(correct=False)
        self.assertIn("questão 2 de 5", self.page.locator(".tb2").inner_text())
        self.assertEqual(self.page.locator("button.o.ok").count(), 0)
        self.assertEqual(self.page.locator(".feedback").count(), 0)
        for _ in range(4):
            self.answer()
        self.assertIn("4 de 5 (80%)", self.page.locator("#app").inner_text())
        self.assertEqual(self.page.locator("details.rv").count(), 1)
        self.assertEqual(self.page.locator(".feedback").count(), 0)
        self.page.locator("details.rv summary").click()
        self.assertIn("Resposta correta:", self.page.locator("details.rv").inner_text())
        self.assertEqual(self.page.evaluate("H.map(row => row[3])"), [1] * 5)

    def test_05_hardcore(self):
        self.configure("Hardcore")
        self.assertTrue(self.page.evaluate("qz.ids.every(id => Q[id - 1][2] === 3)"))
        self.assertEqual(self.page.locator(".aj").count(), 0)
        self.finish("Hardcore")
        self.assertEqual(self.page.evaluate("H.map(row => row[3])"), [2] * 5)

    def test_06_persistence_progress_and_reset(self):
        self.configure()
        self.finish()
        history = self.page.evaluate("H")
        self.page.reload()
        self.page.get_by_text("Progresso salvo neste navegador.", exact=False).wait_for()
        self.assertEqual(self.page.evaluate("H"), history)
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["5", "5", "0", "100%"])
        self.assertEqual(self.page.get_by_role("img", name="Aproveitamento por dia").count(), 1)
        self.click("Zerar histórico")
        self.assertEqual(len(self.page.evaluate("H")), 5)
        self.click("Confirmar: apagar tudo")
        self.page.reload()
        self.page.get_by_text("Progresso salvo neste navegador.", exact=False).wait_for()
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["0", "0", "0", "0%"])

    def test_07_errors_and_retry(self):
        self.configure()
        self.answer(correct=False)
        wrong_id = self.page.evaluate("qz.ids[qz.i]")
        self.click("Encerrar")
        self.click("Erros (1)")
        self.assertEqual(self.page.locator("details.rv").count(), 1)
        self.click("Refazer erros (modo estudo)")
        self.assertEqual(self.page.evaluate("qz.ids"), [wrong_id])
        self.answer()
        self.click("Ver resultado")
        self.click("Erros (0)")
        self.assertIn("Nenhum erro pendente", self.page.locator("#app").inner_text())

    def test_08_lesson_level_and_unseen_filters(self):
        self.configure()
        self.finish()
        answered = self.page.evaluate("H.map(row => row[0])")
        self.click("Nova prática")
        self.page.locator("button.oc").filter(has=self.page.get_by_text("Aula 2", exact=True)).click()
        self.page.locator("button.oc").filter(has=self.page.get_by_text("Difícil", exact=True)).click()
        self.page.locator("button.oc").filter(has=self.page.get_by_text("Nunca respondidas", exact=True)).click()
        self.click("Iniciar estudo")
        ids = self.page.evaluate("qz.ids")
        self.assertEqual(len(ids), 5)
        self.assertTrue(set(ids).isdisjoint(answered))
        self.assertTrue(self.page.evaluate("qz.ids.every(id => Q[id - 1][0] === 2 && Q[id - 1][2] === 2)"))

    def test_09_daily_study(self):
        self.click("Começar")
        self.assertEqual(self.page.evaluate("qz.ids.length"), 10)
        self.assertEqual(len(set(self.page.evaluate("qz.ids"))), 10)
        self.assertEqual(self.page.evaluate("[0, 1, 2].map(level => qz.ids.filter(id => Q[id - 1][2] === level).length)"), [3, 5, 2])
        self.finish(count=10)

    def test_10_mobile_functional_flow(self):
        self.page.set_viewport_size({"width": 390, "height": 844})
        self.configure()
        self.assertTrue(self.page.locator(".en").is_visible())
        self.assertEqual(self.page.locator("button.o").count(), 4)
        self.finish()

    def test_11_feedback_after_right_and_wrong_answers(self):
        self.configure()
        for correct in [False, True]:
            self.assertEqual(self.page.locator(".feedback").count(), 0)
            self.answer(correct)
            self.assertEqual(self.page.locator(".fb-option").count(), 4)
            self.assertEqual(self.page.locator(".fb-correct").count(), 1)
            self.assertEqual(self.page.locator(".fb-selected").count(), 1)
            self.assertEqual(self.page.locator(".fb-selected.fb-correct").count(), int(correct))
            self.assertEqual(self.page.locator("button.o:disabled").count(), 4)
            self.assertEqual(self.page.locator(".fb-choice").inner_text(), "Sua resposta")
            self.click("Próxima")
            self.assertEqual(self.page.locator(".feedback").count(), 0)

    def test_12_all_questions_and_shuffled_alternatives_have_matching_feedback(self):
        # Exercita os quatro caminhos de resposta das 600 questões no DOM real.
        result = self.page.evaluate("""() => {
            let checked = 0;
            for (let id = 1; id <= Q.length; id++) {
                for (let originalIndex = 0; originalIndex < 4; originalIndex++) {
                    begin([id], Q[id - 1][2] === 3 ? 'h' : 'e');
                    if (document.querySelector('.feedback')) throw Error('Feedback antes da resposta: ' + id);
                    const chosen = qz.o.findIndex(o => o[2] === originalIndex);
                    pick(chosen);
                    const cards = [...document.querySelectorAll('.fb-option')];
                    if (cards.length !== 4) throw Error('Feedbacks incompletos: ' + id);
                    cards.forEach((card, displayIndex) => {
                        const option = qz.o[displayIndex];
                        if (card.dataset.optionIndex !== String(option[2])) throw Error('Índice trocado: ' + id);
                        if (card.querySelector('h4').textContent !== 'ABCD'[displayIndex] + ') ' + option[0]) throw Error('Alternativa trocada: ' + id);
                        if (card.querySelector('p').textContent !== Q[id - 1][11][option[2]]) throw Error('Explicação trocada: ' + id);
                        if (card.classList.contains('fb-correct') !== Boolean(option[1])) throw Error('Correção trocada: ' + id);
                        if (card.classList.contains('fb-selected') !== (displayIndex === chosen)) throw Error('Escolha trocada: ' + id);
                    });
                    const before = H.length;
                    pick(chosen);
                    if (H.length !== before) throw Error('Resposta duplicada: ' + id);
                    checked++;
                }
            }
            return {checked, questions: Q.length, history: H.length};
        }""")
        self.assertEqual(result["checked"], result["questions"] * 4)
        self.assertEqual(result["history"], result["checked"])

    def test_13_future_question_contract_and_feedback(self):
        errors = self.page.evaluate("""() => {
            const invalid = [];
            const missing = structuredClone(Q[0]);
            missing.length = 11;
            invalid.push(missing);
            for (let index = 0; index < 4; index++) {
                const empty = structuredClone(Q[0]);
                empty[11][index] = ' ';
                invalid.push(empty);
            }
            const short = structuredClone(Q[0]); short[11].pop(); invalid.push(short);
            const generic = structuredClone(Q[0]); generic[11].fill('Uma justificativa para todas.'); invalid.push(generic);
            const duplicate = structuredClone(Q[0]); duplicate[5] = ' ' + duplicate[4].toLocaleUpperCase('pt-BR') + ' '; invalid.push(duplicate);
            return invalid.map(question => {
                try { validateQuestionBank([...Q, question]); return null; }
                catch (error) { return error.message; }
            });
        }""")
        self.assertEqual(len(errors), 8)
        self.assertTrue(all(errors))
        self.page.evaluate("""() => {
            const question = structuredClone(Q[0]);
            question[3] = 'Nova questão com feedback próprio';
            question[11] = [
                'Explicação específica da resposta certa futura.',
                'Explicação específica do primeiro erro futuro.',
                'Explicação específica do segundo erro futuro.',
                'Explicação específica do terceiro erro futuro.'
            ];
            Q.push(question);
            validateQuestionBank();
            begin([Q.length], 'e');
        }""")
        self.answer()
        self.assertEqual(self.page.locator(".fb-option").count(), 4)
        self.assertIn("Explicação específica da resposta certa futura.", self.page.locator(".feedback").inner_text())

    def test_14_negative_question_explains_true_distractors(self):
        self.page.evaluate("begin([29], 'e')")
        self.answer(correct=False)
        self.assertIn("afirmação incorreta", self.page.locator(".fb-correct p").inner_text())
        self.assertIn("afirmação é verdadeira", self.page.locator('[data-option-index="1"] p').inner_text())
        self.assertIn("não é a exceção", self.page.locator('[data-option-index="1"] p').inner_text())

    def test_15_error_review_and_legacy_history(self):
        self.page.evaluate("localStorage.setItem('cpaH', JSON.stringify([[1,0,1700000000000,0],[600,1,1700000001000,2]]))")
        self.page.reload()
        self.page.get_by_text("Progresso salvo neste navegador.", exact=False).wait_for()
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["2", "1", "1", "50%"])
        self.click("Erros (1)")
        self.page.locator("details.rv summary").click()
        self.assertEqual(self.page.locator(".fb-option").count(), 4)
        self.click("Refazer erros (modo estudo)")
        self.answer()
        self.page.reload()
        self.page.get_by_text("Progresso salvo neste navegador.", exact=False).wait_for()
        self.assertEqual(self.page.evaluate("H.length"), 3)
        self.assertEqual(self.page.evaluate("H.slice(0,2).map(row => row[0])"), [1, 600])
        self.assertEqual(self.page.get_by_role("button", name="Erros (0)", exact=True).count(), 1)

    def test_16_feedback_is_text_not_executable_markup(self):
        self.page.evaluate("""() => {
            Q[0][11][0] = '<img src=x onerror="window.feedbackExecuted=true"> & explicação';
            begin([1], 'e');
        }""")
        self.answer()
        self.assertEqual(self.page.locator(".feedback img").count(), 0)
        self.assertIn('<img src=x', self.page.locator(".fb-correct p").inner_text())
        self.assertFalse(self.page.evaluate("Boolean(window.feedbackExecuted)"))

    def test_17_shuffle_has_24_equiprobable_permutations_with_feedback_links(self):
        result = self.page.evaluate("""() => {
            const options = questionOptions(Q[0]);
            const original = JSON.stringify(options);
            const permutations = new Set();
            const correctPositions = [0, 0, 0, 0];
            for (let first = 0; first < 4; first++) {
                for (let second = 0; second < 3; second++) {
                    for (let third = 0; third < 2; third++) {
                        const draws = [(first + .5) / 4, (second + .5) / 3, (third + .5) / 2];
                        const shuffled = shuffle(options, () => draws.shift());
                        const indices = shuffled.map(option => option[2]);
                        permutations.add(indices.join(','));
                        correctPositions[shuffled.findIndex(option => option[1])]++;
                        if (new Set(indices).size !== 4) throw Error('Alternativa perdida');
                        for (const option of shuffled) {
                            if (option[0] !== Q[0][4 + option[2]]) throw Error('Texto desvinculado');
                            if (option[1] !== Number(option[2] === 0)) throw Error('Gabarito desvinculado');
                        }
                    }
                }
            }
            return { count: permutations.size, correctPositions, unchanged: JSON.stringify(options) === original };
        }""")
        self.assertEqual(result["count"], 24)
        self.assertEqual(result["correctPositions"], [6, 6, 6, 6])
        self.assertTrue(result["unchanged"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
