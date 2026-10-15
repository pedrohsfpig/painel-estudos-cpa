"""Regressões de apresentação das siglas e das justificativas do caso DPGE."""
import copy
import json
from pathlib import Path
import unittest
from validate_bank import load_questions
from question_revision import digest,questions_before_numeric_revision,bate_pronto_before_numeric_revision
import smoke as harness

ROOT=Path(__file__).resolve().parents[1]
def bp_bank():return json.JSONDecoder().raw_decode((ROOT/'index.html').read_text().split('const BP=',1)[1])[0]

class NumericFeedback(unittest.TestCase):
    def test_manifest_preserves_answers_and_prior_revision(self):
        q=load_questions();before=questions_before_numeric_revision(q)
        bp=bp_bank();previous=bate_pronto_before_numeric_revision(bp)
        c=json.loads((ROOT/'docs/revisao-feedbacks-numericos.json').read_text())['contagens']
        self.assertEqual(c['questoes_alteradas'],sum(a!=b for a,b in zip(q,before)))
        self.assertEqual(c['feedbacks_principais_alterados'],sum(x!=y for a,b in zip(q,before) for x,y in zip(a[11],b[11])))
        self.assertEqual(c['bate_pronto_alterados'],sum(a!=b for a,b in zip(bp,previous)))
        self.assertEqual(c['feedbacks_bate_pronto_alterados'],sum(a[i]!=b[i] for a,b in zip(bp,previous) for i in [5,6]))
        for a,b in zip(q,before):self.assertEqual(a[:8]+a[9:11],b[:8]+b[9:11])
        for a,b in zip(bp,previous):self.assertEqual(a[:5]+a[7:],b[:5]+b[7:])
        bad=copy.deepcopy(q);bad[887][11][0]='Só um número.'
        with self.assertRaises(AssertionError):questions_before_numeric_revision(bad)

    def test_dpge_teaches_guarantee_and_no_longer_compares_units(self):
        b=bp_bank()[437]
        self.assertEqual(b[3:5],['R$ 40 milhões','R$ 40 mil'])
        for f in b[5:7]:
            self.assertIn('garantia especial',f);self.assertIn('FGC',f)
            self.assertIn('titular e instituição/conglomerado',f)
            self.assertNotIn('mil vezes',f)
        self.assertIn('garantia ordinária de R$ 250 mil',b[6])
        q=load_questions()[887]
        self.assertIn('separada da garantia ordinária',q[11][0])
        self.assertIn('simultaneamente',q[11][3])
        self.assertEqual(q[8],q[11][0])

    def test_other_context_and_numerical_rules(self):
        bp=bp_bank();q=load_questions()
        self.assertIn('36 meses',q[260][11][1]);self.assertIn('vigência',q[260][11][2])
        self.assertIn('fundo de liquidez',q[613][11][2]);self.assertIn('obrigações',q[613][11][2])
        self.assertIn('supervisiona as entidades fechadas',bp[248][5])
        self.assertNotIn('Secretaria de Políticas',bp[248][5])
        self.assertIn('teto agregado',bp[427][6]);self.assertIn('simultaneamente',bp[427][6])

