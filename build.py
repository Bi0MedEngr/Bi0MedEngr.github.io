# Build the launcher site (docs/), this repo's README.md and the GitHub profile README (profile/README.md)
# from tools.json, icons/ and shots/. Pure Python, no network.   python3 -I build.py
import base64, hashlib, html, json, os, shutil

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
cfg = json.load(open('tools.json'))
site, groups, tools = cfg['site'], cfg['groups'], cfg['tools']
for t in tools:
    t['url'] = site['url'] + t['slug'] + '/'
    t['repo'] = f"https://github.com/{site['owner']}/{t['slug']}"
    for f in (f"icons/{t['slug']}.svg", f"shots/{t['slug']}-light.webp", f"shots/{t['slug']}-dark.webp"):
        assert os.path.exists(f), f + ' missing: run refresh.py'
    assert t['group'] in {g['id'] for g in groups}, t['slug'] + ': unknown group'
e = lambda s: html.escape(s, quote=True)

faces = [('IBM Plex Sans', '400 600', 'plex-sans-var'), ('IBM Plex Sans Condensed', '600', 'plex-sans-cond-600'), ('IBM Plex Mono', '400', 'plex-mono-400')]
fonts = ''.join("@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2')}\n"
                % (fam, w, base64.b64encode(open(f'fonts/{f}.woff2', 'rb').read()).decode()) for fam, w, f in faces)

def card(t):
    labs = ''.join(f'<li>{e(l)}</li>' for l in t['labs'])
    words = ' '.join([t['name'], t['blurb']] + t['labs']).lower()
    return f'''<article class="card" style="--tool:{t['accent']};--tool-dark:{t['accentDark']}" data-words="{e(words)}">
  <a class="shot" href="{t['url']}" tabindex="-1" aria-hidden="true">
    <img class="only-light" src="shots/{t['slug']}-light.webp" alt="" width="720" height="450" loading="lazy">
    <img class="only-dark" src="shots/{t['slug']}-dark.webp" alt="" width="720" height="450" loading="lazy">
  </a>
  <div class="body">
    <h3><img src="icons/{t['slug']}.svg" alt="" width="28" height="28"><a href="{t['url']}">{e(t['name'])}</a></h3>
    <p>{e(t['blurb'])}</p>
    <ul class="labs">{labs}</ul>
    <div class="actions">
      <a class="open" href="{t['url']}">Open<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3h7v7M13 3 4 12"/></svg></a>
      <a class="src" href="{t['repo']}">Source<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M5.5 4 1.5 8l4 4M10.5 4l4 4-4 4"/></svg></a>
    </div>
  </div>
</article>'''

