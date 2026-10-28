"""Testes dos fluxos do HTML importado, usando um navegador real."""

import os
import json
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
        self.assertEqual(self.page.locator("details.rv").count(), 0)
        self.page.locator('.error-group:not([disabled])').click()
        self.assertEqual(self.page.locator("details.rv").count(), 1)
        self.click("Refazer erros (modo estudo)")
        self.assertEqual(self.page.locator('.practice-setup').count(),1)
        self.click("Iniciar estudo")
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
        self.assertEqual(self.page.evaluate("qz.ids.length"), 20)
        self.assertEqual(len(set(self.page.evaluate("qz.ids"))), 20)
        self.assertEqual(self.page.evaluate("[0, 1, 2].map(level => qz.ids.filter(id => Q[id - 1][2] === level).length)"), [5, 10, 5])
        self.assertEqual(self.page.evaluate("new Set(qz.ids.map(id=>Q[id-1][0])).size"),self.page.evaluate("AL.length"))
        self.finish(count=20)
        self.click("Ver painel")
        self.assertEqual(self.page.locator("[data-daily-score]").inner_text(),"100%")
        self.assertTrue(self.page.get_by_role("button",name="Concluído hoje",exact=True).is_disabled())

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
                        if (button.querySelector('.answer-text').textContent !== 'ABCD'[displayIndex] + ') ' + questionDisplay(Q[id-1],true).options[option[2]]) throw Error('Alternativa trocada: ' + id);
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
        self.page.locator('.error-group:not([disabled])').click()
        self.page.locator("details.rv summary").click()
        self.assertEqual(self.page.locator(".fb-option").count(), 4)
        self.click("Refazer erros (modo estudo)")
        self.assertEqual(self.page.locator('.practice-setup').count(),1)
        self.click("Iniciar estudo")
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
        for screen in ["Painel", "Quadro do SFN", "Trilha", "Consulta", "Praticar", "Erros (0)", "Material de apoio"]:
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
        self.click("Estatísticas")
        self.click("Estudo")
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["3", "1", "2", "33%"])
        self.click("Painel")
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["6", "3", "3", "50%"])
        self.assertEqual(self.page.locator(".trail-count").nth(0).inner_text(), f"2 de {totals[0]} questões")
        self.assertEqual(self.page.get_by_role("button", name="Revisar 2 erros", exact=True).count(), 1)
        self.assertEqual(self.page.locator("[data-evolution-day]").get_attribute("data-evolution-percent"),"50")
        self.assertIn("50%", self.page.get_by_role("img", name="Aproveitamento por dia").text_content())
        self.click("Estatísticas")
        self.click("Hardcore")
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["0", "0", "0", "—"])
        self.assertIn("Nenhuma resposta com estes filtros.", self.page.locator(".metric-note").inner_text())
        self.click("Qualquer")
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["1", "1", "0", "100%"])
        self.click("Painel")
        self.page.locator(".trail-row[data-lesson='3']").click()
        self.assertEqual(self.page.evaluate("[view,tr]"), ["t",3])
        self.click("Painel")
        self.click("Abrir aula")
        self.assertEqual(self.page.evaluate("[view,tr]"), ["t",6])
        self.click("Painel")
        self.click("Revisar 2 erros")
        self.assertEqual(self.page.locator("details.rv").count(), 0)
        self.assertEqual(self.page.locator('[data-error-total]').inner_text(), "2")
        self.assertEqual(self.page.locator('.error-group').evaluate_all('cards=>cards.reduce((n,c)=>n+Number(c.dataset.errorCount),0)'),2)
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
                self.assertEqual(self.page.locator(".nav button .ui-icon").count(), self.page.locator(".nav button").count())
                self.assertEqual(self.page.locator(".sidebar").evaluate("e => getComputedStyle(e).position"), "fixed")
                main = self.page.locator("main").bounding_box()
                sidebar = self.page.locator(".sidebar").bounding_box()
                self.assertGreaterEqual(main["x"], sidebar["x"] + sidebar["width"])
                for screen in ["Painel","Quadro do SFN","Estatísticas","Guia da prova","Trilha","Consulta","Praticar","Erros (0)","Material de apoio"]:
                    self.click(screen)
                    self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Rolagem horizontal: {width}, {theme}, {screen}")
                self.click("Estatísticas")
                self.page.locator(".stats-matrix-section > summary").click()
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
                         5: ["CNSP", "Susep", "CNPC", "Previc"], 10: ["Comef"]}
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
                    "Previc": "Superintendente da Previc",
                    "Comef": "Presidente do BACEN — presidente do Comef"}
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
        self.page.locator('[data-error-group="easy"]').click()
        self.assertEqual(self.page.locator("details.rv").count(), 2)
        self.click("Refazer erros (modo estudo)")
        self.assertEqual(self.page.locator('.practice-setup').count(),1)
        self.click("Iniciar estudo")
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

    def test_33_lesson7_content_filter_is_next_to_sections_and_keeps_them_open(self):
        self.page.evaluate("begin([1,2],'e')")
        state = self.page.evaluate("({ids:qz.ids,index:qz.i,start:qz.t0,history:H,questions:Q,lessons:AL})")
        self.click("Trilha")
        self.page.locator("button.tb").nth(6).click()
        for section in ["lesson-summary", "lesson-tips", "lesson-traps"]:
            self.page.locator(f"#{section}>summary").click()

        def plain(text):
            return re.sub(r"\{\{(?:atencao|negacao)\|([^{}]+)\}\}", r"\1", text).replace("**", "")

        for theme in ["light", "dark"]:
            self.page.evaluate("theme=>document.documentElement.dataset.theme=theme", theme)
            for block_id in [1,2,3,4,0]:
                with self.subTest(theme=theme, block=block_id):
                    controls = self.page.locator(".lesson-content-filter")
                    self.assertEqual(controls.count(), 1)
                    self.assertEqual(controls.get_by_role("heading").inner_text(), "Filtrar conteúdo da aula")
                    self.assertEqual(controls.get_by_role("button").count(), 5)
                    controls.locator(f"button[data-lesson-block='{block_id}']").click()
                    expected = next((b for b in state["lessons"][6]["b"] if b["id"] == block_id), state["lessons"][6])
                    self.assertEqual(controls.locator("button[aria-pressed='true']").get_attribute("data-lesson-block"), str(block_id))
                    self.assertEqual(self.page.evaluate("document.activeElement.dataset.lessonBlock"), str(block_id))
                    for section, key in [("lesson-summary","r"),("lesson-tips","d"),("lesson-traps","p")]:
                        self.assertTrue(self.page.locator(f"#{section}").evaluate("e=>e.open"))
                        self.assertEqual(self.page.locator(f"#{section} .pt").all_text_contents(),
                                         [plain(text) for text in expected[key]])
                    self.assertEqual(self.page.locator("#lesson-numbers .mv").all_text_contents(),
                                     [item[0] for item in expected["n"]])
                    first_section = self.page.locator("#lesson-numbers" if expected["n"] else "#lesson-summary")
                    filter_box, section_box = controls.bounding_box(), first_section.bounding_box()
                    self.assertLessEqual(filter_box["y"] + filter_box["height"], section_box["y"])
                    self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth<=innerWidth"))
                    self.assertEqual(self.page.evaluate("({ids:qz.ids,index:qz.i,start:qz.t0,history:H,questions:Q,lessons:AL})"), state)

    def test_34_lesson_sections_remember_independent_open_and_closed_choices(self):
        self.click("Trilha")
        self.page.locator("button.tb").nth(6).click()
        self.page.locator("#lesson-summary>summary").click()
        self.page.locator("#lesson-traps>summary").click()
        for block in [1,2,3,4,0]:
            self.page.locator(f".lesson-blocks button[data-lesson-block='{block}']").click()
            self.assertEqual(self.page.evaluate("['lesson-summary','lesson-tips','lesson-traps'].map(id=>document.getElementById(id).open)"), [True,False,True])
        self.page.locator("#lesson-summary>summary").click()
        self.page.locator(".hero").get_by_role("button", name="Material de apoio", exact=True).click()
        self.click("Trilha")
        self.assertEqual(self.page.evaluate("['lesson-summary','lesson-tips','lesson-traps'].map(id=>document.getElementById(id).open)"), [False,False,True])
        self.page.locator("button.tb").nth(0).click()
        self.assertEqual(self.page.locator("details.lesson-section[open]").count(), 0)
        self.page.locator("button.tb").nth(6).click()
        self.assertTrue(self.page.locator("#lesson-traps").evaluate("e=>e.open"))
        for theme in ["light","dark"]:
            self.page.evaluate("theme=>document.documentElement.dataset.theme=theme", theme)
            colors = self.page.locator(".lesson-blocks button:not([data-lesson-block='0'])").evaluate_all("nodes=>nodes.map(e=>getComputedStyle(e).borderTopColor)")
            self.assertEqual(len(set(colors)), 4)

    def test_35_multiple_lesson_selection_preview_matches_balanced_session(self):
        self.click("Praticar")
        for lesson in [1,2,3]:
            self.page.locator(f"[data-practice-lesson='{lesson}']").click()
        self.assertEqual(self.page.locator("[data-practice-lesson][aria-pressed='true']").evaluate_all("nodes=>nodes.map(e=>+e.dataset.practiceLesson)"), [1,2,3])
        self.page.locator("button.oc").filter(has=self.page.get_by_text("30", exact=True)).click()
        plan = self.page.evaluate("sessionPlan()")
        self.assertEqual([g["count"] for g in plan["groups"]], [10,10,10])
        self.assertEqual([sum(g["counts"][level] for g in plan["groups"]) for level in range(3)], [8,15,7])
        for group in plan["groups"]:
            for actual, weight in zip(group["counts"], [.25,.5,.25]):
                self.assertLessEqual(abs(actual-group["count"]*weight), 1)
        self.assertEqual(self.page.locator(".session-distribution>div").count(), 3)
        self.click("Iniciar estudo")
        actual = self.page.evaluate("[1,2,3].map(lesson=>[0,1,2,3].map(level=>qz.ids.filter(id=>Q[id-1][0]===lesson&&Q[id-1][2]===level).length))")
        self.assertEqual(actual, [g["counts"] for g in plan["groups"]])
        self.assertEqual(self.page.evaluate("new Set(qz.ids).size"), 30)
        self.click("Encerrar")
        self.assertNotEqual(self.page.evaluate("sessionPlan().groups.map(g=>g.counts)"),
                            [g["counts"] for g in plan["groups"]],
                            "O arredondamento dos níveis não deve favorecer sempre as mesmas aulas")
        self.page.locator("[data-practice-lesson='3']").click()
        self.page.locator("button.oc").filter(has=self.page.get_by_text("5", exact=True)).click()
        extra_before = self.page.evaluate("sessionPlan().groups.map(g=>g.count)")
        self.click("Iniciar estudo")
        self.click("Encerrar")
        self.assertEqual(self.page.evaluate("sessionPlan().groups.map(g=>g.count)"), extra_before[::-1])
        self.page.locator("[data-practice-lesson='0']").click()
        self.assertEqual(self.page.evaluate("selectedPracticeLessons()"), [])
        self.assertEqual(self.page.locator("[data-practice-lesson][aria-pressed='true']").count(), 1)

    def test_36_balanced_multiple_lessons_respect_all_modes_levels_and_integer_sizes(self):
        cases = self.page.evaluate("""() => {
            const results=[];
            for(const md of ['e','s','h'])for(const as of [[1,2],[1,2,3],[1,2,3,4],[1,7],[2,5,7],[1,2,3,4,5,6,7]])
            for(const c of [5,10,15,20,30])for(const n of (md==='h'?[-1]:[-1,0,1,2])){
                cfg={a:0,as,b:0,n,c,md,m:'all'};
                const plan=sessionPlan(),ids=mix(plan);
                results.push({md,as,c,n,total:plan.n,note:plan.note,
                    counts:as.map(a=>ids.filter(id=>Q[id-1][0]===a).length),
                    levels:[0,1,2,3].map(l=>ids.filter(id=>Q[id-1][2]===l).length),
                    preview:plan.groups.map(g=>g.counts),
                    actual:as.map(a=>[0,1,2,3].map(l=>ids.filter(id=>Q[id-1][0]===a&&Q[id-1][2]===l).length)),
                    unique:new Set(ids).size===ids.length,
                    valid:ids.every(id=>as.includes(Q[id-1][0])&&(md!=='s'||!Q[id-1][9]))});
            }
            return results;
        }""")
        for case in cases:
            with self.subTest(mode=case["md"], lessons=case["as"], count=case["c"], level=case["n"]):
                self.assertTrue(case["unique"] and case["valid"])
                self.assertEqual(sum(case["counts"]), case["total"])
                self.assertLessEqual(max(case["counts"])-min(case["counts"]), 1)
                self.assertEqual(case["preview"], case["actual"])
                if case["c"] < len(case["as"]):
                    self.assertEqual(case["total"], 0)
                    self.assertIn("pelo menos", case["note"])
                elif case["md"] == "h":
                    self.assertEqual(case["levels"], [0,0,0,case["total"]])
                elif case["n"] >= 0:
                    self.assertEqual(case["levels"][case["n"]], case["total"])
                elif "Alguns níveis" not in case["note"]:
                    medium = int(case["total"]/2+.5)
                    easy = (case["total"]-medium+1)//2
                    self.assertEqual(case["levels"], [easy,medium,case["total"]-medium-easy,0])

    def test_37_sparse_filters_reduce_quantity_without_silently_dropping_lessons(self):
        result = self.page.evaluate("""() => {
            const one=Q.findIndex(q=>q[0]===1&&q[2]===0)+1;
            const two=Q.findIndex(q=>q[0]===2&&q[2]===1)+1;
            H=[[one,0,1700000000000,0],[two,0,1700000001000,0]];
            cfg={a:0,as:[1,2],b:0,n:-1,c:20,md:'e',m:'err'};
            const plan=sessionPlan(),ids=mix(plan);
            cfg.as=[1,2,3];const empty=sessionPlan();view='q';go();
            return {plan,ids,one,two,empty};
        }""")
        self.assertEqual(result["plan"]["n"], 2)
        self.assertEqual([g["count"] for g in result["plan"]["groups"]], [1,1])
        self.assertEqual(set(result["ids"]), {result["one"], result["two"]})
        self.assertIn("Quantidade reduzida", result["plan"]["note"])
        self.assertEqual(result["empty"]["n"], 0)
        self.assertIn("aula 3", result["empty"]["note"])
        self.assertTrue(self.page.get_by_role("button", name="Iniciar estudo", exact=True).is_disabled())
        self.assertIn("aula 3", self.page.locator(".sum").inner_text())

    def test_38_multiple_lessons_do_not_leak_into_single_lesson_or_block_shortcuts(self):
        self.page.evaluate("cfg.as=[1,2,3];cfg.a=0;view='t';tr=7;go()")
        self.page.locator(".lesson-blocks button[data-lesson-block='2']").click()
        self.click("Estudar este bloco")
        self.assertEqual(self.page.evaluate("selectedPracticeLessons()"), [7])
        self.assertTrue(self.page.evaluate("qz.ids.every(id=>Q[id-1][0]===7&&AL[6].b[1].topics.includes(Q[id-1][1]))"))
        self.click("Encerrar")
        self.page.locator("[data-practice-lesson='1']").click()
        self.assertEqual(self.page.evaluate("selectedPracticeLessons()"), [1,7])
        self.assertEqual(self.page.locator(".practice-blocks").count(), 0)
        self.assertEqual(self.page.evaluate("cfg.b"), 0)
        self.page.locator("[data-practice-lesson='1']").click()
        self.assertEqual(self.page.evaluate("selectedPracticeLessons()"), [7])
        self.assertEqual(self.page.locator(".practice-blocks").count(), 1)

    def test_39_available_levels_are_allocated_jointly_without_breaking_lesson_shares(self):
        result = self.page.evaluate("""() => {
            const failed=(lesson,level,count)=>Q.map((q,i)=>({q,id:i+1})).filter(x=>x.q[0]===lesson&&x.q[2]===level).slice(0,count).map(x=>[x.id,0,1700000000000,0]);
            cfg={a:0,as:[1,2],b:0,n:-1,c:20,md:'e',m:'err'};
            H=[...failed(1,0,5),...failed(1,1,10),...failed(2,0,5),...failed(2,2,5)];
            const possible=sessionPlan(),possibleIds=mix(possible);
            H=[...failed(1,0,10),...failed(2,2,10)];
            const unavailable=sessionPlan(),unavailableIds=mix(unavailable);
            return {possible:possible.groups.map(g=>g.counts),possibleLevels:[0,1,2].map(level=>possibleIds.filter(id=>Q[id-1][2]===level).length),unavailable:unavailable.groups.map(g=>g.counts),unavailableLevels:[0,1,2].map(level=>unavailableIds.filter(id=>Q[id-1][2]===level).length),note:unavailable.note};
        }""")
        self.assertEqual(result["possible"], [[0,10,0,0],[5,0,5,0]])
        self.assertEqual(result["possibleLevels"], [5,10,5])
        self.assertEqual(result["unavailable"], [[10,0,0,0],[0,0,10,0]])
        self.assertEqual(result["unavailableLevels"], [10,0,10])
        self.assertIn("Alguns níveis", result["note"])


    def complete_ids(self, ids, mode, correct_positions):
        self.page.evaluate("([ids,mode])=>begin(ids,mode)", [ids, mode])
        for index in range(len(ids)):
            self.answer(correct=index in correct_positions)
            if mode != "s":
                self.click("Próxima" if index < len(ids)-1 else "Ver resultado")

    def test_40_roman_statements_are_lists_in_every_question_view(self):
        for mode, question in [("e",85),("h",491),("s",85)]:
            self.page.evaluate("([id,mode])=>begin([id],mode)", [question, mode])
            labels = self.page.locator(".en .statement-label").all_text_contents()
            self.assertEqual(labels, ["I.","II.","III."] if question == 85 else ["I.","II.","III.","IV."])
            tops = self.page.locator(".en li").evaluate_all("nodes=>nodes.map(n=>n.getBoundingClientRect().top)")
            self.assertEqual(tops, sorted(set(tops)))
            self.assertEqual(self.page.locator(".en .stem-intro").count(), 1)
            self.assertEqual(self.page.locator(".en .stem-question").count(), 1)
            self.answer(correct=False)
            if mode != "s":
                self.click("Ver resultado")
            self.page.locator("details.rv summary").click()
            self.assertEqual(self.page.locator(".rv .statement-label").all_text_contents(), labels)
            self.assertEqual(self.page.locator(".fb-option").count(), 0 if mode == "s" else 4)

    def test_41_all_current_and_future_statements_preserve_text_and_uppercase(self):
        result = self.page.evaluate("""() => {
            let checked=0;
            const clean=s=>s.replace(/\\s+/g,' ').trim();
            for (const [index,q] of Q.entries()) {
                const markers=[...q[3].matchAll(/^([IVX]+)\\. /gm)];
                if (!markers.length) continue;
                const box=document.createElement('div');box.innerHTML=questionStemHtml(q[3]);
                if (box.querySelectorAll('li').length!==markers.length) throw Error('Lista incompleta: '+(index+1));
                const labels=[...box.querySelectorAll('.statement-label')].map(n=>n.textContent);
                if (JSON.stringify(labels)!==JSON.stringify(markers.map(m=>m[1]+'.'))) throw Error('Romano incorreto: '+(index+1));
                box.querySelectorAll('.statement-label').forEach(n=>n.remove());
                if(clean(box.textContent)!==clean(q[3].replace(/^([IVX]+)\\. /gm,''))) {
                    // Elementos adjacentes podem não inserir espaço em textContent.
                    const p=questionStemParts(q[3]);
                    if(clean([p.intro,...p.items,p.footer].join(' '))!==clean(q[3].replace(/^([IVX]+)\\. /gm,'')))
                        throw Error('Texto perdido: '+(index+1));
                }
                checked++;
            }
            const future=questionStemParts('Considere: i. Uma afirmação. ii. Outra afirmação. iii. A última. Estão corretas:');
            const other=questionStemParts('No estágio II da análise, qual providência é adequada?');
            const secure=document.createElement('div');secure.innerHTML=questionStemHtml('Considere: I. <img src=x onerror=alert(1)> II. Texto. Estão corretas:');
            return {checked,future,plain:!other.items,images:secure.querySelectorAll('img').length};
        }""")
        self.assertGreaterEqual(result["checked"], 70)
        self.assertEqual(result["future"]["items"], ["Uma afirmação.","Outra afirmação.","A última."])
        self.assertEqual(result["future"]["footer"], "Estão corretas:")
        self.assertTrue(result["plain"])
        self.assertEqual(result["images"], 0)

    def test_42_result_counts_current_session_not_prior_history(self):
        self.page.evaluate("H=Array.from({length:100},()=>[121,0,1700000000000,0]);save()")
        self.complete_ids([501,502,509,529,20,235], "e", {0,1,4})
        self.assertEqual(self.page.locator("[data-result-score]").inner_text(), "3 de 6 (50%)")
        self.assertEqual(self.page.evaluate("H.length"), 106)
        for level, percent in [(0,"100%"),(1,"0%"),(2,"50%")]:
            self.assertIn(percent, self.page.locator(f'[data-result-level="{level}"]').inner_text())
        self.assertIn("2 de 4 corretas", self.page.locator('[data-result-lesson="6"]').inner_text())
        self.assertIn("1 de 2 corretas", self.page.locator('[data-result-lesson="2"]').inner_text())
        priority = self.page.locator(".result-priority").first
        self.assertIn("Aula 6 · 2 erros em 4 respostas", priority.inner_text())
        self.assertEqual(self.page.locator(".result-patterns li").count(), 1)
        self.assertIn("2 dos 3 erros", self.page.locator(".result-patterns").inner_text())
        self.assertIn("Amostra pequena", self.page.locator(".session-result").inner_text())
        self.assertEqual(self.page.locator("details.rv").count(), 3)

    def test_43_result_dashboard_all_modes_and_retry_session_only(self):
        for mode, ids in [("e",[1,2,16]),("s",[1,2,16]),("h",[496,599,698])]:
            self.page.evaluate("H=[[121,0,1700000000000,0]];save()")
            self.complete_ids(ids, mode, {1})
            self.assertEqual(self.page.locator("[data-result-score]").inner_text(), "1 de 3 (33%)")
            self.assertEqual(self.page.locator(".result-review details.rv").count(), 2)
            self.assertEqual(self.page.locator(".result-patterns").count(), 0)
            self.assertIn("Nenhum grupo de assuntos", self.page.locator(".session-result").inner_text())
            self.click("Refazer erros desta sessão")
            self.assertEqual(self.page.evaluate("qz.ids"), [ids[0],ids[2]])
            self.assertEqual(self.page.evaluate("qz.md"), "h" if mode == "h" else "e")
            self.assertEqual(self.page.evaluate("H.length"), 4)
            self.answer()
            self.assertEqual(self.page.locator(".fb-option").count(), 4)

    def test_44_result_content_shortcut_opens_block_and_returns_to_practice_setup(self):
        self.complete_ids([601,626], "s", {1})
        history = self.page.evaluate("H")
        self.click("Revisar conteúdo da aula 7")
        self.assertEqual(self.page.evaluate("selectedLessonBlocks[7]"), 1)
        self.assertTrue(self.page.locator("#lesson-summary").evaluate("node=>node.open"))
        self.assertTrue(self.page.evaluate("qz===null"))
        self.assertEqual(self.page.evaluate("H"), history)
        self.click("Praticar")
        self.assertEqual(self.page.locator(".practice-setup").count(), 1)
        self.assertEqual(self.page.locator(".session-result").count(), 0)
        self.assertTrue(self.page.evaluate("qz===null"))
        self.assertEqual(self.page.evaluate("H"), history)

    def test_45_results_handle_empty_perfect_and_zero_scores(self):
        self.page.evaluate("begin([], 'e')")
        self.assertIn("Nenhuma questão respondida", self.page.locator(".session-result").inner_text())
        self.assertNotIn("NaN", self.page.locator(".session-result").inner_text())
        for correct, percent in [(True,"100%"),(False,"0%")]:
            self.complete_ids([1,2], "e", {0,1} if correct else set())
            self.assertIn(percent, self.page.locator("[data-result-score]").inner_text())
            self.assertEqual(self.page.locator(".result-priority").count(), 0 if correct else 2)
            self.assertEqual(self.page.locator(".result-success").count(), 1 if correct else 0)
            cards=self.page.locator(".result-performance-card")
            self.assertGreater(cards.count(),0)
            self.assertTrue(cards.evaluate_all("""nodes=>nodes.every(n=>
                n.querySelectorAll('.result-answer-mark').length===Number(n.dataset.resultTotal)&&
                n.querySelectorAll('.result-answer-mark.is-error').length===Number(n.dataset.resultWrong)&&
                Number.isFinite(Number(n.dataset.resultCorrect)/Number(n.dataset.resultTotal)))"""))

    def test_46_final_response_stops_timer_before_feedback_reading(self):
        self.page.evaluate("begin([1], 'e');qz.t0=Date.now()-60000")
        self.answer()
        end = self.page.evaluate("qz.end")
        self.assertGreater(end, 0)
        self.page.evaluate("qz.t0-=60000")
        self.click("Ver resultado")
        self.assertEqual(self.page.evaluate("qz.end"), end)
        self.assertIn("02:00", self.page.locator(".result-stat").last.inner_text())
        self.page.evaluate("go()")
        self.assertEqual(self.page.evaluate("qz.end"), end)

    def test_47_results_and_statement_lists_fit_desktop_in_both_themes(self):
        self.complete_ids([496,599,698,534,672], "h", {1,4})
        state = self.page.evaluate("JSON.stringify(qz)")
        history = self.page.evaluate("H")
        for width in [1024,1280,1440,1920]:
            self.page.set_viewport_size({"width":width,"height":1000})
            for theme in ["light","dark"]:
                self.page.evaluate("theme=>document.documentElement.dataset.theme=theme", theme)
                self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth<=innerWidth"))
                self.assertTrue(self.page.locator(".result-panel,.result-overview,.result-stat").evaluate_all(
                    "nodes=>nodes.every(n=>n.getBoundingClientRect().width>100 && n.scrollWidth<=n.clientWidth+1)"))
                self.page.locator("#theme-toggle").click()
                self.assertEqual(self.page.evaluate("JSON.stringify(qz)"), state)
                self.assertEqual(self.page.evaluate("H"), history)
                if width == 1440:
                    self.page.evaluate("theme=>document.documentElement.dataset.theme=theme", theme)
                    self.page.screenshot(path=f"/tmp/cpa-result-{theme}.png", full_page=True)
        self.page.evaluate("begin([491], 'h')")
        self.page.screenshot(path="/tmp/cpa-roman-statements.png", full_page=True)


    def open_operator_overview(self):
        self.page.locator(".nav").get_by_role("button", name="Material de apoio", exact=True).click()
        self.click("Aula 7")
        self.click("Quadro geral")

    def test_48_operator_overview_covers_participants_with_meaningful_columns(self):
        self.open_operator_overview()
        table = self.page.locator(".operator-overview-table")
        self.assertEqual(table.locator("thead th").all_text_contents(), [
            "Operador / forma","Foco e público","Atuação","Recursos / remuneração",
            "Limites e condições","Regulação / supervisão","Observações"])
        self.assertEqual(table.locator("tbody tr").count(), 18)
        self.assertEqual(table.locator("tbody th[scope='row']").count(), 18)
        self.assertEqual(table.locator("tbody td").count(), 108)
        self.assertEqual(table.locator("tbody .overview-notes").count(), 18)
        self.assertEqual(table.locator(".overview-operator-icon svg").count(), 18)
        self.assertIn("10% das obrigações", table.locator('[data-operator="fomento"] .overview-notes').inner_text())
        self.assertIn("público", table.locator('[data-operator="fomento"] [data-feature="limits"]').inner_text())
        self.assertIn("não é proibição legal geral", table.locator('[data-operator="sci"] .overview-notes').inner_text())
        self.assertIn("Não recebe depósitos de poupança", table.locator('[data-operator="hipotecaria"] [data-feature="limits"]').inner_text())
        self.assertIn("2009", table.locator('[data-operator="dtvm"] .overview-notes').inner_text())
        self.assertIn("CNSP", table.locator('[data-operator="eapc"] [data-feature="oversight"]').inner_text())
        self.assertIn("CNPC", table.locator('[data-operator="efpc"] [data-feature="oversight"]').inner_text())
        self.assertEqual(table.locator(".overview-missing").count(), 3)
        self.assertEqual(table.locator("th .context-negative").count(), 0)
        self.assertIn("não uma proibição", self.page.locator(".overview-footnote").inner_text())
        def plain(text):
            return re.sub(r"\{\{(?:atencao|negacao)\|([^{}]+)\}\}", r"\1", text).replace("**", "")
        for row in self.page.evaluate("OPERATOR_OVERVIEW_ROWS"):
            rendered = table.locator(f'[data-operator="{row["id"]}"]')
            for feature in ["focus","activity","resources","limits","oversight","notes"]:
                cell = rendered.locator(f'[data-feature="{feature}"]')
                if row[feature]:
                    self.assertEqual(cell.locator("li").all_text_contents(), [plain(x) for x in row[feature]],
                                     f'{row["id"]} / {feature}')
                else:
                    self.assertEqual(cell.inner_text(), "Não detalhado na aula")
        self.assertTrue(table.locator("th,td").evaluate_all(
            "cells=>cells.every(c=>getComputedStyle(c).textAlign==='center')"))
        for theme in ["light","dark"]:
            self.page.evaluate("theme=>document.documentElement.dataset.theme=theme", theme)
            colors = self.page.evaluate("""()=>{
                const panel=document.querySelector('.operator-overview'),s=document.createElement('span');panel.append(s);
                s.style.color='var(--hd)';const negative=getComputedStyle(s).color;
                s.style.color='var(--material-violet)';const attention=getComputedStyle(s).color;s.remove();
                return {negative,attention,actualNegative:getComputedStyle(panel.querySelector('.context-negative')).color,
                    actualAttention:getComputedStyle(panel.querySelector('.lesson-attention')).color};
            }""")
            self.assertEqual(colors["negative"], colors["actualNegative"])
            self.assertEqual(colors["attention"], colors["actualAttention"])

    def test_49_operator_filters_cover_four_blocks_and_share_material_selection(self):
        self.open_operator_overview()
        blocks = {
            1:["investimento","desenvolvimento","fomento","cambio"],
            2:["sci","hipotecaria","financeira","scmepp"],
            3:["consorcio","b3","ctvm","dtvm"],
            4:["capitalizacao","eapc","efpc","seguradora","resseguradora","corretor-seguros"],
        }
        for block, ids in blocks.items():
            self.page.locator(f'[data-overview-block="{block}"]').click()
            self.assertEqual(self.page.locator(".operator-overview-table tbody tr").evaluate_all(
                "rows=>rows.map(row=>row.dataset.operator)"), ids)
            self.assertEqual(self.page.evaluate("selectedLessonBlocks[7]"), block)
            self.assertEqual(self.page.locator(".overview-filters [aria-pressed='true']").get_attribute("data-overview-block"), str(block))
            self.assertEqual(self.page.evaluate("document.activeElement.dataset.overviewBlock"), str(block))
        self.click("Mapa mental")
        self.assertEqual(self.page.evaluate("currentMaterial().mm[0]"), "Seguros, capitalização e previdência")
        self.click("Quadro geral")
        self.assertEqual(self.page.locator(".operator-overview-table tbody tr").count(), 6)
        self.page.locator('[data-overview-block="0"]').click()
        self.assertEqual(self.page.locator(".operator-overview-table tbody tr").count(), 18)
        self.click("Tabelas")
        self.assert_material_content("Tabelas")

    def test_50_operator_overview_shortcut_and_lesson_transition_keep_quiz(self):
        self.page.evaluate("begin([601,626],'e')")
        state = self.page.evaluate("JSON.stringify(qz)")
        self.click("Trilha")
        self.page.locator("button.tb").nth(6).click()
        self.click("Quadro comparativo")
        self.assertEqual(self.page.evaluate("[mt.a,mt.c,view]"), [7,"geral","m"])
        self.assertEqual(self.page.evaluate("JSON.stringify(qz)"), state)
        self.click("Aula 3")
        self.assertEqual(self.page.evaluate("mt.c"), "mapa")
        self.assertEqual(self.page.get_by_role("button", name="Quadro geral", exact=True).count(), 0)
        self.click("Trilha")
        self.page.locator("button.tb").nth(2).click()
        self.page.locator(".hero").get_by_role("button", name="Material de apoio", exact=True).click()
        self.assertEqual(self.page.evaluate("mt.a"), 3)
        self.click("Praticar")
        self.assertEqual(self.page.evaluate("JSON.stringify(qz)"), state)
        self.assertEqual(self.page.locator(".en").count(), 1)

    def test_51_operator_overview_expansion_keeps_theme_scroll_filters_and_history(self):
        self.page.evaluate("begin([601,626],'e');H=[[1,0,1700000000000,0]];save()")
        self.open_operator_overview()
        state = self.page.evaluate("({quiz:JSON.stringify(qz),history:H,questions:Q})")
        self.page.locator("#overview-scroll").evaluate("node=>{node.scrollTop=400;node.scrollLeft=40}")
        self.page.get_by_role("button", name="Ampliar quadro comparativo", exact=True).click()
        self.assertTrue(self.page.locator("body").evaluate("node=>node.classList.contains('overview-expanded')"))
        self.assertFalse(self.page.locator(".sidebar").is_visible())
        top = self.page.locator("#overview-scroll").evaluate("node=>node.scrollTop")
        self.assertEqual(top, 400)
        self.page.locator("#theme-toggle").click()
        self.assertEqual(self.page.locator("#overview-scroll").evaluate("node=>node.scrollTop"), top)
        self.assertEqual(self.page.evaluate("({quiz:JSON.stringify(qz),history:H,questions:Q})"), state)
        self.page.locator('[data-overview-block="4"]').click()
        self.assertEqual(self.page.locator("#overview-scroll").evaluate("node=>node.scrollTop"), 0)
        self.assertEqual(self.page.locator(".operator-overview-table tbody tr").count(), 6)
        self.page.keyboard.press("Escape")
        self.assertFalse(self.page.locator("body").evaluate("node=>node.classList.contains('overview-expanded')"))
        self.assertTrue(self.page.locator(".sidebar").is_visible())
        self.assertEqual(self.page.evaluate("document.activeElement.id"), "overview-expand")
        self.assertEqual(self.page.evaluate("({quiz:JSON.stringify(qz),history:H,questions:Q})"), state)
        self.click("Praticar")
        self.assertFalse(self.page.locator("body").evaluate("node=>node.classList.contains('overview-expanded')"))

    def test_52_operator_overview_sticky_headers_and_columns_fit_desktop(self):
        self.open_operator_overview()
        for width in [1024,1280,1440,1920]:
            self.page.set_viewport_size({"width":width,"height":1000})
            for expanded in [False,True]:
                self.page.evaluate("expanded=>{overviewExpanded=expanded;go()}", expanded)
                for theme in ["light","dark"]:
                    self.page.evaluate("theme=>document.documentElement.dataset.theme=theme", theme)
                    self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth<=innerWidth"))
                    cells = self.page.locator(".operator-overview-table th,.operator-overview-table td")
                    self.assertTrue(cells.evaluate_all(
                        "nodes=>nodes.every(n=>n.getBoundingClientRect().width>90 && n.scrollWidth<=n.clientWidth+1)"))
                    self.page.locator("#overview-scroll").evaluate("node=>{node.scrollTop=1000;node.scrollLeft=100}")
                    rects = self.page.evaluate("""()=>{
                        const sc=document.getElementById('overview-scroll').getBoundingClientRect(),
                         head=document.querySelector('.operator-overview-table thead th').getBoundingClientRect(),
                         row=document.querySelector('.operator-overview-table tbody th').getBoundingClientRect();
                        return {container:sc.toJSON(),head:head.toJSON(),row:row.toJSON()};
                    }""")
                    self.assertLess(abs(rects["container"]["top"]-rects["head"]["top"]), 3)
                    self.assertLess(abs(rects["container"]["left"]-rects["row"]["left"]), 3)
                    if width == 1440:
                        self.page.locator("#overview-scroll").evaluate("node=>{node.scrollTop=0;node.scrollLeft=0}")
                        self.page.screenshot(path=f"/tmp/cpa-overview7-{theme}-{'expanded' if expanded else 'normal'}.png", full_page=True)


    def test_53_new_overviews_compare_the_correct_features_for_each_lesson(self):
        self.click("Material de apoio")
        expected = {
            1: (["cmn","bcb","cvm","cnsp","susep","cnpc","previc"],
                ["Órgão / nível","Segmento","Papel","Relação na estrutura","Operadores do segmento","Observações"]),
            5: (["cnsp","susep","cnpc","previc"],
                ["Órgão / natureza","Segmento","Competências","Composição / liderança","Vinculação / sede","Reuniões / decisão","Observações"]),
            6: (["comercial","multiplo","caixa","cooperativa","banco-cooperativo"],
                ["Operador / forma","Foco e público","Atuação","Captação","Estrutura / regra central","Depósitos à vista / condição","Observações"]),
        }
        for lesson, (ids, headers) in expected.items():
            self.click(f"Aula {lesson}")
            if self.page.evaluate("mt.c") != "geral":
                self.click("Quadro geral")
            table = self.page.locator(".operator-overview-table")
            self.assertEqual(table.locator("thead th").all_text_contents(), headers)
            self.assertEqual(table.locator("tbody tr").evaluate_all(
                "rows=>rows.map(r=>r.dataset.operator)"), ids)
            self.assertEqual(table.locator(".overview-notes").count(), len(ids))
            self.assertEqual(table.locator(".overview-operator-icon svg").count(), len(ids))
            for row in self.page.evaluate("lessonOverview().rows"):
                rendered = table.locator(f'[data-operator="{row["id"]}"]')
                self.assertTrue(row["sources"])
                for key, _ in self.page.evaluate("lessonOverview().columns.slice(1)"):
                    expected_text = [re.sub(r"\{\{(?:atencao|negacao)\|([^{}]+)\}\}", r"\1", x).replace("**", "") for x in row[key]]
                    self.assertEqual(rendered.locator(f'[data-feature="{key}"] li').all_text_contents(), expected_text)
                    self.assertEqual(rendered.locator(f'[data-feature="{key}"]').get_attribute("headers"),
                                     f'overview-row-{row["id"]} overview-col-{key}')
            if lesson == 1:
                self.assertIn("não torna a CVM um conselho", table.locator('[data-operator="cvm"] .overview-notes').inner_text())
                self.assertIn("não é uma atribuição indistinta", table.locator('[data-operator="bcb"] .overview-notes').inner_text())
                self.assertIn("previdência aberta", table.locator('[data-operator="susep"] [data-feature="scope"]').inner_text())
            elif lesson == 5:
                self.assertIn("Representante da Fazenda — presidente do CNSP", table.locator('[data-operator="cnsp"] [data-feature="leadership"]').inner_text())
                self.assertIn("9 membros", table.locator('[data-operator="cnpc"] [data-feature="leadership"]').inner_text())
                self.assertIn("5 membros", table.locator('[data-operator="cnpc"] [data-feature="rules"]').inner_text())
                self.assertIn("ao menos 3", table.locator('[data-operator="previc"] [data-feature="rules"]').inner_text())
                for organ in ["cnpc","previc"]:
                    self.assertEqual(table.locator(f'[data-operator="{organ}"] [data-feature="rules"] .context-negative').count(), 0)
            else:
                self.assertIn("quando possui carteira comercial", table.locator('[data-operator="multiplo"] [data-feature="monetary"] .lesson-attention').inner_text())
                self.assertIn("não capta depósitos", table.locator('[data-operator="cooperativa"] [data-feature="monetary"] .context-negative').inner_text())
                self.assertIn("51% das ações com voto", table.locator('[data-operator="banco-cooperativo"] [data-feature="structure"]').inner_text())
            self.assertEqual(table.locator("th .context-negative").count(), 0)
            self.click("Tabelas")
            self.assert_material_content("Tabelas")
            self.click("Quadro geral")

    def test_54_overview_filters_shortcuts_and_lesson_changes_keep_study_state(self):
        self.page.evaluate("begin([1,601],'e');H=[[1,0,1700000000000,0]];save();cfg.as=[1,6];cfg.b=0")
        state = self.page.evaluate("({quiz:JSON.stringify(qz),history:H,practice:JSON.stringify(cfg),reading:JSON.stringify(selectedLessonBlocks)})")
        for lesson, group, ids in [
            (1,2,["cnsp","susep"]), (5,2,["cnpc","previc"]),
            (6,3,["cooperativa","banco-cooperativo"]),
        ]:
            self.click("Trilha")
            self.page.locator("button.tb").nth(lesson-1).click()
            self.click("Quadro comparativo")
            self.assertEqual(self.page.evaluate("[mt.a,mt.c,view]"), [lesson,"geral","m"])
            self.assertEqual(self.page.locator("#overview-scroll").evaluate("n=>n.scrollTop"), 0)
            self.page.locator(f'[data-overview-block="{group}"]').click()
            self.assertEqual(self.page.locator(".operator-overview-table tbody tr").evaluate_all(
                "rows=>rows.map(r=>r.dataset.operator)"), ids)
            self.assertEqual(self.page.evaluate("document.activeElement.dataset.overviewBlock"), str(group))
        for lesson, group in [(1,2),(5,2),(6,3)]:
            self.click(f"Aula {lesson}")
            self.assertEqual(self.page.evaluate("mt.c"), "geral")
            self.assertEqual(self.page.evaluate("overviewBlock()"), group)
        self.assertEqual(self.page.evaluate("({quiz:JSON.stringify(qz),history:H,practice:JSON.stringify(cfg),reading:JSON.stringify(selectedLessonBlocks)})"), state)
        for lesson in [2,3,4]:
            self.click(f"Aula {lesson}")
            self.assertEqual(self.page.get_by_role("button", name="Quadro geral", exact=True).count(), 0)
            self.assertEqual(self.page.evaluate("mt.c"), "mapa")
            self.click("Trilha")
            self.page.locator("button.tb").nth(lesson-1).click()
            self.assertEqual(self.page.get_by_role("button", name="Quadro comparativo", exact=True).count(), 0)
            self.page.locator(".hero").get_by_role("button", name="Material de apoio", exact=True).click()
        self.click("Aula 7")
        self.click("Quadro geral")
        self.page.locator('[data-overview-block="4"]').click()
        self.click("Aula 1")
        self.assertEqual(self.page.evaluate("overviewBlock()"), 2)
        self.click("Aula 7")
        self.assertEqual(self.page.evaluate("selectedLessonBlocks[7]"), 4)
        self.assertEqual(self.page.locator(".operator-overview-table tbody tr").count(), 6)
        self.click("Praticar")
        self.assertEqual(self.page.evaluate("JSON.stringify(qz)"), state["quiz"])
        self.assertEqual(self.page.evaluate("H"), state["history"])

    def test_55_new_overviews_fit_desktop_and_preserve_scroll_on_expansion(self):
        self.click("Material de apoio")
        for lesson in [1,5,6]:
            self.page.evaluate("n=>{overviewExpanded=false;chooseMaterial('a',n);chooseMaterial('c','geral')}", lesson)
            for width in [1024,1280,1440,1920]:
                self.page.set_viewport_size({"width":width,"height":1000})
                for expanded in [False,True]:
                    self.page.evaluate("expanded=>{overviewExpanded=expanded;go()}", expanded)
                    for theme in ["light","dark"]:
                        self.page.evaluate("theme=>document.documentElement.dataset.theme=theme", theme)
                        self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth<=innerWidth"))
                        self.assertTrue(self.page.locator(".operator-overview-table th,.operator-overview-table td").evaluate_all(
                            "nodes=>nodes.every(n=>n.getBoundingClientRect().width>90 && n.scrollWidth<=n.clientWidth+1 && getComputedStyle(n).textAlign==='center')"))
                        self.assertTrue(self.page.locator("#theme-toggle").is_visible())
                        self.page.locator("#overview-scroll").evaluate("n=>{n.scrollTop=200;n.scrollLeft=100}")
                        offsets = self.page.evaluate("""()=>{
                            const sc=document.getElementById('overview-scroll').getBoundingClientRect();
                            return [document.querySelector('.operator-overview-table thead th').getBoundingClientRect().top-sc.top,
                                    document.querySelector('.operator-overview-table tbody th').getBoundingClientRect().left-sc.left];
                        }""")
                        self.assertTrue(all(abs(x)<3 for x in offsets))
                        if width == 1440:
                            self.page.locator("#overview-scroll").evaluate("n=>{n.scrollTop=0;n.scrollLeft=0}")
                            self.page.screenshot(path=f"/tmp/cpa-overview{lesson}-{theme}-{'expanded' if expanded else 'normal'}.png", full_page=True)
            self.page.evaluate("overviewExpanded=false;go()")
            self.page.locator("#overview-scroll").evaluate("n=>{n.scrollTop=200;n.scrollLeft=80}")
            position = self.page.locator("#overview-scroll").evaluate("n=>[n.scrollTop,n.scrollLeft]")
            self.page.get_by_role("button", name="Ampliar quadro comparativo", exact=True).click()
            # Wider cells can make a small table shorter: the browser clamps to
            # the remaining scroll range, rather than preserving an impossible offset.
            expanded_top = self.page.locator("#overview-scroll").evaluate("n=>n.scrollTop")
            expanded_max = self.page.locator("#overview-scroll").evaluate("n=>n.scrollHeight-n.clientHeight")
            self.assertEqual(expanded_top, min(position[0], expanded_max))
            self.page.locator("#theme-toggle").click()
            self.assertEqual(self.page.locator("#overview-scroll").evaluate("n=>n.scrollTop"), expanded_top)
            self.page.keyboard.press("Escape")
            self.assertEqual(self.page.evaluate("document.activeElement.id"), "overview-expand")
            self.assertTrue(self.page.locator(".sidebar").is_visible())

    def test_56_future_overview_uses_registered_columns_without_navigation_changes(self):
        fixture_lesson = self.page.evaluate("AL.length+1")
        self.page.evaluate("""()=>{
            const n=AL.length+1;
            AL.push({...AL[0],t:`Aula ${n}: Comparação de teste`});MAT[n]=MAT[1];
            LESSON_OVERVIEWS[n]={...LESSON_OVERVIEWS[1],title:'Quadro de teste',
                columns:[['operator','Participante'],['role','Função'],['notes','Observações']],
                widths:[30,40,30],groups:[{id:1,t:'Grupo de teste',icon:'bank'}],
                rows:[{...LESSON_OVERVIEWS[1].rows[0],id:'teste',name:'Participante de teste'}]};
            view='t';tr=n;go();
        }""")
        self.click("Quadro comparativo")
        self.assertEqual(self.page.evaluate("[mt.a,mt.c]"), [fixture_lesson,"geral"])
        self.assertEqual(self.page.locator(".operator-overview-table thead th").all_text_contents(), ["Participante","Função","Observações"])
        self.assertEqual(self.page.locator(".operator-overview-table tbody td").count(), 2)
        self.page.locator('[data-overview-block="1"]').click()
        self.assertEqual(self.page.locator(".overview-operator-name").inner_text(), "Participante de teste")
        self.click("Aula 3")
        self.assertEqual(self.page.evaluate("mt.c"), "mapa")
        self.click(f"Aula {fixture_lesson}")
        self.click("Quadro geral")
        self.assertEqual(self.page.evaluate("overviewBlock()"), 1)

    def test_57_lesson8_filters_keep_sections_open_and_show_complete_materials(self):
        self.click("Trilha")
        self.page.locator("button.tb").nth(7).click()
        for selector in ["#lesson-summary","#lesson-tips","#lesson-traps"]:
            self.page.locator(selector+" summary").click()
        previous = self.page.evaluate("({history:H,practice:JSON.stringify(cfg)})")
        for block, title in [(1,"1. Instituições de Pagamento"),(2,"2. Fintechs de Crédito"),(3,"3. SPB e Arranjos de Pagamento")]:
            self.page.locator(f'.lesson-content-filter [data-lesson-block="{block}"]').click()
            self.assertEqual(self.page.evaluate("lessonContent(8).t"), title)
            for key, selector in [("r","#lesson-summary"),("d","#lesson-tips"),("p","#lesson-traps")]:
                self.assertTrue(self.page.locator(selector).evaluate("node=>node.open"))
                expected = self.page.evaluate("key=>lessonContent(8)[key].map(x=>x.replace(/\\{\\{(?:atencao|negacao)\\|([^{}]+)\\}\\}/g,'$1').replace(/\\*\\*/g,''))", key)
                self.assertEqual(self.page.locator(selector+" .pt").all_text_contents(), expected)
        self.assertEqual(self.page.evaluate("({history:H,practice:JSON.stringify(cfg)})"), previous)
        self.page.locator(".hero").get_by_role("button", name="Material de apoio", exact=True).click()
        for block in [1,2,3,0]:
            self.page.locator(f'.lesson-blocks [data-lesson-block="{block}"]').click()
            for kind in ["Mapa mental","Diagramas","Tabelas","Linha do tempo","Flashcards"]:
                self.click(kind)
                self.assert_material_content(kind)
                if kind == "Flashcards":
                    self.page.locator("#flashcard").click()
                    self.assertTrue(self.page.locator("#flashcard").evaluate("n=>n.classList.contains('is-answer')"))
                    face = self.page.locator(".flashcard-text").inner_text()
                    self.page.locator("#theme-toggle").click()
                    self.assertEqual(self.page.locator(".flashcard-text").inner_text(), face)
        self.assertEqual(self.page.evaluate("({history:H,practice:JSON.stringify(cfg)})"), previous)

    def test_58_lesson8_study_hardcore_and_simulation_preserve_specific_feedback(self):
        for mode, ids in [("e",[701,731,782]),("h",[721,746,799]),("s",[701,731,782])]:
            self.page.evaluate("args=>{qz=null;begin(args.ids,args.mode)}", {"ids":ids,"mode":mode})
            for index in range(len(ids)):
                question = self.page.evaluate("Q[qz.ids[qz.i]-1]")
                self.answer(correct=index!=1)
                self.assertEqual(self.page.locator(".fb-option").count(), 0 if mode=="s" else 4)
                if mode!="s":
                    for row in self.page.locator(".fb-option").all():
                        option = int(row.get_attribute("data-option-index"))
                        self.assertEqual(row.locator("p").inner_text(),question[11][option])
                    self.click("Ver resultado" if index==len(ids)-1 else "Próxima")
            self.assertEqual(self.page.locator("[data-result-score]").inner_text(), "2 de 3 (67%)")
            self.assertIn("Inovação, Pagamentos e Crédito Digital", self.page.locator(".session-result").inner_text())
        self.assertEqual(self.page.evaluate("H.length"),9)

    def test_59_lesson8_blocks_and_multiple_lessons_keep_balanced_practice(self):
        self.page.evaluate("H=[[1,1,1700000000000,0],[700,0,1700000000001,0]];save();view='q';qz=null;go()")
        history = self.page.evaluate("H")
        for mode in ["e","h","s"]:
            for block, expected in [(1,25),(2,25),(3,50)]:
                result = self.page.evaluate("args=>{cfg={a:8,as:[],n:-1,m:'all',c:50,md:args.mode,b:args.block};const ids=pool();return {ids,questions:ids.map(id=>Q[id-1])}}", {"mode":mode,"block":block})
                self.assertEqual(len(result["ids"]), expected//5 if mode=="h" else expected*4//5)
                self.assertTrue(all(q[0]==8 for q in result["questions"]))
                self.assertTrue(all(q[1].startswith("IP:" if block==1 else "Fintechs:" if block==2 else "SPB:") for q in result["questions"]))
            self.page.evaluate("mode=>{cfg={a:0,as:[7,8],n:-1,m:'all',c:20,md:mode,b:0};start()}", mode)
            lessons = self.page.evaluate("qz.ids.map(id=>Q[id-1][0])")
            self.assertEqual(lessons.count(7),10)
            self.assertEqual(lessons.count(8),10)
        self.assertEqual(self.page.evaluate("H"), history)
        self.page.reload()
        self.assertEqual(self.page.evaluate("H"), history)
        self.assertEqual(self.page.evaluate("[Q[0][0],Q[699][0],Q[700][0],Q[799][0]]"),[1,7,8,8])

    def test_60_lesson8_overview_filters_share_reading_without_changing_the_quiz(self):
        self.page.evaluate("begin([701,799],'e')")
        state = self.page.evaluate("({quiz:JSON.stringify(qz),history:H,practice:JSON.stringify(cfg)})")
        self.page.evaluate("openOperatorOverview(8)")
        self.assertEqual(self.page.locator(".operator-overview-table tbody tr").count(),13)
        self.assertEqual(self.page.locator(".operator-overview-table thead th").all_text_contents(),[
            "Participante / natureza","Função","O que movimenta","Conta / registro","Condições e limites","Aplicação","Observações"])
        for block, ids in [(1,["emissor-eletronico","emissor-pos","credenciador","iniciador"]),
                           (2,["scd","sep"]),
                           (3,["str","spi","selic","b3","sitraf","siloc","compe"])]:
            self.page.locator(f'[data-overview-block="{block}"]').click()
            self.assertEqual(self.page.evaluate("selectedLessonBlocks[8]"),block)
            self.assertEqual(self.page.locator(".operator-overview-table tbody tr").evaluate_all("rows=>rows.map(r=>r.dataset.operator)"),ids)
            self.click("Mapa mental")
            self.assert_material_content("Mapa mental")
            self.click("Quadro geral")
        self.assertIn("não é conta de varejo",self.page.locator('[data-operator="spi"] .overview-notes').inner_text())
        self.page.get_by_role("button",name="Ampliar quadro comparativo",exact=True).click()
        self.page.locator("#theme-toggle").click()
        self.page.keyboard.press("Escape")
        self.assertEqual(self.page.evaluate("({quiz:JSON.stringify(qz),history:H,practice:JSON.stringify(cfg)})"),state)
        self.click("Praticar")
        self.assertEqual(self.page.evaluate("qz.ids"),[701,799])

    def test_61_lesson8_materials_fit_desktop_in_both_themes(self):
        self.page.evaluate("mt.a=8;view='m';go()")
        for width in [1024,1280,1440,1920]:
            self.page.set_viewport_size({"width":width,"height":1000})
            for theme in ["light","dark"]:
                self.page.evaluate("theme=>document.documentElement.dataset.theme=theme",theme)
                for key in ["mapa","diag","tab","tl","fc","geral"]:
                    self.page.evaluate("key=>chooseMaterial('c',key)",key)
                    self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth<=innerWidth"),f"{width}/{theme}/{key}")
                    self.assertTrue(self.page.locator("#theme-toggle").is_visible())
                    if key=="geral":
                        self.assertTrue(self.page.locator(".operator-overview-table th,.operator-overview-table td").evaluate_all(
                            "nodes=>nodes.every(n=>n.getBoundingClientRect().width>90 && n.scrollWidth<=n.clientWidth+1)"))
                    if width==1440 and key in ["mapa","diag","geral"]:
                        self.page.screenshot(path=f"/tmp/cpa-aula8-{theme}-{key}.png",full_page=True)
                self.page.get_by_role("button",name="Ampliar quadro comparativo",exact=True).click()
                self.assertTrue(self.page.locator("#theme-toggle").is_visible())
                self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth<=innerWidth"))
                self.page.keyboard.press("Escape")

    def set_daily_clock(self, instant="2026-10-13T15:00:00Z"):
        self.page.evaluate("instant=>{Date.now=()=>Date.parse(instant);go()}",instant)

    def finish_daily(self, correct_count=15):
        self.page.evaluate("hoje()")
        ids=self.page.evaluate("qz.ids")
        for index in range(20):
            self.answer(correct=index<correct_count)
            self.click("Próxima" if index<19 else "Ver resultado")
        return ids

    def test_62_daily_prioritizes_unseen_without_changing_lessons_levels_or_filters(self):
        self.set_daily_clock()
        data=self.page.evaluate("""()=>{
            cfg={a:5,as:[],n:3,m:'err',c:5,md:'h',b:0};selectedLessonBlocks[8]=2;fl=3;fm=1;
            const fresh=new Set(AL.flatMap((_,i)=>[0,1,2].map(level=>Q.findIndex(q=>q[0]===i+1&&q[2]===level)+1)));
            H=Q.map((q,i)=>[i+1,1,1700000000000,0]).filter(r=>!fresh.has(r[0]));save();
            const before={filters:JSON.stringify(cfg),reading:JSON.stringify(selectedLessonBlocks),history:JSON.stringify(H),stats:[fl,fm]};
            const plan=dailyPlan();hoje();
            return {before,after:{filters:JSON.stringify(cfg),reading:JSON.stringify(selectedLessonBlocks),history:JSON.stringify(H),stats:[fl,fm]},
                fresh:plan.unseen,ids:qz.ids,levels:[0,1,2].map(level=>qz.ids.filter(id=>Q[id-1][2]===level).length),
                counts:AL.map((_,i)=>qz.ids.filter(id=>Q[id-1][0]===i+1).length)};
        }""")
        self.assertEqual(data['before'],data['after'])
        lesson_count=len(data['counts'])
        self.assertEqual(data['fresh'],sum(min(lesson_count,n) for n in [5,10,5]),
                         'A oferta de inéditas por nível limita a seleção, sem romper a distribuição')
        self.assertEqual(data['levels'],[5,10,5])
        self.assertEqual(len(set(data['ids'])),20)
        base,extra=divmod(20,lesson_count)
        self.assertEqual(sorted(data['counts']),[base]*(lesson_count-extra)+[base+1]*extra)
        self.assertEqual(self.page.evaluate("qz.md"),'e')
        rotations=self.page.evaluate("""()=>Array.from({length:AL.length},(_,i)=>{
            const day=new Date(Date.parse('2026-10-13T12:00:00Z')+i*86400000).toISOString().slice(0,10);
            return dailyPlan(day).groups.filter(g=>g.count>Math.floor(20/AL.length)).map(g=>g.lesson);
        })""")
        for lesson in range(1,lesson_count+1):
            self.assertEqual(sum(lesson in day for day in rotations),extra)

    def test_63_daily_pause_reload_retains_ids_choices_feedback_and_partial_score(self):
        self.page.add_init_script("Date.now=()=>Date.parse('2026-10-13T15:00:00Z')")
        self.set_daily_clock()
        self.click('Começar')
        ids=self.page.evaluate('qz.ids')
        self.click('Dica')
        self.click('Eliminar 2 alternativas')
        options=self.page.evaluate('qz.o')
        eliminated=self.page.evaluate('qz.x')
        self.click('Pausar')
        self.assertEqual(self.page.locator('.hoje').get_attribute('data-daily-state'),'active')
        self.assertEqual(self.page.locator('[data-daily-streak]').inner_text(),'0')
        self.click('Retomar')
        self.assertEqual(self.page.evaluate('qz.ids'),ids)
        self.assertEqual(self.page.evaluate('qz.o'),options)
        self.assertEqual(self.page.evaluate('qz.x'),eliminated)
        wrong=self.page.evaluate('qz.o.findIndex((o,i)=>!o[1]&&!qz.x.includes(i))')
        self.page.locator('button.o').nth(wrong).click()
        feedback=self.page.locator('.fb-option p').all_text_contents()
        history=self.page.evaluate('H')
        self.page.reload()
        self.click('Retomar')
        self.assertEqual(self.page.evaluate('qz.ids'),ids)
        self.assertEqual(self.page.locator('.fb-option p').all_text_contents(),feedback)
        self.assertEqual(self.page.evaluate('qz.rev.length'),1)
        self.assertEqual(self.page.evaluate('H'),history)
        self.click('Próxima')
        self.assertEqual(self.page.evaluate('qz.i'),1)
        self.click('Painel')
        self.click('Retomar')
        self.assertEqual(self.page.evaluate('qz.i'),1)
        self.assertEqual(self.page.evaluate('H'),history)

    def test_64_daily_completion_locks_persists_and_keeps_original_score_after_retry(self):
        self.page.add_init_script("Date.now=()=>Date.parse('2026-10-13T15:00:00Z')")
        self.set_daily_clock()
        ids=self.finish_daily(15)
        self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'15 de 20 (75%)')
        self.click('Ver painel')
        self.assertEqual(self.page.locator('[data-daily-score]').inner_text(),'75%')
        self.assertTrue(self.page.get_by_role('button',name='Concluído hoje',exact=True).is_disabled())
        self.assertEqual(self.page.locator('[data-daily-streak]').inner_text(),'1')
        history=self.page.evaluate('H')
        self.page.evaluate('hoje();hoje()')
        self.assertEqual(self.page.evaluate('H'),history)
        self.assertEqual(self.page.locator('.hoje').get_attribute('data-daily-state'),'complete')
        self.page.reload()
        self.assertEqual(self.page.locator('[data-daily-score]').inner_text(),'75%')
        self.click('Ver resultado')
        self.assertEqual(self.page.evaluate('qz.ids'),ids)
        self.click('Refazer erros desta sessão')
        self.assertTrue(self.page.evaluate('!qz.dailyId'))
        self.finish(count=5)
        self.click('Ver painel')
        self.assertEqual(self.page.locator('[data-daily-score]').inner_text(),'75%')
        self.assertEqual(self.page.evaluate("Object.keys(dailyBook.results)"),['2026-10-13'])

    def test_65_daily_rollover_streak_and_midnight_completion_use_brasilia(self):
        self.set_daily_clock('2026-10-13T02:59:59Z')
        self.assertEqual(self.page.evaluate('dailyDate()'),'2026-10-12')
        self.finish_daily(20)
        # Keep the completed result open: it must not be recorded again tomorrow.
        self.set_daily_clock('2026-10-13T03:00:00Z')
        self.click('Painel')
        self.assertEqual(self.page.locator('.hoje').get_attribute('data-daily-state'),'ready')
        self.assertEqual(self.page.evaluate('Object.keys(dailyBook.results)'),['2026-10-12'])
        self.finish_daily(18)
        self.assertEqual(self.page.evaluate('dailyStreak()'),{'current':2,'best':2})
        self.set_daily_clock('2026-10-15T15:00:00Z')
        self.assertEqual(self.page.evaluate('dailyStreak()'),{'current':0,'best':2})
        self.finish_daily(17)
        self.assertEqual(self.page.evaluate('dailyStreak()'),{'current':1,'best':2})
        self.set_daily_clock('2026-10-17T02:50:00Z')
        self.page.evaluate('hoje()')
        self.assertEqual(self.page.evaluate('qz.dailyStartDay'),'2026-10-16')
        self.set_daily_clock('2026-10-17T03:10:00Z')
        for i in range(20):
            self.answer()
            self.click('Próxima' if i<19 else 'Ver resultado')
        self.assertNotIn('2026-10-16',self.page.evaluate('Object.keys(dailyBook.results)'))
        self.assertIn('2026-10-17',self.page.evaluate('Object.keys(dailyBook.results)'))
        self.assertEqual(self.page.evaluate('dailyStreak()'),{'current':1,'best':2})

    def test_66_daily_consecutive_days_change_questions_and_refresh_the_open_panel(self):
        self.set_daily_clock()
        first=self.finish_daily(20)
        self.click('Ver painel')
        self.page.evaluate("Date.now=()=>Date.parse('2026-10-14T03:00:00Z');refreshDailyCalendar()")
        self.assertEqual(self.page.locator('.hoje').get_attribute('data-daily-state'),'ready')
        self.click('Começar')
        second=self.page.evaluate('qz.ids')
        self.assertTrue(set(first).isdisjoint(second))
        self.page.evaluate('view="d";go();hoje()')
        self.assertEqual(self.page.evaluate('qz.ids'),second)
        self.assertEqual(self.page.evaluate('qz.i'),0)

    def test_67_evolution_preserves_all_days_modes_and_undated_records(self):
        history=self.page.evaluate("""()=>{
            H=Array.from({length:400},(_,i)=>[1,i%2,Date.parse('2025-01-01T15:00:00Z')+i*86400000,i%3]);
            H.push([1,1],[2,0,0,0],[3,1,'2024-12-31',0],[4,0,'2024-12-31T18:00:00Z',1],[5,1,1e99,0]);
            save();go();return H;
        }""")
        points=self.page.locator('[data-evolution-day]')
        self.assertEqual(points.count(),401)
        self.assertEqual(points.first.get_attribute('data-evolution-day'),'2024-12-31')
        self.assertEqual(points.first.get_attribute('data-evolution-percent'),'50')
        self.assertTrue(points.evaluate_all("nodes=>nodes.every(n=>n.querySelector('text').textContent.endsWith('%'))"))
        self.assertIn('3 respostas · 67%',self.page.locator('[data-evolution-undated]').inner_text())
        self.assertTrue(self.page.locator('#evolution-scroll').evaluate('n=>n.scrollWidth>n.clientWidth'))
        self.click('Início do histórico')
        self.assertEqual(self.page.locator('#evolution-scroll').evaluate('n=>n.scrollLeft'),0)
        self.click('Mais recente')
        self.assertGreater(self.page.locator('#evolution-scroll').evaluate('n=>n.scrollLeft'),1000)
        self.click('Estatísticas')
        self.click('Hardcore')
        self.click('Simulado')
        self.click('Painel')
        self.assertEqual(self.page.locator('[data-evolution-day]').count(),401)
        self.assertEqual(self.page.evaluate('H'),history)

    def test_68_daily_and_long_evolution_fit_pc_and_theme_switch_keeps_state(self):
        self.set_daily_clock()
        self.finish_daily(14)
        self.click('Ver painel')
        self.page.evaluate("H.push(...Array.from({length:90},(_,i)=>[1,i%2,Date.parse('2026-01-01T15:00:00Z')+i*86400000,0]));save();go()")
        state=self.page.evaluate('({history:H,daily:JSON.stringify(dailyBook)})')
        for width in [1024,1280,1440,1920]:
            self.page.set_viewport_size({'width':width,'height':1000})
            for theme in ['light','dark']:
                self.page.evaluate('theme=>document.documentElement.dataset.theme=theme',theme)
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                self.assertTrue(self.page.locator('.hoje').evaluate('n=>n.scrollWidth<=n.clientWidth+1'))
                self.page.locator('#theme-toggle').click()
                self.assertEqual(self.page.evaluate('({history:H,daily:JSON.stringify(dailyBook)})'),state)
                if width==1440:
                    self.page.evaluate('theme=>document.documentElement.dataset.theme=theme',theme)
                    self.page.screenshot(path=f'/tmp/cpa-checkpoint-evolucao-{theme}.png',full_page=True)

    def test_69_daily_shared_tabs_resume_instead_of_starting_a_second_test(self):
        self.page.add_init_script("Date.now=()=>Date.parse('2026-10-13T15:00:00Z')")
        self.set_daily_clock()
        self.click('Começar')
        ids=self.page.evaluate('qz.ids')
        other=self.context.new_page()
        other.add_init_script("Date.now=()=>Date.parse('2026-10-13T15:00:00Z')")
        other.goto(self.url)
        other.get_by_role('button',name='Retomar',exact=True).click()
        self.assertEqual(other.evaluate('qz.ids'),ids)
        self.answer()
        other.wait_for_function('qz.rev.length===1')
        self.assertEqual(other.locator('.fb-option').count(),4)
        self.assertEqual(other.evaluate('H.length'),1)
        self.page.locator('button.chip.on').filter(has_text='Próxima').click()
        for i in range(1,20):
            self.answer()
            self.click('Próxima' if i<19 else 'Ver resultado')
        other.wait_for_function("document.querySelector('.hoje')?.dataset.dailyState==='complete'")
        self.assertTrue(other.get_by_role('button',name='Concluído hoje',exact=True).is_disabled())
        self.assertEqual(other.evaluate('H.length'),20)
        other.close()

    def test_70_daily_storage_failures_and_malformed_book_keep_the_app_usable(self):
        self.page.add_init_script("localStorage.setItem('cpaDaily','{malformed');localStorage.setItem('cpaH','[[1,1,1700000000000,0]]')")
        self.page.reload()
        self.assertEqual(self.page.evaluate('H'),[[1,1,1700000000000,0]])
        self.assertEqual(self.page.locator('.hoje').get_attribute('data-daily-state'),'ready')
        self.page.evaluate("()=>{Storage.prototype.setItem=()=>{throw Error('unavailable')};Storage.prototype.getItem=()=>{throw Error('unavailable')}}")
        self.finish_daily(20)
        self.click('Ver painel')
        self.assertEqual(self.page.locator('[data-daily-score]').inner_text(),'100%')
        self.assertTrue(self.page.get_by_role('button',name='Concluído hoje',exact=True).is_disabled())

    def test_71_daily_cloud_progress_merges_completed_dates_without_losing_history(self):
        self.set_daily_clock()
        self.finish_daily(15)
        remote=self.page.evaluate('({h:JSON.stringify(H),daily:JSON.stringify(dailyBook)})')
        history=json.loads(remote['h'])
        self.page.add_init_script("""
            Date.now=()=>Date.parse('2026-10-13T15:00:00Z');
            const mockData="""+json.dumps(remote)+""";
            window.mockWrites=[];
            window.claude={use:async kind=>kind==='user'?{id:async()=> 'test-user'}:{doc:()=>({
                get:async()=>({exists:true,data:()=>mockData}),
                set:async payload=>{window.mockWrites.push(payload)}
            })}};
        """)
        self.page.evaluate("""()=>{
            localStorage.setItem('cpaH','[]');
            localStorage.setItem('cpaDaily',JSON.stringify({version:1,active:null,lastResult:null,results:{
                '2026-10-12':{n:20,ok:17,end:Date.parse('2026-10-12T15:00:00Z'),dailyId:'old-checkpoint'}
            }}));
        }""")
        self.page.reload()
        self.page.get_by_text('Progresso salvo na sua conta.',exact=False).wait_for()
        self.assertEqual(self.page.evaluate('H'),history)
        self.assertEqual(self.page.evaluate("Object.keys(dailyBook.results).sort()"),['2026-10-12','2026-10-13'])
        self.assertEqual(self.page.locator('[data-daily-score]').inner_text(),'75%')
        self.assertEqual(self.page.locator('[data-daily-streak]').inner_text(),'2')
        self.assertEqual(self.page.evaluate("JSON.parse(localStorage.getItem('cpaH'))"),history)
        self.page.evaluate('sync()')
        self.page.wait_for_function('window.mockWrites.length>0')
        writes=self.page.evaluate('window.mockWrites')
        for payload in writes:
            self.assertEqual(json.loads(payload['h']),history)
            self.assertEqual(sorted(json.loads(payload['daily'])['results']),['2026-10-12','2026-10-13'])


    def test_72_lesson9_blocks_keep_open_sections_and_complete_source_materials(self):
        self.click("Trilha")
        self.page.locator("button.tb").nth(8).click()
        for selector in ["#lesson-summary","#lesson-tips","#lesson-traps"]:
            self.page.locator(selector+" summary").click()
        state=self.page.evaluate("({history:H,practice:JSON.stringify(cfg)})")
        for block,title in [(1,"1. Autorreguladores"),(2,"2. FGC e FGCoop"),(3,"3. Liberdade Econômica")]:
            self.page.locator(f'.lesson-content-filter [data-lesson-block="{block}"]').click()
            self.assertEqual(self.page.evaluate("lessonContent(9).t"),title)
            for key,selector in [("r","#lesson-summary"),("d","#lesson-tips"),("p","#lesson-traps")]:
                self.assertTrue(self.page.locator(selector).evaluate("node=>node.open"))
                expected=self.page.evaluate("key=>lessonContent(9)[key].map(x=>x.replace(/\\{\\{(?:atencao|negacao)\\|([^{}]+)\\}\\}/g,'$1').replace(/\\*\\*/g,''))",key)
                self.assertEqual(self.page.locator(selector+" .pt").all_text_contents(),expected)
        self.page.locator(".hero").get_by_role("button",name="Material de apoio",exact=True).click()
        for block in [1,2,3,0]:
            self.page.locator(f'.lesson-blocks [data-lesson-block="{block}"]').click()
            for kind in ["Mapa mental","Diagramas","Tabelas","Linha do tempo","Flashcards"]:
                self.click(kind)
                self.assert_material_content(kind)
                if kind=="Flashcards":
                    self.page.locator("#flashcard").click()
                    self.assertTrue(self.page.locator("#flashcard").evaluate("n=>n.classList.contains('is-answer')"))
                    face=self.page.locator(".flashcard-text").inner_text()
                    self.page.locator("#theme-toggle").click()
                    self.assertEqual(self.page.locator(".flashcard-text").inner_text(),face)
        self.assertEqual(self.page.evaluate("({history:H,practice:JSON.stringify(cfg)})"),state)

    def test_73_lesson9_feedback_modes_and_balanced_practice_integrate_with_old_history(self):
        self.page.evaluate("H=[[1,1,1700000000000,0],[800,0,1700000000001,2]];save()")
        history=self.page.evaluate('H')
        for mode,ids in [("e",[801,862,897]),("h",[847,885,900]),("s",[821,855,895])]:
            self.page.evaluate("args=>begin(args[1],args[0])",[mode,ids])
            for index in range(3):
                self.assertEqual(self.page.locator('.feedback').count(),0)
                if '\nI. ' in self.page.evaluate('Q[qz.ids[qz.i]-1][3]'):
                    self.assertEqual(self.page.locator('.en .statement-label').all_text_contents(),["I.","II.","III.","IV."])
                self.answer(correct=index!=1)
                if mode=='s':
                    self.assertEqual(self.page.locator('.feedback').count(),0)
                else:
                    question=self.page.evaluate('Q[qz.ids[qz.i]-1]')
                    for row in self.page.locator('.fb-option').all():
                        self.assertEqual(row.locator('p').inner_text(),question[11][int(row.get_attribute('data-option-index'))])
                if mode!='s':
                    self.click('Próxima' if index<2 else 'Ver resultado')
            self.assertEqual(self.page.locator('.session-result').count(),1)
            self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'2 de 3 (67%)')
        self.assertEqual(self.page.evaluate('H.slice(0,2)'),history)
        for mode in ['e','s','h']:
            self.page.evaluate("mode=>{qz=null;cfg={a:9,as:[],n:-1,m:'all',c:20,md:mode,b:0}}",mode)
            result=self.page.evaluate("()=>{const ids=mix();return {ids,levels:ids.map(id=>Q[id-1][2]),lessons:ids.map(id=>Q[id-1][0])}}")
            self.assertEqual(len(set(result['ids'])),20)
            self.assertEqual(set(result['lessons']),{9})
            self.assertEqual([result['levels'].count(i) for i in range(4)],[0,0,0,20] if mode=='h' else [5,10,5,0])

    def test_74_lesson9_overview_and_materials_fit_pc_in_both_themes(self):
        self.page.evaluate("mt.a=9;view='m';go()")
        self.click('Quadro geral')
        self.assertEqual(self.page.locator('.operator-overview-table tbody tr').count(),7)
        self.assertEqual(self.page.locator('.operator-overview-table thead th').all_text_contents(),
                         ['Item / natureza','Função','Âmbito','Vínculo','Instrumentos','Limites e condições','Observações'])
        for block,count in [(1,4),(2,2),(3,1),(0,7)]:
            self.page.locator(f'[data-overview-block="{block}"]').click()
            self.assertEqual(self.page.locator('.operator-overview-table tbody tr').count(),count)
            self.assertEqual(self.page.evaluate('selectedLessonBlocks[9]'),block)
        for width in [1024,1280,1440,1920]:
            self.page.set_viewport_size({'width':width,'height':1000})
            for theme in ['light','dark']:
                self.page.evaluate('theme=>document.documentElement.dataset.theme=theme',theme)
                for key in ['mapa','diag','tab','tl','fc','geral']:
                    self.page.evaluate("key=>chooseMaterial('c',key)",key)
                    self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'{width}/{theme}/{key}')
                    self.assertTrue(self.page.locator('#theme-toggle').is_visible())
                    if width==1440 and key in ['mapa','geral']:
                        self.page.screenshot(path=f'/tmp/cpa-aula9-{theme}-{key}.png',full_page=True)
                self.page.get_by_role('button',name='Ampliar quadro comparativo',exact=True).click()
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                self.page.keyboard.press('Escape')


    def test_75_revised_questions_render_independent_context_in_all_modes(self):
        self.page.evaluate("H=[[1,1,1700000000000,0],[800,0,1700000000001,2]];save()")
        history=self.page.evaluate('H')
        for theme in ['light','dark']:
            self.page.evaluate('theme=>document.documentElement.dataset.theme=theme',theme)
            for mode,ids in [('e',[808,732,880]),('h',[747,888]),('s',[808,732,788,880])]:
                self.page.evaluate('args=>begin(args[1],args[0])',[mode,ids])
                for index,id in enumerate(ids):
                    expected=self.page.evaluate('id=>questionDisplay(Q[id-1]).stem',id)
                    actual=self.page.locator('.en').inner_text()
                    self.assertEqual(re.sub(r'\s+',' ',actual).strip(),re.sub(r'\s+',' ',expected).strip())
                    self.assertNotRegex(actual,r'(?i)\baula\b|\bslide\b|conteúdo enviado')
                    self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                    if id==808 and mode=='e':
                        self.assertIn('cumprimento obrigatório',actual)
                        self.page.locator('button.o').filter(has_text='Programa educacional.').click()
                        self.assertIn('capacita profissionais',self.page.locator('.fb-option[data-option-index="3"] p').inner_text())
                        self.page.screenshot(path=f'/tmp/cpa-enunciado808-{theme}.png',full_page=True)
                    else:
                        self.answer()
                    if mode=='s':
                        self.assertEqual(self.page.locator('.feedback').count(),0)
                    else:
                        question=self.page.evaluate('id=>Q[id-1]',id)
                        for row in self.page.locator('.fb-option').all():
                            self.assertEqual(row.locator('p').inner_text(),question[11][int(row.get_attribute('data-option-index'))])
                        self.click('Próxima' if index<len(ids)-1 else 'Ver resultado')
                self.assertEqual(self.page.locator('.session-result').count(),1)
        self.assertEqual(self.page.evaluate('H.slice(0,2)'),history)


    def test_76_feedback_explains_selected_original_option_after_shuffle(self):
        self.page.evaluate("H=[[1,1,1700000000000,0],[836,0,1700000000001,1]];save()")
        history=self.page.evaluate('H')
        for theme in ['light','dark']:
            self.page.evaluate('theme=>document.documentElement.dataset.theme=theme',theme)
            self.page.evaluate("begin([828,836,829,742,261],'e')")
            for index,id in enumerate([828,836,829,742,261]):
                question=self.page.evaluate('id=>Q[id-1]',id)
                expected=self.page.evaluate('id=>questionDisplay(Q[id-1]).options[id===836?1:0]',id)
                self.page.locator('button.o').filter(has_text=expected).click()
                for row in self.page.locator('.fb-option').all():
                    original=int(row.get_attribute('data-option-index'))
                    self.assertEqual(row.locator('p').inner_text(),question[11][original])
                if id==836:
                    row=self.page.locator('.fb-option[data-option-index="1"]')
                    self.assertIn('Sua resposta',row.inner_text())
                    self.assertIn('APIMEC',row.inner_text())
                    self.assertIn('avaliação técnica',row.inner_text())
                    self.page.screenshot(path=f'/tmp/cpa-feedback836-{theme}.png',full_page=True)
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                self.click('Próxima' if index<4 else 'Ver resultado')
            self.assertEqual(self.page.locator('.session-result').count(),1)
            self.page.evaluate("begin([836],'s')")
            self.answer()
            self.assertEqual(self.page.locator('.feedback').count(),0)
        self.assertEqual(self.page.evaluate('H.slice(0,2)'),history)

if __name__ == "__main__":
    unittest.main(verbosity=2)
