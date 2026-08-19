from pathlib import Path
import re

path = Path("index.html")
s = path.read_text(encoding="utf-8")

# Keep every visible location reference in Rostock.
s = s.replace("Lüneburg", "Rostock").replace("L%C3%BCneburg", "Rostock").replace("Luneburg", "Rostock").replace("luneburg", "rostock")

# The Maps button should open the exact Google Maps place, not just the address search.
maps_url = "https://www.google.com/maps/search/?api=1&query=Kurdistan+Barbershop+-+Friseur+Atelier+Justyna%2C+Rostock&query_place_id=ChIJq4bq9xNXrEcRFlgokdhbPqw"
s = re.sub(
    r'href="https://www\.google\.com/maps/search/\?api=1&query=[^"]+" target="_blank" rel="noopener">Open in Maps</a>',
    f'href="{maps_url}" target="_blank" rel="noopener">Open in Maps</a>',
    s,
)

# Show the actual shop name in the location block.
s = s.replace(
    '<strong>ALOSH</strong><br>\n            Doberaner Str. 48<br>\n            18057 Rostock',
    '<strong>Kurdistan Barbershop</strong><br>\n            Doberaner Str. 48<br>\n            18057 Rostock',
)

# Make the top status dynamic instead of hard-coded.
s = s.replace(
    '<div class="hero-card-line"><span>Mon–Fri</span><strong>08:30–19</strong></div>',
    '<div class="hero-card-line"><span data-shop-status>Opening hours</span><strong data-shop-detail>Mon–Fri 08:30–19:00</strong></div>',
)
s = s.replace(
    '''      <div class="info-box reveal reveal-pop" style="--delay:.02s">\n        <strong>Mon–Fri</strong>\n        <span>08:30 – 19:00</span>\n      </div>''',
    '''      <div class="info-box reveal reveal-pop" style="--delay:.02s">\n        <strong data-shop-status>Opening hours</strong>\n        <span data-shop-detail>Mon–Fri 08:30 – 19:00</span>\n      </div>''',
)

# When measuring anchor positions, temporarily disable sticky positioning so the
# destination is based on the section's natural document position even if the
# visitor is already far down the page.
measurement_css = '''    .scroll-measure .stack-panel{position:relative !important;top:auto !important}\n    .scroll-measure .panel-inner{transform:none !important;filter:none !important}\n\n'''
css_anchor = '    /* Content safety: meaningful text and controls must always fit the viewport. */\n'
if measurement_css.strip() not in s and css_anchor in s:
    s = s.replace(css_anchor, measurement_css + css_anchor, 1)

navigation = r'''    function getNaturalAnchorMetrics(target) {
      root.classList.add('scroll-measure');
      void document.body.offsetHeight;

      let focus = target;
      if (target.classList.contains('stack-panel')) focus = target.querySelector('.panel-inner') || target;
      if (target.id === 'visit') focus = target.querySelector('.visit-card') || target;

      const rect = focus.getBoundingClientRect();
      const metrics = { top: rect.top + window.scrollY, height: rect.height };

      root.classList.remove('scroll-measure');
      void document.body.offsetHeight;
      return metrics;
    }

    function scrollTargetToCenter(target, updateHash = true) {
      if (!target) return;
      if (target.id === 'top') {
        window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' });
        if (updateHash) history.replaceState(null, '', '#top');
        return;
      }

      const { top, height } = getNaturalAnchorMetrics(target);
      const headerHeight = header?.offsetHeight || 0;
      const safeTop = headerHeight + 12;
      const safeBottom = 18;
      const availableHeight = Math.max(window.innerHeight - safeTop - safeBottom, 1);
      const visibleHeight = Math.min(height, availableHeight);
      const centeredTop = top - safeTop - Math.max((availableHeight - visibleHeight) / 2, 0);
      const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 0);
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

        // Call directly instead of deferring through requestAnimationFrame. This
        // makes repeated quick-link use reliable even during/after long scrolling.
        scrollTargetToCenter(target);
      });
    });

    window.addEventListener('load', () => {
      if (!window.location.hash) return;
      const target = document.querySelector(window.location.hash);
      if (target) setTimeout(() => scrollTargetToCenter(target, false), 0);
    }, { once: true });

    function updateShopStatus() {
      // Verified Rostock hours: Mon–Fri 08:30–19:00, Sat 08:30–16:00, Sun closed.
      // Europe/Berlin handles German daylight-saving time automatically.
      const schedule = {
        0: null,
        1: [8 * 60 + 30, 19 * 60],
        2: [8 * 60 + 30, 19 * 60],
        3: [8 * 60 + 30, 19 * 60],
        4: [8 * 60 + 30, 19 * 60],
        5: [8 * 60 + 30, 19 * 60],
        6: [8 * 60 + 30, 16 * 60]
      };
      const weekdayMap = { Sun:0, Mon:1, Tue:2, Wed:3, Thu:4, Fri:5, Sat:6 };
      const dayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
      const parts = new Intl.DateTimeFormat('en-GB', {
        timeZone: 'Europe/Berlin', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
      }).formatToParts(new Date());
      const values = Object.fromEntries(parts.map(part => [part.type, part.value]));
      const day = weekdayMap[values.weekday];
      const nowMinutes = Number(values.hour) * 60 + Number(values.minute);
      const hours = schedule[day];
      const formatTime = minutes => `${String(Math.floor(minutes / 60)).padStart(2,'0')}:${String(minutes % 60).padStart(2,'0')}`;

      let status = 'Closed now';
      let detail = '';

      if (hours && nowMinutes >= hours[0] && nowMinutes < hours[1]) {
        status = 'Open now';
        detail = `Until ${formatTime(hours[1])}`;
      } else if (hours && nowMinutes < hours[0]) {
        status = 'Opens today';
        detail = formatTime(hours[0]);
      } else {
        for (let offset = 1; offset <= 7; offset++) {
          const nextDay = (day + offset) % 7;
          const nextHours = schedule[nextDay];
          if (!nextHours) continue;
          status = day === 0 ? 'Closed today' : 'Closed now';
          detail = `Opens ${offset === 1 ? 'tomorrow' : dayNames[nextDay]} ${formatTime(nextHours[0])}`;
          break;
        }
      }

      document.querySelectorAll('[data-shop-status]').forEach(el => { el.textContent = status; });
      document.querySelectorAll('[data-shop-detail]').forEach(el => { el.textContent = detail; });
    }

    updateShopStatus();
    setInterval(updateShopStatus, 60000);

'''

# Replace the previous anchor-navigation implementation completely so old sticky
# geometry cannot interfere with later quick-link clicks.
pattern = r'''    function (?:getDocumentTop|getNaturalAnchorMetrics)\(.*?\n(?=    function handleScrollState\(\)\{)'''
s, count = re.subn(pattern, navigation, s, flags=re.S)
if count != 1:
    raise SystemExit(f"Could not replace navigation block (matches: {count})")

path.write_text(s, encoding="utf-8")
