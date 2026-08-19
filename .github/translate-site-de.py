from pathlib import Path

files = {
    'index.html': Path('index.html'),
    'script.js': Path('script.js'),
    'gender-scroll-fix.js': Path('gender-scroll-fix.js'),
}

html = files['index.html'].read_text(encoding='utf-8')
js = files['script.js'].read_text(encoding='utf-8')
addon = files['gender-scroll-fix.js'].read_text(encoding='utf-8')

html_replacements = {
    'ALOSH – Hair · Barber · Beauty. Elegante, kompakte Barber Landingpage mit flüssigen Scroll-Animationen.': 'ALOSH × VIVO in Rostock – Herren bei ALOSH, Damen bei VIVO. Haar, Kosmetik und Barber an einer gemeinsamen Adresse.',
    '<title>ALOSH — Hair · Barber · Beauty</title>': '<title>ALOSH × VIVO — Haar · Kosmetik · Barber</title>',
    'Hair · Barber · Beauty': 'Haar · Kosmetik · Barber',
    '>Reviews<': '>Bewertungen<',
    '>Visit<': '>Standort<',
    '>Book<': '>Termin<',
    'Barber experience in Rostock.': 'Friseur- und Barber-Erlebnis in Rostock.',
    'Cuts.<br>Beards.<br>Style.': 'Schnitt.<br>Bart.<br>Stil.',
    'Elegant atmosphere, precise work and a clean, premium finish. Built to feel strong on desktop and fast on mobile.': 'Elegante Atmosphäre, präzise Arbeit und ein hochwertiges Ergebnis – klar gestaltet für Desktop und Mobilgeräte.',
    '>Book Appointment<': '>Termin anfragen<',
    '>See Location<': '>Standort ansehen<',
    'aria-label="Basic salon info"': 'aria-label="Saloninformationen"',
    '>Opening hours<': '>Öffnungszeiten<',
    'Mon–Fri': 'Mo–Fr',
    '>Call us<': '>Anrufen<',
    '>Address<': '>Adresse<',
    '>Call now<': '>Jetzt anrufen<',
    '>Walk‑ins<': '>Ohne Termin<',
    'Welcome when free': 'Willkommen, wenn etwas frei ist',
    'Google reviews': 'Google-Bewertungen',
    'Tap for appointment': 'Termin anfragen',
    '<figcaption>Clean Fade</figcaption>': '<figcaption>Präziser Fade</figcaption>',
    '<figcaption>Texture</figcaption>': '<figcaption>Textur</figcaption>',
    '<figcaption>Classic</figcaption>': '<figcaption>Klassisch</figcaption>',
    '<figcaption>Cut + Beard</figcaption>': '<figcaption>Schnitt + Bart</figcaption>',
    '<figcaption>Soft Layers</figcaption>': '<figcaption>Weiche Stufen</figcaption>',
    '<figcaption>Soft Waves</figcaption>': '<figcaption>Weiche Wellen</figcaption>',
    '<figcaption>Modern Cut</figcaption>': '<figcaption>Moderner Schnitt</figcaption>',
    '<figcaption>Color + Style</figcaption>': '<figcaption>Farbe + Styling</figcaption>',
    '<h2 data-gender-price-title>Herren.</h2>': '<h2 data-gender-price-title>Herren</h2>',
    'Dark tones.<br>Warm light.': 'Dunkle Töne.<br>Warmes Licht.',
    'A calm space, warm lighting and a focused atmosphere designed around one thing: a great result.': 'Ein ruhiger Salon, warmes Licht und eine konzentrierte Atmosphäre – mit Fokus auf ein starkes Ergebnis.',
    'aria-label="Previous image"': 'aria-label="Vorheriges Bild"',
    'aria-label="Next image"': 'aria-label="Nächstes Bild"',
    '<figcaption>Interior atmosphere</figcaption>': '<figcaption>Salon-Atmosphäre</figcaption>',
    '<figcaption>Precise cutting</figcaption>': '<figcaption>Präziser Schnitt</figcaption>',
    '<figcaption>Tools & detail</figcaption>': '<figcaption>Werkzeuge & Details</figcaption>',
    '>TRUST<': '>VERTRAUEN<',
    'Customers<br>love it.': 'Unsere Kunden<br>lieben es.',
    'Clients come for the cut and return for the consistency, attention to detail and relaxed experience.': 'Unsere Kundinnen und Kunden kommen für das Ergebnis und bleiben wegen Präzision, Verlässlichkeit und entspannter Atmosphäre.',
    '“Super clean fade, calm atmosphere and the result looked exactly right.”': '„Sehr sauberer Fade, entspannte Atmosphäre und genau das Ergebnis, das ich wollte.“',
    '“Strong design, friendly team and every detail was done with real care.”': '„Starker Salon, freundliches Team und bei jedem Detail merkt man die Sorgfalt.“',
    '“Best barber appointment I had in a long time. Hair and beard both on point.”': '„Mein bester Barber-Termin seit Langem. Haare und Bart waren beide genau auf den Punkt.“',
    'aria-label="Previous review"': 'aria-label="Vorherige Bewertung"',
    'aria-label="Next review"': 'aria-label="Nächste Bewertung"',
    'Easy to visit.<br>Easy to book.': 'Leicht zu finden.<br>Einfach zu buchen.',
    'Find us in Rostock, choose a time that works for you and book your next appointment in just a moment.': 'Du findest uns in Rostock. Wähle dein Studio und kontaktiere direkt ALOSH oder VIVO für deinen nächsten Termin.',
    '>Saturday<': '>Samstag<',
    '>Sunday<': '>Sonntag<',
    '>Closed<': '>Geschlossen<',
    '>Open in Maps<': '>In Maps öffnen<',
    'aria-label="Google Maps location"': 'aria-label="Standort in Google Maps"',
}
for old, new in html_replacements.items():
    html = html.replace(old, new)

