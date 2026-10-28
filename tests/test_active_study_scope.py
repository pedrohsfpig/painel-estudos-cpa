"""Coerência entre o conjunto completo e os conceitos visíveis de cada material."""
import re
import unittest
import smoke as harness

class ActiveStudyScope(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    answer=harness.PainelCPA.answer

    def material(self,n,kind):
        self.page.evaluate("([n,c])=>{qz=null;view='m';mt={a:n,c};go()}",[n,kind])

    def test_liquidity_filters_share_thirteen_unique_questions_not_market_risk(self):
        self.material(13,'mapa')
        panel=self.page.locator('.mind-branch').filter(has=self.page.get_by_role('heading',name=re.compile('^Liquidez$',re.I)))
        key=panel.get_attribute('data-active-study')
        parent=self.page.evaluate('k=>ActiveStudy.audit().find(e=>e.key===k)',key)
        self.assertEqual(parent['ids'],[176,195,218,*range(1201,1211)])
        panel.locator('.active-study-options-trigger').click()
        dialog=self.page.get_by_role('dialog',name='Escolher conceito')
        self.assertIn('não devem ser somadas',dialog.inner_text())
        keys=dialog.locator('.active-study-choice:not(.is-whole)').evaluate_all('es=>es.map(e=>e.dataset.activeStudyKey)')
        children=self.page.evaluate('ks=>ActiveStudy.audit().filter(e=>ks.includes(e.key))',keys)
        union=set(id for e in children for id in e['ids'])
        self.assertEqual(union,set(parent['ids']))
        self.assertGreater(sum(len(e['ids']) for e in children),len(union))
        self.assertTrue(set(range(1229,1237)).isdisjoint(union))
        dialog.get_by_role('searchbox').fill('Negociar um ativo')
        row=dialog.locator('.active-study-choice').first
        child=self.page.evaluate('k=>ActiveStudy.audit().find(e=>e.key===k)',row.get_attribute('data-active-study-key'))
        self.assertTrue(child['ids']);self.assertTrue(set(child['ids']).issubset(parent['ids']))
        row.locator('button').click()
        self.assertEqual(set(self.page.evaluate('qz.ids')),set(child['ids']))
        self.assertEqual(len(self.page.evaluate('qz.ids')),len(child['ids']))
        self.answer();self.assertEqual(self.page.locator('.fb-option').count(),4)

    def test_collegiate_members_and_inflation_roles_keep_their_parent_subject(self):
        examples=[
            ('Composição','Ministro da Fazenda','Integra o colegiado',set(range(1011,1041))),
            ('Meta de inflação','Banco Central','Persegue a meta definida pelo CMN',{53,58,69,283,304}),
            ('Objetivos','Liquidez e solvência','Zelar pela liquidez e solvência das instituições',{176,195,1201,1203}),
        ]
        for parent,label,text,excluded in examples:
            result=self.page.evaluate("s=>({ids:ActiveStudy.matching(s),profile:ActiveStudy.profile(s)})",dict(lesson=2,label=label,text=text,parents=['Aula 2: Conselho Monetário Nacional (CMN)',parent]))
            self.assertTrue(result['ids'],parent)
            self.assertTrue(excluded.isdisjoint(result['ids']),(parent,result))
            # Role-specific macroeconomic or liquidity questions never replace
            # composition/competences of the institution whose facts are shown.
            self.assertEqual(result['profile']['owners'],['inflationtarget'] if parent=='Meta de inflação' else ['cmn'])

    def test_operator_characteristics_do_not_become_unrelated_financial_subjects(self):
        examples=[
            (7,['Agências de fomento','Fundo de liquidez'],'Mínimo de 10% do valor das obrigações','fomento'),
            (7,['Bancos de investimento','Finalidades principais'],'Capital fixo: máquinas, instalações e expansão','investment'),
            (7,['Administradoras de consórcios','BACEN'],'Recebe informações contábeis e não contábeis periódicas','consortium'),
        ]
        for lesson,parents,label,owner in examples:
            source=dict(lesson=lesson,label=label,text=label,parents=['Aula 7: Operadores Não Monetários',*parents])
            result=self.page.evaluate("s=>({ids:ActiveStudy.matching(s),profile:ActiveStudy.profile(s)})",source)
            self.assertEqual(result['profile']['owners'],[owner]);self.assertTrue(result['ids'])
            self.assertTrue(all(601<=id<=700 for id in result['ids']),result)
        for label,owner in [('B3','b3'),('Selic','selicsystem'),('Sitraf: transferências eletrônicas de fundos','otherpayments')]:
            source=dict(lesson=8,label=label,text=label,parents=['Aula 8: Inovação, Pagamentos e Crédito Digital','Outras infraestruturas'],whole=True)
            result=self.page.evaluate("s=>({ids:ActiveStudy.matching(s),profile:ActiveStudy.profile(s)})",source)
            self.assertEqual(result['profile']['owners'],[owner]);self.assertTrue(result['ids'])
            self.assertTrue(set(range(1065,1091)).isdisjoint(result['ids']))
        for name,parents in [('Aprovação: Senado Federal',['Diretoria','Caminho']),('Processo administrativo disciplinar',['Diretoria','Exoneração'])]:
            result=self.page.evaluate("s=>({ids:ActiveStudy.matching(s),profile:ActiveStudy.profile(s)})",dict(lesson=4,label=name,text=name,parents=['Aula 4: CVM',*parents]))
            self.assertEqual(result['profile']['facets'],['appointment'] if 'Aprovação' in name else ['dismissal'])
            self.assertTrue(result['ids']);self.assertNotIn(89,result['ids']);self.assertLess(len(result['ids']),12)

    def test_every_lesson_block_and_dense_material_has_consistent_subsets(self):
        result=self.page.evaluate('''()=>{
            const stable=JSON.stringify([Q,BP,AL,MAT,H,cfg]),checked=new Set(),issues=[];let views=0,nested=0;
            function check(source,path){
                const ids=ActiveStudy.matching(source),own=new Set(ids);
                if(ids.length!==own.size||ids.some(id=>id<1||id>Q.length))issues.push({path,type:'invalid ids'});
                for(const child of source.concepts||[]){
                    nested++;const childIds=ActiveStudy.matching(child),outside=childIds.filter(id=>!own.has(id));
                    if(outside.length)issues.push({path,child:child.label,outside});check(child,path+' / '+child.label);
                }
            }
            for(let n=1;n<=AL.length;n++)for(const block of [0,...(AL[n-1].b||[]).map(b=>b.id)])for(const c of ['mapa','diag','tl','geral']){
                if(c==='geral'&&!hasLessonOverview(n))continue;
                selectedLessonBlocks[n]=block;view='m';mt={a:n,c};go();views++;
                const registry=new Map(ActiveStudy.audit().map(e=>[e.key,e]));
                for(const panel of document.querySelectorAll('.mind-branch,.diagram-group,.diagram-sequence,.material-time-panel,.operator-overview')){
                    const parent=registry.get(panel.dataset.activeStudy);if(!parent)throw Error('Quadro sem conjunto');
                    const signature=JSON.stringify(parent.source);if(checked.has(signature))continue;checked.add(signature);
                    const ids=new Set(parent.ids);
                    for(const node of panel.querySelectorAll('[data-active-study]')){
                        const child=registry.get(node.dataset.activeStudy),outside=child.ids.filter(id=>!ids.has(id));
                        if(outside.length)issues.push({lesson:n,block,c,parent:parent.source.label,child:child.source.label,outside});
                    }
                    const shown=Number(panel.querySelector(':scope>.active-study-action .active-study-count').textContent.match(/\\d+/)[0]);
                    if(shown!==ids.size)issues.push({lesson:n,c,type:'count',shown,actual:ids.size});
                    if(ids.size!==parent.ids.length)issues.push({lesson:n,c,type:'duplicate'});
                    if(panel.querySelector(':scope>.active-study-action .active-study-button').disabled!==!ids.size)issues.push({lesson:n,c,type:'disabled'});
                    check(parent.source,n+' / '+c+' / '+parent.source.label);
                }
            }
            return {views,scopes:checked.size,nested,issues,unchanged:stable===JSON.stringify([Q,BP,AL,MAT,H,cfg])};
        }''')
        self.assertEqual(result['issues'],[])
        self.assertGreaterEqual(result['views'],129);self.assertGreaterEqual(result['scopes'],277)
        self.assertGreater(result['nested'],2000);self.assertTrue(result['unchanged'])

    def test_whole_content_includes_specific_concepts_even_without_a_general_match(self):
        result=self.page.evaluate('''()=>{
            const child={lesson:3,label:'Composição da Diretoria do BACEN',text:'1 presidente e 8 diretores'},
            source={lesson:3,label:'Quadro sem nome de assunto',text:'',concepts:[child,child]};
            const ids=ActiveStudy.matching(source),expected=ActiveStudy.matching(child);
            return {ids,expected};
        }''')
        self.assertTrue(result['ids']);self.assertEqual(result['ids'],result['expected'])
        self.assertEqual(len(result['ids']),len(set(result['ids'])))

    def test_cache_updates_for_new_questions_and_callers_cannot_change_counts(self):
        result=self.page.evaluate('''()=>{
            const source={lesson:13,label:'Liquidez',text:'Liquidez de mercado e financiamento',whole:true},before=ActiveStudy.matching(source);
            const mutated=ActiveStudy.matching(source);mutated.push(-1);
            const protectedCopy=ActiveStudy.matching(source),q=JSON.parse(JSON.stringify(Q[1200]));Q.push(q);
            const added=Q.length,after=ActiveStudy.matching(source);Q.pop();const restored=ActiveStudy.matching(source);
            return {before,protectedCopy,after,restored,added};
        }''')
        self.assertEqual(result['before'],result['protectedCopy']);self.assertEqual(result['before'],result['restored'])
        self.assertIn(result['added'],result['after']);self.assertNotIn(-1,result['protectedCopy'])

if __name__=='__main__':unittest.main(verbosity=2)
