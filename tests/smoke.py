"""Testes dos fluxos do HTML importado, usando um navegador real."""

import os
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
        self.assertEqual(len(data), 600)
        self.assertEqual([sum(q[0] == lesson for q in data) for lesson in range(1, 7)], [100] * 6)
        self.assertEqual([sum(q[2] == level for q in data) for level in range(4)], [120, 240, 120, 120])
        for q in data:
            self.assertTrue(all(isinstance(value, str) and value.strip() for value in q[3:9]))
        self.assertEqual(self.page.locator(".g4 .mv").all_text_contents(), ["0", "0", "0", "0%"])
        self.assertIn("480 questões da prova e 120 hardcore, 600 nunca respondidas", self.page.locator("#app").inner_text())

    def test_02_navigation_and_all_materials(self):
        self.click("Quadro do SFN")
        self.assertIn("Banco Central do Brasil", self.page.locator("#app").inner_text())
        self.click("Trilha")
        for lesson in range(1, 7):
            self.page.locator("button.tb").nth(lesson - 1).click()
            self.assertIn(f"Aula {lesson} de 6", self.page.locator(".hero").inner_text())
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
        self.finish()

    def test_04_simulation_and_review(self):
        self.configure("Simulado")
        self.assertEqual(self.page.locator(".aj").count(), 0)
        self.answer(correct=False)
        self.assertIn("questão 2 de 5", self.page.locator(".tb2").inner_text())
        self.assertEqual(self.page.locator("button.o.ok").count(), 0)
        for _ in range(4):
            self.answer()
        self.assertIn("4 de 5 (80%)", self.page.locator("#app").inner_text())
        self.assertEqual(self.page.locator("details.rv").count(), 1)
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
