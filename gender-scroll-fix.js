(() => {
  function decorateDualBrand() {
    if (document.body.dataset.dualBrandReady === 'true') return;
    document.body.dataset.dualBrandReady = 'true';

    document.title = 'ALOSH × VIVO — Haar · Kosmetik · Barber';
    const meta = document.querySelector('meta[name="description"]');
    if (meta) meta.content = 'ALOSH × VIVO in Rostock – Herren bei ALOSH, Damen bei VIVO. Haar, Kosmetik und Barber an einer gemeinsamen Adresse.';

    const headerBrand = document.querySelector('.site-header .brand');
    if (headerBrand) {
      headerBrand.classList.add('brand-dual');
      headerBrand.setAttribute('aria-label', 'ALOSH und VIVO Startseite');
      headerBrand.innerHTML = '<span class="brand-name"><span>ALOSH</span><i>×</i><span>VIVO</span></span><span class="brand-sub">Haar · Kosmetik · Barber</span>';
    }

    const heroCopy = document.querySelector('.hero-copy');
    if (heroCopy) {
      heroCopy.innerHTML = `
        <h1>Zwei Namen.<br>Ein Salon.</h1>
        <div class="ornament-divider hero-title-ornament" aria-hidden="true"><span>❦</span></div>
        <p>Zwei eigenständige Marken, eine gemeinsame Adresse und derselbe Anspruch an präzise, persönliche Haar- und Kosmetikleistungen.</p>`;
    }

    const heroCard = document.querySelector('.hero-card');
    if (heroCard) {
      heroCard.setAttribute('aria-label', 'ALOSH und VIVO Kontakt');
      heroCard.innerHTML = `
        <div class="hero-card-line"><span data-shop-status>Öffnungszeiten</span><strong data-shop-detail>Mo–Fr 08:30–19:00</strong></div>
        <div class="ornament-divider hero-card-ornament" aria-hidden="true"><span>❦</span></div>
        <div class="hero-dual-contact">
          <a class="hero-brand-contact alosh" href="tel:+491777289259" aria-label="ALOSH unter 0177 7289259 anrufen">
            <span>ALOSH · Herren</span>
            <strong>0177 7289259</strong>
            <small>ALOSH anrufen</small>
            <svg class="hero-call-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.69 2.8a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.33 1.84.56 2.8.69A2 2 0 0 1 22 16.92Z"/></svg>
          </a>
          <a class="hero-brand-contact vivo" href="tel:+491629105910" aria-label="VIVO unter 0162 9105910 anrufen">
            <span>VIVO · Damen</span>
            <strong>0162 9105910</strong>
            <small>VIVO anrufen</small>
            <svg class="hero-call-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.69 2.8a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.33 1.84.56 2.8.69A2 2 0 0 1 22 16.92Z"/></svg>
          </a>
        </div>
        <div class="hero-card-line hero-address-line"><span>Adresse</span><a class="hero-address-link" href="#map" aria-label="Zur Karte für Doberaner Straße 48 scrollen"><svg class="hero-map-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/></svg><span>Doberaner Str. 48</span></a></div>`;
    }

    const heroDecor = document.querySelector('.hero-decor.two');
    if (heroDecor) heroDecor.textContent = 'VIVO';

    const infoStrip = document.querySelector('.info-strip');
    if (infoStrip) {
      infoStrip.innerHTML = `
        <div class="info-box info-feature info-feature-dark"><strong>Ohne Termin</strong><span>Spontan vorbeikommen</span></div>
        <div class="info-box info-feature info-feature-dark"><strong>Haar &amp; Bart</strong><span>Schnitt, Kontur &amp; Rasur</span></div>
        <div class="info-box info-feature"><strong>Farbe &amp; Beauty</strong><span>Styling, Farbe &amp; Kosmetik</span></div>
        <div class="info-box info-feature"><strong>4,9 ★</strong><span>Google Bewertungen</span></div>`;
    }

    const visitContent = document.querySelector('.visit-content');
    if (visitContent) {
      const heading = visitContent.querySelector('h2');
      const intro = visitContent.querySelector(':scope > p');
      if (heading && !visitContent.querySelector('.shared-salon-mark')) {
        heading.insertAdjacentHTML('beforebegin', '<div class="shared-salon-mark"><strong>ALOSH × VIVO</strong></div>');
      }
      if (heading) heading.textContent = 'Dein Studio für Herren und Damen.';
      if (intro) intro.remove();

      const address = visitContent.querySelector('.address-box');
      if (address) address.remove();

      const oldBooking = visitContent.querySelector('.visit-actions#booking');
      if (oldBooking) {
        const booking = document.createElement('div');
        booking.id = 'booking';
        booking.innerHTML = `
          <div class="brand-contact-panel" data-addon-gender-panel="herren">
            <div class="brand-contact-head"><div><h3>ALOSH</h3><span>Herrenfriseur</span></div></div>
            <div class="ornament-divider contact-card-ornament" aria-hidden="true"><span>❦</span></div>
            <div class="brand-contact-details">
              <a href="tel:+491777289259">0177 7289259</a>
              <small>Doberaner Straße 48 · 18057 Rostock</small>
            </div>
            <div class="visit-actions">
              <a class="button button-gold button-with-icon" href="tel:+491777289259">
                <svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.69 2.8a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.33 1.84.56 2.8.69A2 2 0 0 1 22 16.92Z"/></svg>
                <span>ALOSH anrufen</span>
              </a>
              <a class="button button-outline instagram-button" href="https://www.instagram.com/alosh.barbershop/" target="_blank" rel="noopener">
                <svg class="instagram-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" class="instagram-icon-dot"/></svg>
                <span>@alosh.barbershop</span>
              </a>
              <a class="button button-outline button-with-icon" href="https://www.google.com/maps/search/?api=1&query=Doberaner+Stra%C3%9Fe+48%2C+18057+Rostock" target="_blank" rel="noopener">
                <svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/></svg>
                <span>In Maps öffnen</span>
              </a>
            </div>
          </div>
          <div class="brand-contact-panel" data-addon-gender-panel="damen" hidden>
            <div class="brand-contact-head"><div><h3>VIVO</h3><span>Haar · Kosmetik</span></div></div>
            <div class="ornament-divider contact-card-ornament" aria-hidden="true"><span>❦</span></div>
            <div class="brand-contact-details">
              <a href="tel:+491629105910">0162 9105910</a>
              <small>Doberaner Straße 48 · 18057 Rostock</small>
            </div>
            <div class="visit-actions">
              <a class="button button-gold button-with-icon" href="tel:+491629105910">
                <svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.69 2.8a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.33 1.84.56 2.8.69A2 2 0 0 1 22 16.92Z"/></svg>
                <span>VIVO anrufen</span>
              </a>
              <a class="button button-outline instagram-button" href="https://www.instagram.com/avin_friseur/" target="_blank" rel="noopener">
                <svg class="instagram-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" class="instagram-icon-dot"/></svg>
                <span>@avin_friseur</span>
              </a>
              <a class="button button-outline button-with-icon" href="https://www.google.com/maps/search/?api=1&query=Doberaner+Stra%C3%9Fe+48%2C+18057+Rostock" target="_blank" rel="noopener">
                <svg class="action-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/></svg>
                <span>In Maps öffnen</span>
              </a>
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
      footerBrand.innerHTML = '<span class="brand-name"><span>ALOSH</span><i>×</i><span>VIVO</span></span><span class="brand-sub">Haar · Kosmetik · Barber</span>';
    }

    const footerYear = document.getElementById('year');
    if (footerYear?.parentElement) {
      const parent = footerYear.parentElement;
      parent.classList.add('footer-dual-note');
      parent.textContent = '';
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
    if (salonHeading) salonHeading.innerHTML = gender === 'damen' ? 'VIVO.<br>Hell & elegant.' : 'ALOSH.<br>Dunkel & präzise.';
    if (salonCopy) salonCopy.textContent = gender === 'damen'
      ? 'Eine helle, ruhige Identität für Haare, Farbe und Kosmetik – weiterhin am gemeinsamen Standort in Rostock.'
      : 'Eine dunkle, präzise Identität für Haarschnitte, Bart und klare Details – am gemeinsamen Standort in Rostock.';
  }

  function syncDockVisibility() {
    const dock = document.querySelector('[data-gender-dock]');
    if (!dock) return;
    const footer = document.querySelector('.footer');
    const footerLift = footer
      ? Math.max(0, window.innerHeight - footer.getBoundingClientRect().top + 14)
      : 0;
    dock.style.setProperty('--dock-footer-lift', `${footerLift}px`);
    dock.classList.toggle('is-footer-lifted', footerLift > 1);
    const visible = document.body.dataset.genderDockReady === 'true';
    if (dock.classList.contains('is-visible') !== visible) dock.classList.toggle('is-visible', visible);
    const hiddenValue = String(!visible);
    if (dock.getAttribute('aria-hidden') !== hiddenValue) dock.setAttribute('aria-hidden', hiddenValue);
  }

  decorateDualBrand();
  syncGenderPresentation();
  syncDockVisibility();
  window.setTimeout(() => {
    document.body.dataset.genderDockReady = 'true';
    syncDockVisibility();
    window.setTimeout(() => {
      document.querySelector('[data-gender-dock]')?.classList.add('is-settled');
    }, 520);
  }, 500);

  new MutationObserver(mutations => {
    if (mutations.some(mutation => mutation.attributeName === 'data-gender')) {
      syncGenderPresentation();
      syncDockVisibility();
    }
  }).observe(document.body, { attributes: true, attributeFilter: ['data-gender'] });

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

  const captureGenderScrollAnchor = () => {
    const header = document.querySelector('.site-header');
    const headerOffset = header?.offsetHeight || 0;
    const viewportHeight = Math.max(window.innerHeight - headerOffset, 1);
    const footer = document.querySelector('.footer');
    const footerRect = footer?.getBoundingClientRect();
    if (footerRect && footerRect.top < window.innerHeight && footerRect.bottom > 0) {
      const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 0);
      return {
        section: footer,
        isFooterAnchor: true,
        distanceFromBottom: Math.max(maxScroll - window.scrollY, 0)
      };
    }
    const referenceY = headerOffset + viewportHeight * .38;
    const sections = [...document.querySelectorAll('main section[id]'), footer]
      .filter(Boolean);
    const containingSections = sections.filter(candidate => {
      const candidateRect = candidate.getBoundingClientRect();
      return candidateRect.top <= referenceY && candidateRect.bottom >= referenceY;
    });
    let section = containingSections[0];

    const hasStackedSalonCards = containingSections.some(candidate => candidate.id === 'salon')
      && containingSections.some(candidate => candidate.id === 'reviews');
    if (hasStackedSalonCards) {
      const visibleSection = document
        .elementFromPoint(window.innerWidth * .5, referenceY)
        ?.closest('main section[id]');
      if (visibleSection && containingSections.includes(visibleSection)) section = visibleSection;
    }

    section ||= sections.reduce((closest, candidate) => {
      const distance = Math.abs(candidate.getBoundingClientRect().top - referenceY);
      return !closest || distance < closest.distance ? { candidate, distance } : closest;
    }, null)?.candidate;

    if (!section) return null;

    const anchorElement = (section.id === 'salon' || section.id === 'reviews')
      ? document.querySelector('#reviews .panel-inner') || section.querySelector('.panel-inner') || section
      : section;
    const rect = anchorElement.getBoundingClientRect();
    const isPriceSection = section.id === 'services';
    const sectionRect = section.getBoundingClientRect();
    const sectionTop = sectionRect.top + window.scrollY;
    const sectionTravel = Math.max(sectionRect.height - viewportHeight, 0);
    const progress = isPriceSection && sectionTravel > 1
      ? Math.min(Math.max((window.scrollY - (sectionTop - headerOffset)) / sectionTravel, 0), 1)
      : 0;
    return { section, anchorElement, headerOffset, viewportHeight, isPriceSection, progress, anchorTop: rect.top };
  };

  const applyGenderScrollAnchor = anchor => {
    if (!anchor) {
      requestDockSync();
      return;
    }

    const {
      section,
      anchorElement,
      headerOffset,
      viewportHeight,
      isPriceSection,
      isFooterAnchor,
      distanceFromBottom,
      progress,
      anchorTop
    } = anchor;

    if (isFooterAnchor) {
      const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 0);
      window.scrollTo({ top: Math.max(maxScroll - distanceFromBottom, 0), behavior: 'instant' });
      requestDockSync();
      return;
    }

    const updatedRect = (anchorElement || section).getBoundingClientRect();
    if (isPriceSection) {
      const updatedSectionRect = section.getBoundingClientRect();
      const updatedTop = updatedSectionRect.top + window.scrollY;
      const updatedTravel = Math.max(updatedSectionRect.height - viewportHeight, 0);
      const targetScroll = updatedTop - headerOffset + progress * updatedTravel;
      const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 0);
      window.scrollTo({ top: Math.min(Math.max(targetScroll, 0), maxScroll), behavior: 'instant' });
    } else {
      window.scrollBy({ top: updatedRect.top - anchorTop, behavior: 'instant' });
    }

    requestDockSync();
  };

  const restoreGenderScrollAnchor = anchor => {
    // Correct the changed document height in the same task as the content
    // swap, before the browser can paint a frame from a neighbouring section.
    applyGenderScrollAnchor(anchor);
    return new Promise(resolve => {
      requestAnimationFrame(() => {
        // One refinement catches late font/image geometry without exposing the
        // price list or map between the two gender states.
        applyGenderScrollAnchor(anchor);
        resolve();
      });
    });
  };

  window.__runGenderSwitch = (nextGender, updateGender) => {
    const anchor = captureGenderScrollAnchor();
    const updateAndRestore = () => {
      updateGender(nextGender);
      return restoreGenderScrollAnchor(anchor);
    };
    document.documentElement.classList.add('gender-switching');
    document.dispatchEvent(new CustomEvent('gender-switch-start'));
    return updateAndRestore().finally(() => {
      document.documentElement.classList.remove('gender-switching');
      document.dispatchEvent(new CustomEvent('gender-switch-end'));
    });
  };
})();
