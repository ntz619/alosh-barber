from pathlib import Path

index_path = Path('index.html')
script_path = Path('script.js')
html = index_path.read_text(encoding='utf-8')
script = script_path.read_text(encoding='utf-8')

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly 1 match, found {count}')
    return text.replace(old, new, 1)

html = replace_once(
    html,
    '<meta name="description" content="ALOSH – Hair · Barber · Beauty. Elegante, kompakte Barber Landingpage mit flüssigen Scroll-Animationen." />',
    '<meta name="description" content="ALOSH × VIVO in Rostock – Herren bei ALOSH, Damen bei VIVO. Hair · Beauty · Barber an einer gemeinsamen Adresse." />',
    'meta description'
)
html = replace_once(html, '<title>ALOSH — Hair · Barber · Beauty</title>', '<title>ALOSH × VIVO — Hair · Beauty · Barber</title>', 'title')
html = replace_once(
    html,
    '  <link rel="stylesheet" href="price-icon-scale.css?v=1">',
    '  <link rel="stylesheet" href="price-icon-scale.css?v=1">\n  <link rel="stylesheet" href="dual-brand.css?v=20260819-1">',
    'dual stylesheet'
)

old_header_brand = '''    <a class="brand" href="#top" aria-label="ALOSH Startseite">
      <span class="brand-name">ALOSH</span>
      <span class="brand-sub">Hair · Barber · Beauty</span>
    </a>'''
new_header_brand = '''    <a class="brand brand-dual" href="#top" aria-label="ALOSH und VIVO Startseite">
      <span class="brand-name"><span>ALOSH</span><i>×</i><span>VIVO</span></span>
      <span class="brand-sub">Hair · Beauty · Barber</span>
    </a>'''
html = replace_once(html, old_header_brand, new_header_brand, 'header brand')

old_hero_copy = '''        <div class="hero-copy reveal reveal-left">
          <p class="hero-kicker">Barber experience in Rostock.</p>
          <h1>Cuts.<br>Beards.<br>Style.</h1>
          <p>Elegant atmosphere, precise work and a clean, premium finish. Built to feel strong on desktop and fast on mobile.</p>
          <div class="hero-actions">
            <a class="button button-gold" href="#booking">Book Appointment</a>
            <a class="button button-outline" href="#visit">See Location</a>
          </div>
        </div>'''
new_hero_copy = '''        <div class="hero-copy reveal reveal-left">
          <p class="hero-kicker">ALOSH × VIVO · Doberaner Straße 48 · Rostock</p>
          <h1>Two names.<br>One salon.</h1>
          <p>ALOSH for Herren. VIVO for Damen. Two distinct identities, one shared address and the same focus on precise, personal hair and beauty service.</p>
          <div class="hero-actions">
            <a class="button button-gold" href="#booking">Choose your studio</a>
            <a class="button button-outline" href="#visit">See Location</a>
          </div>
        </div>'''
html = replace_once(html, old_hero_copy, new_hero_copy, 'hero copy')

old_hero_card = '''        <aside class="hero-card reveal reveal-pop" aria-label="Basic salon info">
          <div class="hero-card-top">
            <div class="hero-card-line"><span data-shop-status>Opening hours</span><strong data-shop-detail>Mon–Fri 08:30–19:00</strong></div>
            <div class="hero-card-line"><span>Call us</span><strong>0381 76016450</strong></div>
            <div class="hero-card-line"><span>Address</span><strong>Doberaner Str. 48</strong></div>
          </div>
          <a class="button button-gold" href="tel:+4938176016450">Call now</a>
        </aside>'''
new_hero_card = '''        <aside class="hero-card reveal reveal-pop" aria-label="ALOSH und VIVO Kontakt">
          <div class="hero-card-line"><span data-shop-status>Opening hours</span><strong data-shop-detail>Mon–Fri 08:30–19:00</strong></div>
          <div class="hero-dual-contact">
            <div class="hero-brand-contact alosh">
              <span>ALOSH · Herren</span>
              <strong>0177 7289259</strong>
              <a href="tel:+491777289259">Call ALOSH</a>
            </div>
            <div class="hero-brand-contact vivo">
              <span>VIVO · Damen</span>
              <strong>0162 9105910</strong>
              <a href="https://www.instagram.com/avin_friseur/" target="_blank" rel="noopener">@avin_friseur</a>
            </div>
          </div>
          <div class="hero-card-line"><span>Shared address</span><strong>Doberaner Str. 48</strong></div>
          <div class="hero-shared-note">18057 Rostock · Hair · Beauty · Barber</div>
        </aside>'''
