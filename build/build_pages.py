# Builds shopify-training/sitemap.html + modules.html from live-store data dumps
# and injects the shared tab nav into all three pages. Reuses index.html's
# inline stylesheet so every page stays self-contained and visually identical.
import base64, json, re, html, os

SCRATCH = os.path.dirname(os.path.abspath(__file__))  # data snapshots live beside this script
OUT = os.path.dirname(SCRATCH)  # pages sit one level up from build/ — works in this repo
                                # (shopify-training/) and in the deploy repo (its root)
MANUAL = os.path.join(OUT, 'index.html')

index_src = open(MANUAL, encoding='utf-8').read()
style = re.search(r'(<style>.*?</style>)', index_src, re.S).group(1)

TAB_CSS = """
    .tab-nav { background: var(--ink); border-bottom: 3px solid var(--accent); }
    .tab-nav .inner { max-width: 76em; margin: 0 auto; padding: 0 1.4em; display: flex; gap: 0.4em; }
    .tab-nav a { color: #cdd6e2; text-decoration: none; padding: 0.75em 1.1em; font-size: 0.86em; font-weight: 600; letter-spacing: 0.02em; border-bottom: 3px solid transparent; margin-bottom: -3px; }
    .tab-nav a:hover { color: #fff; }
    .tab-nav a[aria-current] { color: #fff; border-bottom-color: var(--accent); background: rgba(255,255,255,0.06); }
    @media print { .tab-nav { display: none; } }
"""

def tab_nav(current):
    tabs = [('index.html', 'CMS Manual'), ('modules.html', 'Module Guide'),
            ('pdp-guide.html', 'PDP Guide'),
            ('collections-filtering.html', 'Collections &amp; Filtering'),
            ('supplying-content.html', 'Supplying Content'),
            ('catalogue-audit.html', 'Catalogue Audit'),
            ('sku-checklist.html', 'SKU Checklist')]
    cur_attr = ' aria-current="page"'
    links = ''.join(
        f'<a href="{href}"{cur_attr if href == current else ""}>{label}</a>'
        for href, label in tabs)
    return f'  <nav class="tab-nav"><div class="inner">{links}</div></nav>\n'

def esc(s): return html.escape(str(s or ''))

# ---------------------------------------------------------------- data
menus = json.load(open(f'{SCRATCH}/menus.json'))['menus']['nodes']
pages = json.load(open(f'{SCRATCH}/all-pages.json'))
cols = json.load(open(f'{SCRATCH}/collections.json'))
mods = json.load(open(f'{SCRATCH}/modules.json'))

LIVE = 'https://arbortechtools.com'

def menu_tree(items, depth=0):
    out = '<ul class="site-tree">' if depth == 0 else '<ul>'
    for i in items:
        url = i['url'] or ''
        link = f'<a href="{esc(LIVE + url)}">{esc(i["title"])}</a>' if url.startswith('/') else esc(i['title'])
        path = f' <code>{esc(url)}</code>' if url.startswith('/') else ''
        out += f'<li>{link}{path}'
        if i.get('items'):
            out += menu_tree(i['items'], depth + 1)
        out += '</li>'
    return out + '</ul>'

main_menu = next(m for m in menus if m['handle'] == 'main-menu')

# ---- page inventory grouping
def page_group(p):
    s = p['templateSuffix'] or ''
    if s == 'artist': return 'Artist profile pages'
    if s == 'arbt-tool-resource': return 'Tool resource pages'
    if s.startswith('arbt-power-carve'): return 'Power-carving landing pages'
    if s in ('woodworking', 'masonry', 'landscaping'): return 'Vertical landing pages'
    if s in ('spoon-and-bowl-carving','furniture-and-sculpting','detail-and-texturing','tuckpointing-and-repointing','brick-and-block-repair','heritage-masonry-repairs','timber-landscaping','turf-and-grounds-care','edging-and-trenches','shop-by-project'): return 'Shop-by-project pages'
    if s == '': return 'Standard pages'
    return 'One-off designed pages'

groups = {}
for p in sorted(pages, key=lambda x: x['title'].lower()):
    groups.setdefault(page_group(p), []).append(p)

