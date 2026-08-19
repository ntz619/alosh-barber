from pathlib import Path

path = Path("index.html")
s = path.read_text(encoding="utf-8")

# Make the decorative labels safer on narrow screens.
for old, new in {
    "ALOSH · ALOSH · ALOSH": "ALOSH",
    "BARBER · STYLE · CARE": "BARBER",
    "CRAFT · CRAFT · CRAFT": "CRAFT",
    "SALON · SALON · SALON": "SALON",
    "TRUST · TRUST · TRUST": "TRUST",
}.items():
    s = s.replace(old, new)

# Replace the example-cuts block with a true horizontal carousel.
start = s.index('    <section class="cuts-showcase" id="cuts"')
end = s.index('    <div class="stack-shell">', start)
new_cuts = '''    <section class="cuts-showcase" id="cuts" aria-label="Example haircuts">
      <div class="cuts-stage">
        <div class="cuts-word parallax" data-speed="0.045" aria-hidden="true">CUTS</div>
        <div class="cuts-carousel">
          <div class="cuts-track" data-cuts-carousel tabindex="0" aria-label="Haircut examples. Swipe or drag sideways.">
            <figure class="cut-card animate-on-scroll" style="--delay:.02s">
              <img loading="lazy" src="https://images.unsplash.com/photo-1622286342621-4bd786c2447c?auto=format&fit=crop&w=1000&q=88" alt="Example modern fade haircut" />
              <figcaption>Clean Fade</figcaption>
            </figure>
            <figure class="cut-card animate-on-scroll" style="--delay:.1s">
              <img loading="lazy" src="https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=1000&q=88" alt="Example textured men's haircut" />
              <figcaption>Texture</figcaption>
            </figure>
            <figure class="cut-card animate-on-scroll" style="--delay:.18s">
              <img loading="lazy" src="https://images.unsplash.com/photo-1599351431202-1e0f0137899a?auto=format&fit=crop&w=1000&q=88" alt="Example classic men's barber haircut" />
              <figcaption>Classic</figcaption>
            </figure>
            <figure class="cut-card animate-on-scroll" style="--delay:.26s">
              <img loading="lazy" src="https://images.unsplash.com/photo-1585747860715-2ba37e788b70?auto=format&fit=crop&w=1000&q=88" alt="Example beard and haircut combination" />
              <figcaption>Cut + Beard</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </section>

'''
s = s[:start] + new_cuts + s[end:]

