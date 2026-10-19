"""Casos em que iniciais ou nomes por extenso substituíam conhecimento financeiro."""
import copy
import json
from pathlib import Path
import re
import unittest
from validate_bank import load_questions
from question_revision import questions_before_clue_revision,bate_pronto_before_clue_revision
import smoke as harness

ROOT=Path(__file__).resolve().parents[1]
def bp_bank():return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split('const BP=',1)[1])[0]

class ClueContent(unittest.TestCase):
    def test_four_rewrites_are_traced_without_changing_pools_or_history_ids(self):
        q=load_questions();old=questions_before_clue_revision(q)
        bp=bp_bank();oldbp=bate_pronto_before_clue_revision(bp)
        changed=[i for i,(a,b) in enumerate(zip(old,q),1) if a!=b]
        changedbp=[i for i,(a,b) in enumerate(zip(oldbp,bp),100001) if a!=b]
        self.assertEqual(changed,[753]);self.assertEqual(changedbp,[100379,100394,100445])
        for a,b in zip(old,q):self.assertEqual(a[:3]+[a[9]],b[:3]+[b[9]])
        for a,b in zip(oldbp,bp):self.assertEqual(a[:2]+[a[7]],b[:2]+[b[7]])
        report=json.loads((ROOT/'docs/revisao-pistas-siglas.json').read_text())
        self.assertEqual(len(report['expansao_adiada']),56)
        self.assertEqual(sum(a[11][i]!=b[11][i] for a,b in zip(old,q) for i in range(4)),4)
        self.assertEqual(sum(a[i]!=b[i] for a,b in zip(oldbp,bp) for i in [5,6]),6)
        bad=copy.deepcopy(q);bad[752][4]='Outra resposta'
        with self.assertRaises(AssertionError):questions_before_clue_revision(bad)

    def test_rdc_now_tests_combined_guarantee_not_its_initials(self):
        r=bp_bank()[444]
        self.assertIn('mesma cooperativa',r[2]);self.assertIn('FGCoop',r[2])
        self.assertEqual(r[3:5],['Sim, considerando os créditos elegíveis','Não, cada produto tem limite próprio'])
        for text in r[5:7]:
            self.assertIn('R$ 250 mil',text);self.assertIn('beneficiário',text)
        self.assertNotIn('Recibo de Depósito Cooperativo',r[3])
        self.assertIn('fundos disponíveis',bp_bank()[378][3])
        self.assertIn('preços continuam sujeitos',bp_bank()[393][3])

    def test_no_current_bare_acronym_question_asks_only_its_expansion(self):
        entries=json.loads((ROOT/'docs/siglas-questoes.json').read_text())['entradas']
        for r,si,oi in [(r,3,4) for r in load_questions()]+[(r,2,3) for r in bp_bank()]:
            stem=r[si]
            if not re.search(r'\bsigla\b|\bsignifica\b|^\w+ é:',stem,re.I):continue
            for e in entries:
                if not any(re.search(r'(?<!\w)'+re.escape(a)+r'(?!\w)',stem,re.I) for a in e['aliases']):continue
                self.assertNotIn(r[oi].strip('.').lower(),[name.lower() for name in [e['name']]+e['variants']],stem)

class ClueBrowser(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    answer=harness.PainelCPA.answer

    def test_all_editorial_guards_show_definitions_only_after_answer(self):
        ids=self.page.evaluate('QUESTION_ACRONYM_CLUES')
        historical=json.loads((ROOT/'docs/revisao-pistas-siglas.json').read_text())['expansao_adiada']
        authored=json.loads((ROOT/'docs/aula-10-cobertura.json').read_text())['siglas_adiadas']
        correction=json.loads((ROOT/'docs/revisao-exibicao-siglas-2026-10-19.json').read_text())
        removed={r['id'] for r in correction['adiamentos_removidos']}
        self.assertEqual(ids,sorted(set(historical+authored)-removed))
        result=self.page.evaluate('''()=>{
          const seen=[];
          for(const id of QUESTION_ACRONYM_CLUES){
            const q=questionById(id),mode=q[12]==='b'?'b':q[2]===3?'h':'e';begin([id],mode);
            if(document.querySelector('.acronym-expansion'))throw Error('Pista antes de responder '+id);
            if(document.querySelector('.fb-option'))throw Error('Feedback antecipado '+id);
            const original=qz.o.findIndex(o=>o[1]);pick(original);
            if(!document.querySelector('.en .acronym-expansion,.answer-text .acronym-expansion'))throw Error('Expansão não foi mostrada '+id);
            for(const row of document.querySelectorAll('.fb-option')){
              if(row.querySelector('p').textContent!==q[11][Number(row.dataset.optionIndex)])throw Error('Feedback trocado '+id);
            }
            if(qz.rev[0][2]!==q[4])throw Error('Histórico alterado '+id);
            seen.push(id);
          }return seen;
        }''')
        self.assertEqual(result,ids)

    def test_rdc_and_rewritten_questions_keep_safe_expansions_and_both_feedbacks(self):
        for id in [753,100379,100394,100445]:
            self.page.evaluate('id=>begin([id],id>100000?"b":"e")',id)
            self.assertGreater(self.page.locator('.acronym-expansion').count(),0)
            stem=self.page.locator('.en').inner_text()
            answers=self.page.locator('button.o .answer-text').all_inner_texts()
            if id==100445:
                self.assertIn('RDC (Recibo de Depósito Cooperativo)',stem)
                self.assertNotIn('Recibo de Depósito Cooperativo',' '.join(answers))
                self.assertIn('Sim, considerando os créditos elegíveis',' '.join(answers))
            self.answer(correct=False)
            self.assertEqual(self.page.locator('.fb-option').count(),2 if id>100000 else 4)
            for row in self.page.locator('.fb-option').all():
                i=int(row.get_attribute('data-option-index'))
                self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('x=>questionById(x.id)[11][x.i]',dict(id=id,i=i)))

if __name__=='__main__':unittest.main(verbosity=2)