GROUP_NOTES = {
    'Standard pages': 'Default template – the rich-text Content box renders. These are yours to edit freely (Manual §3.1).',
    'Artist profile pages': 'One per artist, all on the <code>artist</code> template. The portrait, pull-quote, tools and techniques come from artist metafields – those are a call-us item. The bio is different: it is the page\'s own rich-text Content box, so artist bios are yours to edit (Manual §3.1).',
    'Tool resource pages': 'One per tool, on the <code>arbt-tool-resource</code> template – manuals, videos and FAQs pulled from structured data. The Content box is not rendered on these pages: editing it changes nothing on the storefront.',
    'Power-carving landing pages': 'Bespoke designed template per tool – layout lives in the theme, call us for changes. The Content box is not rendered on these pages: editing it changes nothing on the storefront.',
    'Vertical landing pages': 'The three audience gateways (Woodworking / Masonry &amp; Trade / Landscaping) – bespoke templates. The Content box is not rendered on these pages: editing it changes nothing on the storefront.',
    'Shop-by-project pages': 'Project-led shopping pages, one bespoke template each. The Content box is not rendered on these pages: editing it changes nothing on the storefront.',
    'One-off designed pages': 'Each has its own designed template (About, Support, Inspiration, Events, Stories, etc.), built from theme sections. The Content box is not rendered on these pages: editing it changes nothing on the storefront – ask us for text or layout changes. The one exception is the German Widerrufsrecht page, which is entirely its Content box.',
}

sitemap_body = f"""
    <div class="article">
      <h2 id="how-to-read">How to read this page</h2>
      <p>This is the structural map of <strong>arbortechtools.com</strong> – what exists, where it lives in the navigation, and which admin screen each thing is edited from. Every URL below is the Australian (root) address; the same page exists automatically under each market prefix (<code>/en-us</code>, <code>/en-ca</code>, <code>/en-uk</code>, <code>/de-de</code>, <code>/en-de</code>).</p>
      <table>
        <thead><tr><th>Content kind</th><th>Where you edit it</th></tr></thead>
        <tbody>
          <tr><td>Pages</td><td><strong>Online Store → Pages</strong> (Manual §3.1–3.2)</td></tr>
          <tr><td>Products</td><td><strong>Products</strong> (Manual §2)</td></tr>
          <tr><td>Collections</td><td><strong>Products → Collections</strong> (Manual §2.4)</td></tr>
          <tr><td>Blog posts</td><td><strong>Online Store → Blog posts</strong> (Manual §3.3)</td></tr>
          <tr><td>The navigation itself</td><td><strong>Online Store → Navigation</strong> (Manual §4)</td></tr>
        </tbody>
      </table>

      <h2 id="nav-structure">1. The storefront, as the main menu presents it</h2>
      <p>This mirrors the live <strong>main menu</strong> – the mega-nav your customers use. Indentation = menu nesting.</p>
      {menu_tree(main_menu['items'])}
      <div class="callout info"><div class="callout-title">Remember</div>
      <p>This tree is <em>navigation</em>, not the full page list – a page can exist without being linked here (and is then invisible to customers). The full inventory is below.</p></div>

      <h2 id="collections">2. Collections ({len(cols['collections']['nodes'])})</h2>
      <table>
        <thead><tr><th>Collection</th><th>URL</th><th>Products</th></tr></thead>
        <tbody>
"""
for c in cols['collections']['nodes']:
    sitemap_body += f"          <tr><td>{esc(c['title'])}</td><td><code>/collections/{esc(c['handle'])}</code></td><td>{c['productsCount']['count']}</td></tr>\n"
sitemap_body += f"""        </tbody>
      </table>
      <p>Plus <code>/collections/all</code> (Shop All – every active product). The vertical collections (Woodworking, Masonry &amp; Trade, Landscaping) are <em>smart</em> collections driven by tags – products join them via tagging, not manual lists (Manual §2.4).</p>

      <h2 id="blog">3. The News blog</h2>
      <p><code>/blogs/news</code> – <strong>{sum(1 for p in pages if False) or 65} articles</strong>, including the designed story articles and their per-market copies (handles prefixed <code>story-au-</code>, <code>story-us-</code>, <code>story-uk-</code>, <code>story-ca-</code>, <code>story-de-</code>). See Manual §3.3 for what is and isn't editable on story articles.</p>

      <h2 id="page-inventory">4. Full page inventory ({len(pages)} pages)</h2>
      <p>Everything under <strong>Online Store → Pages</strong>, grouped by what kind of page it is. The kind matters because it decides how editable the page is.</p>
"""
order = ['Standard pages', 'One-off designed pages', 'Vertical landing pages', 'Shop-by-project pages',
         'Power-carving landing pages', 'Tool resource pages', 'Artist profile pages']
for g in order:
    plist = groups.get(g, [])
    if not plist: continue
    sitemap_body += f"      <h3>{esc(g)} ({len(plist)})</h3>\n      <p>{GROUP_NOTES[g]}</p>\n      <p class=\"page-list\">"
    sitemap_body += ' · '.join(
        f'<a href="{LIVE}/pages/{esc(p["handle"])}">{esc(p["title"])}</a>' + ('' if p['isPublished'] else ' <em>(draft)</em>')
        for p in plist)
    sitemap_body += "</p>\n"