sections = ''.join(
    f'<section class="group" data-group="{g["id"]}"><h2>{e(g["name"])}</h2><div class="grid">'
    + ''.join(card(t) for t in tools if t['group'] == g['id']) + '</div></section>' for g in groups)

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(site['name'])}</title>
<meta name="description" content="{e(site['tagline'])}">
<meta name="theme-color" content="#f6f5f1" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#16181d" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="{e(site['name'])}">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-192.png">
<style>
{fonts}
:root {{
  color-scheme: light;
  --bg: #f6f5f1; --panel: #ffffff; --ink: #1c1f24; --muted: #5d6470; --line: #dedcd5; --chip: #efeee9;
  --link: #1d5fd1; --grid: rgba(28, 31, 36, 0.045); --shadow: 0 1px 2px rgba(20, 22, 26, 0.06), 0 6px 18px rgba(20, 22, 26, 0.06);
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    color-scheme: dark;
    --bg: #16181d; --panel: #1e2128; --ink: #e8eaee; --muted: #a0a7b3; --line: #2f333c; --chip: #262a32;
    --link: #7aa7ff; --grid: rgba(232, 234, 238, 0.04); --shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --bg: #16181d; --panel: #1e2128; --ink: #e8eaee; --muted: #a0a7b3; --line: #2f333c; --chip: #262a32;
  --link: #7aa7ff; --grid: rgba(232, 234, 238, 0.04); --shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}}
* {{ box-sizing: border-box; }}
[hidden] {{ display: none !important; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{
  margin: 0; background: var(--bg); color: var(--ink);
  font: 15px/1.5 'IBM Plex Sans', system-ui, sans-serif;
  background-image: linear-gradient(var(--grid) 1px, transparent 1px), linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 24px 24px;
}}
.wrap {{ max-width: 1240px; margin: 0 auto; padding: max(28px, env(safe-area-inset-top)) max(16px, env(safe-area-inset-right)) 40px max(16px, env(safe-area-inset-left)); }}
header {{ display: flex; gap: 16px; align-items: center; flex-wrap: wrap; margin-bottom: 8px; }}
header .mark {{ width: 52px; height: 52px; border-radius: 12px; flex: none; }}
header .titles {{ flex: 1 1 320px; min-width: 0; }}
h1 {{ font: 600 30px/1.1 'IBM Plex Sans Condensed', 'IBM Plex Sans', sans-serif; margin: 0; letter-spacing: 0.2px; }}
.tag {{ margin: 4px 0 0; color: var(--muted); }}
.tools {{ display: flex; gap: 8px; align-items: center; }}
.search {{ position: relative; }}
.search svg {{ position: absolute; left: 10px; top: 50%; width: 16px; height: 16px; transform: translateY(-50%); }}
.search input {{
  width: 220px; max-width: 100%; height: 38px; padding: 0 12px 0 34px; border-radius: 8px; border: 1px solid var(--line);
  background: var(--panel); color: var(--ink); font: inherit;
}}
.theme {{ height: 38px; width: 38px; border-radius: 8px; border: 1px solid var(--line); background: var(--panel); color: var(--ink); cursor: pointer; display: grid; place-items: center; padding: 0; }}
.theme svg {{ width: 18px; height: 18px; }}
svg {{ fill: none; stroke: currentColor; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }}
.facts {{ display: flex; flex-wrap: wrap; gap: 6px 18px; margin: 18px 0 6px; padding: 0; list-style: none; color: var(--muted); font-size: 13.5px; }}
.facts li {{ display: flex; align-items: center; gap: 7px; }}
.facts svg {{ width: 16px; height: 16px; color: var(--ink); }}
h2 {{ font: 600 13px/1 'IBM Plex Sans Condensed', sans-serif; letter-spacing: 1.2px; text-transform: uppercase; color: var(--muted); margin: 30px 0 12px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); gap: 16px; }}
.card {{
  --c: var(--tool); display: flex; flex-direction: column; background: var(--panel); border: 1px solid var(--line);
  border-top: 3px solid var(--c); border-radius: 10px; overflow: hidden; box-shadow: var(--shadow); min-width: 0;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) .card {{ --c: var(--tool-dark); }} }}
:root[data-theme="dark"] .card {{ --c: var(--tool-dark); }}
.shot {{ display: block; aspect-ratio: 16 / 10; overflow: hidden; border-bottom: 1px solid var(--line); background: var(--chip); }}
.shot img {{ width: 100%; height: 100%; object-fit: cover; object-position: top left; transition: transform 0.25s ease; }}
.card:hover .shot img {{ transform: scale(1.02); }}
.only-dark {{ display: none; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) .only-dark {{ display: block; }} :root:not([data-theme="light"]) .only-light {{ display: none; }} }}
:root[data-theme="dark"] .only-dark {{ display: block; }} :root[data-theme="dark"] .only-light {{ display: none; }}
.body {{ padding: 14px 16px 16px; display: flex; flex-direction: column; flex: 1; }}
.card h3 {{ display: flex; align-items: center; gap: 10px; margin: 0 0 6px; font: 600 19px/1.2 'IBM Plex Sans Condensed', sans-serif; }}
.card h3 img {{ border-radius: 6px; flex: none; }}
.card h3 a {{ color: inherit; text-decoration: none; }}
.card p {{ margin: 0 0 10px; color: var(--muted); font-size: 14px; }}
.labs {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 14px; padding: 0; list-style: none; }}
.labs li {{ font: 400 12px/1 'IBM Plex Mono', monospace; padding: 5px 7px; border-radius: 5px; background: var(--chip); color: var(--ink); }}
.actions {{ display: flex; gap: 8px; margin-top: auto; }}
.actions a {{ display: inline-flex; align-items: center; gap: 6px; height: 34px; padding: 0 14px; border-radius: 7px; font-weight: 600; font-size: 14px; text-decoration: none; }}
.actions svg {{ width: 14px; height: 14px; stroke-width: 1.8; }}
.open {{ background: var(--c); color: #fff; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) .open {{ color: #12141a; }} }}
:root[data-theme="dark"] .open {{ color: #12141a; }}
.src {{ color: var(--ink); border: 1px solid var(--line); }}
.actions a:hover {{ filter: brightness(1.08); }}
a:focus-visible, button:focus-visible, input:focus-visible {{ outline: 2px solid var(--link); outline-offset: 2px; }}
.none {{ color: var(--muted); padding: 30px 0; }}
footer {{ margin-top: 40px; padding-top: 18px; border-top: 1px solid var(--line); color: var(--muted); font-size: 13.5px; display: grid; gap: 8px; }}
footer p {{ margin: 0; max-width: 820px; }}
footer a {{ color: var(--link); }}
@media (max-width: 560px) {{
  h1 {{ font-size: 25px; }}
  .tools, .search, .search input {{ width: 100%; }}
  .search {{ flex: 1; }}
  .grid {{ grid-template-columns: 1fr; }}
}}
</style>
<script>try {{ const t = localStorage.getItem('bench-theme'); if (t) document.documentElement.dataset.theme = t; }} catch (_) {{}}</script>
</head><body>
<div class="wrap">
<header>
  <img class="mark" src="icon-192.png" alt="">
  <div class="titles"><h1>{e(site['name'])}</h1><p class="tag">{e(site['tagline'])}</p></div>
  <div class="tools">
    <label class="search"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="4.5"/><path d="m10.5 10.5 3.5 3.5"/></svg>
      <input id="q" type="search" placeholder="Find a tool or topic" aria-label="Find a tool or topic" autocomplete="off"></label>
    <button class="theme" id="theme" type="button" aria-label="Switch light or dark" title="Switch light or dark">
      <svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="5.5"/><path d="M8 2.5v11a5.5 5.5 0 0 0 0-11z" fill="currentColor"/></svg></button>
  </div>
</header>
<ul class="facts">
  <li><svg viewBox="0 0 16 16"><path d="M3 8.5 6.5 12 13 4.5"/></svg>Checked against textbook closed-form answers</li>
  <li><svg viewBox="0 0 16 16"><path d="M2 9.5h12M4 9.5V6h8v3.5M5 12.5h6"/></svg>Show the math: equations with your numbers in</li>
  <li><svg viewBox="0 0 16 16"><rect x="4" y="1.5" width="8" height="13" rx="1.5"/><path d="M7 12h2"/></svg>Phone, tablet or desktop; installable</li>
  <li><svg viewBox="0 0 16 16"><path d="M2 6.5a9 9 0 0 1 12 0M4.5 9a5.5 5.5 0 0 1 7 0M2 2l12 12"/></svg>Works offline; no account, no download</li>
</ul>
<main id="list">{sections}<p class="none" id="none" hidden>No tool matches that. Try a topic like "spring", "heat" or "fatigue".</p></main>
<footer>
  <p>Each tool is a single self-contained page: your work stays in your browser, files save to your device, nothing is sent anywhere. Every model is tested against independent hand or textbook answers before release; each tool's Method note states what it solves and its limits.</p>
  <p>To keep a tool on an iPad or phone, open it, then Safari &rarr; Share &rarr; Add to Home Screen. It then opens full screen and works offline.</p>
  <p><a href="https://github.com/{site['owner']}">github.com/{site['owner']}</a></p>
</footer>
</div>
<script>
(() => {{
  const q = document.getElementById('q'), none = document.getElementById('none');
  q.addEventListener('input', () => {{
    const words = q.value.toLowerCase().trim().split(/\\s+/).filter(Boolean);
    let shown = 0;
    document.querySelectorAll('.group').forEach(g => {{
      let n = 0;
      g.querySelectorAll('.card').forEach(c => {{ const ok = words.every(w => c.dataset.words.includes(w)); c.hidden = !ok; n += ok; }});
      g.hidden = !n; shown += n;
    }});
    none.hidden = shown > 0;
  }});
  const root = document.documentElement;
  document.getElementById('theme').addEventListener('click', () => {{
    const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark';
    try {{ localStorage.setItem('bench-theme', root.dataset.theme); }} catch (_) {{}}
  }});
  const standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  if (standalone) document.querySelectorAll('.card a').forEach(a => a.target = '_blank');
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js', {{ scope: './' }}).catch(() => {{}});
}})();
</script>
</body></html>
'''

if os.path.isdir('docs'):
    shutil.rmtree('docs')
os.makedirs('docs/icons'); os.makedirs('docs/shots')
open('docs/index.html', 'w').write(page)
for t in tools:
    shutil.copy(f"icons/{t['slug']}.svg", 'docs/icons/')
    for s in ('light', 'dark'):
        shutil.copy(f"shots/{t['slug']}-{s}.webp", 'docs/shots/')
for n in (180, 192, 512):
    shutil.copy(f'web/icon-{n}.png', 'docs/')
open('docs/.nojekyll', 'w').close()

manifest = {'name': site['name'], 'short_name': site['name'], 'description': site['tagline'], 'start_url': './', 'scope': './',
            'display': 'standalone', 'background_color': '#16181d', 'theme_color': '#16181d',
            'icons': [{'src': f'icon-{n}.png', 'sizes': f'{n}x{n}', 'type': 'image/png', 'purpose': 'any'} for n in (192, 512)]}
open('docs/manifest.webmanifest', 'w').write(json.dumps(manifest, indent=1))

# Service worker: precaches the launcher's own files only and answers only for those paths, so the
# tools under /<slug>/ (each with its own worker and narrower scope) are never intercepted.
files = ['./', 'index.html', 'manifest.webmanifest', 'icon-180.png', 'icon-192.png', 'icon-512.png'] + \
        [f"icons/{t['slug']}.svg" for t in tools] + [f"shots/{t['slug']}-{s}.webp" for t in tools for s in ('light', 'dark')]
h = hashlib.sha1()
for f in sorted(os.listdir('docs')) + [f'icons/{x}' for x in sorted(os.listdir('docs/icons'))] + [f'shots/{x}' for x in sorted(os.listdir('docs/shots'))]:
    if os.path.isfile('docs/' + f): h.update(f.encode()); h.update(open('docs/' + f, 'rb').read())
build = h.hexdigest()[:10]
open('docs/sw.js', 'w').write(f'''// Offline cache for the launcher page. Only the launcher's own files are served from here.
const CACHE = 'bench-hub-{build}';
const FILES = {json.dumps(files)};
const OWN = new Set(FILES.map(f => new URL(f, self.registration.scope).pathname));
self.addEventListener('install', e => {{ e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); }});
self.addEventListener('activate', e => {{
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('bench-hub-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
}});
self.addEventListener('fetch', e => {{
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== self.location.origin || !OWN.has(u.pathname)) return;
  e.respondWith(caches.open(CACHE).then(async c => {{
    const hit = await c.match(e.request, {{ ignoreSearch: true }});
    const net = fetch(e.request).then(r => {{ if (r.ok) c.put(e.request, r.clone()); return r; }}).catch(() => hit);
    return hit || net;
  }}));
}});
''')

# READMEs: this repo's, and the profile README for github.com/<owner>/<owner>.
def table(img_base):
    rows = []
    for g in groups:
        rows.append(f"\n### {g['name']}\n\n| | Tool | What it does |\n|---|---|---|")
        for t in tools:
            if t['group'] == g['id']:
                rows.append(f"| <img src=\"{img_base}icons/{t['slug']}.svg\" width=\"40\" alt=\"\"> | **[{t['name']}]({t['url']})**<br>[source]({t['repo']}) | {t['blurb']} |")
    return '\n'.join(rows)

about = ('Every tool is one self-contained HTML page: no account, no install, nothing sent anywhere, and it works offline once opened. '
         'Most have a **Show the math** view with the equations and your numbers, and every model is tested against '
         'independent textbook or closed-form answers before release. On an iPad or phone: open a tool, then Share → Add to Home Screen.')

open('profile/README.md', 'w').write(f'''## {site['name']}

Engineering calculators and simulators that run in the browser. **Browse them all: [{site['url'].replace('https://', '').rstrip('/')}]({site['url']})**

{about}
{table(site['url'])}
''')

open('README.md', 'w').write(f'''# {site['name']}

The launcher page for the bench tools: **{site['url']}**

{about}
{table('docs/')}

## How this site is built

- `tools.json` is the list: name, group, accent colors, blurb and labs for each tool. Add a tool there.
- `refresh.py` copies each tool's icon and takes light and dark preview shots from the sibling tool folders (needs Playwright).
- `build.py` writes the site to `docs/` (GitHub Pages serves that folder), this README and the profile README.
- `tests/browser_test.py` checks the page in light, dark, iPad and phone widths.
- The site's offline service worker answers only for the launcher's own files, so it never gets in the way of the tools under `/<tool>/`.
- Fonts: IBM Plex, SIL Open Font License (`fonts/OFL.txt`).
''')
print('built docs/ (build', build + '),', len(page), 'bytes; README.md, profile/README.md')