html = replace_once(html, old_hero_card, new_hero_card, 'hero card')
html = replace_once(html, '<div class="hero-decor two parallax" data-speed="0.11">BARBER</div>', '<div class="hero-decor two parallax" data-speed="0.11">VIVO</div>', 'hero decor')

old_info = '''    <section class="info-strip">
      <div class="info-box reveal reveal-pop" style="--delay:.02s">
        <strong data-shop-status>Opening hours</strong>
        <span data-shop-detail>Mon–Fri 08:30 – 19:00</span>
      </div>
      <div class="info-box reveal reveal-pop" style="--delay:.08s">
        <strong>Walk‑ins</strong>
        <span>Welcome when free</span>
      </div>
      <div class="info-box reveal reveal-pop" style="--delay:.14s">
        <strong>4.9 ★</strong>
        <span>Google reviews</span>
      </div>
      <div class="info-box reveal reveal-pop" style="--delay:.2s">
        <strong>Book</strong>
        <a href="#booking">Tap for appointment</a>
      </div>
    </section>'''
new_info = '''    <section class="info-strip">
      <div class="info-box reveal reveal-pop" style="--delay:.02s">
        <strong>One address</strong>
        <span>Doberaner Straße 48 · Rostock</span>
      </div>
      <div class="info-box info-brand alosh-info reveal reveal-pop" style="--delay:.08s">
        <strong>ALOSH</strong>
        <span>Herren · 0177 7289259</span>
      </div>
      <div class="info-box info-brand vivo-info reveal reveal-pop" style="--delay:.14s">
        <strong>VIVO</strong>
        <span>Damen · 0162 9105910</span>
      </div>
      <div class="info-box reveal reveal-pop" style="--delay:.2s">
        <strong data-shop-status>Opening hours</strong>
        <span data-shop-detail>Mon–Fri 08:30 – 19:00</span>
      </div>
    </section>'''
html = replace_once(html, old_info, new_info, 'info strip')

html = replace_once(html, '<h2 data-gender-price-title>Herren.</h2>', '<h2 data-gender-price-title>Herren</h2>', 'price title html')

old_visit_intro = '''          <h2>Easy to visit.<br>Easy to book.</h2>
          <p>Find us in Rostock, choose a time that works for you and book your next appointment in just a moment.</p>'''
new_visit_intro = '''          <div class="shared-salon-mark"><span>One salon · two studios</span><strong>ALOSH × VIVO</strong></div>
          <h2>Same address.<br>Your studio.</h2>
          <p>Choose Herren or Damen with the selector below. Contact and booking details change with your selection.</p>'''
html = replace_once(html, old_visit_intro, new_visit_intro, 'visit intro')

old_address_actions = '''          <div class="address-box animate-on-scroll reveal-pop" style="--delay:.26s">
            <strong>Kurdistan Barbershop</strong><br>
            Doberaner Str. 48<br>
            18057 Rostock
          </div>

          <div class="visit-actions" id="booking">
            <a class="button button-gold" href="tel:+4938176016450">Call 0381 76016450</a>
            <a class="button button-outline" style="color:#201b14;border-color:rgba(17,15,11,.14)" href="https://www.google.com/maps/search/?api=1&query=Kurdistan+Barbershop+-+Friseur+Atelier+Justyna%2C+Rostock&query_place_id=ChIJq4bq9xNXrEcRFlgokdhbPqw" target="_blank" rel="noopener">Open in Maps</a>
          </div>'''
