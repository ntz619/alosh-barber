(() => {
  const clamp01 = value => Math.min(Math.max(value, 0), 1);

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

        const targetTravel = Math.max(targetPanel.getBoundingClientRect().height - viewportHeight, 0);
        const targetScroll = startScroll + progress * targetTravel;
        const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 0);

        window.scrollTo({
          top: Math.min(Math.max(targetScroll, 0), maxScroll),
          behavior: 'auto'
        });
      });
    });
  }, true);
})();
