# Launcher page checks: light/dark/iPad/phone screenshots, no console errors, no horizontal scroll,
# every card's images load, search filters, theme toggle.   python tests/browser_test.py <outdir>
import json, os, sys
from playwright.sync_api import sync_playwright

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'shots_test')
os.makedirs(out, exist_ok=True)
url = 'file://' + os.path.join(here, 'docs', 'index.html')
n_tools = len(json.load(open(os.path.join(here, 'tools.json')))['tools'])
fails = []
def check(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok: fails.append(msg)

views = [('desktop-light', 1440, 1000, 'light', False), ('desktop-dark', 1440, 1000, 'dark', False),
         ('ipad', 1180, 820, 'light', True), ('phone-dark', 390, 844, 'dark', True)]
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    for name, w, h, scheme, touch in views:
        ctx = b.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme, has_touch=touch, is_mobile=touch and w < 600)
        pg = ctx.new_page()
        errs = []
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.on('pageerror', lambda x: errs.append(str(x)))
        pg.goto(url)
        pg.evaluate('document.querySelectorAll("img[loading=lazy]").forEach(i => i.loading = "eager")')
        pg.wait_for_timeout(600)
        check(pg.locator('.card').count() == n_tools, f'{name}: {n_tools} cards')
        bad = pg.evaluate('[...document.images].filter(i => getComputedStyle(i).display !== "none" && !(i.complete && i.naturalWidth)).map(i => i.src)')
        check(not bad, f'{name}: visible images load {bad}')
        check(pg.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{name}: no horizontal scroll')
        pg.screenshot(path=os.path.join(out, name + '.png'), full_page=True)
        if name == 'desktop-light':
            pg.fill('#q', 'fatigue')
            check(pg.locator('.card:visible').count() == 1, 'search "fatigue" -> 1 card')
            pg.fill('#q', 'zzzz')
            check(pg.locator('#none').is_visible(), 'no-match message shows')
            pg.fill('#q', '')
            check(pg.locator('.card:visible').count() == n_tools, 'clearing search restores all')
            pg.click('#theme')
            check(pg.evaluate('document.documentElement.dataset.theme') == 'dark', 'theme toggle -> dark')
            check(pg.locator('.only-dark').first.is_visible(), 'dark shots shown after toggle')
            pg.click('#theme')
        check(not errs, f'{name}: no console errors {errs}')
        ctx.close()
    b.close()
print('ALL PASS' if not fails else f'{len(fails)} FAILED')
sys.exit(1 if fails else 0)
