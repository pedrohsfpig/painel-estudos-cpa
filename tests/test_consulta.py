"""Consulta local: relevância, fontes, navegação e preservação dos dados."""
import unittest
import smoke as harness

class Consulta(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click

    def ask(self,question):
        if self.page.evaluate('view')!='c':self.click('Consulta')
        self.page.locator('#consult-question').fill(question)
        self.page.get_by_role('button',name='Consultar',exact=True).click()
        return self.page.locator('.consult-current').inner_text()

    def result(self,q):return self.page.evaluate('q=>Consulta.answer(q)',q)

    def test_menu_position_inline_answers_examples_and_keyboard_submit(self):
        labels=self.page.locator('.nav button>span:first-of-type').all_text_contents()
        self.assertEqual(labels[:4],['Painel','Trilha','Consulta','Praticar'])
        self.click('Consulta')
        self.assertEqual(self.page.locator('.nav-item[aria-current="page"]').inner_text(),'Consulta')
        self.assertEqual(self.page.locator('.consult-examples button').count(),4)
        self.page.locator('#consult-question').fill('Quantos membros compõem o Bacen?')
        self.page.locator('#consult-question').press('Enter')
        self.assertEqual(self.page.evaluate('view'),'c')
        self.assertIn('9',self.page.locator('.consult-current').inner_text())
        self.assertIn('8 diretores',self.page.locator('.consult-current').inner_text())
        self.assertTrue(self.page.locator('#consult-answer-title').evaluate('n=>n===document.activeElement'))
        self.assertGreater(self.page.locator('.consult-current .consult-source').count(),0)
        self.assertEqual(self.page.locator('.consult-current a').count(),0)
        self.page.locator('.consult-examples button').first.click()
        self.assertIn('Banco dos bancos',self.page.locator('.consult-current').inner_text())

    def test_membership_answers_total_composition_not_conditional_arithmetic(self):
        for q in ['Quantos membros e quais são os membros do Bacen?','composição do BCB','integrantes do Banco Central do Brasil']:
            result=self.result(q)
            self.assertEqual(result['request']['subjects'][0]['name'],'Banco Central do Brasil')
            first=' '.join(result['items'][0]['record']['lines'])
            self.assertIn('9',first);self.assertIn('8 diretores',first)
            self.assertNotIn('2 por ano',first)
        text=self.ask('quais são os membros do CMN?')
        for term in ['Ministro da Fazenda','Ministro do Planejamento','Presidente do Banco Central']:self.assertIn(term,text)

    def test_acronyms_voice_variants_plurals_accents_and_action_synonyms(self):
        subjects=[]
        for q in ['função do Bacen','funções do bacém','atribuições do BCB','responsabilidades do Banco Central']:
            result=self.result(q);subjects.append([e['id'] for e in result['request']['subjects']])
            self.assertEqual(result['status'],'found')
            self.assertEqual(result['originalTable']['title'],'Os quatro papéis do Banco Central')
        self.assertTrue(all(s==subjects[0] for s in subjects))
        for q in ['IPs','instituições de pagamentos','instituição de pagamento']:
            result=self.result(q)
            self.assertEqual(result['request']['subjects'][0]['name'],'Instituição de Pagamento')
        answer=self.ask('qual é o órgão responsável por emitir moeda?')
        self.assertIn('BACEN',answer)
        self.assertIn('Emissão',answer)

    def test_comparisons_have_correct_subjects_values_and_sources_inside_the_view(self):
        text=self.ask('Comparação entre CVM e Susep')
        self.assertEqual(self.page.locator('.consult-current table').count(),1)
        self.assertIn('Mercado de capitais',text)
        self.assertIn('previdência aberta',text)
        self.assertIn('Aula 4',text);self.assertIn('Aula 5',text)
        result=self.result('Comparação entre CVM e Susep')
        composition=next(row for row in result['comparisons'] if row['facet']=='composition')
        self.assertIn('4 diretores',' '.join(composition['cells'][0][0]['record']['lines']))
        self.assertIn('superintendente',' '.join(composition['cells'][1][0]['record']['lines']))
        original=self.page.evaluate("MAT[8].tb.find(t=>t[0]==='SCD e SEP')")
        result=self.result('Diferenças entre SCDs e SEPs')
        self.assertEqual(result['originalTable']['headers'],original[1])
        self.assertEqual(result['originalTable']['rows'],original[2])
        context=self.result('diferença entre fluxos real e monetário')
        self.assertEqual([e['name'] for e in context['request']['subjects']],['Fluxo real','Fluxo monetário'])

    def test_followups_keep_the_subject_and_previous_answers_remain_available(self):
        self.ask('composição do Bacen')
        text=self.ask('e o mandato?')
        self.assertIn('4 anos',text)
        self.assertIn('Banco Central',text)
        self.assertEqual(self.page.locator('.consult-previous').count(),1)
        self.page.locator('.consult-previous summary').click()
        self.assertIn('8 diretores',self.page.locator('.consult-previous').inner_text())
        self.ask('comparação entre CVM e Susep')
        self.ask('e a composição?')
        self.assertEqual(self.page.locator('.consult-current table').count(),1)
        self.assertIn('superintendente',self.page.locator('.consult-current').inner_text())

    def test_partial_and_unknown_questions_do_not_claim_facts_not_found(self):
        result=self.result('Qual CPF do presidente do Bacen?')
        self.assertEqual(result['status'],'related')
        text=self.ask('Bacen e unicórnios intergalácticos')
        self.assertIn('trechos relacionados',text)
        self.assertIn('não encontrei uma resposta específica',text)
        result=self.result('temperatura em Marte hoje zyxw987')
        self.assertEqual(result['status'],'missing');self.assertEqual(result['items'],[])
        text=self.ask('temperatura em Marte hoje zyxw987')
        self.assertIn('Não encontrei conteúdo',text)
        self.assertEqual(self.page.locator('.consult-current .consult-facts').count(),0)

    def test_source_records_are_literal_and_do_not_include_distractor_alternatives(self):
        self.assertTrue(self.page.evaluate('''()=>{const db=Consulta.index();return ['Resumo','Mapa mental','Tabela','Linha do tempo','Diagrama','Flashcard','Quadro comparativo','Explicação de questão','Explicação Bate-pronto'].every(t=>db.records.some(r=>r.type===t))&&new Set(db.records.map(r=>r.lesson)).size===AL.length}'''))
        for q in ['funções do Bacen','limites do FGC','Qual o mandato da CVM?','Comparação entre CVM e Susep','SPI','PIB','contraparte central']:
            self.assertTrue(self.page.evaluate('''q=>{const db=Consulta.index(),a=Consulta.answer(q);return a.items.length>0&&[...a.items,...a.comparisons.flatMap(r=>r.cells.flat())].every(i=>JSON.stringify(i.record.lines)===JSON.stringify(db.records[i.record.id].lines))}''',q),q)
        self.assertTrue(self.page.evaluate('''()=>Consulta.index().records.filter(r=>r.type==='Explicação de questão').every(r=>!r.lines.some(l=>l==='Normativos fiscalizam as instituições no dia a dia.'))'''))

    def test_selic_limit_and_guarantee_answers_preserve_the_registered_context(self):
        result=self.result('Selic atua como contraparte central?')
        first=' '.join(result['items'][0]['record']['lines'])
        self.assertIn('Não atua como contraparte central',first)
        text=self.ask('limites do FGC')
        self.assertIn('250 mil',text);self.assertIn('1 milhão',text)
        fgcoop=self.result('Qual a cobertura do FGCoop?')
        self.assertIn('250 mil',' '.join(fgcoop['items'][0]['record']['lines']))
        result=self.result('limite do DPGE')
        self.assertTrue(any('40 milhões' in ' '.join(i['record']['lines']) for i in result['items']))

    def test_consultation_preserves_session_history_filters_material_selection_and_draft(self):
        self.page.evaluate("H=[[1,false,1700000000000,0]];begin([1,2],'e');pick(0);view='d';go()")
        before=self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz,fl,fm,mt,selectedLessonBlocks])')
        self.ask('funções do Bacen');self.ask('comparação entre CVM e Susep')
        self.page.locator('#consult-question').fill('Minha próxima pergunta')
        self.click('Painel');self.click('Consulta')
        self.assertEqual(self.page.locator('#consult-question').input_value(),'Minha próxima pergunta')
        self.assertIn('CVM',self.page.locator('.consult-current').inner_text())
        self.click('Limpar')
        self.assertEqual(self.page.locator('.consult-current').count(),0)
        self.assertEqual(self.page.locator('#consult-question').input_value(),'')
        self.assertEqual(self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz,fl,fm,mt,selectedLessonBlocks])'),before)
        self.click('Praticar');self.assertEqual(self.page.evaluate('qz.ids'),[1,2])

    def test_queries_do_not_contact_external_services_and_html_is_escaped(self):
        self.click('Consulta');requests=[]
        self.page.on('request',lambda request:requests.append(request.url))
        self.page.route('**/*',lambda route:route.abort())
        self.ask('Bacen <img src=x onerror="window.injected=1">')
        self.assertEqual(self.page.locator('.consult-current img').count(),0)
        self.assertIsNone(self.page.evaluate('window.injected'))
        self.assertIn('<img',self.page.locator('#consult-answer-title').inner_text())
        self.assertEqual(requests,[])

    def test_future_lesson_content_is_indexed_without_changing_existing_materials(self):
        self.page.evaluate('Consulta.index()')
        self.page.evaluate('''()=>{AL.push({t:'Aula 12: Caderno adicional',r:['Referência complementar: texto de consulta exclusivo do caderno adicional.'],n:[],d:[],p:[]});MAT[12]={mm:['Caderno adicional',[]],tb:[],dg:[],tl:[],fc:[]}}''')
        result=self.result('texto de consulta exclusivo do caderno adicional')
        self.assertTrue(result['items'])
        self.assertEqual(result['items'][0]['record']['lesson'],12)
        self.assertIn('texto de consulta exclusivo',' '.join(result['items'][0]['record']['lines']))

    def test_both_themes_comparisons_and_single_answers_fit_desktop_and_mobile(self):
        self.click('Consulta')
        for width in [390,1024,1280,1440,1920]:
            self.page.set_viewport_size(dict(width=width,height=1000))
            for theme in ['light','dark']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
                for q in ['composição do Bacen','comparação entre CVM e Susep','diferença entre SCD e SEP']:
                    self.ask(q)
                    self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'),(width,theme,q))
                    self.assertTrue(self.page.locator('.consult-page').evaluate('n=>n.scrollWidth<=n.clientWidth+1'))
                    self.click('Limpar')

if __name__=='__main__':unittest.main(verbosity=2)
