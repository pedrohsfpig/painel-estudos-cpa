"""A evolução mostra volume e aproveitamento juntos, sem alterar o histórico."""
import unittest
from pathlib import Path
import smoke as harness


class EvolutionVolume(unittest.TestCase):
    setUpClass = classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass = classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp = harness.PainelCPA.setUp
    tearDown = harness.PainelCPA.tearDown
    click = harness.PainelCPA.click

    def test_daily_counts_include_repetitions_and_all_modes_with_brasilia_dates(self):
        history = self.page.evaluate("""()=>{
            H=[[1,true,'2026-10-19T02:59:00Z',0],
               [1,false,'2026-10-19T03:00:00Z',0],
               [1,true,'2026-10-19T12:00:00Z',1],
               [2,true,'2026-10-19T12:01:00Z',2],
               [100001,false,'2026-10-19T12:02:00Z',3],
               [3,true,'2026-10-21',0],[999999,true,'2026-10-19',0],
               [1,true],[2,false,0,0]];save();go();return H;
        }""")
        groups = self.page.locator('[data-evolution-day]')
        self.assertEqual(groups.count(), 3)
        expected = [('2026-10-18', 1, 100), ('2026-10-19', 4, 50), ('2026-10-21', 1, 100)]
        for group, (day, count, percent) in zip(groups.all(), expected):
            self.assertEqual(group.get_attribute('data-evolution-day'), day)
            self.assertEqual(group.get_attribute('data-evolution-count'), str(count))
            self.assertEqual(group.get_attribute('data-evolution-percent'), str(percent))
            self.assertEqual(group.locator('.evolution-count').text_content(), str(count))
            self.assertIn(f'{count} respostas', group.locator('title').text_content())
            self.assertEqual(group.locator('circle').get_attribute('cx'), group.locator('.evolution-count').get_attribute('x'))
        self.assertIn('2 respostas · 50%', self.page.locator('[data-evolution-undated]').inner_text())
        self.assertIn('Aproveitamento (%)', self.page.locator('.evolution-legend').inner_text())
        self.assertIn('Questões respondidas', self.page.locator('.evolution-legend').inner_text())
        self.click('Estatísticas')
        self.click('Hardcore')
        self.click('Simulado')
        self.click('Painel')
        self.assertEqual(self.page.locator('[data-evolution-day="2026-10-19"] .evolution-count').text_content(), '4')
        self.assertEqual(self.page.evaluate('H'), history)

    def test_volume_scale_is_independent_from_percentage_and_single_day_is_visible(self):
        self.page.evaluate("""H=Array.from({length:500},()=>[1,false,'2026-10-19',0]);
            H.push([1,true,'2026-10-20',0]);go()""")
        first, second = self.page.locator('[data-evolution-day]').all()
        self.assertEqual(first.get_attribute('data-evolution-percent'), '0')
        self.assertEqual(second.get_attribute('data-evolution-percent'), '100')
        self.assertGreater(float(first.locator('rect').get_attribute('height')), float(second.locator('rect').get_attribute('height')))
        self.assertGreaterEqual(float(second.locator('rect').get_attribute('height')), 2)
        self.assertEqual(first.locator('.evolution-count').text_content(), '500')
        self.page.evaluate("H=[[1,true,'2026-10-20',0]];go()")
        self.assertEqual(self.page.locator('[data-evolution-day] circle').count(), 1)
        self.assertEqual(self.page.locator('[data-evolution-day] rect').count(), 1)
        self.assertEqual(self.page.locator('.evolution-count').text_content(), '1')
        self.page.evaluate('H=[];go()')
        self.assertEqual(self.page.locator('.evolution-volume,.evolution-legend').count(), 0)
        self.assertIn('assim que houver respostas', self.page.locator('.evolution').inner_text())

    def test_long_history_keyboard_scroll_and_layout_preserve_state_in_both_themes(self):
        self.page.evaluate("""H=Array.from({length:400},(_,i)=>[1,i%2,Date.parse('2025-01-01T15:00:00Z')+i*86400000,i%4]);
            begin([1,2],'e');view='d';go()""")
        state = self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz,fl,fm])')
        for width in [390, 1024, 1440, 1920]:
            self.page.set_viewport_size(dict(width=width, height=1000))
            for theme in ['light', 'dark']:
                self.page.evaluate('theme=>document.documentElement.dataset.theme=theme', theme)
                self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'))
                self.assertEqual(self.page.locator('[data-evolution-day]').count(), 400)
                self.assertEqual(self.page.locator('.evolution-count').count(), 400)
                self.assertTrue(self.page.locator('.evolution').evaluate('n=>n.scrollWidth<=n.clientWidth+1'))
                self.click('Início do histórico')
                self.assertEqual(self.page.locator('#evolution-scroll').evaluate('n=>n.scrollLeft'), 0)
                self.page.locator('#evolution-scroll').focus()
                self.page.keyboard.press('ArrowRight')
                self.page.wait_for_function('document.getElementById("evolution-scroll").scrollLeft>0')
                self.click('Mais recente')
                self.assertGreater(self.page.locator('#evolution-scroll').evaluate('n=>n.scrollLeft'), 1000)
                self.assertEqual(self.page.evaluate('JSON.stringify([H,Q,BP,AL,MAT,cfg,qz,fl,fm])'), state)

    def test_daily_values_and_labels_fit_the_chart(self):
        self.page.evaluate("""H=[];[23,45,24,40,5,20].forEach((n,i)=>{
            const day=['13','14','17','19','20','28'][i],ok=[20,40,19,26,1,17][i];
            for(let j=0;j<n;j++)H.push([1,j<ok,'2026-10-'+day,j%4]);
        });go()""")
        folder = Path('/tmp/cpa-evolution-volume')
        folder.mkdir(exist_ok=True)
        for width in [390, 1280, 1920]:
            self.page.set_viewport_size(dict(width=width, height=1000))
            for theme in ['dark', 'light']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t', theme)
                if width >= 1280:
                    self.assertTrue(self.page.locator('#evolution-scroll').evaluate('n=>n.scrollWidth<=n.clientWidth+1'))
                # Check SVG coordinates: labels stay inside and the two measures occupy separate bands.
                self.assertTrue(self.page.locator('#evolution-scroll>svg').evaluate("""svg=>{
                    const bounds=svg.viewBox.baseVal;
                    return [...svg.querySelectorAll('text')].every(n=>{
                        const b=n.getBBox();return b.x>=0&&b.x+b.width<=bounds.width&&b.y>=0&&b.y+b.height<=bounds.height;
                    })&&[...svg.querySelectorAll('[data-evolution-day]')].every(g=>{
                        const p=g.querySelector('circle'),r=g.querySelector('rect');
                        return +p.getAttribute('cy')+5<+r.getAttribute('y');
                    });
                }"""))
                self.page.locator('.evolution').screenshot(path=str(folder/f'{theme}-{width}.png'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
