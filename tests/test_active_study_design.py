"""Acesso por conceito sem botões dentro de nós e células do material."""
import re
import unittest
from pathlib import Path
import smoke as harness


class ActiveStudyDesign(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown
    answer=harness.PainelCPA.answer

    def material(self,n,kind):self.page.evaluate("([n,c])=>{view='m';mt={a:n,c};go()}",[n,kind])
    def branch(self,title='Diretoria'):
        return self.page.locator('.mind-branch').filter(has=self.page.get_by_role('heading',name=re.compile('^'+title+'$',re.I)))
    def picker(self):return self.page.get_by_role('dialog',name='Escolher conceito')
    def entry(self,key):return self.page.evaluate('k=>ActiveStudy.audit().find(e=>e.key===k)',key)

    def test_controls_leave_map_nodes_diagrams_and_overview_geometry_free(self):
        self.material(3,'mapa')
        self.assertEqual(self.page.locator('.mind-children .active-study-action').count(),0)
        self.assertEqual(self.page.locator('.mind-branch>.active-study-action').count(),self.page.locator('.mind-branch').count())
        self.assertEqual(self.page.locator('.mind-children button').count(),0)
        before=self.page.locator('.mind-map').bounding_box()['height']
        self.page.locator('.active-study-action').evaluate_all('es=>es.forEach(e=>e.remove())')
        baseline=self.page.locator('.mind-map').bounding_box()['height'];self.assertLess(before,baseline*1.15)
        self.material(6,'diag');self.assertEqual(self.page.locator('.diagram-step button').count(),0)
        heights=self.page.locator('.diagram-step').evaluate_all('es=>es.map(e=>e.getBoundingClientRect().height)')
        self.page.locator('.active-study-action').evaluate_all('es=>es.forEach(e=>e.remove())')
        self.assertEqual(self.page.locator('.diagram-step').evaluate_all('es=>es.map(e=>e.getBoundingClientRect().height)'),heights)
        self.material(7,'geral');self.assertEqual(self.page.locator('.operator-overview-table .active-study-action').count(),0)
        table=self.page.locator('.operator-overview-table').bounding_box()
        self.page.locator('.active-study-action').evaluate_all('es=>es.forEach(e=>e.remove())')
        self.assertEqual(self.page.locator('.operator-overview-table').bounding_box(),table)

    def test_specific_concept_count_opens_exact_same_session_and_returns_to_node(self):
        self.material(3,'mapa');branch=self.branch();branch.locator('.active-study-options-trigger').click()
        dialog=self.picker();self.assertTrue(dialog.is_visible())
        self.assertTrue(dialog.locator('.active-study-choice-start').evaluate_all("es=>es.every(e=>e.querySelector('span').textContent==='Questões'&&e.querySelectorAll('svg').length===1)"))
        before=self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT])')
        search=dialog.get_by_role('searchbox');search.fill('9 membros')
        rows=dialog.locator('.active-study-choice');self.assertGreater(rows.count(),0)
        row=rows.first;key=row.get_attribute('data-active-study-key');entry=self.entry(key)
        self.assertEqual(row.locator(':scope>div>span').inner_text(),f"{len(entry['ids'])} questões disponíveis")
        self.assertTrue({53,283}.issubset(entry['ids']));self.assertNotIn(304,entry['ids'])
        self.assertEqual(self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT])'),before)
        row.locator('.active-study-choice-start').click()
        self.assertEqual(self.page.locator('dialog').count(),0);self.assertEqual(set(self.page.evaluate('qz.ids')),set(entry['ids']))
        self.page.get_by_role('button',name='Voltar ao conteúdo',exact=True).click()
        self.assertEqual(self.page.evaluate('view'),'m')
        self.assertTrue(self.page.locator(f'[data-active-study="{key}"]').evaluate('e=>e===document.activeElement'))

    def test_all_links_available_in_picker_and_search_does_not_change_them(self):
        for n,kind,selector in [(3,'mapa','.mind-branch'),(6,'diag','.material-panel'),(3,'tl','.material-time-panel'),(7,'geral','.operator-overview')]:
            self.material(n,kind);panel=self.page.locator(selector).first
            expected=panel.locator('[data-active-study]').evaluate_all('es=>es.map(e=>e.dataset.activeStudy)')
            rootkey=panel.get_attribute('data-active-study');panel.locator(':scope>.active-study-action .active-study-options-trigger').click()
            dialog=self.picker();actual=dialog.locator('.active-study-choice').evaluate_all('es=>es.map(e=>e.dataset.activeStudyKey)')
            self.assertEqual(set(actual),set(expected+[rootkey]))
            dialog.get_by_role('searchbox').fill('<img src=x onerror=alert(1)>')
            self.assertEqual(dialog.locator('img').count(),0);self.assertIn('Nenhum conceito',dialog.inner_text())
            dialog.get_by_role('searchbox').fill('');self.assertEqual(dialog.locator('.active-study-choice').count(),len(actual))
            dialog.get_by_role('button',name='Fechar seleção de conceitos').click()

    def test_keyboard_escape_outside_click_focus_and_theme(self):
        self.material(3,'mapa');opener=self.branch().locator('.active-study-options-trigger');opener.focus();self.page.keyboard.press('Enter')
        dialog=self.picker();self.assertTrue(dialog.get_by_role('searchbox').evaluate('e=>e===document.activeElement'))
        self.page.keyboard.press('Tab');self.assertTrue(self.page.evaluate('!!document.activeElement.closest("dialog")'))
        theme=self.page.locator('html').get_attribute('data-theme')
        dialog.get_by_role('button',name='Alternar tema na seleção de questões').click()
        self.assertNotEqual(self.page.locator('html').get_attribute('data-theme'),theme);self.assertTrue(dialog.is_visible())
        self.page.keyboard.press('Escape');self.assertEqual(self.page.locator('dialog').count(),0)
        opener=self.branch().locator('.active-study-options-trigger');self.assertTrue(opener.evaluate('e=>e===document.activeElement'))
        opener.click();self.page.mouse.click(5,200);self.assertEqual(self.page.locator('dialog').count(),0);self.assertEqual(self.page.evaluate('view'),'m')

    def test_existing_session_can_be_resumed_from_picker_without_discarding_answers(self):
        self.page.evaluate("begin([1,2],'e')");self.answer();self.material(3,'mapa')
        before=self.page.evaluate('JSON.stringify([H,qz,cfg])');self.branch().locator('.active-study-options-trigger').click()
        dialog=self.picker();dialog.locator('.is-whole .active-study-choice-start').click()
        self.assertIn('Conclua ou encerre',dialog.locator('.active-study-pending').inner_text())
        self.assertEqual(self.page.evaluate('JSON.stringify([H,qz,cfg])'),before)
        dialog.get_by_role('button',name='Retomar sessão',exact=True).click()
        self.assertEqual(self.page.locator('dialog').count(),0);self.assertEqual(self.page.evaluate('view'),'q')
        self.assertEqual(self.page.evaluate('JSON.stringify([H,qz,cfg])'),before)

    def test_responsive_dialog_and_zero_counts_preserve_readability(self):
        output=Path('/tmp/cpa-active-study-design');output.mkdir(exist_ok=True)
        for width in [390,768,1024,1440,1920]:
            self.page.set_viewport_size(dict(width=width,height=1000))
            for theme in ['light','dark']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
                self.material(7,'geral');self.page.locator('.operator-overview>.active-study-action .active-study-options-trigger').click()
                dialog=self.picker();rect=dialog.bounding_box()
                self.assertGreater(dialog.locator('.active-study-choice-start:disabled').count(),0)
                self.assertTrue(dialog.locator('.active-study-choice:has(button:disabled)>div>span').evaluate_all('es=>es.every(e=>e.textContent==="0 questões disponíveis")'))
                self.assertGreaterEqual(rect['x'],0);self.assertLessEqual(rect['x']+rect['width'],width)
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                self.assertTrue(dialog.locator('.active-study-choice').evaluate_all('es=>es.every(e=>e.scrollWidth<=e.clientWidth)'))
                if width in [390,1440]:self.page.screenshot(path=str(output/f'drawer-{theme}-{width}.png'))
                dialog.get_by_role('button',name='Fechar seleção de conceitos').click()
        for n,kind in [(3,'mapa'),(6,'diag'),(7,'geral')]:
            self.material(n,kind);self.page.screenshot(path=str(output/f'{n}-{kind}.png'),full_page=True)

    def test_trail_actions_stay_inside_every_topic_without_changing_content_or_counts(self):
        result=self.page.evaluate('''()=>{
            const before=JSON.stringify([Q,BP,AL,MAT,H,cfg]),issues=[];let topics=0,views=0;
            for(let n=1;n<=AL.length;n++)for(const block of [0,...(AL[n-1].b||[]).map(b=>b.id)]){
                view='t';tr=n;selectedLessonBlocks[n]=block;go();views++;
                const content=lessonContent(n),registry=new Map(ActiveStudy.audit().map(e=>[e.key,e]));
                for(const [id,key] of [['lesson-summary','r'],['lesson-tips','d'],['lesson-traps','p']]){
                    const section=document.getElementById(id);section.open=true;
                    const rows=[...section.querySelectorAll('.pt')];
                    if(rows.length!==content[key].length)issues.push({n,block,id,type:'missing topics'});
                    rows.forEach((row,i)=>{
                        topics++;const text=row.querySelector(':scope>.lesson-topic-text'),actions=row.querySelectorAll(':scope>.active-study-action'),entry=registry.get(row.dataset.activeStudy);
                        if(text?.textContent!==searchPlain(content[key][i]))issues.push({n,block,id,i,type:'changed text'});
                        if(actions.length!==1)issues.push({n,block,id,i,type:'action outside topic'});
                        const action=actions[0],button=action?.querySelector('.active-study-button');
                        if(button?.querySelector('span')?.textContent!=='Questões'||button?.querySelectorAll('svg').length!==1)issues.push({n,id,i,type:'button label/icon'});
                        if(Number(action?.querySelector('.active-study-count').textContent.match(/\\d+/)[0])!==entry?.ids.length)issues.push({n,id,i,type:'wrong count'});
                    });
                    if(section.querySelector('.acb>.active-study-action'))issues.push({n,id,type:'external action'});
                }
            }
            return {topics,views,issues,preserved:before===JSON.stringify([Q,BP,AL,MAT,H,cfg])};
        }''')
        self.assertEqual(result['issues'],[]);self.assertTrue(result['preserved'])
        self.assertGreater(result['views'],13);self.assertGreater(result['topics'],300)

    def test_trail_compact_actions_wrap_inside_cards_in_both_themes_and_resume_session(self):
        out=Path('/tmp/cpa-topic-actions');out.mkdir(exist_ok=True)
        self.page.evaluate("begin([1,2],'e')");self.answer()
        stable=self.page.evaluate('JSON.stringify([H,qz,cfg])')
        for width in [390,768,1440]:
            self.page.set_viewport_size(dict(width=width,height=1000))
            self.page.evaluate("view='t';tr=1;go();document.querySelectorAll('.lesson-section').forEach(e=>e.open=true)")
            for theme in ['light','dark']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                boxes=self.page.locator('.lesson-section .pt').evaluate_all('''es=>es.map(e=>{
                    const r=e.getBoundingClientRect(),lines=[...e.querySelector('.lesson-topic-text').getClientRects()],a=e.querySelector('.active-study-action').getBoundingClientRect();
                    return {fits:a.left>=r.left&&a.right<=r.right&&a.top>=r.top&&a.bottom<=r.bottom,overlap:lines.some(t=>Math.min(t.right,a.right)>Math.max(t.left,a.left)&&Math.min(t.bottom,a.bottom)>Math.max(t.top,a.top)),inline:lines.some(t=>Math.abs(t.top-a.top)<8)};
                })''')
                self.assertTrue(all(b['fits'] and not b['overlap'] for b in boxes))
                if width==1440:self.assertTrue(any(b['inline'] for b in boxes))
                if width in [390,1440]:
                    self.page.locator('#lesson-summary').screenshot(path=str(out/f'topics-{theme}-{width}.png'))
        button=self.page.locator('#lesson-summary .active-study-button:not([disabled])').first
        button.focus();self.page.keyboard.press('Enter')
        self.assertTrue(self.page.get_by_role('button',name='Retomar sessão',exact=True).is_visible())
        self.assertEqual(stable,self.page.evaluate('JSON.stringify([H,qz,cfg])'))
        self.page.get_by_role('button',name='Retomar sessão',exact=True).click()
        self.assertEqual(self.page.evaluate('view'),'q');self.assertEqual(stable,self.page.evaluate('JSON.stringify([H,qz,cfg])'))

if __name__=='__main__':unittest.main(verbosity=2)