sitemap_body += """
      <h2 id="markets">5. Markets – the same site, five addresses</h2>
      <table>
        <thead><tr><th>Market</th><th>Prefix</th><th>Currency</th></tr></thead>
        <tbody>
          <tr><td>Australia (primary)</td><td><code>/</code></td><td>AUD</td></tr>
          <tr><td>United States</td><td><code>/en-us</code></td><td>USD</td></tr>
          <tr><td>Canada</td><td><code>/en-ca</code></td><td>CAD</td></tr>
          <tr><td>United Kingdom</td><td><code>/en-uk</code></td><td>GBP</td></tr>
          <tr><td>Germany</td><td><code>/de-de</code> (+ <code>/en-de</code>)</td><td>EUR</td></tr>
        </tbody>
      </table>
      <p>You never create market copies of a page – Shopify serves every page at every prefix automatically. German <em>text</em> comes from Translate &amp; Adapt (Manual §10).</p>
    </div>
"""

# ---------------------------------------------------------------- modules
PURPOSES = json.load(open(f'{SCRATCH}/module_purposes.json'))
mod_by_type = {m['type']: m for m in mods}

def content_model(m):
    bits = []
    n = len(m['settings'])
    if n:
        labels = [s['label'] or s['id'] for s in m['settings'][:6]]
        bits.append(f"<strong>Settings ({n}):</strong> {esc(', '.join(labels))}{'…' if n > 6 else ''}")
    if m['blocks']:
        bl = ', '.join(f"{esc(b['name'] or b['type'])}" for b in m['blocks'])
        bits.append(f"<strong>Repeatable blocks:</strong> {bl}")
    if m['metafield_hits']:
        mf = ', '.join(f"<code>{esc(h)}</code>" for h in m['metafield_hits'][:3])
        bits.append(f"<strong>Data source:</strong> {mf}")
    return ' &nbsp;·&nbsp; '.join(bits) or '<strong>Settings:</strong> none – fully data-driven.'

# Live-storefront screenshots captured 2026-08-06 (see prep_module_screenshots.py).
# Any build/screenshots/modules/<type>.jpg is embedded under its module entry.
SHOTS_DIR = os.path.join(SCRATCH, 'screenshots', 'modules')

NO_SHOT_NOTES = {
    'arb-testimonials': 'No screenshot – no product currently has testimonial content entered, so this module renders nothing on the live site yet.',
    'arbt-blade-compat': 'No screenshot – this module is deliberately hidden pending design review; once enabled it renders the "Compatible tools" cards on accessory pages.',
    'arbt-accessory-hub': 'No screenshot – its collection (Spare Parts, Blades &amp; Accessories) is not yet published to the Online Store, so its page currently returns a 404.',
}

def module_shot(t):
    p = os.path.join(SHOTS_DIR, t + '.jpg')
    if os.path.exists(p):
        b64 = base64.b64encode(open(p, 'rb').read()).decode('ascii')
        return (f'      <figure class="screenshot"><img src="data:image/jpeg;base64,{b64}" '
                f'alt="The {esc(t)} module as rendered on the storefront" loading="lazy">'
                f'<figcaption>As it renders on the storefront.</figcaption></figure>\n')
    note = NO_SHOT_NOTES.get(t)
    return f'      <p style="font-size:0.86em"><em>{note}</em></p>\n' if note else ''

modules_body = """
    <div class="article">
      <h2 id="about-modules">What a "module" is</h2>
      <p>Every page on the storefront is assembled from <strong>theme sections</strong> – we call them modules. In <strong>Online Store → Themes → Customize</strong>, the left-hand panel lists the modules on the current page; <strong>Add section</strong> offers the library below. Each module has <em>settings</em> (fields you fill in) and some have <em>repeatable blocks</em> (items you add, remove and drag to reorder – cards, slides, FAQ items).</p>
      <div class="callout warn"><div class="callout-title">Two kinds of content</div>
      <p>Some modules hold their content <em>in their settings</em> – what you type in the theme editor is what renders. Others are <em>data-driven</em>: they pull from products, metafields or metaobjects, and their settings only control headings and layout. The "Data source" line on each entry tells you which – for data-driven modules, edit the data (product, metafield, metaobject), not the module.</p></div>
      <div class="callout info"><div class="callout-title">Theme edits are per-theme</div>
      <p>Module settings live in the theme. Editing the live theme changes the live site immediately; and a rebuilt preview theme starts from the development copy's settings (Manual §5).</p></div>
"""
cur_group = None
for entry in PURPOSES['entries']:
    if entry['group'] != cur_group:
        cur_group = entry['group']
        gid = re.sub(r'[^a-z0-9]+', '-', cur_group.lower()).strip('-')
        modules_body += f"      <h2 id=\"{gid}\">{esc(cur_group)}</h2>\n"
        note = PURPOSES['group_notes'].get(cur_group)
        if note: modules_body += f"      <p>{note}</p>\n"
    m = mod_by_type.get(entry['type'])
    if not m:
        raise SystemExit(f"unknown module type {entry['type']}")
    used = len(m['used_in'])
    name = m['name'] if not m['name'] or not m['name'].startswith('PARSE') else entry['type']
    usage_note = entry.get('usage') or (f"used on {used} template{'s' if used != 1 else ''}" if used else 'not currently placed on any page')
    modules_body += f"""      <h3>{esc(name)} <code style="font-weight:400;font-size:0.72em">{esc(entry['type'])}</code></h3>
      <p>{entry['purpose']} <em>({esc(usage_note)}.)</em></p>
      <p style="font-size:0.86em">{content_model(m)}</p>
"""
    modules_body += module_shot(entry['type'])

