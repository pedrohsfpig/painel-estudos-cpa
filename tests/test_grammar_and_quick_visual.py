"""Pistas gramaticais reconhecidas e isolamento visual do Bate-pronto.

A verificação lexical sinaliza padrões conhecidos; não certifica todo o português.
"""
import copy
import json
from pathlib import Path
import re
import unittest
from validate_bank import load_questions
from question_revision import questions_before_grammar_revision,bate_pronto_before_grammar_revision,questions_before_numeric_revision,bate_pronto_before_numeric_revision,digest
import smoke as harness

ROOT=Path(__file__).resolve().parents[1]
def bank():return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split('const BP=',1)[1])[0]
# Gênero do nome/expressão institucional, não inferência pela última letra.
FEMININE={'cvm','comoc','susep','previc','casa','receita','fazenda','previdência','secretaria-executiva','secretaria','diretoria','comissão','presidência','superintendência','planejar','apimec','anbima','coordenação','primeira','reunião','liquidez','impressão','depositária','administradora','disponibilidade','carência','guarda','iniciação','área','instituição','letra','autarquia','empresa','sociedade','fundação','operação','ação','cota','apólice','diferença','taxa'}
MASCULINE={'cmn','copom','cnsp','cnpc','bc','bcb','bacen','banco','bndes','ministério','ministro','congresso','senado','tesouro','secretário-executivo','secretário','presidente','diário','emissor','consorciado','vínculo','saldo','scr','spi','spread','compulsório','mercado','terceiro','primeiro'}
def forced_gender_hint(stem,options):
    pattern=r'\b(pelo|pela|pelos|pelas|do|da|dos|das|no|na|nos|nas|ao|aos|à|às)\s*(?::|\?|$|_{3,})'
    match=re.search(pattern,stem,re.I)
    if not match:match=re.search(r'\b(?:é|são|seria|seriam)\s+(o|a|os|as|um|uma|uns|umas)\s*[:?]?$',stem,re.I)
    if not match:return False
    expected='f' if match[1].lower() in {'pela','pelas','da','das','na','nas','à','às','a','as','uma','umas'} else 'm'
    def gender(option):
        word=option.strip().split()[0].strip('.,;:').lower()
        if word in FEMININE or word in {'a','as','uma','umas'}:return 'f'
        if word in MASCULINE or word in {'o','os','um','uns'}:return 'm'
    genders=[gender(o) for o in options]
    return expected in genders and any(g and g!=expected for g in genders)

class GrammarTests(unittest.TestCase):
    def test_detector_flags_the_real_examples_and_accepts_neutral_prompts(self):
        self.assertTrue(forced_gender_hint('Assinaturas nas atas são colhidas pela:',['Secretaria-Executiva','Senado']))
        self.assertTrue(forced_gender_hint('Redesconto é oferecido pelo:',['Banco Central','CVM']))
        self.assertFalse(forced_gender_hint('Quem colhe as assinaturas nas atas do CMN?',['Secretaria-Executiva','Senado']))
        self.assertFalse(forced_gender_hint('Susep é vinculada ao Ministério:',['Da Fazenda','Da Previdência Social']))
        for i,q in enumerate(load_questions(),1):self.assertFalse(forced_gender_hint(q[3],q[4:8]),i)
        for i,b in enumerate(bank(),100001):self.assertFalse(forced_gender_hint(b[2],b[3:5]),i)

    def test_review_counts_stable_ids_and_all_non_stem_fields_are_preserved(self):
        live=load_questions();q=questions_before_numeric_revision(live);before=questions_before_grammar_revision(live)
        bp=bate_pronto_before_numeric_revision(bank());previous=bate_pronto_before_grammar_revision(bank())
        report=json.loads((ROOT/'docs/revisao-pistas-gramaticais.json').read_text());c=report['contagens']
        self.assertEqual(c['enunciados_principais_alterados'],sum(a!=b for a,b in zip(before,q)))
        self.assertEqual(c['enunciados_bate_pronto_alterados'],sum(a!=b for a,b in zip(previous,bp)))
        self.assertEqual(c['questoes_revisadas'],len(q));self.assertEqual(c['bate_pronto_revisados'],len(bp))
        for a,b,row in zip(before,q,report['questoes']):
            self.assertEqual(a[:3]+a[4:],b[:3]+b[4:]);self.assertEqual(digest(b),row['hash_depois'])
        for a,b in zip(previous,bp):
            self.assertEqual(a[:2]+a[3:],b[:2]+b[3:]);self.assertLessEqual(len(b[2].split()),12)
        mutant=copy.deepcopy(q);mutant[93][3]='É competência do:'
        with self.assertRaises(AssertionError):questions_before_grammar_revision(mutant)

    def test_gap_agreement_and_known_subjects_do_not_reveal_or_change_answers(self):
        rows=bank();self.assertIn('Quem colhe',rows[94][2])
        self.assertEqual(rows[94][3:5],['Secretaria-Executiva','Senado'])
        self.assertIn('descontar _____',rows[40][2]);self.assertNotIn('abatidos',rows[40][2])
        self.assertIn('operação de _____',rows[266][2])
        self.assertEqual(rows[266][3:5],['Captação','Aplicação'])
        self.assertEqual(sum('____' in r[2] for r in rows),61)