# Add final CSS overrides instead of relying on fragile earlier selectors.
css_marker = "/* mobile-carousel-safety-v2 */"
if css_marker not in s:
    css = r'''

    /* mobile-carousel-safety-v2 */
    .hero-decor.one{left:var(--pad);right:auto}
    .hero-decor.two{right:var(--pad)}
    .panel-copy .scroll-decor{left:4%;bottom:-4%;font-size:clamp(64px,9vw,128px);pointer-events:none}
    .gallery-copy .scroll-decor{left:auto;right:4%;top:8%;bottom:auto}

    .hero-inner>*,.panel-grid>*,.visit-card>*,.service-card,.review-side,.gallery-side,.hero-card,.info-box{min-width:0;max-width:100%}
    h1,h2,h3,blockquote,.hero-card-line strong,.hero-card-line span,.button,.address-box,.hour-box,.info-box{overflow-wrap:anywhere;word-break:normal}
    iframe{max-width:100%}

    .cuts-showcase{height:auto;position:relative;background:linear-gradient(180deg,var(--bg) 0%,#0d0c0a 100%);overflow:hidden;padding:clamp(54px,7vw,96px) 0}
    .cuts-stage{position:relative;top:auto;height:auto;min-height:0;display:block;padding:0;overflow:visible}
    .cuts-word{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);font-size:clamp(72px,14vw,210px);line-height:.82;letter-spacing:.04em;z-index:0}
    .cuts-carousel{position:relative;z-index:2;width:100%;overflow:hidden}
    .cuts-track{display:flex;grid-template-columns:none;align-items:stretch;gap:clamp(14px,1.8vw,26px);width:100%;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x proximity;scrollbar-width:none;-ms-overflow-style:none;overscroll-behavior-x:contain;touch-action:pan-x pan-y;padding:24px max(var(--pad),calc((100vw - 1480px)/2)) 34px;cursor:grab;-webkit-overflow-scrolling:touch}
    .cuts-track::-webkit-scrollbar{display:none}
    .cuts-track.is-dragging{cursor:grabbing;scroll-snap-type:none;user-select:none}
    .cut-card,.cut-card:nth-child(n){position:relative;flex:0 0 clamp(290px,31vw,470px);width:auto;height:clamp(390px,57vw,620px);min-height:0;max-height:68svh;border-radius:24px;overflow:hidden;scroll-snap-align:center;transform:none!important;background:#171511}
    .cut-card img{width:100%;height:100%;object-fit:cover;object-position:center}
    .cut-card figcaption{left:20px;right:20px;bottom:18px;font-size:clamp(30px,3.2vw,48px);line-height:1;overflow-wrap:anywhere}

    @media (max-width:780px){
      body{overflow-x:hidden}
      .hero{min-height:0;padding-top:calc(var(--header) + 24px);padding-bottom:28px}
      .hero-inner{width:100%;min-width:0}
      .hero-copy,.hero-card{width:100%;min-width:0}
      .hero-copy h1{font-size:clamp(54px,18vw,72px);line-height:.88}
      .hero-copy p,.panel-copy p,.visit-content p{font-size:clamp(19px,5.4vw,22px)}
      .hero-card-line{display:grid;grid-template-columns:1fr;gap:6px;align-items:start}
      .hero-card-line strong{font-size:clamp(26px,8vw,30px);text-align:left;max-width:100%}
      .button{white-space:normal;text-align:center;line-height:1.2;padding:13px 18px}
      .hero-decor{font-size:clamp(54px,19vw,76px)}
      .hero-decor.one{left:18px}
      .hero-decor.two{right:18px}
      .info-box{min-width:0}

      .cuts-showcase{padding:44px 0 50px}
      .cuts-word{font-size:clamp(72px,24vw,112px);top:40%}
      .cuts-track{gap:14px;padding:18px 18px 26px;scroll-padding-inline:18px}
      .cut-card,.cut-card:nth-child(n){flex-basis:min(82vw,340px);height:min(64svh,500px);min-height:360px;max-height:none;border-radius:20px}
      .cut-card figcaption{left:16px;right:16px;bottom:14px;font-size:clamp(30px,9vw,40px)}

      .stack-panel{height:auto;min-height:0}
      .panel-inner{height:auto;min-height:0;overflow:hidden}
      .panel-grid{height:auto;min-height:0}
      .panel-copy{overflow:hidden}
      .panel-copy h2,.visit-content h2{font-size:clamp(42px,14vw,58px);line-height:.94}
      .service-card h3{font-size:clamp(30px,10vw,38px)}
      .service-card p{font-size:19px}
      .service-price{font-size:17px;flex-wrap:wrap}
      .gallery-card figcaption{max-width:calc(100% - 24px);white-space:normal;overflow-wrap:anywhere}
      .review-card blockquote{font-size:clamp(30px,9vw,38px);line-height:1.08}
      .review-card footer{font-size:17px;overflow-wrap:anywhere}
      .hours-grid{grid-template-columns:1fr}
      .address-box{font-size:18px}
      .visit-actions{display:grid;grid-template-columns:1fr}
      .visit-map iframe{min-height:330px}
      .footer nav{width:100%}
    }

    @media (max-width:390px){
      :root{--pad:16px;--section-space:12px}
      .site-header{padding-inline:16px}
      .brand-name{font-size:25px}
      .brand-sub{font-size:9px;letter-spacing:.18em}
      .hero-copy h1{font-size:clamp(50px,17vw,64px)}
      .hero-copy p,.panel-copy p,.visit-content p{font-size:19px}
      .info-box strong{font-size:31px}
      .review-card blockquote{font-size:30px}
      .rating-big{font-size:90px}
      .cut-card,.cut-card:nth-child(n){flex-basis:calc(100vw - 48px);min-height:330px;height:56svh}
      .footer{padding-inline:16px}
    }
'''
    s = s.replace("  </style>", css + "\n  </style>", 1)

