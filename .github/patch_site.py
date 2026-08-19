from pathlib import Path

path = Path("index.html")
s = path.read_text(encoding="utf-8")

replacements = {
    "html{scroll-behavior:smooth}": "html{scroll-behavior:smooth;scroll-padding-top:var(--header)}",
    "Luxury barber experience in Lüneburg.": "Barber experience in Rostock.",
    '<div class="hero-card-line"><span>Open today</span><strong>09–19</strong></div>': '<div class="hero-card-line"><span>Mon–Fri</span><strong>08:30–19</strong></div>',
    '<div class="hero-card-line"><span>Call us</span><strong>04131 123456</strong></div>': '<div class="hero-card-line"><span>Call us</span><strong>0381 76016450</strong></div>',
    '<div class="hero-card-line"><span>Address</span><strong>Musterstraße 24</strong></div>': '<div class="hero-card-line"><span>Address</span><strong>Doberaner Str. 48</strong></div>',
    'href="tel:+494131123456">Call now': 'href="tel:+4938176016450">Call now',
    '<strong>Today</strong>\n        <span>Open until 19:00</span>': '<strong>Mon–Fri</strong>\n        <span>08:30 – 19:00</span>',
    "Find us in Lüneburg, choose a time that works for you and book your next appointment in just a moment.": "Find us in Rostock, choose a time that works for you and book your next appointment in just a moment.",
    '<div class="hour-box animate-on-scroll reveal-pop" style="--delay:.02s"><strong>Mon–Wed</strong><span>09:00 – 19:00</span></div>': '<div class="hour-box animate-on-scroll reveal-pop" style="--delay:.02s"><strong>Mon–Fri</strong><span>08:30 – 19:00</span></div>',
    '<div class="hour-box animate-on-scroll reveal-pop" style="--delay:.08s"><strong>Thu–Fri</strong><span>09:00 – 20:00</span></div>': '<div class="hour-box animate-on-scroll reveal-pop" style="--delay:.08s"><strong>Saturday</strong><span>08:30 – 16:00</span></div>',
    '<div class="hour-box animate-on-scroll reveal-pop" style="--delay:.14s"><strong>Saturday</strong><span>09:00 – 16:00</span></div>': '',
    '<div class="hour-box animate-on-scroll reveal-pop" style="--delay:.2s"><strong>Sunday</strong><span>Closed</span></div>': '<div class="hour-box animate-on-scroll reveal-pop" style="--delay:.14s"><strong>Sunday</strong><span>Closed</span></div>',
    "Musterstraße 24<br>\n            21335 Lüneburg": "Doberaner Str. 48<br>\n            18057 Rostock",
    'href="tel:+494131123456">Call 04131 123456': 'href="tel:+4938176016450">Call 0381 76016450',
    'href="https://www.google.com/maps?q=L%C3%BCneburg"': 'href="https://www.google.com/maps/search/?api=1&query=Doberaner+Str.+48%2C+18057+Rostock"',
    '.hours-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:28px 0}': '.hours-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:28px 0}',
}

for old, new in replacements.items():
    s = s.replace(old, new)

marker = "// centered-anchor-navigation"
if marker not in s:
    needle = "    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n"
    navigation = r'''

    // centered-anchor-navigation
    function getDocumentTop(element) {
      let top = 0;
      let node = element;
      while (node) {
        top += node.offsetTop || 0;
        node = node.offsetParent;
      }
      return top;
    }

    function scrollTargetToCenter(target, updateHash = true) {
      if (!target) return;
      if (target.id === 'top') {
        window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' });
        if (updateHash) history.replaceState(null, '', '#top');
        return;
      }

      const headerHeight = header?.offsetHeight || 0;
      const viewportHeight = window.innerHeight;
      const availableHeight = Math.max(viewportHeight - headerHeight, 1);
      const targetHeight = Math.min(target.offsetHeight || target.getBoundingClientRect().height || 0, availableHeight);
      const normalTop = getDocumentTop(target);
      const centeredTop = normalTop - headerHeight - Math.max((availableHeight - targetHeight) / 2, 0);
      const maxScroll = Math.max(document.documentElement.scrollHeight - viewportHeight, 0);
      const destination = clamp(centeredTop, 0, maxScroll);

      window.scrollTo({ top: destination, behavior: reducedMotion ? 'auto' : 'smooth' });
      if (updateHash && target.id) history.replaceState(null, '', `#${target.id}`);
    }

    document.querySelectorAll('a[href^="#"]').forEach(link => {
      link.addEventListener('click', event => {
        const hash = link.getAttribute('href');
        if (!hash || hash === '#') return;
        const target = document.querySelector(hash);
        if (!target) return;
        event.preventDefault();

        document.body.classList.remove('menu-open');
        menuToggle?.setAttribute('aria-expanded', 'false');
        mobileMenu?.setAttribute('aria-hidden', 'true');

        requestAnimationFrame(() => scrollTargetToCenter(target));
      });
    });

    window.addEventListener('load', () => {
      if (!window.location.hash) return;
      const target = document.querySelector(window.location.hash);
      if (target) requestAnimationFrame(() => scrollTargetToCenter(target, false));
    }, { once: true });
'''
    if needle not in s:
        raise SystemExit("Could not find JavaScript insertion point")
    s = s.replace(needle, needle + navigation, 1)

path.write_text(s, encoding="utf-8")
# trigger workflow after workflow definition exists
