(() => {
  const map = document.querySelector('[data-map-src]');
  const consent = map?.querySelector('[data-map-consent]');
  const loadButton = consent?.querySelector('[data-map-load]');

  if (!map || !consent || !loadButton) return;

  let iframe = null;
  let disableButton = null;

  function disableMap() {
    iframe?.remove();
    disableButton?.remove();
    iframe = null;
    disableButton = null;
    map.classList.remove('map-is-loaded');
    consent.hidden = false;
    loadButton.focus({ preventScroll: true });
  }

  function loadMap() {
    if (iframe) return;

    iframe = document.createElement('iframe');
    iframe.title = 'Kurdistan Barbershop und Friseur Atelier Justyna in Google Maps';
    iframe.src = map.dataset.mapSrc;
    iframe.loading = 'eager';
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    iframe.allowFullscreen = true;

    disableButton = document.createElement('button');
    disableButton.type = 'button';
    disableButton.className = 'map-disable-button';
    disableButton.textContent = 'Karte deaktivieren';
    disableButton.addEventListener('click', disableMap);

    consent.hidden = true;
    map.classList.add('map-is-loaded');
    map.append(iframe, disableButton);
  }

  loadButton.addEventListener('click', loadMap);
})();
