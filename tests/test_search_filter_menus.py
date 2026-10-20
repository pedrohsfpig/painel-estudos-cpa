"""Os seletores visuais preservam os filtros e funcionam por mouse e teclado."""
import unittest
import smoke as harness

class SearchFilterMenus(unittest.TestCase):
    setUpClass=classmethod(harness.PainelCPA.setUpClass.__func__)
    tearDownClass=classmethod(harness.PainelCPA.tearDownClass.__func__)
    setUp=harness.PainelCPA.setUp
    tearDown=harness.PainelCPA.tearDown

    def search(self,area='questoes'):
        self.page.locator('#content-search-input').fill('Bacen')
        self.page.locator(f'[data-search-area="{area}"]').click()

    def trigger(self,name='Modo das questões encontradas'):
        return self.page.get_by_role('combobox',name=name,exact=True)

    def test_open_close_switch_and_commit_preserve_filter_values(self):
        self.search()
        before=self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT])')
        mode=self.trigger();mode.click()
        self.assertEqual(mode.get_attribute('aria-expanded'),'true')
        self.assertEqual(self.page.get_by_role('listbox').count(),1)
        self.assertEqual(self.page.get_by_role('listbox').get_by_role('option',selected=True).get_attribute('data-search-value'),'all')
        mode.click()
        self.assertEqual(mode.get_attribute('aria-expanded'),'false')
        mode.click()
        history=self.trigger('Histórico das questões encontradas');history.click()
        self.assertEqual(mode.get_attribute('aria-expanded'),'false')
        self.assertEqual(self.page.get_by_role('listbox').count(),1)
        self.page.get_by_role('option').filter(has_text='Nunca respondidas').click()
        self.assertEqual(self.page.evaluate('currentSearch().qHistory'),'new')
        self.assertEqual(history.get_attribute('aria-expanded'),'false')
        self.assertTrue(history.evaluate('n=>n===document.activeElement'))
        self.assertEqual(self.page.evaluate('JSON.stringify([H,cfg,Q,BP,AL,MAT])'),before)

    def test_keyboard_navigation_typeahead_and_commit(self):
        self.search();mode=self.trigger();mode.focus()
        self.page.keyboard.press('ArrowDown')
        self.assertEqual(mode.get_attribute('aria-expanded'),'true')
        self.page.keyboard.press('End')
        self.assertEqual(self.page.evaluate('document.getElementById(document.activeElement.getAttribute("aria-activedescendant")).dataset.searchValue'),'b')
        self.assertEqual(self.page.evaluate('currentSearch().qMode'),'all')
        self.page.keyboard.press('Home');self.page.keyboard.press('s')
        self.page.keyboard.press('Enter')
        self.assertEqual(self.page.evaluate('currentSearch().qMode'),'s')
        self.assertTrue(mode.evaluate('n=>n===document.activeElement'))
        self.page.keyboard.press('ArrowUp');self.page.keyboard.press('ArrowUp')
        self.page.keyboard.press('Space')
        self.assertEqual(self.page.evaluate('currentSearch().qMode'),'e')

    def test_escape_tab_and_outside_click_dismiss_without_committing(self):
        self.search();mode=self.trigger();mode.click()
        self.page.keyboard.press('End');self.page.keyboard.press('Escape')
        self.assertEqual(mode.get_attribute('aria-expanded'),'false')
        self.assertTrue(mode.evaluate('n=>n===document.activeElement'))
        self.assertEqual(self.page.evaluate('currentSearch().qMode'),'all')
        mode.click();self.page.keyboard.press('Tab')
        self.assertEqual(mode.get_attribute('aria-expanded'),'false')
        self.assertTrue(self.trigger('Histórico das questões encontradas').evaluate('n=>n===document.activeElement'))
        mode.click();self.page.locator('#content-search-input').click()
        self.assertEqual(mode.get_attribute('aria-expanded'),'false')
        self.assertEqual(self.page.evaluate('currentSearch().qMode'),'all')

    def test_long_lesson_menu_keyboard_and_viewport_bounds_in_both_themes(self):
        self.search()
        for width in [390,1280,1920]:
            self.page.set_viewport_size(dict(width=width,height=900))
            for theme in ['light','dark']:
                self.page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
                lesson=self.trigger('Filtrar resultados por aula');lesson.scroll_into_view_if_needed();lesson.click()
                self.page.keyboard.press('End')
                menu=self.page.get_by_role('listbox')
                bounds=menu.bounding_box()
                self.assertGreaterEqual(bounds['x'],0)
                self.assertGreaterEqual(bounds['y'],0)
                self.assertLessEqual(bounds['x']+bounds['width'],width)
                self.assertLessEqual(bounds['y']+bounds['height'],900)
                self.assertTrue(self.page.evaluate('''()=>{const menu=document.querySelector('.search-select-menu:popover-open'),option=menu.querySelector('[data-active="true"]'),m=menu.getBoundingClientRect(),o=option.getBoundingClientRect();return o.top>=m.top&&o.bottom<=m.bottom}'''))
                expected=menu.get_by_role('option').last.get_attribute('data-search-value')
                self.page.keyboard.press('Enter')
                self.assertEqual(str(self.page.evaluate('currentSearch().lesson')),expected)
                self.assertTrue(self.page.evaluate('filteredSearchResults().every(d=>d.lesson===currentSearch().lesson)'))
                self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth'))
                lesson.click();self.page.keyboard.press('Home');self.page.keyboard.press('Enter')
        self.page.set_viewport_size(dict(width=1280,height=900))
        self.page.locator('[data-search-area="materiais"]').click()
        self.trigger('Filtrar resultados por aula').click()
        self.page.keyboard.press('End');self.page.keyboard.press('Enter')
        self.assertTrue(self.page.evaluate('filteredSearchResults().every(d=>searchArea(d)==="materiais"&&d.lesson===currentSearch().lesson)'))

if __name__=='__main__':unittest.main(verbosity=2)