js_marker = "// cuts-horizontal-carousel-v2"
if js_marker not in s:
    insert_before = "    function createCarousel({ trackSelector, itemSelector, prevSelector, nextSelector, progressSelector, mode = 'offset', autoplay = 0 }) {"
    js = r'''
    // cuts-horizontal-carousel-v2
    function setupCutsCarousel() {
      const track = document.querySelector('[data-cuts-carousel]');
      if (!track) return;

      const originals = [...track.children];
      if (!originals.length) return;

      originals.forEach(card => {
        const clone = card.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        clone.classList.add('in-view');
        clone.querySelectorAll('img').forEach(img => img.removeAttribute('loading'));
        track.appendChild(clone);
      });

      let pausedUntil = 0;
      let isDragging = false;
      let dragStartX = 0;
      let dragStartScrollLeft = 0;
      let lastFrame = performance.now();
      let loopWidth = 0;

      const updateLoopWidth = () => {
        const firstClone = track.children[originals.length];
        loopWidth = firstClone ? firstClone.offsetLeft - track.children[0].offsetLeft : track.scrollWidth / 2;
      };

      const pauseAuto = (milliseconds = 3000) => {
        pausedUntil = Math.max(pausedUntil, performance.now() + milliseconds);
      };

      const normalizePosition = () => {
        if (!loopWidth) return;
        while (track.scrollLeft >= loopWidth) track.scrollLeft -= loopWidth;
        while (track.scrollLeft < 0) track.scrollLeft += loopWidth;
      };

      const animate = now => {
        const dt = Math.min(now - lastFrame, 40);
        lastFrame = now;
        if (!reducedMotion && !isDragging && now >= pausedUntil && document.visibilityState === 'visible') {
          track.scrollLeft += dt * 0.032;
          normalizePosition();
        }
        requestAnimationFrame(animate);
      };

      ['touchstart', 'wheel'].forEach(type => {
        track.addEventListener(type, () => pauseAuto(type === 'wheel' ? 2200 : 3200), { passive: true });
      });
      track.addEventListener('touchend', () => pauseAuto(3200), { passive: true });
      track.addEventListener('mouseenter', () => pauseAuto(1200));
      track.addEventListener('focusin', () => pauseAuto(3200));
      track.addEventListener('keydown', event => {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        const amount = Math.min(track.clientWidth * .72, 420);
        track.scrollBy({ left: event.key === 'ArrowRight' ? amount : -amount, behavior: reducedMotion ? 'auto' : 'smooth' });
        pauseAuto(3200);
      });

      track.addEventListener('pointerdown', event => {
        if (event.pointerType !== 'mouse' || event.button !== 0) return;
        isDragging = true;
        dragStartX = event.clientX;
        dragStartScrollLeft = track.scrollLeft;
        track.classList.add('is-dragging');
        track.setPointerCapture?.(event.pointerId);
        pauseAuto(3500);
      });
      track.addEventListener('pointermove', event => {
        if (!isDragging) return;
        track.scrollLeft = dragStartScrollLeft - (event.clientX - dragStartX);
        pauseAuto(3500);
      });
      const stopDragging = event => {
        if (!isDragging) return;
        isDragging = false;
        track.classList.remove('is-dragging');
        if (event?.pointerId != null && track.hasPointerCapture?.(event.pointerId)) track.releasePointerCapture(event.pointerId);
        normalizePosition();
        pauseAuto(3200);
      };
      track.addEventListener('pointerup', stopDragging);
      track.addEventListener('pointercancel', stopDragging);
      track.addEventListener('lostpointercapture', stopDragging);

      window.addEventListener('resize', () => {
        updateLoopWidth();
        normalizePosition();
      });
      requestAnimationFrame(() => {
        updateLoopWidth();
        requestAnimationFrame(animate);
      });
    }

    setupCutsCarousel();

'''
    s = s.replace(insert_before, js + insert_before, 1)

path.write_text(s, encoding="utf-8")
