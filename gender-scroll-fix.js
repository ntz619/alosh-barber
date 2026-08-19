(() => {
  const clamp01 = value => Math.min(Math.max(value, 0), 1);

  function decorateDualBrand() {
    if (document.body.dataset.dualBrandReady === 'true') return;
    document.body.dataset.dualBrandReady = 'true';

    document.title = 'ALOSH × VIVO — Hair · Beauty · Barber';
    const meta = document.querySelector('meta[name="description"]');
    if (meta) meta.content = 'ALOSH × VIVO in Rostock – Herren bei ALOSH, Damen bei VIVO. Hair · Beauty · Barber an einer gemeinsamen Adresse.';

    const headerBrand = document.querySelector('.site-header .brand');
    if (headerBrand) {
      headerBrand.classList.add('brand-dual');
      headerBrand.setAttribute('aria-label', 'ALOSH und VIVO Startseite');
      headerBrand.innerHTML = '<span class="brand-name"><span>ALOSH</span><i>×</i><span>VIVO</span></span><span class="brand-sub">Hair · Beauty · Barber</span>';
    }

    const heroCopy = document.querySelector('.hero-copy');
    if (heroCopy) {
      heroCopy.innerHTML = `
        <p class="hero-kicker">ALOSH × VIVO · Doberaner Straße 48 · Rostock</p>
        <h1>Two names.<br>One salon.</h1>
        <p>ALOSH for Herren. VIVO for Damen. Two distinct identities, one shared address and the same focus on precise, personal hair and beauty service.</p>
        <div class="hero-actions">
          <a class="button button-gold" href="#booking">Choose your studio</a>
          <a class="button button-outline" href="#visit">See Location</a>
        </div>`;
    }

    const heroCard = document.querySelector('.hero-card');
    if (heroCard) {
      heroCard.setAttribute('aria-label', 'ALOSH und VIVO Kontakt');
      heroCard.innerHTML = `
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
        <div class="hero-shared-note">18057 Rostock · Hair · Beauty · Barber</div>`;
    }

    const heroDecor = document.querySelector('.hero-decor.two');
    if (heroDecor) heroDecor.textContent = 'VIVO';

    const infoStrip = document.querySelector('.info-strip');
    if (infoStrip) {
      infoStrip.innerHTML = `
        <div class="info-box"><strong>One address</strong><span>Doberaner Straße 48 · Rostock</span></div>
        <div class="info-box info-brand alosh-info"><strong>ALOSH</strong><span>Herren · 0177 7289259</span></div>
        <div class="info-box info-brand vivo-info"><strong>VIVO</strong><span>Damen · 0162 9105910</span></div>
        <div class="info-box"><strong data-shop-status>Opening hours</strong><span data-shop-detail>Mon–Fri 08:30 – 19:00</span></div>`;
    }

    const visitContent = document.querySelector('.visit-content');
    if (visitContent) {
      const heading = visitContent.querySelector('h2');
      const intro = visitContent.querySelector(':scope > p');
      if (heading && !visitContent.querySelector('.shared-salon-mark')) {
        heading.insertAdjacentHTML('beforebegin', '<div class="shared-salon-mark"><span>One salon · two studios</span><strong>ALOSH × VIVO</strong></div>');
      }
      if (heading) heading.innerHTML = 'Same address.<br>Your studio.';
      if (intro) intro.textContent = 'Choose Herren or Damen with the selector below. Contact and booking details change with your selection.';

      const address = visitContent.querySelector('.address-box');
      if (address) address.innerHTML = '<strong>ALOSH × VIVO</strong><br>Doberaner Straße 48<br>18057 Rostock';

      const oldBooking = visitContent.querySelector('.visit-actions#booking');
      if (oldBooking) {
        const booking = document.createElement('div');
        booking.id = 'booking';
        booking.innerHTML = `
          <div class="brand-contact-panel" data-addon-gender-panel="herren">
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
          <div class="brand-contact-panel" data-addon-gender-panel="damen" hidden>
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
          </div>`;
        oldBooking.replaceWith(booking);
      }
    }

    const map = document.querySelector('.visit-map iframe');
    if (map) map.src = 'https://www.google.com/maps?q=Doberaner+Stra%C3%9Fe+48,+18057+Rostock&output=embed';

    const footerBrand = document.querySelector('.footer .brand');
    if (footerBrand) {
      footerBrand.classList.add('brand-dual');
      footerBrand.innerHTML = '<span class="brand-name"><span>ALOSH</span><i>×</i><span>VIVO</span></span><span class="brand-sub">Hair · Beauty · Barber</span>';
    }
    const footerYear = document.getElementById('year');
    if (footerYear?.parentElement) {
      const parent = footerYear.parentElement;
      parent.classList.add('footer-dual-note');
      while (parent.firstChild) parent.removeChild(parent.firstChild);
      parent.append('© ');
      const year = document.createElement('span');
      year.id = 'year';
      year.textContent = String(new Date().getFullYear());
      parent.append(year, ' ALOSH × VIVO');
    }

    const herrenButton = document.querySelector('[data-gender-toggle="herren"]');
    const damenButton = document.querySelector('[data-gender-toggle="damen"]');
    if (herrenButton) herrenButton.innerHTML = 'Herren<small>ALOSH</small>';
    if (damenButton) damenButton.innerHTML = 'Damen<small>VIVO</small>';
  }

  function syncGenderPresentation() {
    const gender = document.body.dataset.gender === 'damen' ? 'damen' : 'herren';

    document.querySelectorAll('[data-addon-gender-panel]').forEach(panel => {
      panel.hidden = panel.dataset.addonGenderPanel !== gender;
    });

    const priceTitle = document.querySelector('[data-gender-price-title]');
    if (priceTitle) priceTitle.textContent = gender === 'damen' ? 'Damen' : 'Herren';

    const salonHeading = document.querySelector('#salon .panel-copy h2');
    const salonCopy = document.querySelector('#salon .panel-copy p');
    if (salonHeading) salonHeading.innerHTML = gender === 'damen' ? 'VIVO.<br>Light & refined.' : 'ALOSH.<br>Dark & precise.';
    if (salonCopy) salonCopy.textContent = gender === 'damen'
      ? 'A lighter, calm identity for hair, color and beauty — still at the same shared Rostock salon.'
      : 'A darker, focused identity for cuts, beard work and clean detail — at the same shared Rostock salon.';
  }

  function syncDockVisibility() {
    const dock = document.querySelector('[data-gender-dock]');
    const hero = document.querySelector('.hero');
    if (!dock || !hero) return;
    const visible = hero.getBoundingClientRect().bottom <= window.innerHeight * .88;
    dock.classList.toggle('is-visible', visible);
    dock.setAttribute('aria-hidden', String(!visible));
  }

  decorateDualBrand();
  syncGenderPresentation();
  syncDockVisibility();

  new MutationObserver(mutations => {
    if (mutations.some(mutation => mutation.attributeName === 'data-gender')) {
      syncGenderPresentation();
    }
  }).observe(document.body, { attributes: true, attributeFilter: ['data-gender'] });

  const dock = document.querySelector('[data-gender-dock]');
  if (dock) {
    new MutationObserver(() => requestAnimationFrame(syncDockVisibility))
      .observe(dock, { attributes: true, attributeFilter: ['class', 'aria-hidden'] });
  }

  let dockRaf = 0;
  const requestDockSync = () => {
    if (dockRaf) return;
    dockRaf = requestAnimationFrame(() => {
      dockRaf = 0;
      syncDockVisibility();
    });
  };
  window.addEventListener('scroll', requestDockSync, { passive: true });
  window.addEventListener('resize', requestDockSync);

  /* Preserve relative progress when switching between differently sized price lists. */
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-gender-toggle]');
    if (!button) return;

    const services = document.getElementById('services');
    if (!services) return;

    const currentGender = document.body.dataset.gender || 'herren';
    const nextGender = button.dataset.genderToggle;
    if (!nextGender || nextGender === currentGender) return;

    const currentPanel = services.querySelector(`[data-gender-panel="${currentGender}"]:not([hidden])`);
    if (!currentPanel) return;

    const header = document.querySelector('.site-header');
    const headerOffset = header?.offsetHeight || 0;
    const viewportHeight = Math.max(window.innerHeight - headerOffset, 1);
    const rect = currentPanel.getBoundingClientRect();
    const panelTop = rect.top + window.scrollY;
    const panelHeight = rect.height;
    const startScroll = panelTop - headerOffset;
    const endScroll = panelTop + panelHeight;

    if (window.scrollY < startScroll || window.scrollY > endScroll) return;

    const travel = Math.max(panelHeight - viewportHeight, 0);
    const progress = travel > 1
      ? clamp01((window.scrollY - startScroll) / travel)
      : 0;

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        const targetPanel = services.querySelector(`[data-gender-panel="${nextGender}"]:not([hidden])`);
        if (!targetPanel) return;

        const targetRect = targetPanel.getBoundingClientRect();
        const targetTop = targetRect.top + window.scrollY - headerOffset;
        const targetTravel = Math.max(targetRect.height - viewportHeight, 0);
        const targetScroll = targetTop + progress * targetTravel;
        const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 0);

        window.scrollTo({
          top: Math.min(Math.max(targetScroll, 0), maxScroll),
          behavior: 'auto'
        });
      });
    });
  }, true);
})();
