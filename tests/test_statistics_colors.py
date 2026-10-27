"""Verificação visual calculada da escala, contraste e semântica restrita às estatísticas."""
import math
import unittest
import smoke as harness

class StatisticsColors(unittest.TestCase):
 setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
 tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
 setUp=harness.PainelCPA.setUp
 tearDown=harness.PainelCPA.tearDown
 click=harness.PainelCPA.click
 def open(self):
  self.page.evaluate("H=[[1,true,1700000000000,0],[1,false,1700000000001,0]];view='stats';go()")
 def test_green_scale_has_visible_steps_and_readable_text_in_both_themes(self):
  self.open();self.page.locator('.stats-matrix-section summary').click()
  for theme in ['light','dark']:
   self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
   colors=self.page.evaluate('''()=>{
    const parent=document.querySelector('.statistics-page');
    const rgb=c=>c.match(/[\\d.]+/g).slice(0,3).map(Number);
    const luminance=channels=>channels.map(n=>n/255).map(n=>n<=.04045?n/12.92:((n+.055)/1.055)**2.4).reduce((sum,n,i)=>sum+n*[.2126,.7152,.0722][i],0);
    return Array.from({length:101},(_,p)=>{const node=document.createElement('span');node.className='stats-matrix-value';node.style=statisticsHeatStyle(p);node.innerHTML='<strong>'+p+'%</strong><small>amostra</small>';parent.append(node);
     const css=getComputedStyle(node),bg=rgb(css.backgroundColor),fg=rgb(getComputedStyle(node.querySelector('small')).color),a=luminance(bg),b=luminance(fg);node.remove();
     return {bg,luminance:a,contrast:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
    });
   }''')
   for p,c in enumerate(colors):
    self.assertGreaterEqual(c['contrast'],4.5,(theme,p,c));self.assertGreater(c['bg'][1],max(c['bg'][0],c['bg'][2]))
   self.assertGreater(colors[0]['luminance'],.9);self.assertLess(colors[100]['luminance'],.04)
   anchors=[colors[p] for p in [0,25,50,75,100]]
   for a,b in zip(anchors,anchors[1:]):
    self.assertGreater(math.dist(a['bg'],b['bg']),35,(theme,a,b))
    self.assertGreater(a['luminance'],b['luminance'])
   self.assertEqual(self.page.locator('.stats-heat-scale .stats-matrix-value').all_text_contents(),['0%','25%','50%','75%','100%'])
 def test_errors_use_red_and_difficulty_colors_remain_distinct(self):
  self.open()
  for theme in ['light','dark']:
   self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
   result=self.page.evaluate('''()=>{
    const probe=document.createElement('i');document.body.append(probe);probe.style.color='var(--hd)';const red=getComputedStyle(probe).color;probe.remove();
    return {red,errors:[...document.querySelectorAll('.stats-metric-icon.incorrect,.stats-metric:has(.incorrect) .mv,.detail-card-errors,.stats-level-errors')].map(n=>getComputedStyle(n).color),stroke:getComputedStyle(document.querySelector('.stats-ring-track.has-data')).stroke,
     levels:[...document.querySelectorAll('.stats-difficulty:not([data-stat-filter="level:-1"])')].map(n=>getComputedStyle(n).color),
     icons:[...document.querySelectorAll('.stats-origin-chip svg')].map(n=>n.innerHTML)};
   }''')
   self.assertTrue(result['errors']);self.assertTrue(all(color==result['red'] for color in result['errors']));self.assertEqual(result['stroke'],result['red'])
   self.assertEqual(len(set(result['levels'])),4);self.assertEqual(len(set(result['icons'])),4)
   self.page.locator('[data-stat-filter="level:1"]').focus();self.page.keyboard.press('Enter')
   self.assertEqual(self.page.evaluate('fl'),1);self.assertEqual(self.page.locator('[data-stat-filter="level:1"]').get_attribute('aria-pressed'),'true')
   self.click('Limpar filtros')
 def test_all_circular_charts_have_bold_rings_and_readable_center_values(self):
  self.page.evaluate("(()=>{const id=Q.findIndex(q=>q[2]===1)+1;H=[true,true,true,false].map(ok=>[id,ok,1700000000000,0]);view='stats';go()})()")
  for theme in ['light','dark']:
   self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
   for kind in ['lesson','topic','level']:
    self.page.evaluate('kind=>setDetailStatsKind(kind)',kind)
    rings=self.page.locator('.stats-ring').evaluate_all("""nodes=>nodes.map(node=>{const svg=node.querySelector('svg'),circle=svg.querySelector('circle'),text=node.querySelector('.mv,.detail-stat-percent'),weight=parseFloat(getComputedStyle(svg).strokeWidth),r=circle.r.baseVal.value;return {weight,text:text.textContent,visible:text.getBoundingClientRect().width,space:(2*r-weight)*node.clientWidth/100,bounds:2*r+weight}})""")
    self.assertTrue(any(r['text']=='75%' for r in rings))
    for r in rings:
     self.assertGreaterEqual(r['weight'],14);self.assertLessEqual(r['bounds'],100);self.assertLess(r['visible'],r['space'])
    self.assertEqual(self.page.locator('.stats-score .mv').inner_text(),'75%')
 def test_new_colors_keep_filters_responsive_and_history_unchanged(self):
  self.open();state=self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT])')
  for width in [390,768,1024,1440,1920]:
   self.page.set_viewport_size(dict(width=width,height=900))
   for theme in ['light','dark']:
    self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
    self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme))
    self.assertTrue(self.page.locator('.stats-filters').evaluate('e=>e.scrollWidth<=e.clientWidth+1'))
  self.page.locator('[data-stat-filter="origin:3"]').click();self.assertEqual(self.page.evaluate('fm'),3)
  self.assertEqual(self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT])'),state)
if __name__=='__main__':unittest.main(verbosity=2)