modules_body += """
      <h2 id="base-modules">Base theme modules</h2>
      <p>These ship with the underlying theme and run the structural pages. They rarely need touching, and several are safest left to us:</p>
      <table>
        <thead><tr><th>Module</th><th>Role</th></tr></thead>
        <tbody>
          <tr><td><code>header</code> + announcement bar</td><td>The site header, mega-menus (linked to the main menu + promo image blocks – Manual §4) and the optional announcement strip.</td></tr>
          <tr><td><code>main-product</code> family</td><td>Base product page engine – superseded on this store by the custom Main Product module.</td></tr>
          <tr><td><code>main-collection</code></td><td>Collection listing with the custom filter sidebar (Vertical + By Product groups).</td></tr>
          <tr><td><code>main-page</code> / <code>main-blog</code> / <code>main-article</code></td><td>Render standard pages, the News listing, and articles (including the designed story layouts).</td></tr>
          <tr><td><code>main-cart</code> / drawers / <code>main-search</code></td><td>Cart page, cart &amp; search drawers.</td></tr>
          <tr><td><code>main-not-found</code></td><td>The 404 page (it also rescues old <code>/en-au</code> links – don't remove).</td></tr>
          <tr><td><code>newsletter-popup</code>, <code>privacy-banner</code></td><td>Signup popup and the cookie/consent banner.</td></tr>
          <tr><td><code>rich-text</code>, <code>related-products</code>, <code>contact</code></td><td>Generic text band, product recommendations, and the contact form (submissions go to the store contact inbox).</td></tr>
        </tbody>
      </table>
    </div>
"""

EXTRA_CSS = TAB_CSS + """
    .site-tree, .site-tree ul { list-style: none; padding-left: 1.1em; border-left: 2px solid var(--line); margin: 0.4em 0; }
    .site-tree { border-left: 0; padding-left: 0; }
    .site-tree li { margin: 0.34em 0; font-size: 0.92em; }
    .site-tree code { color: var(--muted); font-size: 0.82em; }
    .page-list { line-height: 2; }
  """
page_style = style.replace('</style>', EXTRA_CSS + '</style>')

def page_shell(title, kicker, sub, body, current):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  {page_style}
</head>
<body>

{tab_nav(current)}
  <header class="page-header">
    <div class="inner">
      <span class="kicker">{kicker}</span>
      <h1>{sub}</h1>
    </div>
  </header>

  <div class="page-layout">
{body}
  </div>

</body>
</html>
"""

open(os.path.join(OUT, 'sitemap.html'), 'w', encoding='utf-8').write(
    page_shell('Arbortech – Site Map', 'Personalised CMS Manual · Site Map',
               '<span class="brand">Arbortech</span> – What\'s On the Site, and Where It Lives', sitemap_body, 'sitemap.html'))
open(os.path.join(OUT, 'modules.html'), 'w', encoding='utf-8').write(
    page_shell('Arbortech – Module Guide', 'Personalised CMS Manual · Module Usage Guide',
               '<span class="brand">Arbortech</span> – Theme Modules: What Each One Is For', modules_body, 'modules.html'))

# inject tab nav into index.html (idempotent)
if 'tab-nav' not in index_src:
    index_src = index_src.replace('<body>\n', '<body>\n\n' + tab_nav('index.html'), 1)
    index_src = index_src.replace('</style>', TAB_CSS + '  </style>', 1)
    open(MANUAL, 'w', encoding='utf-8').write(index_src)
print('built sitemap.html + modules.html, tab nav injected')
