from pathlib import Path
import re

index_path = Path('index.html')
styles_path = Path('styles.css')
script_path = Path('script.js')

html = index_path.read_text(encoding='utf-8')
css = styles_path.read_text(encoding='utf-8')
js = script_path.read_text(encoding='utf-8')

# Rename the price navigation everywhere without touching IDs.
html = html.replace('href="#services">Services</a>', 'href="#services">Preise</a>')

cuts_section = r'''    <section class="cuts-showcase" id="cuts" aria-label="Frisuren Beispiele">
      <div class="cuts-stage">
        <div class="cuts-word parallax" data-speed="0.045" data-gender-word aria-hidden="true">HERREN</div>

        <div class="cuts-carousel gender-panel" data-gender-panel="herren">
          <div class="cuts-track" data-cuts-carousel="herren" tabindex="0" aria-label="Herren Frisuren. Seitlich wischen oder ziehen.">
            <figure class="cut-card animate-on-scroll" style="--delay:.02s">
              <img loading="lazy" src="https://images.unsplash.com/photo-1622286342621-4bd786c2447c?auto=format&fit=crop&w=1000&q=88" alt="Moderner Herren Fade" />
              <figcaption>Clean Fade</figcaption>
            </figure>
            <figure class="cut-card animate-on-scroll" style="--delay:.1s">
              <img loading="lazy" src="https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=1000&q=88" alt="Texturierter Herren Haarschnitt" />
              <figcaption>Texture</figcaption>
            </figure>
            <figure class="cut-card animate-on-scroll" style="--delay:.18s">
              <img loading="lazy" src="https://images.unsplash.com/photo-1599351431202-1e0f0137899a?auto=format&fit=crop&w=1000&q=88" alt="Klassischer Herren Haarschnitt" />
              <figcaption>Classic</figcaption>
            </figure>
            <figure class="cut-card animate-on-scroll" style="--delay:.26s">
              <img loading="lazy" src="https://images.unsplash.com/photo-1585747860715-2ba37e788b70?auto=format&fit=crop&w=1000&q=88" alt="Herren Haarschnitt und Bart" />
              <figcaption>Cut + Beard</figcaption>
            </figure>
          </div>
        </div>

        <div class="cuts-carousel gender-panel" data-gender-panel="damen" hidden>
          <div class="cuts-track" data-cuts-carousel="damen" tabindex="0" aria-label="Damen Frisuren. Seitlich wischen oder ziehen.">
            <figure class="cut-card animate-on-scroll in-view">
              <img loading="lazy" src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=1000&q=88" alt="Damen Frisur mit weichen Stufen" />
              <figcaption>Soft Layers</figcaption>
            </figure>
            <figure class="cut-card animate-on-scroll in-view">
              <img loading="lazy" src="https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=1000&q=88" alt="Damen Frisur mit weichen Wellen" />
              <figcaption>Soft Waves</figcaption>
            </figure>
            <figure class="cut-card animate-on-scroll in-view">
              <img loading="lazy" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=88" alt="Moderner Damen Haarschnitt" />
              <figcaption>Modern Cut</figcaption>
            </figure>
            <figure class="cut-card animate-on-scroll in-view">
              <img loading="lazy" src="https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?auto=format&fit=crop&w=1000&q=88" alt="Damen Farbe und Styling" />
              <figcaption>Color + Style</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </section>'''

