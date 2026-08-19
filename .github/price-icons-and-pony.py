from pathlib import Path
import re

index_path = Path('index.html')
styles_path = Path('styles.css')

html = index_path.read_text(encoding='utf-8')
css = styles_path.read_text(encoding='utf-8')

# Ponyschnitt should use the same length-row structure as the surrounding services,
# with its single price occupying the Kurz column only.
html = html.replace(
    '<div class="price-simple-row price-simple-in-table"><span>Ponyschnitt</span><strong>10 €</strong></div>',
    '''<div class="price-length-row">\n                  <span class="price-service">Ponyschnitt</span>\n                  <span class="price-cell"><small>Kurz</small><strong>10 €</strong></span>\n                </div>''',
    1
)

icons = {
    'Haare &amp; Styling': '<svg viewBox="0 0 24 24"><circle cx="6" cy="7" r="2.5"/><circle cx="6" cy="17" r="2.5"/><path d="M8.2 8.4 20 3M8.2 15.6 20 21M9 10l11 11M9 14 20 3"/></svg>',
    'Bart': '<svg viewBox="0 0 24 24"><path d="M5.5 8.5c.7-3.6 2.8-5.5 6.5-5.5s5.8 1.9 6.5 5.5c1 5.1-.4 9.7-6.5 12.5-6.1-2.8-7.5-7.4-6.5-12.5Z"/><path d="M8 10c2.4 1.4 5.6 1.4 8 0M9 15c2 1.2 4 1.2 6 0"/></svg>',
    'Kosmetik': '<svg viewBox="0 0 24 24"><path d="M2.5 12s3.7-5 9.5-5 9.5 5 9.5 5-3.7 5-9.5 5-9.5-5-9.5-5Z"/><circle cx="12" cy="12" r="2.4"/></svg>',
    'Kinder': '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.5"/><path d="M5.5 21c.7-5 2.9-8 6.5-8s5.8 3 6.5 8M8.5 5.5c1.7-2.2 5.3-2.2 7 0"/></svg>',
    'Kostenlose Extras': '<svg viewBox="0 0 24 24"><path d="m12 2 1.3 4.1L17 8l-3.7 1.9L12 14l-1.3-4.1L7 8l3.7-1.9L12 2Z"/><path d="m19 13 .8 2.4L22 16.5l-2.2 1.1L19 20l-.8-2.4-2.2-1.1 2.2-1.1L19 13ZM5 14l.8 2.1L8 17l-2.2.9L5 20l-.8-2.1L2 17l2.2-.9L5 14Z"/></svg>',
    'Schnitt &amp; Styling': '<svg viewBox="0 0 24 24"><circle cx="6" cy="7" r="2.5"/><circle cx="6" cy="17" r="2.5"/><path d="M8.2 8.4 20 3M8.2 15.6 20 21M9 10l11 11M9 14 20 3"/></svg>',
    'Farbe': '<svg viewBox="0 0 24 24"><path d="M12 2.5S5.5 10 5.5 15a6.5 6.5 0 0 0 13 0C18.5 10 12 2.5 12 2.5Z"/></svg>',
    'Blond &amp; Highlights': '<svg viewBox="0 0 24 24"><path d="m12 2 1.4 5.6L18 10l-4.6 2.4L12 18l-1.4-5.6L6 10l4.6-2.4L12 2Z"/><path d="m19 3 .6 1.7L21 5.3l-1.4.6L19 7.5l-.6-1.6L17 5.3l1.4-.6L19 3Z"/></svg>',
    'Glättung &amp; Umformung': '<svg viewBox="0 0 24 24"><path d="M5 2.5c-4 3.8 4 5.3 0 9.5s4 5.7 0 9.5M12 2.5c-4 3.8 4 5.3 0 9.5s4 5.7 0 9.5M19 2.5c-4 3.8 4 5.3 0 9.5s4 5.7 0 9.5"/></svg>',
    'Pflege': '<svg viewBox="0 0 24 24"><path d="M20.5 3.5C12 3.5 5 7.4 4.5 16c4.1 1.7 7.8.2 10.8-2.8 3.8-3.4 4.6-6.7 5.2-9.7Z"/><path d="M3.5 21c3.2-6.2 7.5-10 14.2-14"/></svg>',
    'Hochzeit &amp; Specials': '<svg viewBox="0 0 24 24"><path d="m3.5 8 5 4.2L12 4l3.5 8.2 5-4.2-2.2 11H5.7L3.5 8Z"/><path d="M6 21h12"/></svg>',
}

for title, icon in icons.items():
    pattern = rf'(<div class="price-category-head"><span>)([^<]+)(</span><h3>{re.escape(title)}</h3></div>)'
    replacement = rf'\1{icon}\3'
    html, count = re.subn(pattern, replacement, html, count=1)
    if count != 1:
        raise RuntimeError(f'Could not replace category marker for {title}')

# Kosmetik and Kinder each occur a second time in the Damen list.
for title in ('Kosmetik', 'Kinder'):
    icon = icons[title]
    pattern = rf'(<div class="price-category-head"><span>)([^<]+)(</span><h3>{re.escape(title)}</h3></div>)'
    html, count = re.subn(pattern, rf'\1{icon}\3', html, count=1)
    if count != 1:
        raise RuntimeError(f'Could not replace second category marker for {title}')

marker = '/* Inline category SVGs - preserve number footprint */'
if marker not in css:
    css += '''\n\n/* Inline category SVGs - preserve number footprint */\n#services .price-category-head>span svg{\n  display:block;\n  width:1em;\n  height:1em;\n  fill:none;\n  stroke:currentColor;\n  stroke-width:1.55;\n  stroke-linecap:round;\n  stroke-linejoin:round;\n}\n'''

# Cache-bust only; no layout change.
html = re.sub(r'href="styles\.css(?:\?v=[^"]*)?"', 'href="styles.css?v=20260819-icons6"', html, count=1)

index_path.write_text(html, encoding='utf-8')
styles_path.write_text(css, encoding='utf-8')
