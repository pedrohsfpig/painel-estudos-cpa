"""Segunda aula interna: autoria, preservação e integração real do bloco final."""
from collections import Counter
from decimal import Decimal
import json
from pathlib import Path
import re
import unittest
from validate_bank import load_questions
from question_revision import digest
from final_block import before_payment_flows,unit_count
import smoke as harness

ROOT=Path(__file__).resolve().parents[1]
def read(marker):
    return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split(marker,1)[1])[0]

class Content(unittest.TestCase):
    def setUp(self):
        self.q=load_questions();self.bp=read('const BP=');self.al=read('const AL=');self.mat=read('\n13:')
        self.q=self.q[:1300];self.bp=self.bp[:650];self.al,self.mat=before_payment_flows(self.al,self.mat)
        self.report=json.loads((ROOT/'docs/aula-13-credito-privado-cobertura.json').read_text())
        self.unit=self.al[12]['b'][1];self.m=self.mat['b'][1]

    def test_fifty_questions_per_unit_and_half_other_banks(self):
        self.assertEqual([u['id'] for u in self.al[12]['b']],[1,2])
        self.assertTrue(self.al[12]['internalLessons'])
        for unit in self.al[12]['b']:
            rows=[q for q in self.q if q[0]==13 and q[1] in unit['topics']]
            fast=[r for r in self.bp if r[0]==13 and r[1] in unit['topics']]
            self.assertEqual(Counter(q[2] for q in rows),{0:10,1:20,2:10,3:10})
            self.assertEqual(len(fast),25)
            self.assertEqual({q[1] for q in rows},set(unit['topics']))
        self.assertEqual(Counter(c[2] for c in self.m['fc']),{0:8,1:9,2:8})
        self.assertEqual([len(self.q),len(self.bp),len(self.al)],[1300,650,13])

    def test_old_banks_material_and_first_internal_unit_are_unchanged(self):
        before=self.report['preservacao']
        for name,rows in [('Q',self.q),('BP',self.bp)]:
            self.assertEqual(digest(rows[:before[name]['count']]),before[name]['sha256'])
        self.assertEqual(digest(self.al[:12]),before['AL_1_12'])
        self.assertEqual(digest(self.al[12]['b'][0]),before['unidade_1_AL'])
        self.assertEqual(digest(self.mat['b'][0]),before['unidade_1_MAT'])
        overview=(ROOT/'index.html').read_text().split('LESSON_OVERVIEWS[13]=',1)[1].split('\n',1)[0]
        overview=json.loads(overview.removesuffix(';').replace('groups:AL[12].b','"groups":[]'))
        self.assertEqual(digest(overview['rows'][:6]),before['overview_unit1'])
        for key in ['r','d','p','n']:
            self.assertEqual(self.al[12][key],[r for u in self.al[12]['b'] for r in u[key]])
        for key in ['dg','tb','tl','fc']:
            self.assertEqual(self.mat[key],[r for u in self.mat['b'] for r in u[key]])
        self.assertEqual(self.mat['mm'][1],[r for u in self.mat['b'] for r in u['mm'][1]])

    def test_source_ledger_distinct_angles_options_feedback_and_no_arithmetic_quiz(self):
        items=self.report['itens']
        self.assertEqual([r['id'] for r in items],list(range(1251,1301)))
        self.assertEqual(len({r['angulo'] for r in items}),50)
        for item in items:
            q=self.q[item['id']-1]
            self.assertEqual(digest(q),item['sha256'])
            self.assertEqual(q[9],0)
            self.assertEqual(len(set(q[11])),4)
            self.assertFalse(any(re.fullmatch(r'[\d\s.,%R$+-]+\.?',o) for o in q[4:8]))
            self.assertNotRegex(q[3],r'(?i)\baula\b|professor|slide|transcrição|quanto (?:é|resulta)|calcule')
            self.assertNotIn(q[3],[r[3] for r in self.q[:1250]])
        self.assertEqual([r['id'] for r in self.report['bate_pronto']],list(range(100626,100651)))
        for item,row in zip(self.report['bate_pronto'],self.bp[625:]):
            self.assertEqual(digest(row),item['sha256'])
            self.assertEqual(self.q[row[7]-1][:2],row[:2])
            self.assertLessEqual(len(row[2].split()),12)
            self.assertLessEqual(max(len(o.split()) for o in row[3:5]),10)

    def test_material_qualifies_source_ambiguities_and_own_cash_flow_is_consistent(self):
        text=json.dumps(self.m,ensure_ascii=False)
        for word in ['não é resgate','não é regra universal','mútuo bancário','gratuidade','um período']:
            self.assertIn(word,text.lower())
        for title,head,rows in self.m['tb']:
            self.assertTrue(all(len(r)==len(head) for r in rows),title)
        rate=Decimal('0.05');principal=Decimal('18000');first=Decimal('6000')
        self.assertEqual(principal*rate,900)
        self.assertEqual((principal-first)*rate,600)
        self.assertEqual(first+Decimal('12000'),principal)
        for q in self.q[1250:]:
            self.assertNotIn('60.000',q[3]);self.assertNotIn('72.000',q[3])
            self.assertNotRegex(' '.join(q[3:8]),r'(?i)omiss.*sempre|compost.*sempre maior')