new_address_actions = '''          <div class="address-box animate-on-scroll reveal-pop" style="--delay:.26s">
            <strong>ALOSH × VIVO</strong><br>
            Doberaner Straße 48<br>
            18057 Rostock
          </div>

          <div id="booking">
            <div class="brand-contact-panel gender-panel" data-gender-panel="herren">
              <div class="brand-contact-head"><div><span>Herren</span><h3>ALOSH</h3></div><span>Barber</span></div>
              <div class="brand-contact-details">
                <a href="tel:+491777289259">0177 7289259</a>
                <small>Doberaner Straße 48 · 18057 Rostock</small>
              </div>
              <div class="visit-actions">
                <a class="button button-gold" href="tel:+491777289259">Call ALOSH</a>
                <a class="button button-outline" href="https://www.google.com/maps/search/?api=1&query=Doberaner+Stra%C3%9Fe+48%2C+18057+Rostock" target="_blank" rel="noopener">Open in Maps</a>
              </div>
            </div>

            <div class="brand-contact-panel gender-panel" data-gender-panel="damen" hidden>
              <div class="brand-contact-head"><div><span>Damen</span><h3>VIVO</h3></div><span>Hair · Beauty</span></div>
              <div class="brand-contact-details">
                <a href="tel:+491629105910">0162 9105910</a>
                <a href="https://www.instagram.com/avin_friseur/" target="_blank" rel="noopener">@avin_friseur</a>
                <small>Doberaner Straße 48 · 18057 Rostock</small>
              </div>
              <div class="visit-actions">
                <a class="button button-gold" href="tel:+491629105910">Call VIVO</a>
                <a class="button button-outline" href="https://www.instagram.com/avin_friseur/" target="_blank" rel="noopener">Instagram</a>
                <a class="button button-outline" href="https://www.google.com/maps/search/?api=1&query=Doberaner+Stra%C3%9Fe+48%2C+18057+Rostock" target="_blank" rel="noopener">Open in Maps</a>
              </div>
            </div>
          </div>'''
html = replace_once(html, old_address_actions, new_address_actions, 'visit contacts')

old_iframe = 'src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2782.7605567998803!2d12.11145307220702!3d54.09123819497803!2m3!1f0!2f0!3f0!3m2!1i1024!1i768!4f13.1!3m3!1m2!1s0x47ac5713f7ea86ab%3A0xac3e5bd891285816!2sKurdistan%20Barbershop%20-%20Friseur%20Atelier%20Justyna%2C%20Rostock!5e0!3m2!1sde!2sde!4v1787150658706!5m2!1sde!2sde"'
new_iframe = 'src="https://www.google.com/maps?q=Doberaner+Stra%C3%9Fe+48,+18057+Rostock&output=embed"'
html = replace_once(html, old_iframe, new_iframe, 'map iframe')

old_footer_brand = '''    <a class="brand" href="#top">
      <span class="brand-name">ALOSH</span>
      <span class="brand-sub">Hair · Barber · Beauty</span>
    </a>'''
new_footer_brand = '''    <a class="brand brand-dual" href="#top">
      <span class="brand-name"><span>ALOSH</span><i>×</i><span>VIVO</span></span>
      <span class="brand-sub">Hair · Beauty · Barber</span>
    </a>'''
html = replace_once(html, old_footer_brand, new_footer_brand, 'footer brand')
html = replace_once(html, '<span>© <span id="year"></span> ALOSH</span>', '<span class="footer-dual-note">© <span id="year"></span> ALOSH × VIVO</span>', 'footer copyright')
html = replace_once(
    html,
    '''    <button type="button" class="gender-dock-button is-active" data-gender-toggle="herren" aria-pressed="true">Herren</button>
    <button type="button" class="gender-dock-button" data-gender-toggle="damen" aria-pressed="false">Damen</button>''',
    '''    <button type="button" class="gender-dock-button is-active" data-gender-toggle="herren" aria-pressed="true">Herren<small>ALOSH</small></button>
    <button type="button" class="gender-dock-button" data-gender-toggle="damen" aria-pressed="false">Damen<small>VIVO</small></button>''',
    'dock labels'
)

script = replace_once(
    script,
    "if (priceTitle) priceTitle.textContent = gender === 'damen' ? 'Damen.' : 'Herren.';",
    "if (priceTitle) priceTitle.textContent = gender === 'damen' ? 'Damen' : 'Herren';",
    'price title script'
)
old_visibility = '''    const vh = window.innerHeight;
    const cutsRect = cuts.getBoundingClientRect();
    const salonRect = salon.getBoundingClientRect();
    const reachedExamples = cutsRect.top <= vh * .72;
    const beforeSalonVisuals = salonRect.top > vh * .66;
    const visible = reachedExamples && beforeSalonVisuals;'''
new_visibility = '''    const vh = window.innerHeight;
    const heroRect = document.querySelector('.hero')?.getBoundingClientRect();
    const visible = heroRect ? heroRect.bottom <= vh * .88 : window.scrollY > vh * .6;'''
script = replace_once(script, old_visibility, new_visibility, 'dock visibility')

index_path.write_text(html, encoding='utf-8')
script_path.write_text(script, encoding='utf-8')
