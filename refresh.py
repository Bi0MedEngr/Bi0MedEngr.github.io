# Pull each tool's icon and take light/dark preview shots from the sibling tool folders (../<dir>/).
# Run after a tool changes how it looks:  ~/.venvs/mcmaster_torx/bin/python refresh.py [slug ...]
import base64, json, os, shutil, sys
from playwright.sync_api import sync_playwright

here = os.path.dirname(os.path.abspath(__file__))
work = os.path.dirname(here)
cfg = json.load(open(os.path.join(here, 'tools.json')))
only = set(sys.argv[1:])
W, H, OUT_W = 1280, 800, 720

def shrink(page, png):
    url = 'data:image/png;base64,' + base64.b64encode(png).decode()
    data = page.evaluate("""async ([url, w]) => {
        const img = new Image(); img.src = url; await img.decode();
        const c = document.createElement('canvas'); c.width = w; c.height = Math.round(img.height * w / img.width);
        const g = c.getContext('2d'); g.imageSmoothingQuality = 'high'; g.drawImage(img, 0, 0, c.width, c.height);
        return c.toDataURL('image/webp', 0.82);
    }""", [url, OUT_W])
    return base64.b64decode(data.split(',', 1)[1])

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    for t in cfg['tools']:
        if only and t['slug'] not in only:
            continue
        src = os.path.join(work, t['dir'])
        shutil.copy(os.path.join(src, 'web', 'icon.svg'), os.path.join(here, 'icons', t['slug'] + '.svg'))
        page_file = os.path.join(src, t['slug'] + '.html')
        for scheme in ('light', 'dark'):
            ctx = b.new_context(viewport={'width': W, 'height': H}, color_scheme=scheme)
            pg = ctx.new_page()
            pg.goto('file://' + page_file)
            pg.wait_for_timeout(1800)
            png = pg.screenshot()
            out = os.path.join(here, 'shots', f"{t['slug']}-{scheme}.webp")
            open(out, 'wb').write(shrink(pg, png))
            print(t['slug'], scheme, os.path.getsize(out), 'bytes')
            ctx.close()
    b.close()