class AcronymPresentation(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    click=harness.PainelCPA.click
    answer=harness.PainelCPA.answer

    def display(self,stem,options,answered=False,lesson=8):
        return self.page.evaluate('''x=>questionDisplay([x.lesson,'Teste',0,x.stem,...x.options,'',0,'',[]],x.answered)''',dict(stem=stem,options=options,answered=answered,lesson=lesson))

    def test_stem_preference_aliases_and_option_only_acronyms(self):
        d=self.display('BC e BACEN fiscalizam; a CVM supervisiona valores mobiliários.',['BC e CVM','STR','CVM e SPI','BACEN'])
        self.assertEqual(d['stem'],'BC (Banco Central do Brasil) e BACEN fiscalizam; a CVM (Comissão de Valores Mobiliários) supervisiona valores mobiliários.')
        self.assertEqual(d['options'],['BC e CVM','STR (Sistema de Transferência de Reservas)','CVM e SPI (Sistema de Pagamentos Instantâneos)','BACEN'])
        d=self.display('Quem mantém a conta PI?',['SPI','SPI e SPI','STR','PI'])
        self.assertEqual(d['options'][1],'SPI (Sistema de Pagamentos Instantâneos) e SPI')
        self.assertEqual(d['options'][3],'PI')

    def test_existing_definitions_parentheses_plurals_and_false_statements(self):
        d=self.display('Instituição de Pagamento (IP) e IPs; SCD/SEP (crédito digital).',['IP (Instituição de Pagamento)','CDBs','STR (Sistema de Transferência de Reservas)','CVM (poder executivo)'])
        self.assertEqual(d['stem'],'IP (Instituição de Pagamento) e IPs; SCD (Sociedade de Crédito Direto) / SEP (Sociedade de Empréstimo entre Pessoas) (crédito digital).')
        self.assertEqual(d['options'][0],'IP')
        self.assertEqual(d['options'][1],'CDBs (Certificados de Depósito Bancário)')
        self.assertEqual(d['options'][2],'STR (Sistema de Transferência de Reservas)')
        self.assertEqual(d['options'][3],'CVM (Comissão de Valores Mobiliários) (poder executivo)')

    def test_meaning_questions_defer_only_until_answer_and_future_inverse(self):
        for id in [753,100379]:
            before=self.page.evaluate('id=>questionDisplay(questionById(id))',id)
            after=self.page.evaluate('id=>questionDisplay(questionById(id),true)',id)
            self.assertNotIn('(Sistema de Transferência de Reservas)',before['stem'])
            self.assertIn('STR (Sistema de Transferência de Reservas)',after['stem'])
        d=self.display('Qual sigla identifica o Sistema de Transferência de Reservas?',['STR','SPI','SCR','SPB'])
        self.assertEqual(d['options'],['STR','SPI','SCR','SPB'])
        d=self.display('Qual sigla identifica o Sistema de Transferência de Reservas?',['STR','SPI','SCR','SPB'],True)
        self.assertIn('(Sistema de Transferência de Reservas)',d['options'][0])
        self.assertEqual(self.display('Regular o crédito pelo CMN significa:',['Definir normas','Fiscalizar','Operar','Emprestar'])['deferred'],[])

    def test_contextual_tr_brands_and_security(self):
        d=self.display('Pix e TR; I. BC. II. CVM.',['R$ 40 milhões','A e B','TR','<img src=x onerror=alert(1)>'])
        self.assertIn('TR (Trade Repository — entidade registradora)',d['stem'])
        self.assertNotIn('Pix (',d['stem']);self.assertNotIn('I (',d['stem'])
        self.assertEqual(d['options'][:2],['R$ 40 milhões','A e B'])
        self.assertIn('TR (Taxa Referencial)',self.display('TR',['1','2','3','4'],lesson=7)['stem'])
        html=self.page.evaluate("questionStemHtml('<img src=x onerror=alert(1)> STR (Sistema de Transferência de Reservas)')")
        self.assertNotIn('<img',html);self.assertIn('&lt;img',html);self.assertIn('acronym-expansion',html)

    def test_all_banks_render_without_mutating_records_or_deferring_unrelated_questions(self):
        result=self.page.evaluate('''()=>{
          const bank=[...Q,...BP_Q],before=JSON.stringify([Q,BP]);let changed=0;
          const deferred=[];
          bank.forEach(q=>{
            const d=questionDisplay(q),a=questionDisplay(q,true);
            if(d.stem!==q[3]||d.options.some((o,i)=>o!==q[4+i]))changed++;
            if(d.deferred.length)deferred.push(Q.includes(q)?Q.indexOf(q)+1:100001+BP_Q.indexOf(q));
            if(d.options.length!==questionOptions(q).length)throw Error('Opções perdidas');
            if(!questionStemHtml(d.stem))throw Error('Enunciado vazio');
            d.options.forEach(o=>questionTextHtml(o));
          });
          return {total:bank.length,changed,deferred,preserved:before===JSON.stringify([Q,BP])};
        }''')
        self.assertEqual(result['total'],1350);self.assertGreater(result['changed'],500)
        self.assertEqual(result['deferred'],[753,100379]);self.assertTrue(result['preserved'])

    def test_every_mode_history_and_review_use_original_option_identity(self):
        for mode,id in [('e',701),('h',888),('b',100438),('s',753)]:
            self.page.evaluate('x=>begin([x.id],x.mode)',dict(id=id,mode=mode))
            if mode=='s':self.assertNotIn('(Sistema de Transferência de Reservas)',self.page.locator('.en').inner_text())
            else:self.assertTrue(self.page.locator('.en .acronym-expansion').count()>0)
            original=self.page.evaluate('correct=>qz.o.find(o=>Boolean(o[1])===correct)[0]',mode!='s')
            self.answer(correct=mode!='s')
            if mode!='s':
                self.assertEqual(self.page.locator('.fb-option').count(),2 if mode=='b' else 4)
                for row in self.page.locator('.fb-option').all():
                    index=int(row.get_attribute('data-option-index'))
                    self.assertEqual(row.locator('p').inner_text(),self.page.evaluate('x=>questionById(x.id)[11][x.index]',dict(id=id,index=index)))
                self.click('Ver resultado')
            if mode=='s':self.assertIn('(Sistema de Transferência de Reservas)',self.page.locator('#app').inner_text())
            self.assertEqual(self.page.evaluate('qz.rev[0][2]'),original)
            self.assertEqual(self.page.evaluate('H.at(-1)[0]'),id)

    def test_desktop_themes_and_long_acronyms_keep_cards_accessible(self):
        for theme in ['dark','light']:
            for width in [1024,1280,1920]:
                self.page.set_viewport_size(dict(width=width,height=900))
                self.page.evaluate('x=>{document.documentElement.dataset.theme=x;begin([100438],"b")}',theme)
                self.assertTrue(self.page.locator('#theme-toggle').is_visible())
                self.assertEqual(self.page.locator('button.o').count(),2)
                self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),width)
                self.assertGreater(self.page.locator('.question-stem').bounding_box()['height'],80)
                self.answer();self.assertEqual(self.page.locator('.fb-option').count(),2)
        self.page.evaluate("begin([100408],'b')")
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),1920)

if __name__=='__main__':unittest.main(verbosity=2)
