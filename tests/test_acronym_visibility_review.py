"""Revisão de exceções: nome por extenso não deve sumir sem revelar o gabarito."""
import hashlib
import json
from pathlib import Path
import unittest
import smoke as harness

ROOT=Path(__file__).resolve().parents[1]
REPORT=json.loads((ROOT/'docs/revisao-exibicao-siglas-2026-10-19.json').read_text())

class AcronymVisibility(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    answer=harness.PainelCPA.answer
    click=harness.PainelCPA.click

    def test_banks_keep_their_original_texts_answers_and_feedbacks(self):
        for bank in ['Q','BP']:
            value=self.page.evaluate(bank+'.slice(0,'+str(REPORT["contagens"]["questoes_regulares"] if bank=="Q" else REPORT["contagens"]["bate_pronto"])+')')
            digest=hashlib.sha256(json.dumps(value,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
            self.assertEqual(digest,REPORT['integridade'][bank+'_sha256'])

    def test_lfl_is_expanded_before_answer_in_both_themes_and_all_entry_modes(self):
        for theme in ['light','dark']:
            for mode in ['e','s','h']:
                self.page.evaluate('x=>{document.documentElement.dataset.theme=x.theme;begin([967],x.mode)}',dict(theme=theme,mode=mode))
                self.assertIn('LFL (Linhas Financeiras de Liquidez)',self.page.locator('.en').inner_text())
                self.assertEqual(self.page.locator('.en .acronym-expansion').count(),1)
                self.assertEqual(self.page.locator('.fb-option').count(),0)
                choice=self.page.evaluate('qz.o.find(o=>!o[1])[0]')
                self.answer(correct=False)
                self.assertEqual(self.page.evaluate('qz.rev[0][2]'),choice)
                if mode!='s':
                    for row in self.page.locator('.fb-option').all():
                        index=int(row.get_attribute('data-option-index'))
                        self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('i=>Q[966][11][i]',index))
                    self.click('Ver resultado')
                self.page.locator('details.rv summary').click()
                self.assertIn('LFL (Linhas Financeiras de Liquidez)',self.page.locator('details.rv').inner_text())
                self.assertEqual(self.page.evaluate('H.at(-1)[0]'),967)

    def test_census_of_all_1500_items_has_no_unexplained_missing_definition(self):
        data=self.page.evaluate('''()=>{
          const raw=JSON.stringify([Q,BP]),h=JSON.stringify(H),rows=[...Q.slice(0,1000).map((q,i)=>({id:i+1,q})),...BP_Q.slice(0,500).map((q,i)=>({id:100001+i,q}))];
          return {rows:rows.map(({id,q})=>{const d=questionDisplay(q),after=questionDisplay(q,true),names=new Map();
            for(const text of [q[3],...questionOptions(q).map(o=>o[0])])for(const m of text.matchAll(new RegExp(acronymPattern,'giu'))){const e=acronymAliases.get(m[1].toLocaleLowerCase('pt-BR'));names.set(e.id,acronymMeaning(e,q));}
            return {id,names:[...names],deferred:d.deferred,text:d.stem+' '+d.options.join(' '),after:after.stem+' '+after.options.join(' ')};
          }),unchanged:raw===JSON.stringify([Q,BP])&&h===JSON.stringify(H),guards:QUESTION_ACRONYM_CLUES.filter(id=>id<=1000||id>100000&&id<=100500)};
        }''')
        self.assertTrue(data['unchanged']);self.assertEqual(len(data['rows']),1500)
        self.assertEqual(sum(bool(r['names']) for r in data['rows']),940)
        self.assertEqual(data['guards'],REPORT['excecoes_depois'])
        released={r['id'] for r in REPORT['adiamentos_removidos']}
        self.assertEqual(len(released),32)
        for row in data['rows']:
            for key,name in row['names']:
                if key not in row['deferred']:self.assertIn(name,row['text'],f"{row['id']} / {key}")
                else:self.assertIn(name,row['after'],f"Definição ausente após resposta: {row['id']}")
            if row['id'] in released:self.assertFalse(row['deferred'],row['id'])

    def test_safe_deadlines_and_collateral_expand_while_answer_clues_stay_deferred(self):
        for id in [967,977,978,980,981,982,988,999,100494,100495,100496,100497,100498,100499,100500]:
            d=self.page.evaluate('id=>questionDisplay(questionById(id))',id)
            self.assertFalse(d['deferred'],id)
            self.assertIn('(',d['stem']+' '.join(d['options']))
        for id in [944,961,986,100476,100486]:
            before=self.page.evaluate('id=>questionDisplay(questionById(id))',id)
            self.assertTrue(before['deferred'],id)
            self.assertNotEqual(before,self.page.evaluate('id=>questionDisplay(questionById(id),true)',id))
        self.page.evaluate('begin([100494],"b")')
        self.assertIn('LLI (Linha de Liquidez Imediata)',self.page.locator('.en').inner_text())
        self.answer();self.assertEqual(self.page.locator('.fb-option').count(),2)

if __name__=='__main__':unittest.main(verbosity=2)