# German cache-bust for translated HTML-dependent assets.
html = html.replace('gender-scroll-fix.js?v=1', 'gender-scroll-fix.js?v=20260819-de1')

js_replacements = {
    "const dayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];": "const dayNames = ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'];",
    "let status = 'Closed now';": "let status = 'Jetzt geschlossen';",
    "status = 'Open now';": "status = 'Jetzt geöffnet';",
    "detail = `Until ${formatTime(hours[1])}`;": "detail = `Bis ${formatTime(hours[1])} Uhr`;",
    "status = 'Opens today';": "status = 'Öffnet heute';",
    "detail = formatTime(hours[0]);": "detail = `${formatTime(hours[0])} Uhr`;",
    "status = day === 0 ? 'Closed today' : 'Closed now';": "status = day === 0 ? 'Heute geschlossen' : 'Jetzt geschlossen';",
    "detail = `Opens ${offset === 1 ? 'tomorrow' : dayNames[nextDay]} ${formatTime(nextHours[0])}`;": "detail = `Öffnet ${offset === 1 ? 'morgen' : dayNames[nextDay]} um ${formatTime(nextHours[0])} Uhr`;",
    "if (priceTitle) priceTitle.textContent = gender === 'damen' ? 'Damen.' : 'Herren.';": "if (priceTitle) priceTitle.textContent = gender === 'damen' ? 'Damen' : 'Herren';",
}
for old, new in js_replacements.items():
    js = js.replace(old, new)

addon_replacements = {
    'ALOSH × VIVO — Hair · Beauty · Barber': 'ALOSH × VIVO — Haar · Kosmetik · Barber',
    'ALOSH × VIVO in Rostock – Herren bei ALOSH, Damen bei VIVO. Hair · Beauty · Barber an einer gemeinsamen Adresse.': 'ALOSH × VIVO in Rostock – Herren bei ALOSH, Damen bei VIVO. Haar, Kosmetik und Barber an einer gemeinsamen Adresse.',
    'Hair · Beauty · Barber': 'Haar · Kosmetik · Barber',
    'Two names.<br>One salon.': 'Zwei Namen.<br>Ein Salon.',
    'ALOSH for Herren. VIVO for Damen. Two distinct identities, one shared address and the same focus on precise, personal hair and beauty service.': 'ALOSH für Herren. VIVO für Damen. Zwei eigenständige Marken, eine gemeinsame Adresse und derselbe Anspruch an präzise, persönliche Haar- und Kosmetikleistungen.',
    'Choose your studio': 'Studio wählen',
    'See Location': 'Standort ansehen',
    'Opening hours': 'Öffnungszeiten',
    'Mon–Fri': 'Mo–Fr',
    'Call ALOSH': 'ALOSH anrufen',
    'Shared address': 'Gemeinsame Adresse',
    'One address': 'Eine Adresse',
    'One salon · two studios': 'Ein Salon · zwei Studios',
    'Same address.<br>Your studio.': 'Gleiche Adresse.<br>Dein Studio.',
    'Choose Herren or Damen with the selector below. Contact and booking details change with your selection.': 'Wähle unten Herren oder Damen. Kontakt- und Termininformationen wechseln passend zu deiner Auswahl.',
    '<span>Barber</span>': '<span>Herrenfriseur</span>',
    'Open in Maps': 'In Maps öffnen',
    '<span>Hair · Beauty</span>': '<span>Haar · Kosmetik</span>',
    'Call VIVO': 'VIVO anrufen',
    "'VIVO.<br>Light & refined.'": "'VIVO.<br>Hell & elegant.'",
    "'ALOSH.<br>Dark & precise.'": "'ALOSH.<br>Dunkel & präzise.'",
    'A lighter, calm identity for hair, color and beauty — still at the same shared Rostock salon.': 'Eine helle, ruhige Identität für Haare, Farbe und Kosmetik – weiterhin am gemeinsamen Standort in Rostock.',
    'A darker, focused identity for cuts, beard work and clean detail — at the same shared Rostock salon.': 'Eine dunkle, präzise Identität für Haarschnitte, Bart und klare Details – am gemeinsamen Standort in Rostock.',
}
for old, new in addon_replacements.items():
    addon = addon.replace(old, new)

files['index.html'].write_text(html, encoding='utf-8')
files['script.js'].write_text(js, encoding='utf-8')
files['gender-scroll-fix.js'].write_text(addon, encoding='utf-8')

print('German translation applied.')
