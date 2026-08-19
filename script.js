const header = document.querySelector('.site-header');
    const menuToggle = document.querySelector('.menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const root = document.documentElement;

    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;


    // centered-anchor-navigation
    function getNaturalAnchorMetrics(target) {
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

    function handleScrollState(){
      header.classList.toggle('scrolled', window.scrollY > 18);

      document.querySelectorAll('.parallax').forEach(el => {
        if (reducedMotion) return;
        const speed = parseFloat(el.dataset.speed || '0.12');
        const host = el.closest('.hero, .panel-copy, .cuts-stage') || el.parentElement;
        const rect = host.getBoundingClientRect();
        const move = (window.innerHeight - rect.top) * speed;
        el.style.transform = `translate3d(0, ${-move}px, 0)`;
      });

      const stickyPanels = [...document.querySelectorAll('.stack-panel:not(.price-panel)')];
      const topOffset = parseFloat(getComputedStyle(root).getPropertyValue('--header')) + 12;
      stickyPanels.forEach((panel, index) => {
        const inner = panel.querySelector('.panel-inner');
        const next = stickyPanels[index + 1];
        if (!next || reducedMotion) {
          inner.style.transform = '';
          inner.style.filter = '';
          return;
        }
        const distance = next.getBoundingClientRect().top - topOffset;
        const progress = clamp((180 - distance) / 180, 0, 1);
        inner.style.transform = `scale(${1 - progress * .025}) translateY(${-progress * 6}px)`;
        inner.style.filter = `brightness(${1 - progress * .14})`;
      });
    }

    window.addEventListener('scroll', () => requestAnimationFrame(handleScrollState), { passive: true });
    window.addEventListener('resize', handleScrollState);

    menuToggle?.addEventListener('click', () => {
      const open = document.body.classList.toggle('menu-open');
      menuToggle.setAttribute('aria-expanded', String(open));
      mobileMenu.setAttribute('aria-hidden', String(!open));
    });

    document.querySelectorAll('.mobile-menu a').forEach(link => {
      link.addEventListener('click', () => {
        document.body.classList.remove('menu-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        mobileMenu.setAttribute('aria-hidden', 'true');
      });
    });

    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.14 });

    document.querySelectorAll('.reveal, .animate-on-scroll').forEach(el => revealObserver.observe(el));

const cutsCarouselControllers = new Map();

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
  const priceTitle = document.querySelector('[data-gender-price-title]');
  const cuts = document.getElementById('cuts');
  const salon = document.getElementById('salon');
  if (!dock || !buttons.length || !cuts || !salon) return;

  let selectedGender = 'herren';

  const applyGender = gender => {
    selectedGender = gender;
    document.body.dataset.gender = gender;
    if (genderWord) genderWord.textContent = gender === 'damen' ? 'DAMEN' : 'HERREN';
    if (priceTitle) priceTitle.textContent = gender === 'damen' ? 'Damen.' : 'Herren.';

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

initGenderExperience();

    function createCarousel({ trackSelector, itemSelector, prevSelector, nextSelector, progressSelector, mode = 'offset', autoplay = 0 }) {
      const track = document.querySelector(trackSelector);
      const items = [...document.querySelectorAll(itemSelector)];
      const prev = document.querySelector(prevSelector);
      const next = document.querySelector(nextSelector);
      const progress = progressSelector ? document.querySelector(progressSelector) : null;
      if (!track || !items.length) return;

      let index = 0;
      let timer;
      let touchStartX = 0;

      function update() {
        items.forEach((item, itemIndex) => item.classList.toggle('active', itemIndex === index));
        if (mode === 'offset') {
          track.style.transform = `translateX(${-items[index].offsetLeft}px)`;
        } else {
          track.style.transform = `translateX(-${index * 100}%)`;
        }
        if (progress) {
          progress.style.transform = `translateX(${index * 100}%)`;
        }
      }

      function restart() {
        if (!autoplay) return;
        clearInterval(timer);
        timer = setInterval(goNext, autoplay);
      }

      function goNext() {
        index = (index + 1) % items.length;
        update();
        restart();
      }

      function goPrev() {
        index = (index - 1 + items.length) % items.length;
        update();
        restart();
      }

      prev?.addEventListener('click', goPrev);
      next?.addEventListener('click', goNext);

      track.addEventListener('touchstart', e => {
        touchStartX = e.touches[0].clientX;
      }, { passive: true });

      track.addEventListener('touchend', e => {
        const diff = e.changedTouches[0].clientX - touchStartX;
        if (Math.abs(diff) > 40) {
          diff < 0 ? goNext() : goPrev();
        }
      }, { passive: true });

      window.addEventListener('resize', update);
      update();
      restart();
    }

    createCarousel({
      trackSelector: '.gallery-track',
      itemSelector: '.gallery-card',
      prevSelector: '[data-gallery-prev]',
      nextSelector: '[data-gallery-next]',
      mode: 'offset'
    });

    createCarousel({
      trackSelector: '.review-track',
      itemSelector: '.review-card',
      prevSelector: '[data-review-prev]',
      nextSelector: '[data-review-next]',
      progressSelector: '.review-progress span',
      autoplay: 6500,
      mode: 'percent'
    });

    document.getElementById('year').textContent = new Date().getFullYear();
    handleScrollState();
