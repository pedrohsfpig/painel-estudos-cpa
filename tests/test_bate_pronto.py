"""Banco conceitual rápido e regressões de integração, sem certificação normativa."""
from collections import Counter
import json
from pathlib import Path
import re
import unittest
from validate_bank import load_questions
from final_block import unit_count
import smoke as harness

ROOT=Path(__file__).resolve().parents[1]

def bank():return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split('const BP=',1)[1])[0]

class BateProntoContentTests(unittest.TestCase):
    def test_fifty_per_lesson_with_two_options_and_two_specific_explanations(self):
        rows=bank();lessons={q[0] for q in load_questions()};self.assertEqual(len(rows),sum(25*unit_count() if l==13 else 50 for l in lessons))
        self.assertEqual(Counter(r[0] for r in rows),{l:(25*unit_count() if l==13 else 50) for l in lessons})
        for r in rows:
            self.assertEqual(len(r),8)
            self.assertNotEqual(r[3].lower(),r[4].lower())
            self.assertNotEqual(r[5],r[6]);self.assertTrue(all(r[i].strip() for i in range(1,7)))
            self.assertLessEqual(len(r[2].split()),12)
            self.assertLessEqual(max(len(r[3].split()),len(r[4].split())),10)
            for t in r[2:7]:self.assertNotRegex(t,r'(?i)\b(?:aula|professor|slide|transcrição)\b')

    def test_mixed_gap_and_direct_formats_are_unique_and_referenced(self):
        rows=bank();ledger=json.loads((ROOT/'docs/bate-pronto-banco.json').read_text())['questoes'];normal=load_questions()
        self.assertEqual(len(ledger),len(rows))
        for lesson in sorted({r[0] for r in rows}):
            a=[r for r in rows if r[0]==lesson]
            self.assertEqual(len({r[2] for r in a}),25*unit_count() if lesson==13 else 50)
            self.assertGreater(sum('____' in r[2] for r in a),0)
            if lesson==13:
                source=(ROOT/'index.html').read_text().split('const AL=',1)[1]
                units=json.JSONDecoder().raw_decode(source)[0][12]['b']
                for unit in units:
                    cards=[r for r in a if r[1] in unit['topics']]
                    gaps=sum('____' in r[2] for r in cards)
                    self.assertGreater(gaps,0)
                    self.assertLess(gaps,len(cards))
            else:
                self.assertLess(sum('____' in r[2] for r in a),25)
        for i,(r,record) in enumerate(zip(rows,ledger)):
            self.assertEqual(record['id'],100001+i)
            self.assertEqual(record['fonte_Q'],r[7])
            self.assertEqual(normal[r[7]-1][0],r[0]);self.assertEqual(normal[r[7]-1][1],r[1])
        # Preservar a divisão temática solicitada para as aulas condensadas.
        self.assertEqual(Counter(r[1].split(':')[0] for r in rows if r[0]==8),{'IP':12,'Fintechs':13,'SPB':25})
        self.assertEqual(Counter('ANBIMA' if r[1].startswith('ANBIMA') else 'Garantias' if r[1].startswith('Garantias') else 'Liberdade' for r in rows if r[0]==9),{'ANBIMA':25,'Garantias':20,'Liberdade':5})

    def test_core_concept_distinctions_do_not_turn_into_universal_guarantees(self):
        rows=bank()
        def find(text):return next(r for r in rows if r[2]==text)
        self.assertEqual(find('Instituição de pagamento é instituição financeira de crédito?')[3],'Não')
        self.assertEqual(find('Recondução de dirigentes da CVM:')[3],'Vedada')
        self.assertEqual(find('Recondução de diretor do BC:')[3],'Uma possível')
        self.assertEqual(find('Conta PI admite saldo negativo para liquidar?')[3],'Não')
        self.assertEqual(find('Limite especial do DPGE por titular e instituição/conglomerado:')[3],'R$ 40 milhões')
        self.assertEqual(find('Cooperativa de capital e empréstimo pode captar depósitos?')[3],'Não')
        self.assertIn('conglomerado',find('FGC ordinário por CPF/CNPJ e instituição/conglomerado:')[2])