class Browser(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click
    answer=harness.PainelCPA.answer
    assert_material_content=harness.PainelCPA.assert_material_content

    def test_real_internal_selection_and_full_block_balance_all_modes(self):
        for mode,single in [('e',40),('s',40),('h',10),('b',25)]:
            total=single*unit_count()
            self.page.evaluate("md=>{cfg={a:13,as:[],b:0,us:[],md,n:-1,m:'all',c:30};qz=null;view='q';go()}",mode)
            self.assertEqual(self.page.evaluate('pool().length'),total)
            self.page.locator('.practice-blocks [data-lesson-block="2"]').click()
            self.assertEqual(self.page.evaluate('cfg.us'),[2]);self.assertEqual(self.page.evaluate('pool().length'),single)
            ids=self.page.evaluate('mix(sessionPlan())')
            self.assertEqual(len(ids),min(single,30));self.assertEqual(len(set(ids)),len(ids))
            self.assertTrue(self.page.evaluate('ids=>ids.every(id=>AL[12].b[1].topics.includes(questionById(id)[1]))',ids))
            self.page.locator('.practice-blocks [data-lesson-block="1"]').click()
            groups=self.page.evaluate('sessionPlan().groups.map(g=>[g.unit,g.count])')
            self.assertEqual({g[0] for g in groups},{1,2})
            self.assertLessEqual(abs(groups[0][1]-groups[1][1]),1)
            self.page.locator('.practice-blocks [data-lesson-block="0"]').click()
            self.assertEqual(self.page.evaluate('cfg.us'),[])

    def test_reading_materials_and_overview_are_scoped_without_losing_unit_one(self):
        self.page.evaluate("view='t';tr=13;go()")
        self.page.locator('.lesson-blocks [data-lesson-block="2"]').click()
        self.assertEqual(self.page.evaluate('lessonContent(13).id'),2)
        self.assertIn('Crédito Privado',self.page.inner_text('#app'))
        for name,key in [('Ramificações','mapa'),('Diagramas','diag'),('Tabelas','tab'),('Linha do tempo','tl'),('Flashcards','fc')]:
            self.page.evaluate("k=>{view='m';mt={a:13,c:k};fi=0;ff=0;go()}",key)
            self.assert_material_content(name)
            self.assertEqual(self.page.evaluate('currentMaterial().id'),2)
        self.page.evaluate("mt.c='geral';go()")
        self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),5)
        self.assertEqual(self.page.locator('[data-operator-block="1"]').count(),0)
        self.page.evaluate('selectedLessonBlocks[13]=0;go()')
        self.assertEqual(self.page.locator('#overview-scroll tbody tr').count(),self.page.evaluate('LESSON_OVERVIEWS[13].rows.length'))

    def test_concept_actions_do_not_confuse_financial_and_insurance_capitalization(self):
        examples=[
            ('Emissor e dívida','Investidor e emissora',1251),
            ('Juros e indexadores','Parcela fixa e referência variável',1262),
            ('Amortização e resgate','Bullet e devolução de principal',1271),
            ('Empréstimo e mútuo','Mutuante e mutuário',1281),
            ('Capitalização financeira','Base inicial e juros incorporados',1291),
        ]
        for label,text,id in examples:
            result=self.page.evaluate('s=>({ids:ActiveStudy.matching(s),profile:ActiveStudy.profile(s)})',dict(lesson=13,label=label,text=text,whole=True))
            self.assertIn(id,result['ids'],result)
            self.assertTrue(set(range(401,501)).isdisjoint(result['ids']),result)
        for label,ids in [('Amortização e resgate',[1257,1266,1269,1299,1300]),('Juros e indexadores',[1273,1276,1299]),('Capitalização financeira',[1288,1289])]:
            result=self.page.evaluate('s=>ActiveStudy.matching(s)',dict(lesson=13,label=label,text='',whole=True))
            self.assertTrue(set(ids).issubset(result),(label,result))
        self.page.evaluate("selectedLessonBlocks[13]=2;view='m';mt={a:13,c:'mapa'};go()")
        panels=self.page.locator('.mind-branch')
        self.assertEqual(panels.count(),5)
        for panel in panels.all():
            result=self.page.evaluate('k=>ActiveStudy.audit().find(r=>r.key===k)',panel.get_attribute('data-active-study'))
            self.assertTrue(result['ids'],result['source'])
            self.assertTrue(any(1251<=id<=1300 for id in result['ids']))
            self.assertTrue(set(range(401,501)).isdisjoint(result['ids']))
        panel=panels.filter(has=self.page.get_by_role('heading',name=re.compile('^Amortização e resgate$',re.I)))
        expected=self.page.evaluate('k=>ActiveStudy.audit().find(r=>r.key===k).ids',panel.get_attribute('data-active-study'))
        panel.locator(':scope>.active-study-action .active-study-button').click()
        self.assertCountEqual(self.page.evaluate('qz.ids'),expected)
        self.assertEqual(self.page.locator('.quiz-progress-segment').count(),len(expected))

    def test_all_options_feedback_acronyms_history_and_modes_use_stable_ids(self):
        for mode,ids in [('e',[1262,1274,1297]),('h',[1259,1279,1300]),('s',[1262,1274,1297]),('b',[100626,100634,100650])]:
            self.page.evaluate('x=>{H=[[1,true,1000,0]];begin(x.ids,x.mode)}',dict(ids=ids,mode=mode))
            for i,id in enumerate(ids):
                if id==1262:self.assertIn('Índice Nacional de Preços ao Consumidor Amplo',self.page.locator('.en').inner_text())
                self.answer(correct=i!=1)
                if mode!='s':
                    self.assertEqual(self.page.locator('.fb-option').count(),2 if mode=='b' else 4)
                    for row in self.page.locator('.fb-option').all():
                        index=int(row.get_attribute('data-option-index'))
                        self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('x=>questionById(x.id)[11][x.index]',dict(id=id,index=index)))
                    self.click('Próxima' if i<2 else 'Ver resultado')
            self.assertEqual(self.page.locator('[data-result-score]').inner_text(),'2 de 3 (67%)')
            self.assertEqual(self.page.evaluate('H.map(r=>r[0])'),[1,*ids])

    def test_new_content_is_searchable_and_both_themes_fit_without_mutating_session(self):
        self.assertTrue(self.page.evaluate("contentSearchIndex().some(r=>r.lesson===13&&/mútuo/.test(r.text))"))
        self.page.evaluate("begin([1261,1291],'e');selectedLessonBlocks[13]=2;view='m';mt={a:13,c:'mapa'};go()")
        before=self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz])')
        folder=Path('/tmp/cpa-aula13-credito/screens');folder.mkdir(exist_ok=True)
        for width in [390,1280,1920]:
            self.page.set_viewport_size(dict(width=width,height=1000))
            for theme in ['dark','light']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
                for key in ['mapa','diag','tab','tl','fc','geral']:
                    self.page.evaluate('k=>{mt.c=k;go()}',key)
                    self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme,key))
                    self.assertEqual(self.page.locator('.mind-node .active-study-button,.diagram-step .active-study-button').count(),0)
                    self.assertEqual(self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz])'),before)
                if width==1280:
                    self.page.evaluate("mt.c='mapa';go()")
                    self.page.screenshot(path=str(folder/f'map-{theme}.png'),full_page=True)

    def test_consulta_recovers_new_concepts_and_keeps_causal_questions_from_older_lessons(self):
        for query,terms in [
            ('Como funciona a amortização bullet?',['principal','vencimento']),
            ('Quem é o mutuante?',['fornece','restitui']),
            ('Diferença entre capitalização simples e composta',['simples','composta']),
            ('Resgate antecipado e venda do título',['venda','emissora']),
        ]:
            result=self.page.evaluate('q=>Consulta.answer(q,[],{lessons:[13]})',query)
            self.assertEqual(result['status'],'found',query)
            text=' '.join(' '.join(i['record']['lines']) for i in result['items']).lower()
            for term in terms:self.assertIn(term,text)
        result=self.page.evaluate("Consulta.answer('Por que juros maiores afetam o consumo?')")
        self.assertEqual(result['status'],'found')
        self.assertEqual(result['items'][0]['record']['lesson'],11)
        self.assertIn('consumo',' '.join(result['items'][0]['record']['lines']))

if __name__=='__main__':unittest.main(verbosity=2)
