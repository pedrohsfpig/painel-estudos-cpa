"""Consulta compacta do histórico, sem alterar estatísticas ou sessões."""
from collections import defaultdict
import unittest
import smoke as harness

class DashboardDetails(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown

    def fixture(self):
        self.records=self.page.evaluate('''()=>{
            H=Q.map((q,i)=>[i+1,i%3!==0,1700000000000,i%3]);
            BP_Q.forEach((q,i)=>{if(i%10===0)H.push([BP_FIRST_ID+i,i%20===0,1700000000000,3])});
            H.push([1,true,1700000000001,0],[1,false,1700000000002,0],[99999,false,1700000000003,0]);go();
            return H.map(([id,ok,,origin])=>{const q=questionById(id);return q?{lesson:q[0],topic:q[1],level:q[2],ok,origin}:null}).filter(Boolean);
        }''')

    def open(self):
        self.page.locator('.detail-stats>summary').click()

    def select(self,kind):
        self.page.locator('#detail-tab-'+kind).click()

    def cards(self):
        return self.page.locator('.detail-stat-card').evaluate_all('''nodes=>nodes.map(n=>({key:n.dataset.detailKey,percent:n.querySelector('.detail-stat-percent').textContent,ok:n.querySelector('.detail-card-correct').textContent.trim(),wrong:n.querySelector('.detail-card-errors').textContent.trim(),n:n.querySelector('.detail-card-attempts').textContent.trim()}))''')

    def all_cards(self):
        found=[]
        while True:
            rows=self.cards();self.assertLessEqual(len(rows),6);found+=rows
            next_page=self.page.locator('[data-detail-page="next"]')
            if not next_page.count() or next_page.is_disabled():break
            next_page.click()
        return found

    def test_collapsed_default_compact_views_and_consistent_semantic_colors(self):
        self.fixture()
        self.assertFalse(self.page.locator('.detail-stats').evaluate('n=>n.open'))
        summary=self.page.locator('.detail-stats>summary');summary.focus();summary.press('Enter')
        self.assertTrue(self.page.locator('.detail-stats').evaluate('n=>n.open'))
        self.assertEqual(self.page.get_by_role('tab',selected=True).get_attribute('id'),'detail-tab-lesson')
        self.assertEqual(self.page.locator('.detail-stats [role="tab"]').count(),3)
        self.assertEqual(self.page.locator('.detail-stats .bar').count(),0)
        self.assertEqual(len(self.cards()),6)
        self.page.set_viewport_size(dict(width=1440,height=1000))
        self.assertLess(self.page.locator('.detail-stats').bounding_box()['height'],630)
        for theme in ['light','dark']:
            self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
            self.assertTrue(self.page.locator('.detail-stat-percent').evaluate_all('nodes=>nodes.every(n=>getComputedStyle(n).color===getComputedStyle(document.body).color)'))
            for selector,var in [('.detail-card-correct','--ok'),('.detail-card-errors','--md')]:
                self.assertTrue(self.page.locator(selector).evaluate_all('''(nodes,v)=>{const probe=document.createElement('i');probe.style.color='var('+v+')';document.body.append(probe);const expected=getComputedStyle(probe).color;probe.remove();return nodes.every(n=>getComputedStyle(n).color===expected)}''',var))
        summary.press('Enter');self.assertFalse(self.page.locator('.detail-stats').evaluate('n=>n.open'))

    def test_all_groups_pages_and_percentages_match_the_full_attempt_history(self):
        self.fixture();self.open()
        for kind in ['lesson','topic','level']:
            self.select(kind)
            expected=defaultdict(lambda:[0,0])
            for r in self.records:
                group=expected[str(r[kind])];group[0]+=bool(r['ok']);group[1]+=1
            cards=self.all_cards()
            self.assertEqual(len(cards),len(expected))
            self.assertEqual(set(r['key'] for r in cards),set(expected))
            for card in cards:
                ok,n=expected[card['key']]
                self.assertEqual(card['percent'],f'{int(ok*100/n+0.5)}%')
                self.assertEqual(card['ok'],f'{ok} '+('acerto' if ok==1 else 'acertos'))
                self.assertEqual(card['wrong'],f'{n-ok} '+('erro' if n-ok==1 else 'erros'))
                self.assertEqual(card['n'],f'{n} '+('tentativa' if n==1 else 'tentativas'))
            if kind=='lesson':self.assertEqual([int(r['key']) for r in cards],sorted({r['lesson'] for r in self.records}))
            if kind=='level':self.assertEqual([int(r['key']) for r in cards],[-1,0,1,2,3])

    def test_global_level_origin_filters_apply_without_changing_history_or_active_session(self):
        self.fixture()
        self.page.evaluate("begin([1,2],'e');view='d';fl=0;fm=0;go()")
        before=self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz,fl,fm])')
        self.open();self.select('lesson')
        expected=sum(r['level']==0 and r['origin']==0 for r in self.records)
        self.assertEqual(sum(int(r['n'].split()[0]) for r in self.all_cards()),expected)
        self.select('topic');self.page.locator('[data-detail-order="default"]').click()
        self.page.get_by_role('searchbox',name='Buscar no desempenho detalhado').fill('Bacen')
        self.select('level');self.page.locator('[data-detail-order="attention"]').click()
        self.assertEqual(self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz,fl,fm])'),before)
        self.assertTrue(self.page.locator('.detail-stats').evaluate('n=>n.open'))

    def test_search_sort_keyboard_tabs_empty_results_and_small_sample(self):
        self.fixture();self.open()
        self.select('lesson');self.page.locator('[data-detail-order="attention"]').focus();self.page.keyboard.press('Enter')
        ordered=self.all_cards();percentages=[int(r['percent'][:-1]) for r in ordered]
        self.assertEqual(percentages,sorted(percentages))
        field=self.page.get_by_role('searchbox',name='Buscar no desempenho detalhado');field.fill('Macroeconomia')
        self.assertEqual([r['key'] for r in self.cards()],['11'])
        self.assertTrue(field.evaluate('n=>n===document.activeElement'))
        field.fill('<img src=x onerror=alert(1)>');self.assertEqual(len(self.cards()),0)
        self.assertIn('Nenhum resultado',self.page.locator('.detail-empty').inner_text())
        field.press('Escape');self.assertEqual(len(self.cards()),6)
        self.page.locator('#detail-tab-lesson').focus();self.page.keyboard.press('ArrowRight')
        self.assertEqual(self.page.get_by_role('tab',selected=True).get_attribute('id'),'detail-tab-topic')
        self.page.keyboard.press('End');self.assertEqual(self.page.get_by_role('tab',selected=True).get_attribute('id'),'detail-tab-level')
        self.page.keyboard.press('Home');self.assertEqual(self.page.get_by_role('tab',selected=True).get_attribute('id'),'detail-tab-lesson')
        self.page.evaluate('H=[[1,true,1700000000000,0]];go()');self.open()
        self.assertEqual(self.page.locator('.detail-focus').count(),0)
        self.assertEqual(self.cards()[0]['percent'],'100%')
        self.assertIn('Poucas respostas',self.page.locator('.detail-help').inner_text())
        self.page.evaluate('H=[];go()');self.open()
        self.assertIn('Ainda não há respostas',self.page.locator('.detail-empty').inner_text())
        self.assertEqual(self.page.locator('.detail-focus').count(),0)

    def test_both_themes_screen_sizes_and_all_views_without_overflow(self):
        self.fixture();self.open()
        for width in [390,1024,1280,1440,1920]:
            self.page.set_viewport_size(dict(width=width,height=1000))
            for theme in ['light','dark']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
                for kind in ['lesson','topic','level']:
                    self.select(kind)
                    self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'),(width,theme,kind))
                    self.assertTrue(self.page.locator('.detail-stat-card,.detail-stats-content').evaluate_all('nodes=>nodes.every(n=>n.scrollWidth<=n.clientWidth+1)'))
                    self.assertTrue(self.page.locator('#detail-tab-'+kind).evaluate('n=>n===document.activeElement'))

if __name__=='__main__':unittest.main(verbosity=2)
