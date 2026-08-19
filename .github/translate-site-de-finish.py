from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

replacements = {
    '>Call 0381 76016450<': '>Anrufen: 0381 76016450<',
    'title="Google Maps location"': 'title="Standort in Google Maps"',
    'alt="Barber shop interior"': 'alt="Innenraum des Salons"',
    'alt="Haircut in progress"': 'alt="Haarschnitt während der Behandlung"',
    'alt="Barber tools and styling area"': 'alt="Barber-Werkzeuge und Stylingbereich"',
    'Blond &amp; Highlights': 'Blond &amp; Strähnen',
    'Hochzeit &amp; Specials': 'Hochzeit &amp; Extras',
}
for old, new in replacements.items():
    html = html.replace(old, new)

path.write_text(html, encoding='utf-8')
print('German translation cleanup applied.')
