from pathlib import Path
import re

root = Path('.')
index_path = root / 'index.html'
s = index_path.read_text(encoding='utf-8')

style = re.search(r'\n\s*<style>\n(.*?)\n\s*</style>', s, re.S)
script = re.search(r'\n\s*<script>\n(.*?)\n\s*</script>', s, re.S)

if not style or not script:
    raise SystemExit('Expected inline <style> and <script> blocks in index.html')

css = style.group(1).strip() + '''\n\n/* Impressum */\n.legal-page{min-height:100svh;background:var(--cream);color:var(--ink);padding:calc(var(--header) + 48px) var(--pad) 72px}\n.legal-wrap{width:min(920px,100%);margin:0 auto}\n.legal-back{display:inline-flex;align-items:center;gap:10px;margin-bottom:36px;font-size:18px;color:#76552c}\n.legal-title{font:500 clamp(56px,9vw,110px)/.88 "Cormorant Garamond",serif;letter-spacing:-.035em;margin:0 0 30px}\n.legal-card{background:#fff;border:1px solid rgba(17,15,11,.09);border-radius:26px;padding:clamp(24px,5vw,48px);box-shadow:0 18px 55px rgba(13,10,5,.08)}\n.legal-card h2{font:500 clamp(32px,5vw,48px)/1 "Cormorant Garamond",serif;margin:32px 0 12px}\n.legal-card h2:first-child{margin-top:0}\n.legal-card p,.legal-card address{font:400 clamp(18px,2.2vw,22px)/1.55 Inter,system-ui,sans-serif;font-style:normal;margin:0;color:#504a42;overflow-wrap:anywhere}\n.legal-card a{color:#805d30;text-decoration:underline;text-underline-offset:3px}\n.legal-note{margin-top:26px;font-size:16px;line-height:1.5;color:#7a7167}\n@media (max-width:780px){.legal-page{padding-top:calc(var(--header) + 28px);padding-bottom:48px}.legal-back{margin-bottom:24px}.legal-card{border-radius:20px}}\n'''
js = script.group(1).strip() + '\n'

(root / 'styles.css').write_text(css, encoding='utf-8')
(root / 'script.js').write_text(js, encoding='utf-8')

s = s[:style.start()] + '\n  <link rel="stylesheet" href="styles.css">' + s[style.end():]
script2 = re.search(r'\n\s*<script>\n(.*?)\n\s*</script>', s, re.S)
s = s[:script2.start()] + '\n  <script src="script.js" defer></script>' + s[script2.end():]

footer_old = '''    <nav>\n      <a href="#services">Services</a>\n      <a href="#salon">Salon</a>\n      <a href="#reviews">Reviews</a>\n      <a href="#visit">Visit</a>\n    </nav>'''
footer_new = '''    <nav>\n      <a href="#services">Services</a>\n      <a href="#salon">Salon</a>\n      <a href="#reviews">Reviews</a>\n      <a href="#visit">Visit</a>\n      <a href="impressum.html">Impressum</a>\n    </nav>'''
if footer_old not in s:
    raise SystemExit('Footer navigation pattern not found')
s = s.replace(footer_old, footer_new, 1)
index_path.write_text(s, encoding='utf-8')

impressum = '''<!DOCTYPE html>\n<html lang="de">\n<head>\n  <meta charset="UTF-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n  <meta name="theme-color" content="#efe8dc" />\n  <meta name="robots" content="noindex" />\n  <title>Impressum — ALOSH</title>\n  <link rel="preconnect" href="https://fonts.googleapis.com">\n  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">\n  <link rel="stylesheet" href="styles.css">\n</head>\n<body>\n  <main class="legal-page">\n    <div class="legal-wrap">\n      <a class="legal-back" href="index.html#visit">← Zurück zur Website</a>\n      <h1 class="legal-title">Impressum</h1>\n      <section class="legal-card" aria-label="Beispiel-Impressum">\n        <h2>Angaben gemäß § 5 DDG</h2>\n        <address>\n          ALOSH Barber Rostock<br>\n          Max Mustermann<br>\n          Doberaner Str. 48<br>\n          18057 Rostock<br>\n          Deutschland\n        </address>\n\n        <h2>Kontakt</h2>\n        <p>\n          Telefon: <a href="tel:+4938176016450">0381 76016450</a><br>\n          E-Mail: <a href="mailto:beispiel@alosh-barber.de">beispiel@alosh-barber.de</a>\n        </p>\n\n        <h2>Umsatzsteuer-ID</h2>\n        <p>Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz: DE123456789</p>\n\n        <h2>Verantwortlich für den Inhalt</h2>\n        <p>Max Mustermann, Doberaner Str. 48, 18057 Rostock</p>\n\n        <h2>Verbraucherstreitbeilegung</h2>\n        <p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>\n      </section>\n      <p class="legal-note">Hinweis: Die Angaben auf dieser Seite sind derzeit Beispieldaten und müssen vor Veröffentlichung durch die echten Unternehmensdaten ersetzt werden.</p>\n    </div>\n  </main>\n</body>\n</html>\n'''
(root / 'impressum.html').write_text(impressum, encoding='utf-8')

# trigger workflow after it exists
