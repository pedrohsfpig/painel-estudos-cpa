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

    def lesson_numbers(self):
        return range(1, self.page.evaluate("AL.length") + 1)

    def assert_material_content(self, kind):
        material = self.page.evaluate("typeof currentMaterial === 'function' ? currentMaterial() : MAT[mt.a]")

        def strings(value):
            if isinstance(value, str):
                return [value]
            return [text for child in value for text in strings(child)]

        if kind == "Mapa mental":
            self.assertEqual(self.page.locator(".mind-root>span").inner_text(), material["mm"][0])
            branches = self.page.locator(".mind-branch")
            self.assertEqual(branches.count(), len(material["mm"][1]))
            for index, branch in enumerate(material["mm"][1]):
                rendered = self.page.locator(
                    f'.mind-branch[data-source-index="{index}"]')
                self.assertEqual(rendered.count(), 1)
                self.assertEqual(rendered.locator("h3>span,.mind-node").all_text_contents(), strings(branch))
            self.assertTrue(self.page.locator(".mind-node").evaluate_all(
                "nodes => nodes.every(node => node.getBoundingClientRect().height > 0)"
            ))
        elif kind == "Diagramas":
            actual = self.page.locator(".material-body .material-panel h3,.diagram-step strong,.diagram-step p").all_text_contents()
            expected = [text for diagram in material["dg"] for text in
                        [diagram[1]] + [text for node in diagram[2] for text in node[:2]]]
            self.assertEqual(actual, expected)
        elif kind == "Tabelas":
            panels = self.page.locator(".material-table").all()
            self.assertEqual(len(panels), len(material["tb"]))
            for panel, table in zip(panels, material["tb"]):
                self.assertEqual(panel.locator("h3").inner_text(), table[0])
                title, headers, rows = table
                # A transposição muda os eixos, sem perder células nem associações.
                transpose = {"Intermediação x serviços", "Quadro do SFN", "Heterorregulação x autorregulação",
                             "Os três tipos de entidade", "Emissão x impressão", "Composição do CNSP e do CNPC",
                             "Ativas, passivas e acessórias", "Cooperativa de crédito: atividades"}
                if title in transpose:
                    expected_headers = [headers[0]] + [row[0] for row in rows]
                    expected_rows = [[headers[i]] + [row[i] for row in rows]
                                     for i in range(1, len(headers))]
                else:
                    expected_headers, expected_rows = headers, rows
                self.assertEqual(panel.locator("thead th").all_text_contents(), expected_headers)
                for rendered, expected in zip(panel.locator("tbody tr").all(), expected_rows):
                    self.assertEqual(rendered.locator("th,td").all_text_contents(), expected)
                self.assertEqual(panel.locator("tbody tr").count(), len(expected_rows))
                self.assertTrue(panel.locator("th,td").evaluate_all(
                    "cells => cells.every(e=>getComputedStyle(e).textAlign==='center')"
                ))
        elif kind == "Linha do tempo":
            panels = self.page.locator(".material-time-panel").all()
            self.assertEqual(len(panels), len(material["tl"]))
            for panel, (title, items) in zip(panels, material["tl"]):
                self.assertEqual(panel.locator("h3").inner_text(), title)
                self.assertEqual(panel.locator(".time-record").count(), len(items))
                for index, item in enumerate(items):
                    record = panel.locator(f'.time-record[data-source-index="{index}"]')
                    self.assertEqual(record.count(), 1)
                    self.assertEqual(record.locator(".time-value,.timeline-value").inner_text(), item[0])
                    self.assertEqual(record.locator(".time-description").inner_text(), item[1])
                    self.assertEqual(record.locator(".timeline-extra").all_text_contents(), item[2:])
        else:
            self.assertEqual(self.page.locator(".flashcard-text").inner_text(), material["fc"][0][0])

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
        # As seis aulas originais continuam completas; futuras aulas não herdam
        # uma quota editorial, mas precisam oferecer Estudo e Hardcore.
        self.assertTrue(all(sum(q[0] == lesson for q in data) >= 100 for lesson in range(1, 7)))
        self.assertTrue(all(sum(q[2] == level for q in data) >= count for level, count in enumerate([120, 240, 120, 120])))
        for lesson in self.lesson_numbers():
            self.assertTrue(any(q[0] == lesson and q[2] < 3 for q in data))
            self.assertTrue(any(q[0] == lesson and q[2] == 3 for q in data))
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
        total_lessons = self.page.evaluate("AL.length")
        for lesson in self.lesson_numbers():
            self.page.locator("button.tb").nth(lesson - 1).click()
            self.assertIn(f"Aula {lesson} de {total_lessons}", self.page.locator(".hero").inner_text())
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
                for selector, variable in [(".lesson-attention", "--lesson-attention"), (".lesson-negative", "--hd")]:
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
        for lesson in self.lesson_numbers():
            self.click(f"Aula {lesson}")
            content = self.page.evaluate("lesson => AL[lesson - 1]", lesson)
            for kind in ["Mapa mental", "Diagramas", "Tabelas", "Linha do tempo", "Flashcards"]:
                self.click(kind)
                self.assertGreater(len(self.page.locator("#app").inner_text()), 300)
                self.assertEqual(self.page.locator(".material-lesson h2").inner_text(), content["t"])
                self.assert_material_content(kind)
            question = self.page.locator(".fcd").inner_text()
            self.click("Virar cartão")
            self.assertNotEqual(question, self.page.locator(".fcd").inner_text())
            self.click("Voltar à pergunta")
            self.assertEqual(question, self.page.locator(".fcd").inner_text())
            self.click("Próximo")
            self.click("Anterior")
            self.assertEqual(question, self.page.locator(".fcd").inner_text())
            self.page.locator(".fcd").focus()
            self.page.locator(".fcd").press("Space")
            self.assertNotEqual(question, self.page.locator(".fcd").inner_text())
            self.page.locator(".fcd").press("Enter")
            self.assertEqual(question, self.page.locator(".fcd").inner_text())
            self.click("Aleatório")
            self.assertEqual(self.page.locator(".flashcard-text").inner_text(),
                             self.page.evaluate("MAT[mt.a].fc[fi][0]"))
            self.assertEqual(self.page.locator(".flashcard-progress").get_attribute("aria-valuenow"),
                             str(self.page.evaluate("fi + 1")))

    def test_03_study_aids_and_result(self):
        self.configure()
        self.click("Dica")
        self.assertIn("Dica:", self.page.locator(".aj").inner_text())
        self.click("Eliminar 2 alternativas")
        self.assertEqual(self.page.locator("button.o:disabled").count(), 2)
        self.assertFalse(self.page.evaluate("qz.x.some(i => qz.o[i][1])"))
        self.answer()
        self.assertEqual(self.page.locator(".feedback .fb-option").count(), 4)
        for explanation in self.page.locator(".feedback .fb-option p").all():
            self.assertTrue(explanation.is_visible())
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
        self.assertEqual("Questão 2 de 5", self.page.locator(".quiz-position").inner_text())
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
            pairs = self.page.locator(".feedback .answer-row").evaluate_all("""rows => rows.map(row => {
                const option=row.querySelector('button.o'), feedback=row.querySelector('.fb-option');
                const left=option.getBoundingClientRect(), right=feedback.getBoundingClientRect();
                return right.x >= left.right && Math.abs(right.y-left.y) < 1 &&
                       option.getAttribute('aria-describedby') === feedback.querySelector('p').id;
            })""")
            self.assertEqual(pairs, [True] * 4)
            self.click("Próxima")
            self.assertEqual(self.page.locator(".feedback").count(), 0)

    def test_12_all_questions_and_shuffled_alternatives_have_matching_feedback(self):
        # Exercita os quatro caminhos de resposta de todo o banco no DOM real.
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
                        const button = card.parentElement.querySelector('button.o');
                        if (button.querySelector('.answer-text').textContent !== 'ABCD'[displayIndex] + ') ' + option[0]) throw Error('Alternativa trocada: ' + id);
                        if (button.getAttribute('aria-describedby') !== card.querySelector('p').id) throw Error('Feedback associado à alternativa errada: ' + id);
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

    def toggle_theme(self):
        button = self.page.locator("#theme-toggle")
        current = self.page.locator("html").get_attribute("data-theme")
        expected = "light" if current == "dark" else "dark"
        background = self.page.locator("body").evaluate("element => getComputedStyle(element).backgroundColor")
        snapshot = "element => {const copy=element.cloneNode(true);const timer=copy.querySelector('#tm');if(timer)timer.textContent='';return copy.innerHTML}"
        content = self.page.locator("#app").evaluate(snapshot)
        self.assertEqual(button.count(), 1)
        self.assertTrue(button.is_visible())
        self.assertEqual(button.evaluate("element => getComputedStyle(element).position"), "fixed")
        button.click()
        self.assertEqual(self.page.locator("html").get_attribute("data-theme"), expected)
        self.assertEqual(button.get_attribute("aria-pressed"), str(expected == "dark").lower())
        self.assertEqual(button.get_attribute("aria-label"), "Ativar modo " + ("claro" if expected == "dark" else "escuro"))
        self.assertNotEqual(self.page.locator("body").evaluate("element => getComputedStyle(element).backgroundColor"), background)
        self.assertEqual(self.page.locator("#app").evaluate(snapshot), content)

    def test_18_theme_button_is_global_and_remembers_choice(self):
        self.assertEqual(self.page.locator("#theme-toggle svg").count(), 1)
        for screen in ["Painel", "Quadro do SFN", "Trilha", "Praticar", "Erros (0)", "Material de apoio"]:
            self.click(screen)
            self.toggle_theme()
        self.click("Flashcards")
        self.click("Virar cartão")
        self.toggle_theme()
        self.assertEqual(self.page.get_by_role("button", name="Voltar à pergunta", exact=True).count(), 1)
        self.page.locator("#theme-toggle").focus()
        previous = self.page.locator("html").get_attribute("data-theme")
        self.page.locator("#theme-toggle").press("Space")
        chosen = self.page.locator("html").get_attribute("data-theme")
        self.assertNotEqual(chosen, previous)
        self.assertEqual(self.page.evaluate("localStorage.getItem('cpaTheme')"), chosen)
        self.page.reload()
        self.page.get_by_text("Progresso salvo neste navegador.", exact=False).wait_for()
        self.assertEqual(self.page.locator("html").get_attribute("data-theme"), chosen)
        self.assertTrue(self.page.locator("#theme-toggle").is_visible())

    def test_19_theme_switch_preserves_quizzes_and_stays_clickable_on_mobile(self):
        self.page.set_viewport_size({"width": 390, "height": 720})
        for mode in ["Estudo", "Hardcore", "Simulado"]:
            self.configure(mode)
            state = self.page.evaluate("({ids:qz.ids,index:qz.i,start:qz.t0,history:H})")
            self.toggle_theme()
            self.assertEqual(self.page.evaluate("({ids:qz.ids,index:qz.i,start:qz.t0,history:H})"), state)
            self.answer()
            state = self.page.evaluate("({index:qz.i,chosen:qz.a,history:H})")
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.toggle_theme()
            self.assertEqual(self.page.evaluate("({index:qz.i,chosen:qz.a,history:H})"), state)
            box = self.page.locator("#theme-toggle").bounding_box()
            self.assertLessEqual(box["x"], 16)
            self.assertLessEqual(box["y"], 16)
            self.assertEqual(box["width"], box["height"])
            self.assertGreaterEqual(box["width"], 44)
            self.assertTrue(self.page.locator("#theme-toggle").evaluate("""element => {
                const rect=element.getBoundingClientRect();
                return document.elementFromPoint(rect.x+rect.width/2,rect.y+rect.height/2).closest('#theme-toggle')===element;
            }"""))
            if mode != "Simulado":
                self.click("Próxima")
            for index in range(4):
                self.answer()
                if mode != "Simulado":
                    self.click("Próxima" if index < 3 else "Ver resultado")
            self.assertIn("Resultado do " + mode.lower(), self.page.locator("#app").inner_text())
            self.toggle_theme()
            self.click("Nova prática")

    def test_20_theme_system_preference_and_unavailable_storage(self):
        self.page.evaluate("localStorage.removeItem('cpaTheme')")
        self.page.emulate_media(color_scheme="dark")
        self.page.reload()
        self.assertEqual(self.page.locator("html").get_attribute("data-theme"), "dark")
        self.page.emulate_media(color_scheme="light")
        self.page.wait_for_function("document.documentElement.dataset.theme === 'light'")
        self.toggle_theme()
        self.page.reload()
        self.assertEqual(self.page.locator("html").get_attribute("data-theme"), "dark")
        self.page.emulate_media(color_scheme="light")
        self.assertEqual(self.page.locator("html").get_attribute("data-theme"), "dark")
        self.page.add_init_script("Storage.prototype.getItem = () => {throw Error('Armazenamento indisponível')}; Storage.prototype.setItem = () => {throw Error('Armazenamento indisponível')}")
        self.page.reload()
        self.assertEqual(self.page.locator("html").get_attribute("data-theme"), "light")
        self.toggle_theme()

    def test_21_dashboard_distinguishes_attempts_coverage_and_pending_errors(self):
        fixture = self.page.evaluate("""() => {
            const find = (lesson, level) => Q.findIndex(q => q[0] === lesson && q[2] === level) + 1;
            const [a, b, c, h] = [find(1, 0), find(1, 1), find(3, 2), find(6, 3)];
            const now = Date.now();
            H = [[a,0,now,0],[a,1,now,0],[a,1,now,1],
                 [b,0,now,0],[c,0,now,1],[h,1,now,2],[99999,0,now,0]];
            save();go();return {history:H,pending:[b,c]};
        }""")
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["6", "3", "3", "50%"])
        progress = self.page.get_by_role("progressbar").evaluate_all(
            "elements => elements.map(e => [Number(e.getAttribute('aria-valuenow')), Number(e.getAttribute('aria-valuemax'))])"
        )
        totals = self.page.evaluate("AL.map((_,i)=>Q.filter(q=>q[0]===i+1).length)")
        covered = [2, 0, 1, 0, 0, 1] + [0] * (len(totals) - 6)
        self.assertEqual(progress, [[seen,total] for seen,total in zip(covered,totals)])
        self.assertEqual(self.page.locator(".trail-percent").all_text_contents(),
                         [f"{seen * 100 // total}%" for seen,total in zip(covered,totals)])
        self.assertEqual(self.page.locator(".priority-list li").count(), 2)
        self.assertIn(f"{sum(totals) - 4} nunca respondidas", self.page.locator(".dashboard-footer").inner_text())
        self.page.locator(".dashboard-filters > summary").click()
        self.click("Estudo")
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["3", "1", "2", "33%"])
        self.assertEqual(self.page.locator(".trail-count").nth(0).inner_text(), f"2 de {totals[0]} questões")
        self.assertEqual(self.page.get_by_role("button", name="Revisar 2 erros", exact=True).count(), 1)
        self.assertIn("33%", self.page.get_by_role("img", name="Aproveitamento por dia").text_content())
        self.click("Hardcore")
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["0", "0", "0", "0%"])
        self.assertIn("Nenhuma resposta com estes filtros.", self.page.locator(".metric-note").inner_text())
        self.click("Qualquer")
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["1", "1", "0", "100%"])
        self.page.locator(".trail-row[data-lesson='3']").click()
        self.assertEqual(self.page.evaluate("[view,tr]"), ["t",3])
        self.click("Painel")
        self.click("Abrir aula")
        self.assertEqual(self.page.evaluate("[view,tr]"), ["t",6])
        self.click("Painel")
        self.click("Revisar 2 erros")
        self.assertEqual(self.page.locator("details.rv").count(), 2)
        self.assertEqual(sorted(self.page.evaluate("errs()")), sorted(fixture["pending"]))
        self.assertEqual(self.page.evaluate("H"), fixture["history"])
        self.page.reload()
        self.page.get_by_text("Progresso salvo neste navegador.", exact=False).wait_for()
        self.assertEqual(self.page.evaluate("H"), fixture["history"])
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["6", "3", "3", "50%"])

    def test_22_desktop_sidebar_and_dashboard_layout_in_both_themes(self):
        for theme in ["light", "dark"]:
            if self.page.locator("html").get_attribute("data-theme") != theme:
                self.page.locator("#theme-toggle").click()
            for width in [1024,1280,1440,1920]:
                self.page.set_viewport_size({"width":width,"height":900})
                self.click("Painel")
                self.assertEqual(self.page.locator(".nav button[aria-current='page']").inner_text(), "Painel")
                self.assertEqual(self.page.locator(".nav button .ui-icon").count(), 6)
                self.assertEqual(self.page.locator(".sidebar").evaluate("e => getComputedStyle(e).position"), "fixed")
                main = self.page.locator("main").bounding_box()
                sidebar = self.page.locator(".sidebar").bounding_box()
                self.assertGreaterEqual(main["x"], sidebar["x"] + sidebar["width"])
                for screen in ["Painel","Quadro do SFN","Trilha","Praticar","Erros (0)","Material de apoio"]:
                    self.click(screen)
                    self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Rolagem horizontal: {width}, {theme}, {screen}")
                self.click("Painel")
                self.page.locator(".detail-stats > summary").click()
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                self.assertEqual(self.page.locator(".sidebar").bounding_box()["y"], 0)
                self.assertTrue(self.page.locator("#theme-toggle").is_visible())
                self.page.evaluate("window.scrollTo(0,0)")


    def test_23_lesson_shortcuts_open_sections_without_changing_study_state(self):
        self.page.emulate_media(reduced_motion="reduce")
        self.configure()
        state = self.page.evaluate("({ids:qz.ids,index:qz.i,start:qz.t0,history:H})")
        self.click("Trilha")
        sections = [("Números","lesson-numbers"),("Resumo","lesson-summary"),
                    ("Dicas e macetes","lesson-tips"),("Pegadinhas","lesson-traps")]
        for lesson in self.lesson_numbers():
            self.page.locator("button.tb").nth(lesson-1).click()
            shortcuts = self.page.get_by_role("navigation", name="Atalhos desta aula")
            self.assertEqual(shortcuts.get_by_role("link").count(), 4)
            self.assertEqual(self.page.locator(".lesson-section > summary .ui-icon").count(), 3)
            for label, section_id in sections:
                shortcut = shortcuts.get_by_role("link", name=label, exact=True)
                shortcut.focus()
                shortcut.press("Enter")
                section = self.page.locator("#" + section_id)
                if section_id != "lesson-numbers":
                    self.assertTrue(section.evaluate("e => e.open"))
                self.assertTrue(section.evaluate("e => e.contains(document.activeElement)"))
                # A seção pode já caber na tela: o atalho precisa tornar seu título visível.
                heading = section.locator("summary, h3").first.bounding_box()
                self.assertGreaterEqual(heading["y"], 0)
                self.assertLessEqual(heading["y"] + heading["height"], self.page.viewport_size["height"])
            self.assertEqual(self.page.evaluate("location.hash"), "")
            self.assertEqual(self.page.evaluate("({ids:qz.ids,index:qz.i,start:qz.t0,history:H})"), state)
        self.toggle_theme()
        self.assertEqual(self.page.evaluate("({ids:qz.ids,index:qz.i,start:qz.t0,history:H})"), state)
        self.click("Praticar")
        self.assertEqual(self.page.get_by_role("progressbar", name="Andamento da sessão").get_attribute("aria-valuenow"), "0")

    def test_24_session_progress_matches_answers_in_all_modes(self):
        for mode, title in [("e","Estudo"),("h","Hardcore"),("s","Simulado")]:
            self.page.evaluate("mode => begin(Q.map((q,i)=>i+1).filter(id => mode==='h' ? Q[id-1][2]===3 : Q[id-1][2]<3).slice(0,3),mode)", mode)
            started = self.page.evaluate("qz.t0")
            for i in range(3):
                progress = self.page.get_by_role("progressbar", name="Andamento da sessão")
                self.assertEqual(progress.get_attribute("aria-valuenow"), str(i))
                self.assertEqual(progress.get_attribute("aria-valuemax"), "3")
                self.assertEqual(self.page.locator(".quiz-position").inner_text(), f"Questão {i+1} de 3")
                self.assertEqual(self.page.get_by_role("timer", name="Tempo da sessão").count(), 1)
                self.answer(correct=i != 1)
                self.assertEqual(self.page.evaluate("qz.t0"), started)
                if mode == "s":
                    self.assertEqual(self.page.locator(".feedback, .answer-result").count(), 0)
                    if i < 2:
                        self.assertEqual(progress.get_attribute("aria-valuenow"), str(i+1))
                else:
                    self.assertEqual(progress.get_attribute("aria-valuenow"), str(i+1))
                    self.assertEqual(progress.get_attribute("aria-valuetext"), f"{i+1} de 3 respondidas")
                    self.assertEqual(self.page.locator(".fb-option").count(), 4)
                    self.assertEqual(self.page.locator(".fb-heading .ui-icon").count(), 1 if i != 1 else 2)
                    self.assertEqual(self.page.locator(".result-correct" if i != 1 else ".result-incorrect").count(), 1)
                    self.click("Próxima" if i < 2 else "Ver resultado")
            self.assertIn("Resultado do " + title.lower(), self.page.locator("#app").inner_text())
            self.assertIn("2 de 3 (67%)", self.page.locator("#app").inner_text())
            self.assertEqual(self.page.get_by_role("progressbar", name="Andamento da sessão").count(), 0)


    def test_25_material_comparison_negatives_timelines_and_card_faces(self):
        for theme in ["light", "dark"]:
            self.page.evaluate("theme => document.documentElement.dataset.theme=theme", theme)
            self.page.evaluate("view='m';chooseMaterial('a',4);chooseMaterial('c','tab')")
            table = self.page.locator(".material-table").filter(
                has=self.page.locator("h3").filter(has_text=re.compile(r"^CVM x BACEN$"))
            )
            geometry = table.locator("thead th").evaluate_all(
                "cells => cells.map(e=>e.getBoundingClientRect().width)"
            )
            self.assertAlmostEqual(geometry[1], geometry[2], delta=1)
            colors = table.locator(".comparison-head").evaluate_all(
                "cells => cells.map(e=>getComputedStyle(e).backgroundColor)"
            )
            self.assertNotEqual(colors[0], colors[1])
            self.assertEqual(table.locator("tbody tr:first-child th").evaluate(
                "e => getComputedStyle(e).borderRightWidth"
            ), "1px")
            backgrounds = table.locator("tbody tr td:nth-child(2)").evaluate_all(
                "cells => cells.map(e=>getComputedStyle(e).backgroundColor)"
            )
            self.assertEqual(len(set(backgrounds)), 1, "A coluna não deve ter listras por linha")
            self.assertIn("sem recondução", table.locator(".context-negative").all_text_contents())

            self.page.evaluate("chooseMaterial('a',6);chooseMaterial('c','mapa')")
            self.assertIn("Não recebem depósitos à vista", self.page.locator(".context-negative").all_text_contents())
            self.assertTrue(self.page.locator(".context-negative").evaluate_all("""elements=>elements.every(e=>{
                const sample=document.createElement('span');sample.style.color='var(--hd)';e.append(sample);
                const expected=getComputedStyle(sample).color;sample.remove();return getComputedStyle(e).color===expected;
            })"""))
            self.assertFalse(any(re.search(r"não (?:monetári|bancári|associad)", text, re.I)
                                 for text in self.page.locator(".context-negative").all_text_contents()))
            classifications = self.page.locator(".mind-group>.mind-node .context-classification")
            self.assertGreaterEqual(classifications.count(), 2)
            self.assertNotEqual(classifications.first.evaluate("e=>getComputedStyle(e).color"),
                                classifications.last.evaluate("e=>getComputedStyle(e).color"))
            self.assertEqual(self.page.locator(".mind-branch h3").first.evaluate(
                "e=>getComputedStyle(e).textAlign"
            ), "center")

            self.page.evaluate("chooseMaterial('a',7);chooseLessonBlock(7,2);chooseMaterial('c','mapa')")
            negatives = self.page.locator(".context-negative").all_text_contents()
            self.assertFalse(any(re.search(r"não residenciais", text, re.I) for text in negatives),
                             "Não residenciais é uma classificação, não uma proibição")
            self.assertIn("Não recebe depósitos de poupança", negatives,
                          "Proibições reais devem continuar destacadas")

            self.page.evaluate("chooseMaterial('a',4);chooseMaterial('c','tl')")
            ratios = self.page.locator(".duration-row .duration-track").evaluate_all("""tracks=>tracks.map(e=>
                e.querySelector('.duration-line').getBoundingClientRect().width/e.getBoundingClientRect().width)""")
            for actual, expected in zip(ratios, [.25, 1, .5]):
                self.assertAlmostEqual(actual, expected, delta=.01)
            self.assertEqual(len(ratios), 3)
            self.assertEqual(self.page.locator(".timeline-value").all_text_contents(),
                             ["1º de janeiro", "15 de julho"])
            self.assertEqual(self.page.locator(".material-body .number-card").count(), 0)
            composition = self.page.locator(".collegiate-facts .collegiate-chart")
            self.assertEqual(composition.locator(".collegiate-leader span").inner_text(), "Presidente da CVM")
            self.assertEqual(composition.locator(".collegiate-peer").count(), 4)
            self.assertIn("Renovação do colegiado", self.page.locator(".collegiate-fact").inner_text())
            self.assertIn("1/5 por ano", self.page.locator(".collegiate-fact").inner_text())
            leader = composition.locator(".collegiate-leader").bounding_box()
            peer = composition.locator(".collegiate-peer").first.bounding_box()
            self.assertLess(leader["y"] + leader["height"], peer["y"])
            for lesson, count in [(3, 8), (4, 4)]:
                self.page.evaluate("lesson=>{chooseMaterial('a',lesson);chooseMaterial('c','mapa')}", lesson)
                self.assertEqual(self.page.locator(".collegiate-leader span").inner_text(),
                                 "Presidente do BACEN" if lesson == 3 else "Presidente da CVM")
                self.assertEqual(self.page.locator(".collegiate-peer").count(), count)
            self.page.evaluate("chooseMaterial('a',5);chooseMaterial('c','mapa')")
            self.assertEqual(self.page.locator(".collegiate-chart").count(), 4)
            self.assertEqual(self.page.locator(".collegiate-leader span").all_text_contents(),
                             ["Representante do Ministério da Fazenda — presidente do CNSP", "Superintendente da Susep",
                              "Ministro da Previdência Social — presidente do CNPC", "Superintendente da Previc"])

            self.page.evaluate("chooseMaterial('a',6);chooseMaterial('c','fc');fi=8;go()")
            self.assertIn("destinação do dinheiro", self.page.locator(".flashcard-text").inner_text())
            question_color = self.page.locator(".fcd").evaluate("e=>getComputedStyle(e).backgroundColor")
            self.page.locator(".fcd").click()
            self.assertEqual(self.page.locator(".fcd.is-answer").count(), 1)
            self.assertNotEqual(self.page.locator(".fcd").evaluate("e=>getComputedStyle(e).backgroundColor"), question_color)
            self.assertEqual(self.page.locator(".fcd .context-negative").count(), 0)
            self.page.locator(".fcd").press("Space")
            self.assertEqual(self.page.locator(".fcd.is-answer").count(), 0)

            self.page.evaluate("begin([1,2,3,4,5],'e')")
            self.assertEqual(self.page.locator(".en .context-negative,.o .context-negative").count(), 0)
            self.answer()
            self.assertEqual(self.page.locator(".feedback .context-negative").count(), 0)

    def test_26_map_structure_has_blue_titles_and_identified_leaders(self):
        expected_orgs = {2: ["CMN", "Comoc"], 3: ["BACEN"], 4: ["CVM"],
                         5: ["CNSP", "Susep", "CNPC", "Previc"]}
        for theme in ["light", "dark"]:
            self.page.evaluate("theme=>document.documentElement.dataset.theme=theme", theme)
            for lesson in self.lesson_numbers():
                self.page.evaluate("lesson=>{view='m';mt={a:lesson,c:'mapa'};go()}", lesson)
                self.assert_material_content("Mapa mental")
                self.assertTrue(self.page.locator(".mind-branch h3,.mind-branch h3>span").evaluate_all(
                    """nodes=>nodes.every(e=>{
                        const sample=document.createElement('span');sample.style.color='var(--ac)';e.append(sample);
                        const expected=getComputedStyle(sample).color;sample.remove();return getComputedStyle(e).color===expected;
                    })"""), f"Títulos principais da aula {lesson} devem ser azuis")
                charts = self.page.locator(".mind-map .collegiate-chart")
                self.assertEqual(charts.evaluate_all("nodes=>nodes.map(e=>e.dataset.organ)"),
                                 expected_orgs.get(lesson, []))
                leader_labels = {
                    "CMN": "Ministro da Fazenda — presidente do CMN",
                    "Comoc": "Presidente do Banco Central — coordenador da Comoc",
                    "BACEN": "Presidente do BACEN", "CVM": "Presidente da CVM",
                    "CNSP": "Representante do Ministério da Fazenda — presidente do CNSP",
                    "Susep": "Superintendente da Susep",
                    "CNPC": "Ministro da Previdência Social — presidente do CNPC",
                    "Previc": "Superintendente da Previc"}
                self.assertEqual(charts.locator(".collegiate-leader span").all_text_contents(),
                                 [leader_labels[organ] for organ in expected_orgs.get(lesson, [])])
                for chart in charts.all():
                    self.assertFalse(any(text in ["Diretor", "Presidente", "Superintendente"]
                                         for text in chart.locator(".collegiate-peer span").all_text_contents()))
                for organ, article in [("BACEN", "do"), ("CVM", "da"), ("Susep", "da"), ("Previc", "da")]:
                    chart = self.page.locator(f'.collegiate-chart[data-organ="{organ}"]')
                    if chart.count():
                        self.assertTrue(all(text == f"Diretor {article} {organ}"
                                            for text in chart.locator(".collegiate-peer span").all_text_contents()))
                if lesson in [2, 3, 4]:
                    self.assertEqual(self.page.locator(".mind-row").first.locator("h3>span").all_text_contents(),
                                     ["Natureza", "Composição" if lesson == 2 else "Diretoria"])
            self.page.evaluate("mt={a:1,c:'tab'};go()")
            table = self.page.locator(".material-table").filter(
                has=self.page.locator("h3").filter(has_text=re.compile(r"^Os três tipos de entidade$")))
            self.assertEqual(table.locator("thead th").all_text_contents(),
                             ["Tipo", "Normativa", "Supervisora", "Operacional"])
            self.assertEqual(table.locator("tbody th").all_text_contents(), ["Papel", "Exemplos"])
            self.assertEqual(len(set(table.locator(".comparison-head").evaluate_all(
                "nodes=>nodes.map(e=>getComputedStyle(e).color)"))), 3)
            self.assertIn("sem função executiva", table.locator(".context-negative").all_text_contents())
            # Nem a priorização visual nem a identificação alteram os dados originais.
            self.assertEqual(self.page.evaluate("MAT[3].mm[1].map(branch=>branch[0])"),
                             ["Natureza", "Objetivos", "Quatro funções", "Política monetária", "Diretoria",
                              "Competências", "Autorizações", "Macetes"])
            for lesson, organ in [(3, "BACEN"), (4, "CVM")]:
                self.page.evaluate("lesson=>{mt={a:lesson,c:'tl'};go()}", lesson)
                self.assertEqual(self.page.locator(".collegiate-leader span").inner_text(),
                                 "Presidente do BACEN" if organ == "BACEN" else "Presidente da CVM")
                self.assertEqual(set(self.page.locator(".collegiate-peer span").all_text_contents()),
                                 {"Diretor do BACEN" if organ == "BACEN" else "Diretor da CVM"})
            self.page.evaluate("mt={a:2,c:'diag'};go()")
            self.assertEqual(self.page.locator(".collegiate-affiliation").all_text_contents(), ["Presidente do CMN"])

    def test_27_lesson7_blocks_cover_operators_and_question_modes(self):
        data = self.page.evaluate("({lesson:AL[6],material:MAT[7],questions:Q})")
        lesson, material, questions = data["lesson"], data["material"], data["questions"]
        self.assertIn("Operadores Não Monetários", lesson["t"])
        self.assertEqual([block["id"] for block in lesson["b"]], [1, 2, 3, 4])
        self.assertEqual([block["id"] for block in material["b"]], [1, 2, 3, 4])
        operators = [operator for block in lesson["b"] for operator in block["operators"]]
        self.assertEqual(len(operators), 18)
        self.assertEqual(len(set(operators)), 18, "Um operador não pode desaparecer na divisão da aula")
        topics = [topic for block in lesson["b"] for topic in block["topics"]]
        self.assertEqual(len(topics), len(set(topics)), "O filtro de um bloco não deve incluir outro bloco")
        new_questions = [(index + 1, q) for index, q in enumerate(questions) if q[0] == 7]
        self.assertEqual(len(new_questions), 100,
                         "A aula 7 deve ter a mesma quantidade de questões das anteriores")
        self.assertEqual([sum(q[2] == level for _, q in new_questions) for level in range(4)],
                         [20, 40, 20, 20], "Preserve a distribuição de dificuldade por aula")
        self.assertTrue(all(question_id > 600 for question_id, _ in new_questions),
                        "As questões novas precisam preservar os IDs do histórico existente")
        self.assertEqual({q[1] for _, q in new_questions}, set(topics))
        for block in lesson["b"]:
            with self.subTest(block=block["id"]):
                block_questions = [q for _, q in new_questions if q[1] in block["topics"]]
                self.assertGreater(sum(q[2] < 3 for q in block_questions), 1)
                self.assertGreater(sum(q[2] == 3 for q in block_questions), 1)
                self.assertTrue(all(len(q[11]) == 4 and len(set(q[11])) == 4
                                    for q in block_questions))

    def test_28_lesson7_block_shortcuts_filter_study_and_hardcore(self):
        self.click("Trilha")
        self.page.locator("button.tb").nth(6).click()
        self.assertEqual(self.page.locator(".lesson-blocks button").count(), 5)
        for block in self.page.evaluate("AL[6].b"):
            for mode, shortcut in [("e", "Estudar este bloco"), ("h", "Hardcore deste bloco")]:
                with self.subTest(block=block["id"], mode=mode):
                    self.click("Trilha")
                    self.page.locator(".lesson-blocks button[data-lesson-block='%d']" % block["id"]).click()
                    self.assertEqual(self.page.locator("#lesson-numbers").count(), int(bool(block["n"])))
                    expected_shortcuts = 4 if block["n"] else 3
                    self.assertEqual(self.page.get_by_role("navigation", name="Atalhos desta aula").get_by_role("link").count(), expected_shortcuts)
                    self.click(shortcut)
                    session = self.page.evaluate("({mode:qz.md,ids:qz.ids,questions:qz.ids.map(id=>Q[id-1])})")
                    self.assertEqual(session["mode"], mode)
                    self.assertGreater(len(session["ids"]), 0)
                    self.assertEqual(len(session["ids"]), len(set(session["ids"])))
                    self.assertTrue(all(q[0] == 7 and q[1] in block["topics"]
                                        and (q[2] == 3 if mode == "h" else q[2] < 3)
                                        for q in session["questions"]))
                    self.assertEqual(self.page.locator(".feedback").count(), 0)
                    self.assertEqual(self.page.locator(".aj").count(), int(mode == "e"))
                    self.answer(correct=mode == "h")
                    self.assertEqual(self.page.locator(".fb-option").count(), 4)
                    self.assertEqual(self.page.locator(".fb-selected.fb-correct").count(), int(mode == "h"))
                    self.assertTrue(self.page.evaluate("[...document.querySelectorAll('.fb-option')].every((e,i)=>e.querySelector('p').textContent===Q[qz.ids[qz.i]-1][11][qz.o[i][2]])"))
        self.assertEqual(self.page.evaluate("H.map(row=>row[3])"), [0, 2] * 4)

    def test_29_lesson7_material_blocks_preserve_all_contents_and_quiz(self):
        self.page.evaluate("begin([Q.findIndex(q=>q[0]===7&&q[2]<3)+1],'e')")
        state = self.page.evaluate("({ids:qz.ids,index:qz.i,start:qz.t0,history:H})")
        self.page.locator(".nav").get_by_role("button", name="Material de apoio", exact=True).click()
        self.click("Aula 7")
        for block in self.page.evaluate("AL[6].b"):
            self.page.locator(".lesson-blocks button[data-lesson-block='%d']" % block["id"]).click()
            self.assertEqual(self.page.locator(".lesson-blocks button[aria-pressed='true']").get_attribute("data-lesson-block"), str(block["id"]))
            for kind in ["Mapa mental", "Diagramas", "Tabelas", "Linha do tempo", "Flashcards"]:
                with self.subTest(block=block["id"], kind=kind):
                    self.click(kind)
                    self.assert_material_content(kind)
                    self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth<=innerWidth"),
                                    "Materiais do bloco não devem criar rolagem horizontal da página")
                    self.assertEqual(self.page.evaluate("({ids:qz.ids,index:qz.i,start:qz.t0,history:H})"), state)
        self.page.locator(".lesson-blocks button[data-lesson-block='0']").click()
        self.click("Mapa mental")
        self.assert_material_content("Mapa mental")
        self.assertEqual(self.page.evaluate("({ids:qz.ids,index:qz.i,start:qz.t0,history:H})"), state)

    def test_30_lesson7_flashcards_wrap_by_selected_block_and_keep_face_on_theme_change(self):
        self.page.locator(".nav").get_by_role("button", name="Material de apoio", exact=True).click()
        self.click("Aula 7")
        self.click("Flashcards")
        for block_id in [0, 1, 2, 3, 4]:
            with self.subTest(block=block_id):
                self.page.locator(".lesson-blocks button[data-lesson-block='%d']" % block_id).click()
                cards = self.page.evaluate("currentMaterial().fc")
                self.assertGreater(len(cards), 1)
                self.assertEqual(self.page.evaluate("[fi,ff]"), [0, 0])
                self.assertEqual(self.page.locator(".flashcard-text").inner_text(), cards[0][0])
                self.assertEqual(self.page.locator(".flashcard-progress").get_attribute("aria-valuemax"), str(len(cards)))
                self.click("Anterior")
                self.assertEqual(self.page.evaluate("fi"), len(cards) - 1)
                self.assertEqual(self.page.locator(".flashcard-text").inner_text(), cards[-1][0])
                self.page.locator(".fcd").click()
                self.assertEqual(self.page.locator(".flashcard-text").inner_text(), cards[-1][1])
                self.assertEqual(self.page.locator(".fcd.is-answer").count(), 1)
                self.toggle_theme()
                self.assertEqual(self.page.locator(".flashcard-text").inner_text(), cards[-1][1])
                self.click("Próximo")
                self.assertEqual(self.page.evaluate("[fi,ff]"), [0, 0])
                self.assertEqual(self.page.locator(".flashcard-text").inner_text(), cards[0][0])
        self.assertEqual(self.page.evaluate("H"), [])

    def test_31_lesson7_history_appends_to_legacy_progress_and_retry_updates_only_pending_error(self):
        legacy = [[1, 0, 1700000000000, 0], [600, 1, 1700000001000, 2]]
        self.page.evaluate("history=>localStorage.setItem('cpaH',JSON.stringify(history))", legacy)
        self.page.reload()
        self.page.get_by_text("Progresso salvo neste navegador.", exact=False).wait_for()
        self.assertEqual(self.page.evaluate("H"), legacy)
        new_id = self.page.evaluate("Q.findIndex(q=>q[0]===7&&q[2]<3)+1")
        self.page.evaluate("id=>begin([id],'e')", new_id)
        self.answer(correct=False)
        self.click("Ver resultado")
        self.click("Ver painel")
        total = self.page.evaluate("Q.filter(q=>q[0]===7).length")
        progress = self.page.get_by_role("progressbar", name="Questões praticadas da aula 7")
        self.assertEqual(progress.get_attribute("aria-valuenow"), "1")
        self.assertEqual(progress.get_attribute("aria-valuemax"), str(total))
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["3", "1", "2", "33%"])
        self.click("Abrir aula")
        self.assertEqual(self.page.evaluate("tr"), 7)
        self.click("Erros (2)")
        self.assertEqual(self.page.locator("details.rv").count(), 2)
        self.click("Refazer erros (modo estudo)")
        self.assertEqual(set(self.page.evaluate("qz.ids")), {1, new_id})
        self.page.evaluate("id=>begin([id],'e')", new_id)
        self.answer(correct=True)
        self.page.reload()
        self.page.get_by_text("Progresso salvo neste navegador.", exact=False).wait_for()
        self.assertEqual(self.page.evaluate("H.slice(0,2)"), legacy)
        self.assertEqual(self.page.evaluate("H.map(row=>row[0])"), [1, 600, new_id, new_id])
        self.assertEqual(self.page.evaluate("errs()"), [1])
        self.assertEqual(self.page.get_by_role("progressbar", name="Questões praticadas da aula 7").get_attribute("aria-valuenow"), "1")

    def test_32_lesson7_practice_block_filter_and_fifty_question_simulation(self):
        self.click("Praticar")
        self.page.locator("button.oc").filter(has=self.page.get_by_text("Aula 7", exact=True)).click()
        self.assertEqual(self.page.locator(".practice-blocks button").count(), 5)
        for block in self.page.evaluate("AL[6].b"):
            self.page.locator(".practice-blocks button[data-lesson-block='%d']" % block["id"]).click()
            self.assertTrue(self.page.evaluate("topics=>pool().every(id=>Q[id-1][0]===7&&topics.includes(Q[id-1][1]))", block["topics"]))
            self.assertGreater(self.page.evaluate("pool().length"), 0)
        self.page.locator(".practice-blocks button[data-lesson-block='0']").click()
        self.page.evaluate("cfg.a=7;cfg.b=0;cfg.n=-1;cfg.m='all';cfg.md='s';cfg.c=50;start()")
        self.assertEqual(self.page.evaluate("qz.ids.length"), 50)
        self.assertEqual(len(set(self.page.evaluate("qz.ids"))), 50)
        self.assertTrue(self.page.evaluate("qz.ids.every(id=>Q[id-1][0]===7&&Q[id-1][2]<3&&!Q[id-1][9])"))
        for index in range(50):
            self.assertEqual(self.page.locator(".feedback,.answer-result,.aj").count(), 0)
            self.answer(correct=index != 0)
        self.assertIn("49 de 50 (98%)", self.page.locator("#app").inner_text())
        self.assertIn("2h30 para 50 questões", self.page.locator("#app").inner_text())
        self.assertEqual(self.page.locator("details.rv").count(), 1)
        self.assertEqual(self.page.locator(".feedback").count(), 0)
        self.assertEqual(self.page.evaluate("H.map(row=>row[3])"), [1] * 50)


if __name__ == "__main__":
    unittest.main(verbosity=2)