html, count = re.subn(
    r'    <section class="cuts-showcase" id="cuts".*?</section>\n\n    <div class="stack-shell">',
    cuts_section + '\n\n    <div class="stack-shell">',
    html,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit(f'Could not replace cuts section: {count}')

services_section = r'''      <section class="stack-panel" id="services" style="--z:10">
        <div class="panel-inner cream">
          <div class="panel-grid">
            <div class="panel-copy cream-copy reveal reveal-left">
              <div class="scroll-decor parallax" data-speed="0.16">PREISE</div>
              <h2>Schnitt. Pflege.<br>Styling.</h2>
              <p>Wähle unten zwischen Damen und Herren. Preise und Leistungen wechseln direkt mit deiner Auswahl.</p>
            </div>

            <div class="service-side gender-panel" data-gender-panel="herren">
              <article class="service-card animate-on-scroll reveal-pop in-view">
                <div>
                  <h3>Herrenhaarschnitt</h3>
                  <p>Beratung, Schnitt und Styling.</p>
                </div>
                <div class="service-price"><span>45 min</span><strong>32 €</strong></div>
              </article>
              <article class="service-card animate-on-scroll reveal-pop in-view">
                <div>
                  <h3>Fade</h3>
                  <p>Saubere Übergänge und präzise Konturen.</p>
                </div>
                <div class="service-price"><span>50 min</span><strong>36 €</strong></div>
              </article>
              <article class="service-card animate-on-scroll reveal-pop in-view">
                <div>
                  <h3>Bart</h3>
                  <p>Konturen, Pflege und Bartstyling.</p>
                </div>
                <div class="service-price"><span>30 min</span><strong>24 €</strong></div>
              </article>
              <article class="service-card animate-on-scroll reveal-pop in-view">
                <div>
                  <h3>Schnitt + Bart</h3>
                  <p>Das komplette Paket für Haare und Bart.</p>
                </div>
                <div class="service-price"><span>70 min</span><strong>52 €</strong></div>
              </article>
            </div>

            <div class="service-side gender-panel" data-gender-panel="damen" hidden>
              <article class="service-card animate-on-scroll reveal-pop in-view">
                <div>
                  <h3>Waschen · Schneiden · Föhnen</h3>
                  <p>Beratung, Schnitt und vollständiges Styling.</p>
                </div>
                <div class="service-price"><span>60 min</span><strong>49 €</strong></div>
              </article>
              <article class="service-card animate-on-scroll reveal-pop in-view">
                <div>
                  <h3>Trockenschnitt</h3>
                  <p>Präziser Schnitt ohne Waschen und Föhnen.</p>
                </div>
                <div class="service-price"><span>35 min</span><strong>34 €</strong></div>
              </article>
              <article class="service-card animate-on-scroll reveal-pop in-view">
                <div>
                  <h3>Ansatzfarbe</h3>
                  <p>Farbe am Ansatz inklusive Pflege.</p>
                </div>
                <div class="service-price"><span>90 min</span><strong>48 €</strong></div>
              </article>
              <article class="service-card animate-on-scroll reveal-pop in-view">
                <div>
                  <h3>Farbe · Schnitt · Styling</h3>
                  <p>Farbe, Schnitt, Pflege und Finish.</p>
                </div>
                <div class="service-price"><span>120 min</span><strong>82 €</strong></div>
              </article>
            </div>
          </div>
        </div>
      </section>'''

html, count = re.subn(
    r'      <section class="stack-panel" id="services".*?</section>\n\n      <section class="stack-panel" id="salon"',
    services_section + '\n\n      <section class="stack-panel" id="salon"',
    html,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit(f'Could not replace services section: {count}')

# Add the floating Damen/Herren selector before the external JS include.
dock = r'''  <nav class="gender-dock" data-gender-dock aria-label="Damen oder Herren" aria-hidden="true">
    <button type="button" class="gender-dock-button is-active" data-gender-toggle="herren" aria-pressed="true">Herren</button>
    <button type="button" class="gender-dock-button" data-gender-toggle="damen" aria-pressed="false">Damen</button>
  </nav>
'''
if 'data-gender-dock' not in html:
    html = html.replace('  <script src="script.js" defer></script>', dock + '  <script src="script.js" defer></script>')

# CSS: append an override block so the existing design remains untouched.
marker = '/* Damen / Herren split */'
if marker not in css:
    css += r'''

/* Damen / Herren split */
.gender-panel[hidden]{display:none!important}
.gender-panel:not([hidden]){animation:genderPanelIn .42s cubic-bezier(.22,.61,.36,1) both}
@keyframes genderPanelIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}

.gender-dock{
  position:fixed;
  left:50%;
  bottom:20px;
  z-index:115;
  width:min(360px,calc(100vw - 32px));
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:6px;
  padding:6px;
  border:1px solid rgba(255,255,255,.14);
  border-radius:999px;
  background:rgba(12,11,10,.88);
  box-shadow:0 18px 55px rgba(0,0,0,.34);
  backdrop-filter:blur(18px);
  -webkit-backdrop-filter:blur(18px);
  opacity:0;
  pointer-events:none;
  transform:translate(-50%,calc(100% + 34px));
  transition:opacity .38s ease,transform .48s cubic-bezier(.22,.61,.36,1);
  will-change:opacity,transform;
}
.gender-dock.is-visible{opacity:1;pointer-events:auto;transform:translate(-50%,0)}
.gender-dock-button{
  min-width:0;
  min-height:48px;
  border:0;
  border-radius:999px;
  background:transparent;
  color:#e4d9c9;
  font-size:16px;
  font-weight:700;
  letter-spacing:.01em;
  cursor:pointer;
  transition:background .25s ease,color .25s ease,transform .2s ease;
}
.gender-dock-button:hover{color:#fff}
.gender-dock-button:active{transform:scale(.98)}
.gender-dock-button.is-active{background:var(--gold);color:#17110a}

#services .service-side.gender-panel{align-content:stretch}

@media (max-width:780px){
  .gender-dock{
    bottom:calc(12px + env(safe-area-inset-bottom));
    width:calc(100vw - 24px);
    max-width:430px;
    padding:6px;
  }
  .gender-dock-button{min-height:52px;font-size:17px}
  .cuts-showcase{padding-bottom:106px}
  #services .service-side.gender-panel{padding-bottom:104px}
}

@media (prefers-reduced-motion:reduce){
  .gender-dock{transition:none}
  .gender-panel:not([hidden]){animation:none}
}
'''

# Replace the single-track carousel with a reusable controller for both gender tracks.
new_carousel = r'''const cutsCarouselControllers = new Map();

function ensureCutsCarousel(track) {
  if (!track) return null;
  if (cutsCarouselControllers.has(track)) return cutsCarouselControllers.get(track);

  const originals = [...track.children];
  if (!originals.length) return null;

  track.style.scrollSnapType = 'none';
  track.style.scrollBehavior = 'auto';
  originals.forEach(card => { card.style.scrollSnapAlign = 'none'; });

  const cloneCard = card => {
    const clone = card.cloneNode(true);
    clone.setAttribute('aria-hidden', 'true');
    clone.classList.add('in-view');
    clone.style.scrollSnapAlign = 'none';
    clone.querySelectorAll('img').forEach(img => img.removeAttribute('loading'));
    return clone;
  };

  // A large repeated buffer makes every last -> first transition a normal move to
  // the physically next card. Coordinate recycling only happens far away from the
  // visible seam and uses exact card offsets, so there is no visible reset.
  const BUFFER_SETS = 5;
  const leftCopies = document.createDocumentFragment();
  for (let set = 0; set < BUFFER_SETS; set += 1) {
    originals.forEach(card => leftCopies.appendChild(cloneCard(card)));
  }
  track.prepend(leftCopies);

  const rightCopies = document.createDocumentFragment();
  for (let set = 0; set < BUFFER_SETS; set += 1) {
    originals.forEach(card => rightCopies.appendChild(cloneCard(card)));
  }
  track.append(rightCopies);

  const count = originals.length;
  const middleSet = BUFFER_SETS;
  const totalSets = BUFFER_SETS * 2 + 1;
  const middleStart = middleSet * count;
  const AUTO_DELAY = 3200;
  const RESUME_DELAY = 3600;
  const AUTO_DURATION = 720;

  let autoTimer = null;
  let manualTimer = null;
  let animationFrame = null;
  let autoAnimating = false;
  let suppressScroll = false;
  let dragging = false;
  let active = false;
  let dragStartX = 0;
  let dragStartScrollLeft = 0;

  const cards = () => [...track.children];
  const centeredLeft = card => card.offsetLeft + card.offsetWidth / 2 - track.clientWidth / 2;

  const nearestIndex = () => {
    const viewportCenter = track.scrollLeft + track.clientWidth / 2;
    let nearest = middleStart;
    let bestDistance = Infinity;

    cards().forEach((card, index) => {
      const cardCenter = card.offsetLeft + card.offsetWidth / 2;
      const distance = Math.abs(cardCenter - viewportCenter);
      if (distance < bestDistance) {
        bestDistance = distance;
        nearest = index;
      }
    });
    return nearest;
  };

  const jumpToEquivalentMiddleCard = index => {
    const setIndex = Math.floor(index / count);
    if (setIndex > 1 && setIndex < totalSets - 2) return index;

    const logicalIndex = ((index % count) + count) % count;
    const targetIndex = middleStart + logicalIndex;
    const source = track.children[index];
    const target = track.children[targetIndex];
    if (!source || !target) return index;

    const exactDelta = target.offsetLeft - source.offsetLeft;
    suppressScroll = true;
    track.scrollLeft += exactDelta;
    requestAnimationFrame(() => requestAnimationFrame(() => { suppressScroll = false; }));
    return targetIndex;
  };

  const maybeRecenter = () => jumpToEquivalentMiddleCard(nearestIndex());

  const clearAuto = () => {
    if (autoTimer) clearTimeout(autoTimer);
    autoTimer = null;
  };

  const clearManual = () => {
    if (manualTimer) clearTimeout(manualTimer);
    manualTimer = null;
  };

  const cancelAnimation = () => {
    if (animationFrame) cancelAnimationFrame(animationFrame);
    animationFrame = null;
    autoAnimating = false;
  };

  const animateTo = (targetLeft, duration, onDone) => {
    cancelAnimation();
    const startLeft = track.scrollLeft;
    const delta = targetLeft - startLeft;
    const startedAt = performance.now();
    autoAnimating = true;

    const step = now => {
      if (!active) {
        cancelAnimation();
        return;
      }
      const progress = Math.min((now - startedAt) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      track.scrollLeft = startLeft + delta * eased;
      if (progress < 1) {
        animationFrame = requestAnimationFrame(step);
      } else {
        animationFrame = null;
        autoAnimating = false;
        onDone?.();
      }
    };
    animationFrame = requestAnimationFrame(step);
  };

  function scheduleAuto(delay = AUTO_DELAY) {
    clearAuto();
    if (!active || reducedMotion) return;
    autoTimer = setTimeout(advance, delay);
  }

  const beginManualInteraction = () => {
    clearAuto();
    clearManual();
    cancelAnimation();
  };

  const scheduleResume = (delay = RESUME_DELAY) => {
    clearManual();
    manualTimer = setTimeout(() => {
      if (!active) return;
      maybeRecenter();
      scheduleAuto(delay);
    }, 220);
  };

  function advance() {
    if (!active) return;
    if (dragging || document.visibilityState !== 'visible') {
      scheduleAuto(900);
      return;
    }

    const current = maybeRecenter();
    const target = track.children[current + 1];
    if (!target) {
      scheduleAuto(500);
      return;
    }

    animateTo(centeredLeft(target), AUTO_DURATION, () => scheduleAuto());
  }

  track.addEventListener('scroll', () => {
    if (!active || autoAnimating || suppressScroll || dragging) return;
    clearAuto();
    scheduleResume();
  }, { passive: true });

  track.addEventListener('touchstart', beginManualInteraction, { passive: true });
  track.addEventListener('touchend', () => scheduleResume(), { passive: true });
  track.addEventListener('wheel', () => {
    beginManualInteraction();
    scheduleResume(2800);
  }, { passive: true });

  track.addEventListener('keydown', event => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    beginManualInteraction();
    const current = maybeRecenter();
    const target = track.children[current + (event.key === 'ArrowRight' ? 1 : -1)];
    if (!target) return;
    animateTo(centeredLeft(target), 560, () => scheduleAuto(RESUME_DELAY));
  });

  track.addEventListener('pointerdown', event => {
    if (event.pointerType !== 'mouse' || event.button !== 0) return;
    beginManualInteraction();
    dragging = true;
    dragStartX = event.clientX;
    dragStartScrollLeft = track.scrollLeft;
    track.classList.add('is-dragging');
    track.setPointerCapture?.(event.pointerId);
  });

  track.addEventListener('pointermove', event => {
    if (!dragging) return;
    track.scrollLeft = dragStartScrollLeft - (event.clientX - dragStartX);
  });

  const stopDragging = event => {
    if (!dragging) return;
    dragging = false;
    track.classList.remove('is-dragging');
    if (event?.pointerId != null && track.hasPointerCapture?.(event.pointerId)) {
      track.releasePointerCapture(event.pointerId);
    }
    scheduleResume();
  };

  track.addEventListener('pointerup', stopDragging);
  track.addEventListener('pointercancel', stopDragging);
  track.addEventListener('lostpointercapture', stopDragging);

  const controller = {
    setActive(nextActive) {
      active = nextActive;
      clearAuto();
      clearManual();
      cancelAnimation();
      if (!active) return;

      requestAnimationFrame(() => requestAnimationFrame(() => {
        const current = nearestIndex();
        const hasUsefulPosition = track.scrollLeft > 1 && current >= 0;
        if (!hasUsefulPosition) {
          const first = track.children[middleStart];
          if (first) {
            suppressScroll = true;
            track.scrollLeft = centeredLeft(first);
            requestAnimationFrame(() => requestAnimationFrame(() => { suppressScroll = false; }));
          }
        } else {
          maybeRecenter();
        }
        scheduleAuto(1400);
      }));
    },
    recenterForResize() {
      if (!active) return;
      beginManualInteraction();
      requestAnimationFrame(() => {
        const current = nearestIndex();
        const logicalIndex = ((current % count) + count) % count;
        const target = track.children[middleStart + logicalIndex];
        if (target) {
          suppressScroll = true;
          track.scrollLeft = centeredLeft(target);
          requestAnimationFrame(() => { suppressScroll = false; });
        }
        scheduleAuto(1000);
      });
    }
  };

  cutsCarouselControllers.set(track, controller);
  return controller;
}

function initGenderExperience() {
  const dock = document.querySelector('[data-gender-dock]');
  const buttons = [...document.querySelectorAll('[data-gender-toggle]')];
  const panels = [...document.querySelectorAll('[data-gender-panel]')];
  const tracks = [...document.querySelectorAll('[data-cuts-carousel]')];
  const genderWord = document.querySelector('[data-gender-word]');
  const cuts = document.getElementById('cuts');
  const salon = document.getElementById('salon');
  if (!dock || !buttons.length || !cuts || !salon) return;

  let selectedGender = 'herren';

  const applyGender = gender => {
    selectedGender = gender;
    document.body.dataset.gender = gender;
    if (genderWord) genderWord.textContent = gender === 'damen' ? 'DAMEN' : 'HERREN';

    buttons.forEach(button => {
      const activeButton = button.dataset.genderToggle === gender;
      button.classList.toggle('is-active', activeButton);
      button.setAttribute('aria-pressed', String(activeButton));
    });

    panels.forEach(panel => {
      panel.hidden = panel.dataset.genderPanel !== gender;
    });

    tracks.forEach(track => {
      const shouldBeActive = track.dataset.cutsCarousel === gender;
      const existing = cutsCarouselControllers.get(track);
      if (!shouldBeActive) {
        existing?.setActive(false);
        return;
      }

      requestAnimationFrame(() => requestAnimationFrame(() => {
        ensureCutsCarousel(track)?.setActive(true);
      }));
    });
  };

  buttons.forEach(button => {
    button.addEventListener('click', () => applyGender(button.dataset.genderToggle));
  });

  let dockRaf = 0;
  const updateDockVisibility = () => {
    dockRaf = 0;
    const vh = window.innerHeight;
    const cutsRect = cuts.getBoundingClientRect();
    const salonRect = salon.getBoundingClientRect();
    const reachedExamples = cutsRect.top <= vh * .72;
    const beforeSalonVisuals = salonRect.top > vh * .66;
    const visible = reachedExamples && beforeSalonVisuals;
    dock.classList.toggle('is-visible', visible);
    dock.setAttribute('aria-hidden', String(!visible));
  };

  const requestDockUpdate = () => {
    if (dockRaf) return;
    dockRaf = requestAnimationFrame(updateDockVisibility);
  };

  window.addEventListener('scroll', requestDockUpdate, { passive: true });
  window.addEventListener('resize', () => {
    requestDockUpdate();
    cutsCarouselControllers.forEach(controller => controller.recenterForResize());
  });

  applyGender(selectedGender);
  updateDockVisibility();
}

initGenderExperience();'''

js, count = re.subn(
    r'function setupCutsCarousel\(\) \{.*?\n\}\n\nsetupCutsCarousel\(\);',
    new_carousel,
    js,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit(f'Could not replace carousel JS: {count}')

index_path.write_text(html, encoding='utf-8')
styles_path.write_text(css, encoding='utf-8')
script_path.write_text(js, encoding='utf-8')
