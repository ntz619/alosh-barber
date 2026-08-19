from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

css_tag = '  <link rel="stylesheet" href="price-icon-scale.css?v=1">'
if css_tag not in html:
    marker = '  <link rel="stylesheet" href="styles.css?v=20260819-icons6">'
    if marker not in html:
        raise SystemExit('Expected main stylesheet tag not found')
    html = html.replace(marker, marker + '\n' + css_tag, 1)

js_tag = '  <script src="gender-scroll-fix.js?v=1" defer></script>'
if js_tag not in html:
    marker = '  <script src="script.js" defer></script>'
    if marker not in html:
        raise SystemExit('Expected main script tag not found')
    html = html.replace(marker, marker + '\n' + js_tag, 1)

path.write_text(html, encoding='utf-8')