class BateProntoBrowserTests(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click
    answer=harness.PainelCPA.answer

    def test_ui_mode_quantity_selection_and_previews(self):
        self.page.locator('.nav').get_by_role('button',name='Praticar',exact=True).click()
        self.page.get_by_role('button',name=re.compile('^Bate-pronto')).click()
        self.assertEqual(self.page.evaluate('cfg.md'),'b')
        self.assertEqual(self.page.get_by_text('Qual dificuldade?',exact=True).count(),0)
        self.assertIn(f'{len(bank())} conceitos',self.page.inner_text('#app'))
        self.page.locator('[data-practice-lesson="1"]').click()
        self.page.locator('[data-practice-lesson="2"]').click()
        self.click('30')
        self.assertEqual(self.page.evaluate('sessionPlan().groups.map(g=>g.count)'),[15,15])
        self.page.get_by_label('Quantidade de questões bate-pronto').fill('45')
        self.page.get_by_label('Quantidade de questões bate-pronto').press('Tab')
        self.assertEqual(self.page.evaluate('sessionPlan().n'),45)
        self.click('Iniciar bate-pronto')
        self.assertEqual(self.page.locator('button.o').count(),2)
        self.assertEqual(self.page.locator('.aj').count(),0)
        self.assertIn('Bate-pronto',self.page.locator('.quiz-mode').inner_text())

    def test_balanced_multi_lessons_custom_counts_rotating_remainders_and_stock(self):
        result=self.page.evaluate('''()=>{
          const results=[];
          for(const lessons of [[1,2],[1,2,3],[1,2,3,4]])for(const n of [5,10,40,45,200]){
            cfg={a:0,as:lessons,n:2,m:'all',c:n,md:'b',b:0};
            const plan=sessionPlan(),ids=mix(plan);results.push({lessons,n:plan.n,counts:plan.groups.map(g=>g.count),ids,actual:ids.map(id=>questionById(id)[0])});
          }return results;
        }''')
        for r in result:
            self.assertEqual(len(r['ids']),r['n']);self.assertEqual(len(set(r['ids'])),r['n'])
            self.assertLessEqual(max(r['counts'])-min(r['counts']),1)
            self.assertEqual(set(r['actual']),set(r['lessons']))
            self.assertTrue(all(id>=100001 for id in r['ids']))
        self.assertEqual(self.page.evaluate("cfg={a:0,as:[1,2],n:-1,m:'all',c:5,md:'b',b:0};practiceRound=0;sessionPlan().groups.map(g=>g.count)"),[3,2])
        self.assertEqual(self.page.evaluate('practiceRound=1;sessionPlan().groups.map(g=>g.count)'),[2,3])
        self.assertEqual(self.page.evaluate("cfg.as=[1,2,3,4];cfg.c=3;sessionPlan().n"),0)
        self.assertIn('pelo menos 4',self.page.evaluate('sessionPlan().note'))
        self.page.evaluate("qz=null;view='q';setBateProntoCount(0)")
        self.assertEqual(self.page.evaluate('cfg.c'),3)
        self.assertIn('quantidade inteira',self.page.inner_text('#app'))

    def test_feedback_original_indices_final_result_retry_history_and_reload(self):
        self.page.evaluate("H=[[1,1,1700000000000,0]];save();begin([100001,100051],'b')")
        for index,id in enumerate([100001,100051]):
            q=self.page.evaluate('id=>questionById(id)',id)
            option=q[5] if index==0 else q[4]
            self.page.locator('button.o').filter(has_text=option).click()
            self.assertEqual(self.page.locator('.fb-option').count(),2)
            for row in self.page.locator('.fb-option').all():
                original=int(row.get_attribute('data-option-index'))
                self.assertEqual(row.locator('p').inner_text(),q[11][original])
            self.page.evaluate('pick(0)') # responder de novo não duplica histórico
            self.assertEqual(self.page.evaluate('qz.i'),index)
            self.click('Próxima' if index==0 else 'Ver resultado')
        self.assertIn('1 de 2 (50%)',self.page.locator('[data-result-score]').inner_text())
        self.assertEqual(self.page.evaluate('H.map(r=>r[3])'),[0,3,3])
        self.assertEqual(self.page.evaluate('H[0]'),[1,1,1700000000000,0])
        self.click('Refazer erros desta sessão')
        self.assertEqual(self.page.evaluate('qz.md'),'b')
        self.assertEqual(self.page.evaluate('qz.ids'),[100001])
        self.answer();self.click('Ver resultado')
        self.assertNotIn(100001,self.page.evaluate('errs()'))
        history=self.page.evaluate('H');self.page.reload()
        self.page.get_by_text('Progresso salvo neste navegador.',exact=False).wait_for()
        self.assertEqual(self.page.evaluate('H'),history)
        self.assertEqual(sum(v['n'] for v in self.page.evaluate('evolutionData().days').values()),4)

    def test_gaps_keyboard_themes_navigation_and_desktop_layout(self):
        id=self.page.evaluate('BP_FIRST_ID+BP.findIndex(r=>r[2].includes("____"))')
        for theme in ['dark','light']:
            self.page.evaluate('theme=>document.documentElement.dataset.theme=theme',theme)
            self.page.evaluate("cfg.md='b'")
            self.page.evaluate('id=>begin([id],"b")',id)
            self.assertEqual(self.page.locator('.concept-gap').count(),1)
            self.assertEqual(self.page.locator('.feedback').count(),0)
            self.page.locator('button.o').first.focus();self.page.keyboard.press('Enter')
            self.assertEqual(self.page.locator('.fb-option').count(),2)
            choice=self.page.evaluate('qz.a')
            self.page.locator('.nav').get_by_role('button',name='Painel',exact=True).click()
            self.page.locator('.nav').get_by_role('button',name='Praticar',exact=True).click()
            self.assertEqual(self.page.evaluate('qz.a'),choice)
            self.assertTrue(self.page.locator('#theme-toggle').is_visible())
            for width in [1024,1280,1920]:
                self.page.set_viewport_size({'width':width,'height':900})
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
            self.page.screenshot(path=f'/tmp/cpa-bate-pronto-{theme}.png',full_page=True)

    def test_normal_banks_daily_and_filters_do_not_receive_concept_items(self):
        self.assertEqual(self.page.evaluate('Q.length'),self.page.evaluate('AL.reduce((n,a)=>n+(a.internalLessons?50*a.b.length:100),0)'))
        for mode in ['e','h','s']:
            self.page.evaluate('mode=>{cfg={a:0,as:[1,2],n:-1,m:"all",c:10,md:mode,b:0}}',mode)
            self.assertTrue(all(id<100001 for id in self.page.evaluate('mix(sessionPlan())')))
        self.assertTrue(all(id<100001 for id in self.page.evaluate('dailyPlan(dailyDate()).ids')))
        self.page.evaluate("H=[[100001,0,1700000000000,3]];cfg={a:1,as:[],n:-1,m:'new',c:50,md:'b',b:0}")
        self.assertEqual(self.page.evaluate('pool().length'),49)
        self.assertNotIn(100001,self.page.evaluate('pool()'))
        self.assertEqual(self.page.evaluate("cfg.m='err';pool()"),[100001])
        self.page.evaluate("H.push([100001,1,1700000001000,3])")
        self.assertEqual(self.page.evaluate('pool()'),[])

if __name__=='__main__':unittest.main(verbosity=2)