class QuickVisualTests(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click

    def test_two_equal_cards_large_prompt_and_feedback_binding_in_both_themes(self):
        for theme in ['light','dark']:
            self.page.evaluate('theme=>{document.documentElement.dataset.theme=theme;cfg.md="b";begin([100095,100041],"b")}',theme)
            self.assertEqual(self.page.locator('.quick-round').count(),1)
            self.assertEqual(self.page.locator('.quick-answer').count(),2)
            self.assertEqual(self.page.locator('.fb-option').count(),0)
            self.assertGreaterEqual(self.page.locator('.question-stem').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)'),27)
            cards=self.page.locator('.quick-answer').evaluate_all('es=>es.map(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {x:r.x,y:r.y,w:r.width,h:r.height,bg:s.backgroundColor,border:s.borderColor}})')
            self.assertEqual(cards[0]['y'],cards[1]['y']);self.assertGreater(cards[1]['x'],cards[0]['x'])
            self.assertAlmostEqual(cards[0]['w'],cards[1]['w'],delta=1);self.assertEqual(cards[0]['h'],cards[1]['h'])
            self.assertEqual(cards[0]['bg'],cards[1]['bg']);self.assertEqual(cards[0]['border'],cards[1]['border'])
            self.page.locator('.quick-answer').filter(has_text='Senado').focus();self.page.keyboard.press('Enter')
            self.assertEqual(self.page.locator('.fb-option').count(),2)
            self.assertEqual(self.page.evaluate('qz.i'),0) # Não avançar antes de ler.
            for row in self.page.locator('.feedback-paired .answer-row').all():
                self.assertLess(row.locator('button.o').bounding_box()['x'],row.locator('.fb-option').bounding_box()['x'])
                original=int(row.locator('.fb-option').get_attribute('data-option-index'))
                self.assertEqual(row.locator('.fb-option p').inner_text(),self.page.evaluate('questionById(100095)[11]')[original])
            self.click('Próxima');self.assertEqual(self.page.locator('.concept-gap').count(),1)

    def test_other_modes_keep_their_existing_presentation(self):
        for mode,id in [('e',544),('h',496),('s',544)]:
            self.page.evaluate('([id,mode])=>begin([id],mode)',[id,mode])
            self.assertEqual(self.page.locator('.quick-round,.quick-answer,.quick-prompt-label').count(),0)
            self.assertEqual(self.page.locator('button.o').count(),4)
            self.assertEqual(self.page.locator('.en').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)'),20)

    def test_desktop_layout_theme_switch_and_reduced_motion_preserve_state(self):
        self.page.evaluate("cfg.md='b';begin([100095,100041],'b')")
        for width in [1024,1280,1440,1920]:
            self.page.set_viewport_size({'width':width,'height':900})
            self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'))
            self.assertEqual(self.page.locator('button.o').count(),2)
        self.page.locator('button.o').first.click();state=self.page.evaluate('({ids:qz.ids,a:qz.a,o:qz.o,rev:qz.rev})')
        self.page.locator('#theme-toggle').click()
        self.assertEqual(self.page.evaluate('({ids:qz.ids,a:qz.a,o:qz.o,rev:qz.rev})'),state)
        self.page.emulate_media(reduced_motion='reduce')
        self.click('Próxima')
        self.assertEqual(self.page.locator('.quick-answer').first.evaluate('e=>getComputedStyle(e).transitionDuration'),'0s')

if __name__=='__main__':unittest.main(verbosity=2)
